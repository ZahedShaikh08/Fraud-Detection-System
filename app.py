from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import os
import logging
from urllib.request import urlretrieve  # For model downloading

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FraudDetectionAPI')

# Model configuration
MODEL_URL = "https://drive.google.com/uc?export=download&id=YOUR_MODEL_ID"  # REPLACE WITH YOUR ACTUAL URL
MODEL_PATH = "fraud_pipeline.joblib"

# Download model if missing
if not os.path.exists(MODEL_PATH):
    logger.info("Downloading model from cloud storage...")
    try:
        urlretrieve(MODEL_URL, MODEL_PATH)
        logger.info("Model downloaded successfully")
    except Exception as e:
        logger.error(f"Model download failed: {str(e)}")
        raise RuntimeError("Model unavailable") from e

# Load model
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
        proba = pipeline.predict_proba([message])[0]
        
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
    try:
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
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host="0.0.0.0", port=port, debug=debug)