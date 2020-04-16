from flask import Flask, json
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

quotesCache = []
cacheIndex = 0

@app.route("/query/titleOrAuthorSearch/<string:queryParameter>", methods=["GET"])
def titleOrAuthorSearch(queryParameter):
    #TODO DB call
    code = 200
    return json.dumps(queryParameter + " SEARCHED"), code, {"ContentType": "application/json"}

@app.route("/query/tagSearch/<string:tags>", methods=["GET"])
def tagSearch(tags):
    #TODO DB call
    code = 200
    global quotesCache
    global cacheIndex
    if (len(quotesCache) == 0): #Populate cache
        quotes = [''.join(random.choices(string.ascii_letters + string.digits, k = random.randint(500,3500))) for x in range(100)]
        quotesCache = [(json.dumps({"quote" : quotes[i], "Title": "TestTitle", "Author" : "TestAuthor",
                           "tags" : [tags]}), code, {"ContentType": "application/json"}) for i in range(100)]
    quotesToReturn = json.dumps({"quotes": quotesCache[cacheIndex: cacheIndex + 10]}) #TODO indexing past end of array
    cacheIndex += 10
    return quotesToReturn

@app.route("/query/getTags/", methods=["GET"])
def getTags():
    #TODO DB call
    code = 200
    return json.dumps({"tags" : ["Finance", "Business", "Technology"]}), code, {"ContentType": "application/json"}

@app.route("/query/quoteSearch/<string:queryParameter>", methods=["GET"])
def quoteSearch(queryParameter):
    #TODO DB call
    code = 200
    return json.dumps(queryParameter + " SEARCHED"), code, {"ContentType": "application/json"}

@app.route("/mail/sendMail/<string:email>", methods=["GET"])
def sendEmail(email):
    #TODO DB call, email
    code = 200
    return json.dumps(email + " Email Sent"), code, {"ContentType": "application/json"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)