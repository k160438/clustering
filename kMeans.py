'''
Created on Feb 16, 2011
k Means Clustering for Ch10 of Machine Learning in Action
@author: Peter Harrington
'''
from numpy import *
from sklearn import preprocessing

def loadDataSet(fileName):      #general function to parse tab -delimited floats
    dataMat = []                #assume last column is target value
    fr = open(fileName, 'r')
    for line in fr.readlines():
        curLine = line.strip().split('|')
        if curLine[33]=='' or curLine[35]=='': continue
        if curLine[15] == '': curLine[15] = 79.8255
        if curLine[27] == '': curLine[27] = 35.5
        fltLine = [float(curLine[14]), float(curLine[33]), float(curLine[35])] #map all elements to float()
        dataMat.append(fltLine)

    dataMat = array(dataMat)
    # dataMat = (dataMat - amin(dataMat, axis=0)) / (amax(dataMat, axis = 0) - amin(dataMat, axis=0))
    # dataMat = dataMat * [1, 2, 3]
    dataMat_scaled = preprocessing.scale(dataMat, axis = 0)
    return dataMat_scaled

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)

def sc(dataSet, clusterAss):   #calculate the silhouette coefficient of result
    sc = 0
    m = shape(dataSet)[0]
    k = int(max(clusterAss[:,0])) + 1
    subDataSet = random.choice(m, int(m/100))
    for i in subDataSet:
        centid = int(clusterAss[i, 0])
        disti_sum = [0]*k
        disti_num = [0]*k
        for j in range(m):
            if j==i: continue
            centidJ = int(clusterAss[j, 0])
            disti_num[centidJ] += 1
            disti_sum[centidJ] += distEclud(dataSet[i], dataSet[j])
        for t in range(k):
            disti_sum[t] = float(disti_sum[t])/disti_num[t]
        a_i = disti_sum[centid]
        del disti_sum[centid]
        b_i = min(disti_sum)
        sc += (b_i-a_i)/max(a_i, b_i)
    return sc*100/m

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))#create centroid mat
    for j in range(n):#create random cluster centers, within bounds of each dimension
        minJ = min(dataSet[:,j]) 
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids
    
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))#create mat to assign data points 
                                      #to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        # print(centroids)
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean 
    return centroids, clusterAssment

def biKmeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList =[centroid0] #create a list with one centroid
    for j in range(m):#calc initial Error
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
    print("Start biKmeans!")
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            # print("sseSplit, and notSplit: ",sseSplit,sseNotSplit)
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        print('the bestCentToSplit is: ',bestCentToSplit)
        # print('the len of bestClustAss is: ', len(bestClustAss))
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids 
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
        s_c = sc(dataSet, clusterAssment)
        print('k = ', len(centList))
        print('sse = ', sum(clusterAssment[:, 1]), '; sc = ', s_c)
        print(centList)
        print('*'*20)
    return mat(centList), clusterAssment

dataSet = loadDataSet('data/label_data_info_201804')
print(dataSet.shape)
print(dataSet.mean(axis = 0))
print(dataSet.std(axis = 0))
centList, clusterAssment = biKmeans(dataSet, 8)
    

# import matplotlib
# import matplotlib.pyplot as plt
# def clusterClubs(numClust=5):
#     datList = []
#     for line in open('places.txt').readlines():
#         lineArr = line.split('\t')
#         datList.append([float(lineArr[4]), float(lineArr[3])])
#     datMat = mat(datList)
#     myCentroids, clustAssing = biKmeans(datMat, numClust, distMeas=distSLC)
#     fig = plt.figure()
#     rect=[0.1,0.1,0.8,0.8]
#     scatterMarkers=['s', 'o', '^', '8', 'p', \
#                     'd', 'v', 'h', '>', '<']
#     axprops = dict(xticks=[], yticks=[])
#     ax0=fig.add_axes(rect, label='ax0', **axprops)
#     imgP = plt.imread('Portland.png')
#     ax0.imshow(imgP)
#     ax1=fig.add_axes(rect, label='ax1', frameon=False)
#     for i in range(numClust):
#         ptsInCurrCluster = datMat[nonzero(clustAssing[:,0].A==i)[0],:]
#         markerStyle = scatterMarkers[i % len(scatterMarkers)]
#         ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0], ptsInCurrCluster[:,1].flatten().A[0], marker=markerStyle, s=90)
#     ax1.scatter(myCentroids[:,0].flatten().A[0], myCentroids[:,1].flatten().A[0], marker='+', s=300)
#     plt.show()
