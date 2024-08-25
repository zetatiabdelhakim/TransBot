from config import app
from flask import jsonify
from RAG_V1 import ask_question


@app.route('/question/<question>', methods=["GET"])
def reponse(question):
    reponse = ask_question(question)
    return jsonify({"response": reponse})


if __name__ == "__main__":
    app.run(debug=True)
