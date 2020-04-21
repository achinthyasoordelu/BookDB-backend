from sqlalchemy import create_engine, text
import database.databaseModels as models

databaseURI = "mysql://root:****@localhost:3306/bookdb"

class databaseAccessor:
    engine = create_engine(databaseURI)
    dbConnection = engine.connect()

    def insertQuote(self, quote):
        insertQuote = models.quotesTable.insert().values(Title=quote.title, Author=quote.author,Quote=quote.quote)
        result = self.dbConnection.execute(insertQuote)
        quoteID = result.inserted_primary_key[0]
        self.insertQuoteTags(quoteID, quote.tags)

    def insertQuoteTags(self, quoteID, tags):
        for tag in tags:
            insertQuoteTags = models.quotesTagsTable.insert().values(QuoteID=quoteID, Tag=tag)
            self.dbConnection.execute(insertQuoteTags)

    def selectQuotes(self, searchTerm):
        search = text("SELECT QuoteID, Title, Author, Quote, GROUP_CONCAT(Tag) as 'Tags' FROM quotes NATURAL JOIN quotetags "
                      "WHERE quotes.Quote like :searchTerm  GROUP BY quotes.QuoteID")
        result = self.dbConnection.execute(search, searchTerm="%" + searchTerm + "%")
        return self.getListFromResult(result)

    def selectByTitleOrAuthor(self, searchTerm):
        search = text("SELECT QuoteID, Title, Author, Quote, GROUP_CONCAT(Tag) as 'Tags' FROM quotes NATURAL JOIN quotetags "
                      "WHERE quotes.Title like :searchTerm OR quotes.Author like :searchTerm GROUP BY quotes.QuoteID")
        result = self.dbConnection.execute(search, searchTerm="%" + searchTerm + "%")
        return self.getListFromResult(result)

    def searchByTags(self, tags):
        whereClauses = []
        for tag in tags:
            whereClauses.append("Tags like {}".format("'%%" + tag + "%%'"))
        whereClause = " AND ".join(whereClauses)
        search = "SELECT * FROM (SELECT QuoteID, Title, Author, Quote, GROUP_CONCAT(Tag) as 'Tags' FROM quotes " \
                 "NATURAL JOIN quotetags GROUP BY quotes.QuoteID) AS Quotes WHERE " + whereClause
        result = self.dbConnection.execute(search)
        return self.getListFromResult(result)

    def getListFromResult(self, result):
        returnList = []
        for row in result:
            returnList.append(dict(row))
        return returnList

    def getTags(self):
        result = self.dbConnection.execute(models.tagsTable.select())
        tagDict = {"tags" : []}
        for row in result:
            tagDict["tags"].append(row[0])
        return tagDict