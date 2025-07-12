from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import PIL.ExifTags as ExifTags
import pandas as pd
import logging
import json
from pathlib import Path
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
import threading
import time

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

destination = os.getenv('DESTINATION_PATH')
results = os.getenv('RESULTS_PATH')
model_path = os.getenv('MODEL_PATH')

if not all([destination, results, model_path]):
    raise EnvironmentError("Environment variables not set")

# Retrieve values from environment variables
DESTINATION_PATH = BASE_DIR / Path(destination)
RESULTS_PATH = BASE_DIR / Path(results)
MODEL_PATH = BASE_DIR / Path(model_path)

# Create directories if they do not exist
DESTINATION_PATH.mkdir(parents=True, exist_ok=True)
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

FEEDBACK_FILE_PATH = DESTINATION_PATH / os.getenv('FEEDBACK_FILE_NAME', 'feedback.json')

# Initialize feedback accumulator
FEEDBACK_BATCH_SIZE = 10
feedback_accumulator = []

logging.basicConfig(level=logging.INFO)

# Load the model
model = tf.keras.models.load_model(MODEL_PATH)

@app.route('/', methods=['GET'])
def greetings():
    return "Hello, world!"

@app.route("/upload-images", methods=['POST'])
def upload_images():
    disease = request.form.get('disease') 
    results = {
        f"THIS PICTURE HAS {disease}": [],
        f"THERE'S A HIGH CHANCE OF {disease}": [],
        f"POSSIBILITY OF {disease}": [],
        f"DOES NOT HAVE {disease}": []
    }
    uploaded_files = request.files.getlist('file')

    if not uploaded_files:
        return 'No files to upload', 400

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(DESTINATION_PATH, filename)
            try:
                file.save(save_path)
            except Exception as e:
                logging.error(f"Failed to save file {filename}: {e}")
                return jsonify({"message": f"Failed to save file {filename}"}), 500

            try:
                img = cv2.imread(save_path)
                prediction = predict_img(img) * 100

                # Categorize based on the prediction value
                if prediction > 99.5:
                    category = f"THIS PICTURE HAS {disease}"
                elif 90 < prediction <= 99.5:
                    category = f"THERE'S A HIGH CHANCE OF {disease}"
                elif 70 < prediction <= 90:
                    category = f"POSSIBILITY OF {disease}"
                else:
                    category = f"DOES NOT HAVE {disease}"

                gps_data = get_gps_data(save_path)
                lat, lon = gps_data['lat'], gps_data['lon']
                results[category].append({
                    'filename': filename,
                    'prediction': f"{prediction:.2f}%",
                    'classification': category,
                    'latitude': lat,
                    'longitude': lon
                })
            except Exception as e:
                logging.error(f"Error processing file {filename}: {e}")
                return jsonify({"message": f"Error processing file {filename}"}), 500

    try:
        # Filter out "Not an Oak Wilt" from the results before saving to CSV and GeoJSON
        filtered_results = sum([items for key, items in results.items() if key != f"DOES NOT HAVE {disease}"], [])
        if filtered_results:
            results_df = pd.DataFrame(filtered_results)
            csv_file_path = os.path.join(RESULTS_PATH, 'results.csv')
            results_df.to_csv(csv_file_path, index=False)
            logging.info(f"CSV file created at {csv_file_path}")

            geojson_data = {
                "type": "FeatureCollection",
                "features": []
            }

            for item in filtered_results:
                if item['latitude'] and item['longitude']:
                    feature = {
                        "type": "Feature",
                        "properties": {
                            "filename": item['filename'],
                            "prediction": item['prediction'],
                            "classification": item['classification'],
                            "latitude": item['latitude'],
                            "longitude": item['longitude']
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [item['longitude'], item['latitude']]
                        }
                    }
                    geojson_data["features"].append(feature)

            geojson_file_path = os.path.join(RESULTS_PATH, 'results.geojson')
            with open(geojson_file_path, 'w') as geojson_file:
                json.dump(geojson_data, geojson_file)
            logging.info(f"GeoJSON file created at {geojson_file_path}")
        else:
            logging.info("No valid data for CSV or GeoJSON — generating empty files.")

            # Create an empty CSV file
            empty_df = pd.DataFrame(columns=['filename', 'prediction', 'classification', 'latitude', 'longitude'])
            csv_file_path = os.path.join(RESULTS_PATH, 'results.csv')
            empty_df.to_csv(csv_file_path, index=False)
            logging.info(f"Empty CSV file created at {csv_file_path}")

            # Create an empty GeoJSON file
            empty_geojson = {
                "type": "FeatureCollection",
                "features": []
            }
            geojson_file_path = os.path.join(RESULTS_PATH, 'results.geojson')
            with open(geojson_file_path, 'w') as geojson_file:
                json.dump(empty_geojson, geojson_file)
            logging.info(f"Empty GeoJSON file created at {geojson_file_path}")

    except Exception as e:
        logging.error(f"Failed to write results files: {e}")
        return jsonify({"message": "Failed to write results files"}), 500

    response_data = {
        "message": "The results files are ready to download",
        "results": results,
        "csv_file_path": f"/results.csv",
        "geojson_file_path": f"/results.geojson"
    }

    return jsonify(response_data)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        feedback_data = request.get_json()
        
        # Enhanced validation
        if not feedback_data:
            return jsonify({'message': 'No data provided'}), 400
        
        required_fields = ['filename', 'isCorrect']
        missing_fields = [field for field in required_fields if field not in feedback_data]
        
        if missing_fields:
            return jsonify({'message': f'Missing required fields: {missing_fields}'}), 400
        
        filename = feedback_data['filename']
        is_correct = feedback_data['isCorrect']
        
        # Validate filename (prevent path traversal)
        if not filename or '..' in filename or '/' in filename:
            return jsonify({'message': 'Invalid filename'}), 400
        
        # Validate isCorrect is boolean
        if not isinstance(is_correct, bool):
            return jsonify({'message': 'isCorrect must be boolean'}), 400

        # Save feedback to file
        save_feedback_to_file(filename, is_correct)
        
        # Add feedback to accumulator for retraining
        try:
            add_feedback_to_accumulator(filename, is_correct)
        except Exception as e:
            logging.error(f"Error adding feedback to accumulator: {e}")
            # Continue execution - feedback was saved successfully
        
        return jsonify({'message': 'Feedback received'}), 200
        
    except Exception as e:
        logging.error(f"Feedback submission error: {e}")
        return jsonify({'message': 'Internal server error'}), 500

def save_feedback_to_file(filename, is_correct):
    """Save feedback to JSON file with proper error handling"""
    try:
        # Load existing feedback
        try:
            with open(FEEDBACK_FILE_PATH, 'r') as file:
                feedback_list = json.load(file)
        except FileNotFoundError:
            feedback_list = []
        except json.JSONDecodeError:
            logging.warning("Corrupted feedback file, starting fresh")
            feedback_list = []

        # Append new feedback with timestamp
        feedback_list.append({
            'filename': filename,
            'isCorrect': is_correct,
            'timestamp': time.time()
        })

        # Save feedback
        with open(FEEDBACK_FILE_PATH, 'w') as file:
            json.dump(feedback_list, file, indent=2)
            
        logging.info(f"Feedback saved for {filename}: {is_correct}")
        
    except Exception as e:
        logging.error(f"Error saving feedback to file: {e}")
        raise

def add_feedback_to_accumulator(filename, is_correct):
    """Add feedback to accumulator and trigger retraining if needed"""
    try:
        # Load and preprocess the image
        image_path = DESTINATION_PATH / filename
        if not image_path.exists():
            logging.warning(f"Image file not found: {filename}")
            return
        
        img = cv2.imread(str(image_path))
        if img is None:
            logging.warning(f"Could not load image: {filename}")
            return
        
        # Preprocess image for training
        processed_img = preprocess_image(img)
        
        # Convert feedback to training label
        # True = correct prediction, False = incorrect prediction
        # You may need to adjust this logic based on your specific needs
        label = 1 if is_correct else 0
        
        # Add to accumulator
        feedback_accumulator.append((processed_img, label))
        
        logging.info(f"Added feedback to accumulator: {filename} -> {label}")
        logging.info(f"Accumulator size: {len(feedback_accumulator)}/{FEEDBACK_BATCH_SIZE}")
        
        # Check if we have enough feedback to retrain
        if len(feedback_accumulator) >= FEEDBACK_BATCH_SIZE:
            # Start retraining in a separate thread to avoid blocking the response
            threading.Thread(target=retrain_model, daemon=True).start()
            
    except Exception as e:
        logging.error(f"Error adding feedback to accumulator: {e}")
        raise

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(DESTINATION_PATH, filename)

@app.route('/results.csv', methods=['GET'])
def download_results_csv():
    try:
        return send_from_directory(RESULTS_PATH, 'results.csv', as_attachment=True)
    except Exception as e:
        logging.error(f"Error sending results.csv: {e}")
        return jsonify({"message": "Error sending results.csv"}), 500

@app.route('/results.geojson', methods=['GET'])
def download_results_geojson():
    try:
        return send_from_directory(RESULTS_PATH, 'results.geojson', as_attachment=False)
    except Exception as e:
        logging.error(f"Error sending results.geojson: {e}")
        return jsonify({"message": "Error sending results.geojson"}), 500

def predict_img(img):
    img_resized = cv2.resize(img, (256, 256))
    img_normalized = img_resized / 255.0
    img_expanded = np.expand_dims(img_normalized, axis=0)

    prediction = model.predict(img_expanded)
    return prediction[0][0]

def get_gps_data(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if not exif_data:
                raise ValueError("No EXIF data")

            lat, lon = get_decimal_coordinates(exif_data)
            if lat is None or lon is None:
                raise ValueError("Invalid GPS data")

            return {'lat': lat, 'lon': lon}
    except Exception:
        # Return arbitrary/fake GPS coordinates for testing
        return {'lat': 42.9634, 'lon': -85.6681}  # Example: Grand Rapids, MI

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_decimal_coordinates(info):
    for tag, value in info.items():
        decoded = ExifTags.TAGS.get(tag, tag)
        if decoded == 'GPSInfo':
            gps_data = {}
            for t in value:
                sub_decoded = ExifTags.GPSTAGS.get(t, t)
                gps_data[sub_decoded] = value[t]

            gps_lat = gps_data.get('GPSLatitude')
            gps_lat_ref = gps_data.get('GPSLatitudeRef')
            gps_lon = gps_data.get('GPSLongitude')
            gps_lon_ref = gps_data.get('GPSLongitudeRef')

            if not all([gps_lat, gps_lat_ref, gps_lon, gps_lon_ref]):
                return None, None

            lat = convert_to_degrees(gps_lat)
            if gps_lat_ref != "N":
                lat = 0 - lat

            lon = convert_to_degrees(gps_lon)
            if gps_lon_ref != "E":
                lon = 0 - lon

            return lat, lon
    return None, None

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def load_original_data_subset(size=50):
    """Load original training data - replace with your actual data loading logic"""
    # This is a placeholder - replace with your actual data loading
    original_training_data = np.random.rand(size, 256, 256, 3)
    original_labels = np.random.randint(0, 2, size)
    return original_training_data, original_labels

def retrain_model():
    """Retrain the model with accumulated feedback data"""
    global feedback_accumulator
    
    try:
        if len(feedback_accumulator) < FEEDBACK_BATCH_SIZE:
            logging.info("Not enough feedback data to retrain. Waiting for more feedback samples.")
            return

        logging.info("Starting model retraining with accumulated feedback data.")
        
        # Load original training data
        original_data, original_labels = load_original_data_subset(size=50)

        # Extract feedback data
        feedback_data, feedback_labels = zip(*feedback_accumulator)
        feedback_data = np.array(feedback_data)
        feedback_labels = np.array(feedback_labels)

        # Combine original and feedback data
        x_train = np.concatenate([feedback_data, original_data])
        y_train = np.concatenate([feedback_labels, original_labels])

        # Split data for training and validation
        x_train, x_val, y_train, y_val = train_test_split(
            x_train, y_train, test_size=0.2, random_state=42
        )

        # Configure model for retraining
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        # Train the model
        history = model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            epochs=3,
            batch_size=4,
            verbose=1
        )

        # Save the retrained model
        model.save(MODEL_PATH)
        
        # Clear the feedback accumulator
        feedback_accumulator.clear()
        
        logging.info("Model retrained and saved successfully.")
        logging.info(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
        logging.info(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
        
    except Exception as e:
        logging.error(f"Error during model retraining: {e}")
        # Don't clear the accumulator if retraining failed
        raise

def preprocess_image(img):
    """Preprocess image for training"""
    img_resized = cv2.resize(img, (256, 256))
    img_normalized = img_resized.astype(np.float32) / 255.0
    return img_normalized

if __name__ == "__main__":
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 5001))
    app.run(host=host, port=port, debug=True)