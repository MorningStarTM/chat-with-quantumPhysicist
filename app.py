from flask import Flask, render_template, request, jsonify
from utils import process_answer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    question = request.form.get("question")
    answer, metadata = process_answer(question)
    print(answer)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
