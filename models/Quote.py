class Quote:
    id = 0
    title = ""
    author = 0
    quote = ""
    tags = []

    def __init__(self, id=None, title=None, author=None, quote=None, tags=None):
        self.id = id
        self.title = title
        self.author = author
        self.quote = quote
        self.tags = tags

def createQuoteFromRequest(request):
    id = request.json["id"]
    title = request.json["title"]
    author = request.json["author"]
    quote = request.json["quote"]
    tags = request.json["tags"].split(",")
    return Quote(id, title, author, quote, tags)