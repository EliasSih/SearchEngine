import re


# reading the query files into an array

def getQueries(dir, *args):

    queries = []
    for queryDoc in args:
        f = open(dir + queryDoc, "r")
        query = f.read()
        # print("query", query, sep= ":")
        queries.append(query)
    return queries

# reading the individual documents into an array

def getDocs(DocPath):
    documents = []
    with open("testbed/Doc_Collection", "r", encoding="utf-8") as file:
        doc_collection = file.read()

    documents = doc_collection.split(".I")
    return documents

def main():
    # relevance scoring through terminal interface
    queries = getQueries("testbed/", "query.1", "query.2", "query.3")
    documents = getDocs("testbed/Doc_Collection")
    print(documents)

    for query in queries:
        for doc in documents:
            print("....................Query.........................", query, sep="\n")
            print("....................Document........................", doc, sep="\n")
            print("on a scale od 0-2, how well does the document match the query?")
            relScore = eval(input("Enter the relevance score"))
            relEntry = str(documents.index(doc)) + " " + str(relScore)
            print("entry:" + relEntry)
            relFile = "relevance" + query[-2]
            with open(relFile, "a") as file:
                file.write(relEntry + "\n")

if __name__ == '__main__':
    main()
