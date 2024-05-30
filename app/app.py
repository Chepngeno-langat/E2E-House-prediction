from flask import Flask, request, jsonify, render_template
import joblib
import logging
import pandas as pd
import math
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Adjust the paths to be relative to the app directory
model_path = os.path.join(os.path.dirname(__file__), '../notebooks/gb_model.pkl')
try:
    model = joblib.load(model_path)
    logging.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise

model_columns_path = os.path.join(os.path.dirname(__file__), '../notebooks/model_columns.pkl')
one_hot_encoder_path = os.path.join(os.path.dirname(__file__), '../notebooks/one_hot_encoder.pkl')

model = joblib.load(model_path)
model_columns = joblib.load(model_columns_path)
one_hot_encoder = joblib.load(one_hot_encoder_path)

categorical_features = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']
numerical_features = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # Extract features from JSON data
        input_features = data['features']

        # Create a DataFrame from the input features
        input_data = pd.DataFrame([input_features])

        # Separate numerical and categorical data
        numerical_data = input_data[numerical_features]
        categorical_data = input_data[categorical_features]

        # Encode the categorical data
        encoded_categorical_data = one_hot_encoder.transform(categorical_data)

        # Create a DataFrame with the encoded categorical data
        encoded_categorical_df = pd.DataFrame(encoded_categorical_data,
                                              columns=one_hot_encoder.get_feature_names_out(categorical_features))

        # # Combine numerical and encoded categorical data
        final_input_data = pd.concat([numerical_data.reset_index(drop=True), encoded_categorical_df.reset_index(drop=True)],
                                     axis=1)

        # Make a prediction using the loaded model
        prediction = model.predict(final_input_data)

        return jsonify({'prediction': math.ceil(float(prediction[0]))})

    except Exception as e:
        return jsonify({'error': str(e)})

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)

