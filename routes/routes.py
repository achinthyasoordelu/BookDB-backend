from flask import Flask, json, request
from flask_cors import CORS
import random
import string
from models import Quote
from database.databaseAccessor import databaseAccessor

app = Flask(__name__)
CORS(app)

#TODO tag cache (don't need to pull tags everytime, once should be good for any single run of the app, probably)
quotesCache = []
tagCache = []
previousSearch = ""
cacheIndex = 0
db = databaseAccessor()
JSON_CONTENT_TYPE = {"ContentType": "application/json"}

def testQuotes(tags=None, code=200):
    global quotesCache
    global cacheIndex
    if (len(quotesCache) == 0):  # Populate cache
        quotes = [''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(500, 3500))) for x in
                  range(100)]
        quotesCache = [(json.dumps({"quote": quotes[i], "Title": "TestTitle", "Author": "TestAuthor",
                                    "tags": [tags]}), code, JSON_CONTENT_TYPE) for i in range(100)]
    quotesToReturn = json.dumps({"quotes": quotesCache[cacheIndex: cacheIndex + 10]})  # TODO indexing past end of array
    cacheIndex += 10
    return quotesToReturn

@app.route("/insertQuote", methods=["POST"])
def insertQuote():
    quote = Quote.createQuoteFromRequest(request)
    print("{}, {}, {}, {}".format(quote.title, quote.author, quote.quote, quote.tags))
    db.insertQuote(quote)
    return json.dumps(200)

@app.route("/query/titleOrAuthorSearch/<string:queryParameter>", methods=["GET"])
def titleOrAuthorSearch(queryParameter):
    global previousSearch
    if previousSearch != queryParameter:
        resetCache(db.selectByTitleOrAuthor(queryParameter))
        previousSearch = queryParameter
    return getQuotesFromCache(), 200, JSON_CONTENT_TYPE

@app.route("/query/tagSearch/<string:tags>", methods=["GET"])
def tagSearch(tags):
    #TODO DB call
    return testQuotes(tags, 200)

@app.route("/query/getTags/", methods=["GET"])
def getTags():
    global tagCache
    if (len(tagCache) == 0):
        tagCache = db.getTags()
    code = 200
    return json.dumps(tagCache), code, {"ContentType": "application/json"}

@app.route("/query/quoteSearch/<string:queryParameter>", methods=["GET"])
def quoteSearch(queryParameter):
    global previousSearch
    if previousSearch != queryParameter:
        resetCache(db.selectQuotes(queryParameter))
        previousSearch = queryParameter
    return getQuotesFromCache(), 200, JSON_CONTENT_TYPE

@app.route("/mail/sendMail/<string:email>", methods=["GET"])
def sendEmail(email):
    #TODO DB call, email
    code = 200
    return json.dumps(email + " Email Sent"), code, {"ContentType": "application/json"}

def resetCache(newCache):
    global quotesCache
    global cacheIndex
    quotesCache = newCache
    cacheIndex = 0

def getQuotesFromCache():
    global quotesCache
    global cacheIndex
    quotesToReturn = json.dumps({"quotes": quotesCache[cacheIndex: cacheIndex + 10]})
    cacheIndex += 10
    return quotesToReturn

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)