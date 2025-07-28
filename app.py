from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import os
import logging
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FraudDetectionAPI')

# Paths to saved artifacts
MODEL_PATH = "fraud_pipeline.joblib"

# Ensure the model exists
if not os.path.exists(MODEL_PATH):
    logger.error(f"Model file not found: {MODEL_PATH}")
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

# Load the full pipeline
try:
    logger.info("Loading fraud detection model...")
    pipeline = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.exception("Failed to load model")
    raise RuntimeError(f"Model loading failed: {str(e)}") from e

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json(force=True) or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify(error="No message provided"), 400

    try:
        pred = pipeline.predict([message])[0]
        proba = pipeline.predict_proba([message])[0]  # Get probability scores
        
        # Return both raw prediction and probabilities for debugging
        return jsonify({
            "result": "Fraudulent" if pred == 1 else "Non-Fraudulent",
            "prediction_value": int(pred),
            "probabilities": {
                "Non-Fraudulent": float(proba[0]),
                "Fraudulent": float(proba[1])
            }
        })
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Simple model test to verify functionality
        test_pred = pipeline.predict(["Health check"])[0]
        return jsonify(
            status="ok",
            model_loaded=True,
            test_prediction=str(test_pred)
        )
    except Exception as e:
        return jsonify(
            status="error",
            error=str(e)
        ), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5001
    port = int(os.environ.get('PORT', 5001))
    
    # Only enable debug mode if explicitly set in environment
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    if debug:
        logger.info("Running in development mode")
    else:
        logger.info("Running in production mode")
    
    app.run(host="0.0.0.0", port=port, debug=debug)