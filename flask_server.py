from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os
import json

app = Flask(__name__, static_folder='public', static_url_path='/public')
CORS(app)

# Load your trained models
model_lr = joblib.load(r'Machine_Learning\Models\logistic_regression_model.pkl')
model_nb = joblib.load(r'Machine_Learning\Models\Naive_Bayes_model.pkl')
model_rf = joblib.load(r'Machine_Learning\Models\Random Forest_model.pkl')

# Load the preprocessed data
X_preprocessed = np.load(r'Machine_Learning\Models\X_preprocessed.npy')

# Example of fetching a specific static file
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Fetch job by index from JSON file
# @app.route('/api/job/<int:index>', methods=['GET'])
# def get_job(index):
#     try:
#         data = X_preprocessed[index]
#         # Validate index
#         if index < 0 or index >= len(data):
#             return jsonify({'error': 'Job not found.'}), 404
        
#         # Return job at index
#         return jsonify(data[index])

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({'error': 'Error processing data file.'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        if 'features' not in data or not isinstance(data['features'], dict):
            return jsonify({'error': 'Invalid or missing features in request'}), 400

        features_list = list(data['features'].values())
        features_array = np.array(features_list)
        if not np.issubdtype(features_array.dtype, np.number):
            features_array = features_array.astype(float)  # Ensure it is numeric
        features_array = features_array.reshape(1, -1)

        prediction_lr = model_lr.predict(features_array)
        prediction_nb = model_nb.predict(features_array)
        prediction_rf = model_rf.predict(features_array)

        return jsonify({
            'Logistic Regression': prediction_lr.tolist(),
            'Naive Bayes': prediction_nb.tolist(),
            'Random Forest': prediction_rf.tolist(),
        })
    except Exception as e:
        print("Error during prediction:", str(e))  # Log the error
        return jsonify({'error': str(e)}), 500

@app.route('/features/<int:index>', methods=['GET'])
def get_features(index):
    try:
        # Validate index
        if index < 0 or index >= X_preprocessed.shape[0]:
            return jsonify({'error': 'Index out of bounds'}), 404

        # Fetch the feature set for the specified index
        feature_set = X_preprocessed[index].tolist()
        return jsonify({'features': feature_set})
    except Exception as e:
        print("Error fetching features:", str(e))
        return jsonify({'error': str(e)}), 500

import boto3
import json
# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobPostings')  

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        employment_type = request.args.get('employment_type', 'all')
        experience_level = request.args.get('required_experience', 'all')
        education = request.args.get('required_education', 'all')

        filter_expressions = []
        expression_values = {}
        params = {}

        if employment_type != 'all':
            filter_expressions.append("employment_type = :employment_type")
            expression_values[':employment_type'] = employment_type
        if experience_level != 'all':
            filter_expressions.append("required_experience = :experience_level")
            expression_values[':experience_level'] = experience_level
        if education != 'all':
            filter_expressions.append("required_education = :education")
            expression_values[':education'] = education


        if filter_expressions:
            params['FilterExpression'] = " AND ".join(filter_expressions)
            params['ExpressionAttributeValues'] = expression_values

        response = table.scan(**params)

        return jsonify({
            'jobs': response.get('Items', []),
            'last_key': response.get('LastEvaluatedKey')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs/all', methods=['GET'])
def get_jobs_all():
    try:
        response = table.scan()

        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return jsonify({
            'jobs': items,
            'last_key': response.get('LastEvaluatedKey')  # This will be None if all items are fetched
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
