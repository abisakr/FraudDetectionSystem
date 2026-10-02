from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

try:
    model = joblib.load('creditcard_fraud_detection_model.pkl')
    print("Fraud Detection Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Make sure 'creditcard_fraud_detection_model.pkl' is in the same folder as app.py")

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Get data from frontend 
        data = request.json
        df = pd.DataFrame([data])
        
        numeric_cols = [
            'amount', 'oldbalanceOrg', 'newbalanceOrig', 
            'oldbalanceDest', 'newbalanceDest'
        ]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        
        prediction = int(model.predict(df)[0])
        
        return jsonify({
            'status': 'success',
            'is_fraud': bool(prediction == 1)
        })

    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)