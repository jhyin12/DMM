

from DMM import DMM
K = 89
alpha = 0.1
beta = 0.1
iterNum = 10
dataset = "Tweet"


def runDMM(K, alpha, beta, iterNum, dataset):
    dmm = DMM(K, alpha, beta, iterNum, dataset)
    dmm.getDocuments()
    dmm.runDMM()


if __name__ == '__main__':
    runDMM(K, alpha, beta, iterNum, dataset)