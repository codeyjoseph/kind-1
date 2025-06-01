from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/message", methods=["POST"])
def receive():
	data = request.get_json()
	print(data)
	return {"response": "success"}

app.run(host="0.0.0.0")