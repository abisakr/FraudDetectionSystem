from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)


# Load trained XGBoost pipeline
try:
    model = joblib.load(
        'creditcard_fraud_detection_xgboost_model.pkl'
    )
    print("Fraud Detection Model loaded successfully.")

except Exception as e:
    print("Error loading model:", e)
    model = None


@app.route('/api/predict', methods=['POST'])
def predict():

    try:

        # Check whether model loaded successfully
        if model is None:
            return jsonify({
                'status': 'error',
                'message': 'Model is not loaded.'
            }), 500


        # Get JSON data from frontend
        data = request.get_json()

        print("Received data:", data)


        # Check whether JSON was received
        if data is None:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data received.'
            }), 400


        # Columns required by the trained model
        required_columns = [
            'type',
            'amount',
            'oldbalanceOrg',
            'newbalanceOrig',
            'oldbalanceDest',
            'newbalanceDest'
        ]


        # Check for missing columns
        missing_columns = [
            column
            for column in required_columns
            if column not in data
        ]

        if missing_columns:
            return jsonify({
                'status': 'error',
                'message':
                    f'Missing fields: {missing_columns}'
            }), 400


        # Create DataFrame
        df = pd.DataFrame([data])


        # Keep columns in expected format
        df = df[required_columns]


        # Numeric columns
        numeric_cols = [
            'amount',
            'oldbalanceOrg',
            'newbalanceOrig',
            'oldbalanceDest',
            'newbalanceDest'
        ]


        # Convert numeric values
        df[numeric_cols] = df[numeric_cols].apply(
            pd.to_numeric
        )


        print("Data sent to model:")
        print(df)


        # Make prediction
        prediction = int(model.predict(df)[0])


        # Return result
        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'is_fraud': prediction == 1
        })


    except Exception as e:

        # Print actual error in Flask terminal
        print("PREDICTION ERROR:", repr(e))

        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )