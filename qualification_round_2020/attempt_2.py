import time
class Book:
    def __init__(self, bookID , bookScore):
        self.id = bookID
        self.score = bookScore
        self.scanned = False
    
    def __repr__(self):
        return ("Book " + str(self.id) + ", score = " + str(self.score))

    def scanBook(self):
        self.scanned = True
        return self.id 

class Library:
    def __init__(self, libID , initBooks , shipRate , signUpSpeed):
        self.id = libID
        self.signUpOrder = None
        self.books = initBooks
        self.shipRate = shipRate
        self.signUpRemaining = signUpSpeed
        self.isSigning = False
        self.signedUp = False
        self.score = 0
        self.booksScore = 0
        self.sentBooks = []
        self.sortBook()
        
    def __repr__(self):
        return ("\nLibrary" + str(self.id) )

    def filterBook(self):
        """ Filter out the library's book that are scanned => None"""
        self.books = list(filter( lambda book:not book.scanned ,self.books))

    def sortBook(self):
        """ Sort library's book From High to Low Score => None"""
        self.books.sort(key = lambda x:x.score , reverse = True)

    def signUp(self):
        """ Sign up the library (by one day) => True when Sign up is completed """
        if (self.signUpRemaining > 1):
            self.signUpRemaining -= 1
            return False
        else:
            self.signedUp = True
            return True

    # def filterSortLibrary(self):
    #     self.filterBook()
    #     self.sortBook()
    
    def getLibScore(self,dayRemaining):
        self.filterBook()
        #self.sortBook()

        remDayAfterSignUp = dayRemaining - self.signUpRemaining

        canSignUpBook = self.books[0:(remDayAfterSignUp * self.shipRate)]
        # # Specially for D
        # score = len(canSignUpBook)
        # return score
        booksScore = sum(map( lambda book:book.score , canSignUpBook))
        
        score = (booksScore)/(self.signUpRemaining)
        
        return score

    def getBookScore(self , dayRemaining):
        self.filterBook()
        remDayAfterSignUp = dayRemaining - self.signUpRemaining

        canSignUpBook = self.books[0:remDayAfterSignUp]
        booksScore = sum(map( lambda book:book.score , canSignUpBook))
        self.booksScore = booksScore

        return booksScore
        
    def getSignUpTime(self):
        """ Filter and sort book and get score for the current library => score"""
        # self.filterBook()
        # self.sortBook()

        #remDayAfterSignUp = dayRemaining - self.signUpRemaining
        
        #canSignUpBook = self.books[0:remDayAfterSignUp]

        #booksScore = sum(map( lambda book:book.score , self.books))
        
        # signUpDrawback = self.signUpRemaining
        # self.bookScore = booksScore

        return 1/self.signUpRemaining
           
    def scanLibrary(self):
        self.filterBook()
        toScan = self.books[0:self.shipRate]
        
        for book in toScan:
            self.sentBooks.append( book.id )
            book.scanBook()
        #self.sentBook += list(map(lambda book: book.scanBook() , toScan))
        return 1


# filename = "a_example" # Score 21
# filename = "b_read_on" # Score :5822900
# filename = "C_incunabula" #5689822
# filename = "d_tough_choices" #score 5032560
# filename = "e_so_many_books"  #5089288
# filename = "f_libraries_of_the_world" #5216624

f = open(filename + ".txt" , "r")

input_data = f.read().splitlines()
currentLine = input_data[0].split(" ")
totalBooksNumber = int(currentLine[0])
totalLibraryNumber = int(currentLine[1])
daysToScan = int(currentLine[2])
input_data.pop(0)

currentLine = input_data[0].split(" ")
scores = list( map(int,currentLine))
input_data.pop(0)

# GENERATING BOOKS
books = []

for bookID in range(totalBooksNumber):
    books.append( Book( bookID , scores[bookID]) )

# GENERATING LIBRARYS
librarys = []
signInDayTotal = 0

for libraryNo in range(totalLibraryNumber):
    currentLine = input_data[0].split(" ")
    input_data.pop(0)

    libraryBooksNum = int(currentLine[0])
    librarySignUpSpeed = int(currentLine[1])
    libraryShipRate = int(currentLine[2])
    
    signInDayTotal += librarySignUpSpeed

    currentLine = input_data[0].split(" ")
    input_data.pop(0)
    currentContainedBooks = list( map(int,currentLine))
    containedBooks = []
    
    for currentContainedBook in currentContainedBooks:
        containedBooks.append( books[currentContainedBook] )

    currentLibrary = Library(libraryNo,containedBooks,libraryShipRate,librarySignUpSpeed)
    
    librarys.append(currentLibrary)

meanSignInDay = signInDayTotal/totalLibraryNumber

#map(lambda library:library.filterSortLibrary() , librarys)
librarys.sort(key = lambda library:library.getLibScore(daysToScan) , reverse = True )

orderNumber = 0
notSigning = True
signingLibrary = None

scanCount = 0

for day in range(daysToScan):
    todayScannedBook = []
    daysRemaining = daysToScan-day
    print ("Day" , day )

    

    signedUpLib = list(filter( lambda library: library.signedUp , librarys))
    signedUpLib.sort( key = lambda library:library.booksScore , reverse = True )

    for library in signedUpLib:
        library.scanLibrary()
    
    if ( notSigning ):
        notSigned = list(filter( lambda library:not library.signedUp , librarys ))
        #for library in notSigned: 
        # notSigned.sort(key = lambda library:library.getBookScore(daysRemaining) , reverse = True )
        notSigned.sort(key = lambda library:library.getLibScore(daysRemaining) , reverse = True )
        # notSigned.sort(key = lambda library:library.signUpRemaining )
        
        if len(notSigned):
            signingLibrary = notSigned[0]
            print( "Signing Up library" , signingLibrary.id , "With Signup time of" , signingLibrary.signUpRemaining)
            signingLibrary.signUpOrder = orderNumber
            orderNumber += 1
            notSigning = False
    
    notSigning = signingLibrary.signUp()
    

    #map(lambda library:library.scanLibrary() , signedUpLib)
    
    #time.sleep(1.5)

score = 0

librarys = list(filter( lambda library:library.signedUp,librarys ))
librarys.sort(key= lambda library:library.signUpOrder)

f = open("attempt2Ans/" + filename +".txt", "w")
f.write(str(len(librarys)))
f.write("\n")

for library in librarys:
    f.write( str(library.id) + " " + str(len(library.sentBooks)) + "\n")

    for book in library.sentBooks:
        f.write(str(book) + " ")
    
    f.write("\n")

    #for sentBook in library.sentBooks
    #print (library.id , len(library.sentBooks))
# print( list( map( lambda library: library.id , librarys) ))

for book in books:
    if book.scanned:
        score += book.score


print("SCORES:" , score)


#print (" SCAN COUNT" , scanCount)

# for orderNo in range(30):
    
#     print( orderNo , librarys[orderNo].id , len(librarys[libraryNo].sentBook) )
    

