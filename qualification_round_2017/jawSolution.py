class Request:
    def __init__(self,ID,vidID,NoR,Enp , vidSize):
        self.ID = ID
        self.vidID = vidID
        self.NoR = NoR
        self.Enp = Enp
        self.vidSize = videoSize
        self.savedTime = 0
        self.fullfilled = False
        
    def checkFillable(self , remainingVal ):
        storedValue = remainingVal - videoSize
        if storedValue >= 0:
            return( storedValue )
        else:
            return None

    def updateFullfilled(self):
        self.fullfilled = True
    
    def updateSavedTime(self , value ):
        self.savedTime = value

class Cache:
    def __init__(self, ID , cacheSize):
        self.ID = ID
        self.storage = cacheSize
        self.timeSavedRanking = []
        self.requests = {
            # timeSaved : RequestOBJ

        }
        self.videosStored = []
        self.totalTimeSaved = 0
    
    def receiveRequest(self, requestObj , latencyDiff):
        timeSaved = requestObj.NoR * latencyDiff
        self.requests[ timeSaved ] = requestObj
    
    def sortRequest(self):
        self.timeSavedRanking = sorted(self.requests , reverse=True)

    def populateCache(self):
        print("Populating Cache" , self.ID)
        for timeSaved in self.timeSavedRanking:
            requestObj = self.requests[timeSaved]
            fullfillStatus = not requestObj.fullfilled

            remainingValue = requestObj.checkFillable(self.storage)

            if fullfillStatus and remainingValue != None and (requestObj.vidID not in self.videosStored ) :
                self.videosStored.append(requestObj.vidID)
                
                self.storage = remainingValue
                
                requestObj.updateFullfilled()
                requestObj.updateSavedTime( timeSaved )

        return self.totalTimeSaved

class Endpoint:
    def __init__(self,ID,latencyDC):
        self.ID = ID 
        self.latencyDC = latencyDC
        self.connections = {
            # CACHE NUMBER : #LATENCY
        }
        self.requests = []

    def addRequest(self,requestObj):
        self.requests.append(requestObj)
    
    def updateConnections( self, cacheID , cacheLat):
        self.connections[cacheID] = cacheLat
    
    def sendRequest(self):
        idx = 0
        for cacheNo in self.connections:
            print("Sending request to" ,cacheNo , "from endpoint" , self.ID)
            latencyDiff = self.latencyDC - self.connections[cacheNo]

            for requestObj in self.requests:
                caches[cacheNo].receiveRequest(requestObj,latencyDiff)

### Starting        
# f = open("testing.txt","r")
# f = open("me_at_the_zoo.in" , "r")
# f = open("videos_worth_spreading.in" , "r")
# f = open("trending_today.in" , "r")
# f = open("kittens.in.txt" , "r")

input_data = f.read().splitlines()
currentLine = input_data[0].split(" ")
numberOfCache = int(currentLine[3])
numberOfEndPoints = int(currentLine[1])
cacheSize = int(currentLine[4])
numOfRequest = int(currentLine[2])
input_data.pop(0)

currentLine = input_data[0].split(" ")
fileSize = list( map(int,currentLine))
input_data.pop(0)

print("Generating caches ... ")
caches = []
for x in range (numberOfCache):
    caches.append(Cache(x,cacheSize))

print("Generating Endpoints ... ")
endpoints = []
for x in range(numberOfEndPoints):
    currentConnections = []
    currentLine = input_data[0].split(" ")
    dataCenterLat = int(currentLine[0])
    currentNumberOfCache = int(currentLine[1])
    input_data.pop(0)

    currentEndpoint = Endpoint(x,dataCenterLat)

    for j in range(currentNumberOfCache):
        currentLine = input_data[0].split(" ")
        currentCacheNo = int(currentLine[0])
        currentCacheLat = int(currentLine[1])
        currentEndpoint.updateConnections(currentCacheNo,currentCacheLat)
        
        input_data.pop(0)

    endpoints.append(currentEndpoint)

print("Parsing Request ... ")

requests = []
requestNo = 0
totalNumberOfRequest = 0
for data in input_data:
    currentRequestData = list ( map(int, data.split(" ")))
    [videoID,endpointNo,NOReq] = currentRequestData
    totalNumberOfRequest += NOReq
    videoSize = fileSize[videoID]
    if videoSize <= cacheSize :
        request = Request(requestNo,videoID,NOReq,endpointNo,videoSize)
        requests.append(request)
        endpoints[endpointNo].addRequest(request)
        
#print(endpoints[1].requests)

print("Sending Requests")

for endpoint in endpoints:
    endpoint.sendRequest()

print("Calculating request")

totalTimeSaved = 0

for cache in caches:
    cache.sortRequest()
    totalTimeSaved += cache.populateCache()
    print( "At cache" , cache.ID , "Video Stored was" , cache.videosStored)
    

score = (totalTimeSaved/totalNumberOfRequest)*1000

print("calculatingScore")

totalTimeSaved = 0
for request in requests:
    totalTimeSaved += request.savedTime
    print(request.savedTime)

score = (totalTimeSaved/totalNumberOfRequest)*1000
print( " TOTAL TIME SAVED:" , totalTimeSaved)
print(" TOTAL SCORE:" , score )
