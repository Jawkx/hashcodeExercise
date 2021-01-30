import time

def variance(data):
    # Number of observations
    n = len(data)
    # Mean of the data
    mean = sum(data) / n
    # Square deviations
    deviations = [(x - mean) ** 2 for x in data]
    # Variance
    variance = sum(deviations) / n
    return variance

class Book:
    def __init__(self, bookID , bookScore):
        self.id = bookID
        self.score = bookScore
        self.scanned = False
    
    def __repr__(self):
        return ("Book " + str(self.id) + ", score = " + str(self.score))

    def scanBook(self):
        self.scanned = True
    
    def returnScore(self):
        return self.score
 
class Library:
    def __init__(self, libID , initBooks , shipRate , signUpSpeed):
        self.id = libID
        self.signUpOrder = 0
        self.allBooks = initBooks
        self.shipRate = shipRate
        self.signUpRemaining = signUpSpeed
        self.signUpSpeed = signUpSpeed
        self.signedUp = False
        self.libraryScore = 0
        self.sentBook = []
        self.sortBook()
        
    def __repr__(self):
        return ("\nLibrary " + str(self.id) + "\nShip Rate of " + str(self.shipRate) + "\nSignup remaining: " + str(self.signUpRemaining) + "\nScore: " + str(self.libraryScore))

    def sortBook(self):
        self.allBooks.sort(key = lambda x:x.score , reverse = True)
    
    def filterBook(self):
        self.allBooks = list(filter( lambda book:not book.scanned ,self.allBooks))
        
    def signUp(self):
        if (self.signUpRemaining > 0):
            self.signUpRemaining -= 1
            return False
        else:
            self.signedUp = True
            return True

    def updateScore(self ):
        self.filterBook()
        sumScore = 0
        for book in self.allBooks:
            sumScore += book.score

        if self.shipRate > len(self.allBooks):
            self.shipRate = len(self.allBooks)
        
        self.libraryScore = (sumScore ^ 2) * (self.shipRate) *  ( 1 / self.signUpSpeed ) 
        return self.libraryScore 

    def scanLibrary(self):
        self.sortBook()
        scanned = 0
        idx = 0 
        while scanned < self.shipRate and idx < len(self.allBooks):
            currentBook = self.allBooks[idx]
            if not currentBook.scanned:
                currentBook.scanBook()
                scanned += 1
                self.sentBook.append( self.allBooks[idx].id )
                #print( self.id,self.allBooks , self.allBooks[idx])
            idx += 1

# f = open("a_example.txt","r") # 21
# f = open("b_read_on.txt","r") # 5437900
# f = open("C_incunabula.txt","r") # 5559866
# f = open("d_tough_choices.txt","r") # 5559866
# f = open("e_so_many_books.txt","r") # 3332715
# f = open("f_libraries_of_the_world.txt","r") # 4833572


input_data = f.read().splitlines()
currentLine = input_data[0].split(" ")
totalBooksNumber = int(currentLine[0])
totalLibraryNumber = int(currentLine[1])
daysToScan = int(currentLine[2])
input_data.pop(0)

currentLine = input_data[0].split(" ")
scores = list( map(int,currentLine))
input_data.pop(0)
print(variance(scores))

books = []

for bookID in range(totalBooksNumber):
    books.append( Book( bookID , scores[bookID]) )

librarys = []

for libraryNo in range(totalLibraryNumber):
    currentLine = input_data[0].split(" ")
    input_data.pop(0)
    libraryBooksNum = int(currentLine[0])
    librarySignUpSpeed = int(currentLine[1])
    libraryShipRate = int(currentLine[2])
    
    currentLine = input_data[0].split(" ")
    input_data.pop(0)
    currentContainedBooks = list( map(int,currentLine))
    containedBooks = []
    
    for currentContainedBook in currentContainedBooks:
        containedBooks.append( books[currentContainedBook] )

    currentLibrary = Library(libraryNo,containedBooks,libraryShipRate,librarySignUpSpeed)
    
    librarys.append(currentLibrary)


allScannedBook = []
librarys.sort(key = lambda library:library.updateScore() , reverse = True)

signUpOrder = 0
notSigning = True
signingLibrary = None


for day in range(daysToScan):
    print ("Day" , day )
    if ( notSigning ):
        notSigned = list(filter( lambda library:not library.signedUp , librarys ))
        notSigned.sort(key = lambda library:library.updateScore() , reverse = True )
        if len(notSigned):
            signingLibrary = notSigned[0]
            print(signingLibrary.id)
            signingLibrary.signUpOrder = signUpOrder
            signUpOrder += 1
            notSigning = False
    
    notSigning = signingLibrary.signUp()

    signedUpLib = filter( lambda library: library.signedUp , librarys)
    

    for library in signedUpLib:
        library.scanLibrary()




librarys.sort(key= lambda library:library.signUpOrder)

score = 0
# for library in librarys:
#     print(library.id)
#     print(library.sentBook)

for book in books:
    if book.scanned:
        score += book.score

print("SCORES:")
print(score)

