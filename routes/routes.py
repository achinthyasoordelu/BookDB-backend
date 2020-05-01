from flask import Flask, json, request
from flask_cors import CORS
from models import Quote
from database.databaseAccessor import databaseAccessor

app = Flask(__name__)
CORS(app)

quotesCache = []
tagCache = []
previousSearch = ""
cacheIndex = 0
db = databaseAccessor()
JSON_CONTENT_TYPE = {"ContentType": "application/json"}

@app.route("/insertQuote", methods=["POST"])
def insertQuote():
    quote = Quote.createQuoteFromRequest(request)
    try:
        db.insertQuote(quote)
        return json.dumps(200)
    except:
        return json.dumps(500)

@app.route("/updateQuote", methods=["POST"])
def updateQuote():
    quote = Quote.createQuoteFromRequest(request)
    try:
        db.updateQuote(quote)
        return json.dumps(200)
    except:
        return json.dumps(500)

@app.route("/query/titleOrAuthorSearch/<string:queryParameter>", methods=["GET"])
def titleOrAuthorSearch(queryParameter):
    global previousSearch
    if previousSearch != queryParameter:
        resetCache(db.selectByTitleOrAuthor(queryParameter))
        previousSearch = queryParameter
    else:
        resetCacheIndex()
    return getQuotesFromCache(), 200, JSON_CONTENT_TYPE

@app.route("/query/tagSearch/<string:tags>", methods=["GET"])
def tagSearch(tags):
    global previousSearch
    if previousSearch != tags:
        resetCache(db.searchByTags(tags.split(",")))
        previousSearch = tags
    else:
        resetCacheIndex()
    return getQuotesFromCache(), 200, JSON_CONTENT_TYPE

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
    else:
        resetCacheIndex()
    return getQuotesFromCache(), 200, JSON_CONTENT_TYPE

def resetCache(newCache):
    global quotesCache
    global cacheIndex
    quotesCache = newCache
    cacheIndex = 0

def resetCacheIndex():
    global quotesCache
    global cacheIndex
    if (cacheIndex >= len(quotesCache)):
        cacheIndex = 0

@app.route("/query/continueQuery/", methods=["GET"])
def getQuotesFromCache():
    global quotesCache
    global cacheIndex
    quotesToReturn = json.dumps({"quotes": quotesCache[cacheIndex: cacheIndex + 10]})
    cacheIndex += 10
    print(quotesToReturn)
    return quotesToReturn

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=266533)