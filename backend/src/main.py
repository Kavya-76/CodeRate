import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from core.evaluator import evaluate_code
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

    @app.route('/api/analyze', methods=['POST'])
    def analyze_code():
        try:
            data = request.get_json(force=True)
            code = data.get('code', '').strip()

            if not code:
                return jsonify({
                    "status": "error",
                    "message": "Code input is empty"
                }), 400

            logging.info("Received code for analysis.")

            result = evaluate_code(code)

            if result["status"] == "success":
                return jsonify({
                    "status": "success",
                    "tokens": result.get("tokens", []),
                    "ast_tree": result.get("ast_tree", "Not available"),
                    "features": result.get("features", {}),
                    "score": result.get("score"),
                    "debug_info": result.get("debug_info")
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "stage": result.get("stage"),
                    "message": result.get("message"),
                    "errors": result.get("errors", [])
                }), 400

        except HTTPException as http_err:
            logging.error(f"HTTP error: {http_err}")
            return jsonify({
                "status": "error",
                "message": str(http_err)
            }), http_err.code

        except Exception as e:
            logging.exception("Unexpected error during code analysis")
            return jsonify({
                "status": "error",
                "message": "Internal server error"
            }), 500

    @app.route('/')
    def home():
        return jsonify({"message": "Code Scorer API is running"}), 200

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"}), 200

    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    # For local development
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    app.run(host=host, port=port, debug=debug)