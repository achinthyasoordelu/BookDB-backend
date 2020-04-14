from flask import Flask, request, abort, json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/query/titleOrAuthorSearch/<string:queryParameter>", methods=["GET"])
def titleOrAuthorSearch(queryParameter):
    #TODO DB call
    code = 200
    return json.dumps(queryParameter + " SEARCHED"), code, {"ContentType": "application/json"}

@app.route("/query/tagSearch/<string:tags>", methods=["GET"])
def tagSearch(tags):
    #TODO DB call
    code = 200
    return json.dumps(tags + " SEARCHED"), code, {"ContentType": "application/json"}

@app.route("/query/quoteSearch/<string:queryParameter>", methods=["GET"])
def quoteSearch(queryParameter):
    #TODO DB call
    code = 200
    return json.dumps(queryParameter + " SEARCHED"), code, {"ContentType": "application/json"}

@app.route("/mail/sendMail/<string:email>", methods=["GET"])
def quoteSearch(email):
    #TODO DB call, email
    code = 200
    return json.dumps(email + " Email Sent"), code, {"ContentType": "application/json"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)