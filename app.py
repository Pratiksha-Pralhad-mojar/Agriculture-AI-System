import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load crop prediction models and encoders
with open('crop_model.pkl', 'rb') as f:
    crop_model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('soil_encoder.pkl', 'rb') as f:
    soil_encoder = pickle.load(f)

with open('crop_encoder.pkl', 'rb') as f:
    crop_encoder = pickle.load(f)

# Load fertilizer prediction model
with open('classifier.pkl', 'rb') as f:
    fertilizer_model = pickle.load(f)

# Load disease prediction model (TensorFlow)
model_path = r"D:\sem 8\Agri\saved_model.h5"  # Path to the disease prediction model
if not os.path.exists(model_path):
    raise Exception(f"Model file not found at {model_path}")

# Load the disease model
disease_model = load_model(model_path)

# Class labels for disease prediction
class_labels = ['Healthy', 'Mosaic', 'RedRot', 'Rust', 'Yellow']

# Define upload folder and allowed file extensions
UPLOAD_FOLDER = 'New_sugarcane_imgs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')  # Render home page

# Crop Recommendation Route
@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        try:
            # Get form data for crop prediction
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            moisture = float(request.form['moisture'])
            soil_type = request.form['soil_type']
            nitrogen = float(request.form['nitrogen'])
            potassium = float(request.form['potassium'])
            phosphorous = float(request.form['phosphorous'])

            # Prepare input data for scaling and encoding
            soil_type_encoded = soil_encoder.transform([soil_type])[0]
            input_data_scaled = scaler.transform([[temperature, humidity, moisture, soil_type_encoded, nitrogen, potassium, phosphorous]])

            # Predict crop
            predicted_crop_code = crop_model.predict(input_data_scaled)

            # Decode predicted crop
            predicted_crop = crop_encoder.inverse_transform(predicted_crop_code)[0]

            # Return the predicted crop in JSON format for frontend to handle
            return jsonify({'predicted_crop': predicted_crop})
        except Exception as e:
            return jsonify({'error': str(e)})
    # Render crop prediction form for GET request
    return render_template('crop.html')  

# Fertilizer Prediction Route
@app.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():
    if request.method == 'POST':
        try:
            # Get form data for fertilizer prediction
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            moisture = float(request.form['moisture'])
            soil_type = request.form['soil_type']
            crop_type = request.form['crop_type']
            nitrogen = float(request.form['nitrogen'])
            potassium = float(request.form['potassium'])
            phosphorous = float(request.form['phosphorous'])

            # Encode soil type and crop type
            soil_type_encoded = soil_encoder.transform([soil_type])[0]
            crop_type_encoded = crop_encoder.transform([crop_type])[0]

            # Prepare input data for prediction
            features = np.array([[temperature, humidity, moisture, soil_type_encoded, crop_type_encoded, nitrogen, potassium, phosphorous]])

            # Predict fertilizer
            prediction = fertilizer_model.predict(features)

            # Map prediction to fertilizer type
            fertilizer_names = ['10-26-26', '14-35-14', '17-17-17', '20-20', '28-28', 'DAP', 'Urea']
            predicted_fertilizer = fertilizer_names[prediction[0]]

            # Return fertilizer prediction in JSON format
            return jsonify({'predicted_fertilizer': predicted_fertilizer})
        except Exception as e:
            return jsonify({'error': str(e)})
    # Render fertilizer prediction form for GET request
    return render_template('ferti.html')

# Leaf Disease Prediction Route
@app.route('/predict', methods=['GET', 'POST'])
def disease():
    if request.method == 'POST':
        try:
            # Get the uploaded leaf image
            leaf_image = request.files['file']  # Use 'file' as the name here

            if not leaf_image or not allowed_file(leaf_image.filename):
                return jsonify({'error': 'Invalid or no file uploaded'}), 400

            # Save the image to the upload folder
            filename = secure_filename(leaf_image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            leaf_image.save(file_path)

            # Load and process the image for prediction
            img = image.load_img(file_path, target_size=(256, 256))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)

            # Make prediction using the disease model
            predictions = disease_model.predict(img_array)
            predicted_class_idx = np.argmax(predictions, axis=1)
            predicted_class = class_labels[predicted_class_idx[0]]

            # Return the disease prediction in JSON format
            return jsonify({'disease_prediction': predicted_class})
        except Exception as e:
            return jsonify({'error': str(e)})
    # Render disease prediction form for GET request
    return render_template('disease.html')

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)
