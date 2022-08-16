import random
import os
import copy
import math
import numpy as np
import sys


class Model:

    def __init__(self, K, V, iterNum, alpha, beta, dataset, ParametersStr):
        self.K = K
        self.V = V
        self.iterNum = iterNum
        self.dataset = dataset
        self.ParametersStr = ParametersStr

        self.alpha = alpha
        self.beta = beta



        self.alpha0 = float(K) * float(alpha)
        self.beta0 = float(V) * float(beta)

        self.smallDouble = 1e-150
        self.largeDouble = 1e150


    def runDMM(self, documentSet, outputPath):
        # The whole number of documents
        self.D_All = documentSet.D
        # Cluster assignments of each document               (documentID -> clusterID)
        self.z = [-1] * self.D_All
        # The number of documents in cluster z               (clusterID -> number of documents)
        self.m_z = [0] * self.K
        # The number of words in cluster z                   (clusterID -> number of words)
        self.n_z = [0] * self.K
        # The number of occurrences of word v in cluster z   (n_zv[clusterID][wordID] = number)
        self.n_zv = [[0] * self.V for _ in range(self.K)]
        # different from K, K is clusterID but K_current is clusterNum
        self.K_current = copy.deepcopy(self.K)


        self.intialize(documentSet)
        self.gibbsSampling(documentSet)
        print("\tGibbs sampling successful! Start to saving results.")
        self.output(documentSet, outputPath)
        print("\tSaving successful!")


    def intialize(self, documentSet):
        print("\t" + str(self.D_All) + " documents will be analyze. alpha is" + " %.2f." % self.alpha +
              " beta is" + " %f." % self.beta + "\n\tInitialization.")

        for d in range(0, self.D_All):
            document = documentSet.documents[d]
            cluster = int(self.K * random.random())
            self.z[d] = cluster
            self.m_z[cluster] += 1

            for w in range(document.wordNum):
                wordNo = document.wordIdArray[w]
                wordFre = document.wordFreArray[w]
                self.n_zv[cluster][wordNo] += wordFre
                self.n_z[cluster] += wordFre

    def gibbsSampling(self, documentSet):
        for i in range(self.iterNum):
            print("\titer is ", i + 1, end="\t")
            print("beta is" + " %f." % self.beta, end='\t')
            print("Kcurrent is" + " %f." % self.K_current, end='\n')
            for d in range(0, self.D_All):
                document = documentSet.documents[d]
                cluster = self.z[d]
                self.m_z[cluster] -= 1

                for w in range(document.wordNum):
                    wordNo = document.wordIdArray[w]
                    wordFre = document.wordFreArray[w]
                    self.n_zv[cluster][wordNo] -= wordFre
                    self.n_z[cluster] -= wordFre
                self.checkEmpty(cluster)


                if i != self.iterNum - 1:
                    cluster = self.sampleCluster(document, "iter")
                else:
                    cluster = self.sampleCluster(document, "last")


                self.z[d] = cluster
                self.m_z[cluster] += 1

                for w in range(document.wordNum):
                    wordNo = document.wordIdArray[w]
                    wordFre = document.wordFreArray[w]
                    self.n_zv[cluster][wordNo] += wordFre
                    self.n_z[cluster] += wordFre

    def sumNormalization(self, x):
        """Normalize the prob."""
        x = np.array(x)
        norm_x = x / np.sum(x)
        return norm_x

    '''
    MODE
    "iter"  Iteration after initialization.
    "last"  Last iteration.
    '''
    def sampleCluster(self, document, MODE):
        prob = [float(0.0)] * (self.K)
        overflowCount = [float(0.0)] * (self.K)


        for k in range(self.K):
            valueOfRule1 = (self.m_z[k] + self.alpha) # / (self.D_All - 1 + self.alpha0)
            valueOfRule2 = 1.0
            i = 0
            for _, w in enumerate(range(document.wordNum)):
                wordNo = document.wordIdArray[w]
                wordFre = document.wordFreArray[w]
                for j in range(wordFre):
                    if valueOfRule2 < self.smallDouble:
                        overflowCount[k] -= 1
                        valueOfRule2 *= self.largeDouble

                    valueOfRule2 *= (self.n_zv[k][wordNo] + self.beta + j) / (self.n_z[k] + self.beta0 + i)
                    i += 1
            prob[k] = valueOfRule1 * valueOfRule2

        max_overflow = -sys.maxsize
        for k in range(self.K):
            if overflowCount[k] > max_overflow and prob[k] > 0.0:
                max_overflow = overflowCount[k]
        for k in range(self.K):
            if prob[k] > 0.0:
                prob[k] = prob[k] * math.pow(self.largeDouble, overflowCount[k] - max_overflow)

        prob = self.sumNormalization(prob)

        if MODE == "iter":
            kChoosed = 0
            for k in range(1, self.K):
                prob[k] += prob[k - 1]
            thred = random.random()
            while kChoosed < self.K:
                if thred < prob[kChoosed]:
                    break
                kChoosed += 1
            return kChoosed

        elif MODE == "last":
            kChoosed = 0
            bigPro = prob[0]
            for k in range(1, self.K):
                if prob[k] > bigPro:
                    bigPro = prob[k]
                    kChoosed = k
            return kChoosed

    # update K_current
    def checkEmpty(self, cluster):
        if self.m_z[cluster] == 0:
            self.K_current -= 1

    def output(self, documentSet, outputPath):
        outputDir = outputPath + self.dataset + self.ParametersStr + "/"
        try:
            # create result/
            isExists = os.path.exists(outputPath)
            if not isExists:
                os.mkdir(outputPath)
                print("\tCreate directory:", outputPath)
            # create after result
            isExists = os.path.exists(outputDir)
            if not isExists:
                os.mkdir(outputDir)
                print("\tCreate directory:", outputDir)
        except:
            print("ERROR: Failed to create directory:", outputDir)
        self.outputClusteringResult(outputDir, documentSet)

    def outputClusteringResult(self, outputDir, documentSet):
        outputPath = outputDir + str(self.dataset)+ "ClusteringResult" + ".txt"
        writer = open(outputPath, 'w')
        for d in range(0, self.D_All):
            cluster = self.z[d]
            writer.write(str(d+1) + " "+str(cluster) + "\n")
        writer.close()
