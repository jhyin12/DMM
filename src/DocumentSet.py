import json
from Document import Document



class DocumentSet:

    def __init__(self, dataDir, wordToIdMap):
        self.D = 0
        self.documents = []
        with open(dataDir) as input:
            line = input.readline()
            while line:
                self.D += 1
                obj = json.loads(line)
                text = obj['text']
                document = Document(text, wordToIdMap)
                self.documents.append(document)
                line = input.readline()
        print("number of documents is ", self.D)
