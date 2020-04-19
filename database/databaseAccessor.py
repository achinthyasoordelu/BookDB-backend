from sqlalchemy import create_engine, text
import database.databaseModels as models

databaseURI = "mysql://root:****@localhost:3306/bookdb"

class databaseAccessor:
    engine = create_engine(databaseURI)
    dbConnection = engine.connect() #TODO cache
    print(engine.table_names())

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
        search = text("SELECT Title, Author, Quote, GROUP_CONCAT(Tag) as 'Tags' FROM quotes NATURAL JOIN quotetags "
                      "WHERE quotes.Quote like :searchTerm  GROUP BY quotes.QuoteID")
        result = self.dbConnection.execute(search, searchTerm="%" + searchTerm + "%")
        returnList = []
        for row in result:
            returnList.append(dict(row))
        return returnList