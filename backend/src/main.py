# src/main.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.evaluator import evaluate_code

app = Flask(__name__)
CORS(app)  # Allows frontend to connect (avoid CORS issues)

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    data = request.get_json()
    code = data.get('code', '')
    print(code)

    if not code.strip():
        return jsonify({
            "status": "error",
            "message": "Code input is empty"
        }), 400

    result = evaluate_code(code)
    print(result)

    # return jsonify({"message": "Code Scorer API is running"}), 200
    if result["status"] == "success":
        formatted_tokens = result.get("tokens", [])

        formatted_result = {
            "status": "success",
            "tokens": formatted_tokens,
            "ast_tree": result.get("ast_tree", "Not available"),
            "features": result.get("features", {}),
            "score": result.get("score"),
            "debug_info": result.get("debug_info", None)
        }

        return jsonify(formatted_result), 200

    else:
        return jsonify({
            "status": "error",
            "stage": result.get("stage"),
            "message": result.get("message"),
            "errors": result.get("errors", [])
        }), 400

@app.route('/')
def home():
    return jsonify({"message": "Code Scorer API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True)
