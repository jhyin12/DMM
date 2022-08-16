from DocumentSet import DocumentSet
from Model import Model


class DMM:

    def __init__(self, K, alpha, beta, iterNum, dataset):
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.iterNum = iterNum
        self.dataset = dataset

        self.wordToIdMap = {}
        self.dataDir = "../data/"
        self.outputPath = "../result/"

    def getDocuments(self):
        self.documentSet = DocumentSet(self.dataDir + self.dataset, self.wordToIdMap)
        self.V = self.wordToIdMap.__len__()

    def runDMM(self):
        ParametersStr = "K" + str(self.K) + "alpha" + str(round(self.alpha, 3)) + "beta" + str(round(self.beta, 3)) + "iterNum" + str(self.iterNum)

        model = Model(self.K, self.V, self.iterNum, self.alpha, self.beta, 
                      self.dataset, ParametersStr)
        model.runDMM(self.documentSet, self.outputPath)
