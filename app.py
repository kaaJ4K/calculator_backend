from flask import Flask, request, jsonify
from flask_cors import CORS

from calculator import calculate_basic

from database import (
    init_database,
    save_history,
    get_history,
    delete_history
)


app = Flask(__name__)

CORS(app)


init_database()



@app.route("/")
def home():

    return "Hello Calculator Backend!"



@app.route("/api/health", methods=["GET"])
def health():

    return jsonify(
        {
            "success": True,
            "message": "Backend is running"
        }
    )



@app.route("/api/calculate", methods=["POST"])
def calculate():


    data = request.get_json()


    if not data or "expression" not in data:

        return jsonify(
            {
                "success": False,
                "message": "Missing expression"
            }
        ), 400



    expression = data["expression"]


    try:


        result = calculate_basic(expression)


        save_history(
            expression,
            result
        )


        return jsonify(
            {
                "success": True,
                "expression": expression,
                "result": result
            }
        )



    except Exception as e:


        return jsonify(
            {
                "success": False,
                "message": str(e)
            }
        ), 400





@app.route("/api/history", methods=["GET"])
def history():


    return jsonify(
        get_history()
    )





@app.route("/api/history/<int:history_id>", methods=["DELETE"])
def remove_history(history_id):


    deleted = delete_history(history_id)


    if deleted == 0:

        return jsonify(
            {
                "success": False,
                "message": "History not found"
            }
        ),404



    return jsonify(
        {
            "success": True,
            "message": "Deleted"
        }
    )






if __name__ == "__main__":

    app.run(debug=True)