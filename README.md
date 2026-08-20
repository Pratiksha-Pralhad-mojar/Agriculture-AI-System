# Agriculture AI System

An AI-powered agriculture application that provides:

- Crop Recommendation
- Fertilizer Recommendation
- Sugarcane Leaf Disease Classification

## Technologies

Python
Flask
Scikit-learn
TensorFlow
NumPy
HTML
CSS
JavaScript

## Machine Learning Models

### Crop Recommendation
Input:
- Temperature
- Humidity
- Moisture
- Soil Type
- Nitrogen
- Potassium
- Phosphorous

Output:
Recommended crop

### Fertilizer Recommendation
Input:
- Temperature
- Humidity
- Moisture
- Soil Type
- Crop Type
- Nitrogen
- Potassium
- Phosphorous

Output:
Recommended fertilizer

### Leaf Disease Classification

Input:
Sugarcane leaf image

Output:
- Healthy
- Mosaic
- RedRot
- Rust
- Yellow

## Project Structure

agriculture-ai-system/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   ├── crop_model.pkl
│   ├── scaler.pkl
│   ├── soil_encoder.pkl
│   ├── crop_encoder.pkl
│   ├── classifier.pkl
│   └── saved_model.h5
│
├── templates/
│   ├── index.html
│   ├── crop.html
│   ├── ferti.html
│   └── disease.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── uploads/
│   └── .gitkeep
│
└── notebooks/
    ├── crop_prediction.ipynb
    ├── fertilizer_prediction.ipynb
    └── leaf_disease_classification.ipynb

## Installation

Flask
numpy
scikit-learn==1.3.2
tensorflow
Werkzeug
Pillow

## Running the Application

python app.py

## Screenshots



## Future Improvements

- Deploy using cloud platform
- Add authentication
- Add database
- Improve model accuracy
- Add more crops and diseases
