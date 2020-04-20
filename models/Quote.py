class Quote:
    title = ""
    author = 0
    quote = ""
    tags = []

    def __init__(self, title=None, author=None, quote=None, tags=None):
        self.title = title
        self.author = author
        self.quote = quote
        self.tags = tags

def createQuoteFromRequest(request):
    title = request.json["title"]
    author = request.json["author"]
    quote = request.json["quote"]
    tags = request.json["tags"].split(",")
    return Quote(title, author, quote, tags)