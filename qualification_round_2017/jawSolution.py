class Request:
    def __init__(self,ID,vidID,NoR,Enp):
        self.ID = ID
        self.vidID = vidID
        self.NoR = NoR
        self.Enp = Enp

        self.fullfilled = False
    
    def updateFullfilled()
        self.fullfilled = True
    

class Cache:
    def __init__(self,ID):
        self.ID = ID
        self.storage = cacheSize
        self.score = 0
        self.connections = {
            # Endpoint : (DC lat , cache latency)
        }
        self.requests = { 
            # VideoID : (Size,Endpoint,Magnitude) 
        }
        self.savedTimes = []
        self.videos = []
    
    def hasVid(self,inputVid):
        if inputVid in self.videos:
            return True
        else:
            return False

    def checkStorage(self,val):
        if ( (self.storage - val) < 0 ):
            return False
        else:
            return True
    
    def changeStorage(self,val):
        self.storage = self.storage + val 
    
    def addRequest(self, size ,videoID , endpoint , numberOfRequest):
        self.requests[videoID] = ( size ,endpoint,numberOfRequest)
    
    def calculateSavedTime(self):
        for video in self.requests:
            size ,endpoint , numberOfRequests = self.requests[video]
            # endpoint = self.requests[video][1]
            # numberOfRequest = self.requests[video][2]
            
            if self.connections[endpoint] and (video not in self.videos):
                savedTime = (self.connections[endpoint][0] - self.connections[endpoint][1]) * numberOfRequests
                self.savedTimes.append((video,savedTime))
            print("At cache" ,self.ID ,"placing video",video ,"will save", savedTime , "ms")
     
    def populateVideo(self,fileSize):
        self.savedTimes.sort( key = lambda x:x[1] , reverse=True)
        print(self.savedTimes)

    def addConnection(self , endpoint , latencyDC , latencyCache):
        self.connections[ endpoint ] = (latencyDC , latencyCache)
        
    def checkUsed(self):
        if (len(self.videos) > 0 ):
            return True
        else:
            return False
    
    def isID(self,arr):
        if self.ID in arr:
            return True
        else:
            return False
    
    def addVideo(self,vidID):
        self.videos.append(vidID)

class Endpoint:
    def __init__(self, ID, latencyDC , connections):
        self.ID = ID
        self.latencyDC = latencyDC
        self.connections = connections

    def isID(self,val):
        if (self.ID == val):
            return True
        else:
            return False
    
    def haveCache(self):
        if (self.connections):
            return True
        else:
            return false

    def getConnectedCache(self):
        return [ item[0] for item in self.connections ]

    def checkConnection(self,val):
        if (val in self.connections):
            return True
            
    def getConnectionCount(self):
        return len(self.connections)

f = open("testing.txt","r")
# f = open("me_at_the_zoo.in" , "r")
input_data = f.read().splitlines()

print("Loading Data")
currentLine = input_data[0].split(" ")
numberOfCache = int(currentLine[3])
numberOfEndPoints = int(currentLine[1])
cacheSize = int(currentLine[4])
totalRequest = int(currentLine[2])
input_data.pop(0)

currentLine = input_data[0].split(" ")
fileSize = list( map(int,currentLine))
input_data.pop(0)

print("Generating caches")
# Generating Caches
caches = []
for x in range (numberOfCache):
    caches.append(Cache(x))

print("Generating endpoints")
# Generating endpoints
endpoints = []
for x in range(numberOfEndPoints):
    currentConnections = []
    currentLine = input_data[0].split(" ")
    dataCenterLat = int(currentLine[0])
    currentNumberOfCache = int(currentLine[1])
    input_data.pop(0)
    
    for j in range(currentNumberOfCache):
        currentLine = input_data[0].split(" ")
        currentConnections.append( ( int(currentLine[0]) , int(currentLine[1])))
        input_data.pop(0)

    for currentConnection in currentConnections:
        currentCache = currentConnection[0]
        currentCacheLat = currentConnection[1]

        caches[currentCache].addConnection( x, dataCenterLat,currentCacheLat )

    endpoints.append(Endpoint(x,dataCenterLat,currentConnections))
    
    
endpointsWithCache = list(filter(lambda x:x.getConnectionCount() , endpoints))

#print(endpoints[0].getConnectedCache())
requests = []

for data in input_data:
    request = list ( map(int, data.split(" ")))
    requests.append(request)

for request in requests:
    [currentVideoID , currentEndpoint , currentRequestCount] = request
    connectedCaches = endpoints[currentEndpoint].getConnectedCache()
    
    for cache in connectedCaches:
        if fileSize[currentVideoID] <= cacheSize:
            caches[cache].addRequest( fileSize[currentVideoID],currentVideoID,currentEndpoint,currentRequestCount)

for cache in caches:
    cache.calculateSavedTime()
    cache.populateVideo(fileSize)

###UNDER DEVELOPMENT LATER UNCOMENT ALL###
# idx = 0
# for request in requests:
#     idx = idx+1
#     #print("currently processing request " + str(idx))
#     currentVideoID = request[0]
#     currentEndpoint = request[1]

#     currentFileSize = fileSize[currentVideoID]

#     if (currentFileSize > cacheSize):
#         continue

    
#     matchingEndPoints = list(filter( lambda x:x.isID(currentEndpoint) , endpointsWithCache))

#     if not matchingEndPoints:
#         continue

#     #End point have cache
#     currentEndpointObj = matchingEndPoints[0]
#     currentCacheOptions = currentEndpointObj.getLeastLatencyCache()

#     for currentCacheOption in currentCacheOptions:
#         currentCache = caches[currentCacheOption]
#         if currentCache.checkStorage(currentFileSize): #enough storage
#             currentCache.addVideo(currentVideoID)
#             currentCache.changeStorage(-currentFileSize)
#             continue


# cachesUsed = len(list(filter( lambda x:x.checkUsed(),caches)))
# print(cachesUsed)
# outF = open("out.txt","w")
# outF = open("out.txt","a")

# outF.write(str(cachesUsed) + "\n")
# print("====ANSWER====")
# idx = 0
# for cache in caches:
#     outF.write(str(idx) + " ")
#     for video in cache.videos:
#         outF.write(str(video) +" ")
    
#     outF.write("\n")
#     idx+=1

