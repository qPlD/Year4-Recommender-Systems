import tkinter as tk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from urllib.request import urlopen
from PIL import Image, ImageTk
import PIL
import urllib.parse
from matplotlib.figure import Figure
from graph_plotter import plotAllPointsLegends
from utility_functions import *
from tkinter import *
from omdb import *
import io
import base64
matplotlib.use("TkAgg")

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

def quitPage(currentPage):
    currentPage.destroy()

#Used by explanation 2
def seeGraph(window,closestPointsCoords, colours, allItemPoints, userXPoints, fileTitles, arrayOfGenres):
    c = Button(window, text="Close", command= lambda: quitPage(window))
    c.grid(row=2,column=1,sticky=N+S+E+W,padx=(10,20),pady=(20,10))
    plotAllPointsLegends(closestPointsCoords, colours, allItemPoints, userXPoints, fileTitles, arrayOfGenres)

def explanationOne(dataset, recommendedIds, recommendedTitles, file):

    allNeighboursInOrder = []
    with open(file, "r") as f:
        for row in csv.reader(f):
            allNeighboursInOrder += row
    f.close()
    
    #We remove the closest neighbour, which is the user himself
    allNeighboursInOrder = allNeighboursInOrder[1:]
    
    recommendedIds = np.asarray(recommendedIds)
    recommendedIds = recommendedIds.astype(np.int32)
    allNeighboursInOrder = np.asarray(allNeighboursInOrder)
    allNeighboursInOrder = allNeighboursInOrder.astype(np.int32)

            
    resultRatings = []
    resultIds = []
    #Overall rank of how similar the user is to the participant.
    resultRanks = []
    for ID in recommendedIds:
        
        allIDRatings = dataset.item_ids==ID
        allRatingsWithID = dataset.ratings[allIDRatings]
        allUsersHavingRated = dataset.user_ids[allIDRatings]

        nCount = 0
        rank = 1
        top3NeighboursIDs = []
        top3NeighboursRatings = []
        top3NeighboursOverallRank = []
        
        for nID in allNeighboursInOrder:
            if (nID in allUsersHavingRated) and (nCount<3):
                k = np.where(allUsersHavingRated==nID)[0][0]
                top3NeighboursIDs += [allRatingsWithID[k]]
                top3NeighboursRatings += [nID]
                top3NeighboursOverallRank += [rank]
                nCount += 1
            rank += 1

        resultRatings += [top3NeighboursIDs]
        resultIds += [top3NeighboursRatings]
        resultRanks += [top3NeighboursOverallRank]
    '''
    print("Result rating: ",resultRatings)
    print("Result ids: ",resultIds)
    print("Result ranks: ",resultRanks)
    print("Recom Titles: ",recommendedTitles)
    '''
    explanationOneUI(resultRatings, resultIds, resultRanks, recommendedTitles)

def explanationOneUI(resultRatings, resultIds, resultRanks, recommendedTitles):
    window = Tk()
    window.configure(background='white')
    window.grid_columnconfigure(0, weight=1)
    FullScreenApp(window)
    window.title(("Explanation Method 1"))
    padx=20
    

    title = "Explanation Method 1:"
    label1 = tk.Label(window, text=title,anchor='w',fg="blue4",bg="royalblue2",bd=4,relief="solid",font=("Arial",26,"bold"))
    explanation = ("The following table shows the ratings given by your closest neighbours (neighbours are users "
                   "with similar tastes as yours) to the 4 movies that have been recommended to you by the system. "
                   "\n\nFor each movie, the 3 users closest to you which have also rated this specific movie have been "
                   "selected and ranked by decreasing order of similarity (so neighbour N°1 should be MOST similar "
                   "to you and neighbour N°3 should be LEAST similar to you overall). "
                   "\n\nNOTE: Since not all users in the database have rated all movies, it is likely that your "
                   "neighbour users will be different for each recommended movie. \n\nTheir rank shows how close to "
                   "you they are OVERALL (regardless of recommended movies), 1 being your closest neighbour and 945 "
                   "being the user least like you in this dataset.")

    label2 = tk.Message(window, text=explanation,width=1200,anchor='w',fg="black",bg="light grey",bd=4,
                        relief="solid",font=("Arial",12))
    label1.grid(row=0,columnspan=5,sticky=N+S+E+W,padx=padx,pady=(10,20))
    label2.grid(row=1,columnspan=5,sticky=N+S+E+W,padx=padx,pady=(0,20))

    i = 1
    for title in recommendedTitles:
        label = tk.Label(window, text="Recommendation N°{}:\n{}".format(i,title),width=30,fg="white",
                         bg="black",font=("Arial",12))
        if(i==4):
            label.grid(row=2,column=i,sticky=N+S+E+W,padx=(2,20),pady=(0,2))
        else:
            label.grid(row=2,column=i,sticky=N+S+E+W,padx=2,pady=(0,2))
        if(i<4):
            label2 = tk.Label(window, text="Neighbour N°{}".format(i),height=4,
                              fg="white",bg="black",font=("Arial",16,"bold"))
            label2.grid(row=i*2+1,column=0,rowspan=2,sticky=N+S+E+W,padx=(20,2),pady=(2,2))
        i += 1

    rowLayout = [3,5,7]
    colLayout = [1,2,3,4]
    k=0
    for threeRanks in resultRanks:
        i=0
        for rank in threeRanks:
            label = tk.Label(window, text="User Rank N°{}".format(rank),fg="black",
                             bg="skyblue1",font=("Arial",12,"italic"))

            if(k==3):
                label.grid(row=rowLayout[i],column=colLayout[k],sticky=N+S+E+W,padx=(2,20),pady=(2,0))
            else:
                label.grid(row=rowLayout[i],column=colLayout[k],sticky=N+S+E+W,padx=2,pady=(2,0))

            i += 1
        k += 1

    k=0
    for threeRatings in resultRatings:
        i=0
        for rating in threeRatings:

            '''
            imageStar = PIL.Image.open("movie_metadata/poster/star{}.png".format(int(rating)))
            imageStar = imageStar.resize((200, 50), PIL.Image.ANTIALIAS)
            imageStar = ImageTk.PhotoImage(imageStar)
            stars = Label(window, image=imageStar,bg="skyblue1")
            stars.image = imageStar
            '''
            stars=Label(window, text=int(rating)*"* ",bg="skyblue1",fg="red4",font=("comic sans ms",20,"bold"))
            if(k==3):
                stars.grid(row=rowLayout[i]+1,column=colLayout[k],sticky=N+S+E+W,padx=(2,20),pady=(0,2))
            else:
                stars.grid(row=rowLayout[i]+1,column=colLayout[k],sticky=N+S+E+W,padx=2,pady=(0,2))

            i += 1
        k += 1    

    b = Button(window, text="Close", command= lambda: quitPage(window))
    b.grid(row=9,column=4,sticky=N+S+E+W,padx=(0,20),pady=(20,10))
    mainloop()

'''
resultRatings=  [[3.0], [2.0], [3.0, 1.0], [3.0, 1.0, 3.0]]
resultIds=  [[655], [782], [655, 405], [782, 405, 486]]
resultRanks=  [[655], [338], [655, 667], [338, 667, 785]]
titles= ['Girls Town', 'MURDER and murder', 'Collectionneuse La', 'Schizopolis']
explanationOneUI(resultRatings, resultIds, resultRanks, titles)


resultRatings=[[2.0, 4.0, 1.0], [2.0, 1.0, 5.0], [4.0, 3.0, 4.0], [5.0, 3.0, 5.0]]
resultIds=[[181, 852, 223], [181, 917, 859], [563, 871, 375], [884, 633, 440]]
resultRanks=[[140, 195, 210], [140, 175, 295], [114, 292, 316], [287, 334, 367]]
titles = ["The following table shows",
          "as yours)",
          "to you which have also rated this movie",
          "different for each"]


'''

def explanationTwo(model, dataset, arrayOfGenres, arrayOfColours, fileTitles, embedding_dim, tsneIterations, perplexity):

    #Number of closest points to show
    num_closest_points = 50
    num_items = dataset.num_items
    num_users = dataset.num_users
    #The last row will correspond to the user to be represented with other items.
    allItemFactors = np.empty((num_items+1,embedding_dim))

    for i in range (num_items):
        allItemFactors[i,:] = model._net.item_embeddings.weight[i].detach()    
    #The participant is the user with the last ID
    allItemFactors[num_items,:] = model._net.user_embeddings.weight[num_users-1].detach()
    
    ArrayOf2DItems = tsne(tsneIterations,allItemFactors, 2, embedding_dim, perplexity)

    allItemPoints = ArrayOf2DItems[:num_items,:]
    userXPoints = ArrayOf2DItems[num_items,:]

    #SECOND STEP: Assign neighbour items
    distances = []

    #Compute the Euclidean distance for high dimensions (more accurate).
    for index in range (num_items):
        itemXPoints = allItemPoints[index,:]
        
        dist = math.sqrt((userXPoints[0]-itemXPoints[0])**2+(userXPoints[1]-itemXPoints[1])**2)
        distances += [dist]

    distIndexes = np.argsort(distances)

    closestItemIndexes = distIndexes[:num_closest_points]

    '''
    closestGenres = []
    closestColours = []
    for index in closestItemIndexes:
        closestGenres += arrayOfGenres[i]
        closestColours += arrayOfColours[i]
            
    
    colours = []
    sizes = []

    for i in range(num_items):
        #istr = str(i)
        if i in closestItemIndexes:
            #print(i,arrayOfGenres[i],arrayOfColours[i])
            colours += [arrayOfColours[i]]
            sizes += [3]
        else:
            colours += ["black"]
            sizes += [1]
            
    colours += ["red"]
    sizes += [10]
    '''
        
    closestPointsCoords = np.empty((num_closest_points,2))
    colours = []

    
    count = 0
    for i in range(num_items):
        if i in closestItemIndexes:
            colours += [arrayOfColours[i]]
            closestPointsCoords[count,:] = ArrayOf2DItems[i,:]
            count += 1


    window = Tk()
    window.configure(background='white')
    #window.grid_columnconfigure(0, weight=1)
    FullScreenApp(window)
    window.title(("Explanation Method 2"))
    padx=20
    
    title = "Explanation Method 2:"
    label1 = tk.Label(window, text=title,anchor='w',fg="red4",bg="IndianRed1",bd=4,relief="solid",font=("Arial",26,"bold"))
    explanation = ("The next page will feature a graph showing you how your tastes may match certain items in the "
                   "dataset.\n\nEach point in the graph (aside from yourself) will represent a certain movie and the "
                   "associated colour will represent its genre. Only the "+str(num_closest_points)+" movies closest to your "
                   "tastes will be in colour, while the remaining movies points will be black.\n\nYou can still hover "
                   "your cursor over any point to see its title and genre."
                   "\nYou may also zoom in/out and move the visualisation around. "
                   "\n\nNOTE: Keep in mind that this is an approximate representation, and the movies that have been "
                   "recommended to you may not necessarily be closest to you on the graph. "
                   "\n\nHOW THIS WORKS: The model can represent each user and each item (or movie) as an "
                   "n-dimensional vector. The factors in each vector are mathematically computed by the model. "
                   "Their exact value is not important; The main idea is that the CLOSER two vectors are, the "
                   "MORE RELATED two items or users will be.\nSince we cannot visualise these vectors in high-"
                   "dimensions, we have used a tool called tSNE which essentially reduces the vectors to 2 "
                   "dimensions while preserving the distances between each point.\n\nThe following graph should "
                   "therefore give you an estimate of how \"closely related\" you are to each movie in the dataset.")

    label2 = tk.Message(window, text=explanation,width=1300,anchor='w',fg="black",bg="light grey",bd=4,
                        relief="solid",font=("Arial",15))
    label1.grid(row=0,columnspan=2,sticky=N+S+E+W,padx=padx,pady=(10,50))
    label2.grid(row=1,columnspan=2,sticky=N+S+E+W,padx=padx,pady=(0,20))

    b = Button(window, text="See Graph", command= lambda: seeGraph(window,closestPointsCoords, colours, allItemPoints, userXPoints, fileTitles, arrayOfGenres))
    b.grid(row=2,column=0,sticky=N+S+E+W,padx=(20,10),pady=(20,10))
    mainloop()


    #return (dimReduc, plot1)#,
'''
# Creates two subplots and unpacks the output array immediately
x = [4,3,7,5]
y = [9,2,0,9]
y2 = [3,4,10,-2]
f, ax = plt.subplots()
plt.scatter(x, y)
#ax1.set_title('Sharing Y axis')
plt.scatter(x, y2)
plt.show()
'''
def displayResults(rowTitles, rowGenres, metadata, selectedUser, numberRec):
    if(len(rowTitles)>4):
        rowTitles=rowTitles[:4]
    window = Tk()
    FullScreenApp(window)
    window.title(("Showing",numberRec,"recommendations for user",selectedUser))
    window.configure(background='white')
    padx=10
    title = "Recommended for you"
    label = tk.Label(window, text=title,anchor='w',fg="blue4",bg="royalblue2",bd=4,relief="solid",font=("Arial",26,"bold"))
    label.grid(row=0,columnspan=8,sticky=N+S+E+W,padx=padx,pady=(10,0))

    colCount = 0
    
    images = []
    for i in range(len(rowTitles)):
        if(colCount==8):
            colCount=0
        
        title = 'N°'+str(i+1)+":   "+rowTitles[i]
        title = tk.Label(window, text=title,anchor='w',fg="black",font=("Arial",16))
        genre = rowGenres[i]
        genre = tk.Label(window, text=genre,anchor='w',fg="black",font=("Arial",14,"italic"))

        try:
            
            year = tk.Label(window, text='('+metadata[i][0]+')',fg="black",font=("Arial",12))
            duration = tk.Label(window, text="Duration: "+metadata[i][1],anchor='w',fg="black",font=("Arial",12,"bold"))
            image_url = metadata[i][2]
            raw_data = urllib.request.urlopen(image_url).read()
            imagePoster = PIL.Image.open(io.BytesIO(raw_data))
            #image = ImageTk.PhotoImage(imagePoster)

        except:
            year = tk.Label(window, text='Data Unavailable!',fg="black",font=("Arial",12))
            duration = tk.Label(window, text='Data Unavailable!',anchor='w',fg="black",font=("Arial",12,"bold"))
            #image = PhotoImage(file="movie_metadata/poster/notFound.png")
            imagePoster = PIL.Image.open("movie_metadata/poster/notFound.png")

            '''
            imagePoster = PIL.Image.open("movie_metadata/poster/star{}.png".format(int(rating)))
            imagePoster = imagePoster.resize((200, 50), PIL.Image.ANTIALIAS)
            imagePoster = ImageTk.PhotoImage(imagePoster)
            stars = Label(window, image=imageStar,bg="skyblue1")
            stars.image = imageStar
            '''
            
        imagePoster = imagePoster.resize((285,450), PIL.Image.ANTIALIAS)
        imagePoster = ImageTk.PhotoImage(imagePoster)
        images.append(imagePoster)
        
        
        title.grid(row=2,column=colCount,padx=(padx,0),pady=(0,10),sticky=N+S+E+W)
        year.grid(row=2,column=colCount+1,padx=(0,padx),pady=(0,10),sticky=N+S+E+W)
        genre.grid(row=3,column=colCount,columnspan=2,padx=padx,pady=(0,10),sticky=N+S+E+W)
        duration.grid(row=4,column=colCount,columnspan=2,padx=padx,pady=(0,30),sticky=N+S+E+W)
        
        colCount += 2
    
    colCount = 0
    for image in images:
        if(colCount==8):
            colCount=0
        poster = Label(window, image=image)
        poster.configure(background='black')
        poster.grid(row=1,column=colCount,columnspan=2,padx=padx,pady=10,sticky=N+S+E+W)

        colCount += 2

    #b = Button(window, text="Next", command= lambda: quitPage(window))
    text=" - Please do not close this tab yet as you may need to refer to it to answer some questions - "
    b = tk.Label(window, text=text,anchor='w',fg="blue4",bg="light cyan",bd=1,relief="solid",font=("Arial",12,"italic"))
    b.grid(row=5,columnspan=8,padx=padx)
    #(row=0,columnspan=8,sticky=N+S+E+W,padx=padx,pady=(10,0))
    return(images)
'''
displayResults(['Mute Witness', 'Safe', 'French Kiss', 'Reality Bites', 'Beverly Hills Cop III', 'Cops and Robbersons'],
               ['Comedy|Horror|Thriller', 'Thriller', 'Action|Comedy|Romance', 'Comedy|Drama|Romance', 'Action|Comedy|Crime|Thriller', 'Comedy'],
               [['1995', '95 min', 'https://m.media-amazon.com/images/M/MV5BNTJkYWU2MjQtMGI4Ny00MGZjLWIzN2QtZDFmYWFkNDQ2NzJhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'],[None], ['2012', '94 min', 'https://m.media-amazon.com/images/M/MV5BMTcxNDI0NzUxMF5BMl5BanBnXkFtZTcwOTIzMjkyNw@@._V1_SX300.jpg'], ['1995', '111 min', 'https://m.media-amazon.com/images/M/MV5BMTkzMjg5MDQ3M15BMl5BanBnXkFtZTgwOTM5NTE0MDE@._V1_SX300.jpg'], ['1994', '99 min', 'https://m.media-amazon.com/images/M/MV5BZWY1ZGEyY2YtNWZhNS00OGZhLTg3OWEtODE2M2U5NjE4YmUyL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg'], ['1994', '104 min', 'https://m.media-amazon.com/images/M/MV5BOTdhMTU4MzMtYTVjMi00MTYzLTkxZDYtOWUwYjI0NDFjZTY1XkEyXkFqcGdeQXVyMDEwMjgxNg@@._V1_SX300.jpg'], ['1994', '93 min', 'https://m.media-amazon.com/images/M/MV5BMjcxM2VkZDEtYmExZi00ODRhLWI3NGItNjZiM2IxOGQxODM5XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg']],
               5,4)

'''
def startsWithNumb(text):
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    if(text[0] in numbers) or (text[1] in numbers) or (text[2] in numbers):
        return True
    else:
        return False

    
class firstFrame():
        
    def __init__(self, userID=-1):#,plot):
        self.root = tk.Tk()
        self.root.geometry = (500,300)
        self.userID = userID
        
        #FullScreenApp(self.root)
        
        self.root.title("Explaining Recommendations for Collaborative Filtering")
        #self.root.grid_columnconfigure(0, weight=1)

        title = "Select your user ID to see recommended movies"
        label1 = tk.Label(self.root, text=title,fg="black",bg="pale green",font=("Helvetica",16))
        label1.grid(row=0,columnspan=3)

        

        label2 = tk.Label(self.root, text = "User ID:",justify = "right",anchor="e",fg="black",bg="white",font=("Helvetica",12))
        label2.grid(row=1,column=0,sticky=N+S+E+W)
        entryID = Entry(self.root) # or tk.Entry
        entryID.grid(row=1,column=1)
        entryID.focus()

        label3 = tk.Label(self.root, text = "Number of recommendations:",anchor="e",justify = "right",fg="black",bg="white",font=("Helvetica",12))
        label3.grid(row=2,column=0,sticky=N+S+E+W)
        entryNRec = Entry(self.root) # or tk.Entry
        entryNRec.grid(row=2,column=1)

        
        #self.setUserID(userID)
        c = Button(self.root, text="Close", command=self.quit)#.grid(row=2,column=2)
        c.grid_forget()
        
        b = Button(self.root, text="Submit", command= lambda: self.setUserID(entryID,entryNRec,c)).grid(row=2,column=2,sticky=N+S+E+W)
        

        #self.quit
        #self.root.quit()  ->  root.mainloop() will still run in the background
        mainloop() #self.root.mainloop()
 
    def getUserID(self): 
        return self.userID
    def getNumberRec(self):
        return self.numberRec
    def setUserID(self, entryID, entryNRec, c):
        userID = entryID.get()
        numberRec = entryNRec.get()
        
        c.grid(row=3,column=2,sticky=N+S+E+W)
        label = tk.Label(self.root, text="Fields Submitted!",fg="black",bg="white")
        label.grid(row=3,column=1)

        self.userID = userID
        self.numberRec = numberRec
    def quit(self):
        self.root.destroy()

        
    def printSomething(userID):
        # button.destroy() or button.pack_forget()
        label = Label(self.root, text=userID.get()).grid(row=1,column=3)
        #str(self.getUserID)


    



def scatterPlotDisplay(fig):
    window = Tk()
    FullScreenApp(window)
    window.title(("Explaining Recommendations"))
    label = tk.Label(window, text="Graph representing movies likely to interest you", font=("Helvetica",16))
    label.pack(pady=10,padx=10)



    #f = Figure(figsize=(5,5), dpi=100)
    #a = f.add_subplot(111)
    #a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    b = Button(window, text="Next", command= lambda: quitPage(window))
    b.pack(side=tk.RIGHT)
    
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    mainloop()
    


def histogramDisplay(nClosestGenres, nDiffGenres):
    window = Tk()
    FullScreenApp(window)
    colours = ['b','g','r','c','m','y','k']
    window.title(("Explaining Recommendations"))
    label = tk.Label(window, text="Histogram of your favourite genres", font=("Helvetica",16))
    label.pack(pady=10,padx=10)

    fig,ax = plt.subplots()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    N, bins, histBars = ax.hist(nClosestGenres, bins=np.arange(nDiffGenres+1)-0.5, rwidth = 0.8, ec="black", linewidth =1)
    for i in range (len(histBars)):
        histBars[i].set_facecolor(colours[i])
        '''
        try:
            histBars[i].set_facecolor(colours[i])
        except:
            print("Too many genres for the amount of colours!")
        '''

    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    b = Button(window, text="Next", command= lambda: quitPage(window))
    b.pack(side=tk.RIGHT)
    
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    mainloop()
    
    
'''
Code taken from https://code.activestate.com/recipes/578860-setting-up-a-listbox-filter-in-tkinterpython-27/history/2/
'''
#First create application class
class Application(Frame):
    def __init__(self, master=None,movieTitles=None, minNumb=3):
        Frame.__init__(self, master)
        

        #These variables will be used in the poll function so i 
        #Set them at the start of the program to avoid errors.
        self.search_var = StringVar()
        #self.grid_columnconfigure(0, weight=1)
        self.movie_titles = movieTitles
        self.switch = False
        self.errormsg = tk.Label(self, text='Error!')
        self.search_mem = ''
        self.selectedTitle = ''
        self.ratedMovies = []
        self.minNumb = minNumb
        
        

        self.pack()
        self.create_widgets()
        
    def submit_rating(self):
        self.errormsg.grid_forget()
        if(self.selectedTitle==''):
            self.errormsg = tk.Label(self, text='Please select a movie to rate first!',anchor='w',fg="black",bg="light grey",font=("Arial",14))
            self.errormsg.grid(row=18,column=1)
        elif(self.selectedTitle in self.ratedMovies):
            self.errormsg = tk.Label(self, text='You have already rated that movie!',anchor='w',fg="black",bg="light grey",font=("Arial",14))
            self.errormsg.grid(row=18,column=1)
        else:
            self.errormsg = tk.Label(self, text='You have rated {}/{} movies'.format(int(len(self.ratedMovies)/2)+1,self.minNumb)
                                     ,anchor='w',fg="black",bg="light grey",font=("Arial",14))
            self.errormsg.grid(row=18,column=1)
            self.ratedMovies += [self.selectedTitle,self.sliderRating.get()]
        
        
    #Create main GUI window
    def create_widgets(self):
        #Use the StringVar we set up in the __init__ function 
        #as the variable for the entry box
        self.entry = Entry(self, textvariable=self.search_var, width=13)
        self.lbox = Listbox(self,width=50,height=24)

        title = "Please provide ratings for 10 movies you have seen:"
        self.label = tk.Label(self, text=title,anchor='w',fg="black",bg="light grey",font=("Arial",26))

        self.sliderRating = Scale(self, from_=1, to=5, orient=HORIZONTAL, length=400)
        self.sliderRating.configure(bg="PaleTurquoise1")
        
        submitRating = Button(self, text="Submit Rating", command=  self.submit_rating)
        finishedRating = Button(self, text="Next Page", command=  self.quit_page)

        self.entry.grid(row=1, column=0, padx=10, pady=3,sticky=W+E)
    
        
        self.lbox.bind("<Button-1>", self.onClick)
        self.lbox.grid(row=2, column=0,rowspan=14,sticky=N+S+E+W)
        
        self.label.grid(row=0, column=0,columnspan=10,pady=(0,15))
        self.sliderRating.grid(row=17, column=1)
        submitRating.grid(row=16, column=2)
        finishedRating.grid(row=17, column=2)

        #b = Button(self, text="Submit", command= printSelected(self))
        #b.grid(row=1,column=1,sticky=N+S+E+W)
        
        
        #Function for updating the list/doing the search.
        #It needs to be called here to populate the listbox.
        self.update_list()

        self.poll()
        
    def onClick(self,event):
        lbox = event.widget
        self.errormsg.grid_forget()
        #print ("you clicked on", self.lbox.curselection())
        index = lbox.curselection()
        
        try:
            self.selectedTitle = lbox.get([index])
        except:
            pass
        
        metadata = get_metadata([self.selectedTitle],True, False)
        self.show_movie(metadata)

        #event.widget.config(text="Thank you!")


    #Runs every 50 milliseconds. 
    def poll(self):
        #Get value of the entry box
        self.search = self.search_var.get()
        if self.search != self.search_mem: #self.search_mem = '' at start of program.
            self.update_list(is_contact_search=True)

            #set switch and search memory
            self.switch = True #self.switch = False at start of program.
            self.search_mem = self.search

        #if self.search returns to '' after preforming search 
        #it needs to reset the contents of the list box. I use 
        #a 'switch' to determine when it needs to be updated.
        if self.switch == True and self.search == '':
            self.update_list()
            self.switch = False
            
        self.update_star_image()
        self.after(50, self.poll)

    def update_star_image(self):

        image = PhotoImage(file="movie_metadata/poster/star{}.png".format(self.sliderRating.get()))
        
        stars = Label(self, image=image)
        stars.image = image
        stars.configure(bg="PaleTurquoise1")
        stars.grid(row=16,column=1,pady=(10,0))
        
    def quit_page(self):
        if(len(self.ratedMovies)<self.minNumb*2):
            self.errormsg = tk.Label(self, text='Please rate at least {} movies!'.format(self.minNumb)
                                     ,anchor='w',fg="black",bg="light grey",font=("Arial",14))
            self.errormsg.grid(row=18,column=1)
        else:
            self.destroy()
            self.master.destroy()
        
    def show_movie(self, metadata):


        padx=10
        images = []

        title = tk.Message(self, text=self.selectedTitle,anchor='w',width=250,fg="white",bg="black",font=("Arial",20,"bold"))
        

        try:
                
            year = tk.Label(self, text='Year: '+metadata[0][0],anchor='w',fg="black",bg="light grey",font=("Arial",12,"bold"))
            genre = tk.Label(self, text='('+metadata[0][3]+')',anchor='w',fg="white",bg="black",font=("Arial",10,"italic"))
            duration = tk.Label(self, text="Duration: "+metadata[0][1],anchor='w',fg="black",bg="light grey",font=("Arial",12,"bold"))
            rated = tk.Label(self, text="Rated: "+metadata[0][4],anchor='w',fg="black",bg="light grey",font=("Arial",12,"bold"))
            director = tk.Message(self, text="Director(s): "+metadata[0][5],anchor='w',fg="black",bg="white",width=400,font=("Arial",12,"italic"))
            actors = tk.Message(self, text="Actors: "+metadata[0][6],anchor='w',fg="black",bg="white",width=400,font=("Arial",12,"italic"))
            plot = tk.Message(self, text="Plot: "+metadata[0][7],anchor='w',fg="black",bg="white",width=400,font=("Arial",12))

            image_url = metadata[0][2]
            raw_data = urllib.request.urlopen(image_url).read()
            imagePoster = PIL.Image.open(io.BytesIO(raw_data))
            #image = ImageTk.PhotoImage(imagePoster)


        
        
        except:
            genre = tk.Label(self, text='Data Unavailable!',anchor='w',fg="black",font=("Arial",14,"italic"))
            year = tk.Label(self, text='Year: ',anchor='w',fg="black",font=("Arial",14,"italic"))
            duration = tk.Label(self, text='Duration: ',anchor='w',fg="black",font=("Arial",14,"italic"))
            rated = tk.Label(self, text='Rated: ',anchor='w',fg="black",font=("Arial",14,"italic"))
            director = tk.Label(self, text='Director(s): ',anchor='w',fg="black",font=("Arial",14,"italic"))
            actors = tk.Label(self, text='Actors: ',anchor='w',fg="black",font=("Arial",14,"italic"))
            plot = tk.Label(self, text='Plot: ',anchor='w',fg="black",font=("Arial",14,"italic"))
            #image = PhotoImage(file="movie_metadata/poster/notFound.png")
            imagePoster = PIL.Image.open("movie_metadata/poster/notFound.png")

        imagePoster = imagePoster.resize((400,500), PIL.Image.ANTIALIAS)
        imagePoster = ImageTk.PhotoImage(imagePoster)
        poster = Label(self, image=imagePoster)
        poster.image = imagePoster
        poster.configure(background='black')


            
        pady=20
        
        year.grid(row=3,column=2,columnspan=3,sticky=N+S+E+W)
        duration.grid(row=4,column=2,columnspan=3,sticky=N+S+E+W)
        rated.grid(row=5,column=2,columnspan=3,pady=(0,pady),sticky=N+S+E+W)
        director.grid(row=6,column=2,columnspan=3,sticky=N+S+E+W)
        actors.grid(row=7,column=2,columnspan=3,rowspan=3,sticky=N+S+E+W)
        plot.grid(row=10,column=2,columnspan=3,rowspan=4,sticky=N+S+E+W)
            
        title.grid(row=1,column=2,columnspan=3,sticky=N+S+E+W)#padx=(padx,0),pady=(0,10)
        genre.grid(row=2,column=2,columnspan=3,pady=(0,pady),sticky=N+S+E+W)
        poster.grid(row=1,column=1,rowspan=13,padx=10,sticky=N+S+E+W)


        #b = Button(window, text="Next", command= lambda: quitPage(window))
        #b.grid(row=5,column=6,columnspan=2,sticky=N+S+E+W)
        


    def update_list(self, **kwargs):
        try:
            is_contact_search = kwargs['is_contact_search']
        except:
            is_contact_search = False

        #Just a generic list to populate the listbox
        lbox_list = self.movie_titles

        self.lbox.delete(0, END)

        for item in lbox_list:
            if is_contact_search == True:
                #Searches contents of lbox_list and only inserts
                #the item to the list if it self.search is in 
                #the current item.
                if self.search.lower() in item.lower():
                    self.lbox.insert(END, item)
            else:
                self.lbox.insert(END, item)

    def getUserRatings(self):
        return self.ratedMovies
    '''
    def setUserRatings(self, entryID, entryNRec, c):
        userID = entryID.get()
        numberRec = entryNRec.get()
        
        c.grid(row=3,column=2,sticky=N+S+E+W)
        label = tk.Label(self.root, text="Fields Submitted!",fg="black",bg="white")
        label.grid(row=3,column=1)

        self.userID = userID
        self.numberRec = numberRec
    '''

def get_user_pref(minNumb,file):
    root = Tk()
    root.title('Gathering user preferences')
    root.grid_columnconfigure(0, weight=1)
    FullScreenApp(root)
    app = Application(master=root,movieTitles=extractTitlesFromText(file),minNumb=minNumb)
    app.mainloop()

    #print(app.getUserRatings(app))
    return Application.getUserRatings(app)

#movieTitles = ['Adam', 'Lucy', 'Barry', 'Bob', 'James', 'Frank', 'Susan', 'Amanda', 'Christie']
#x = get_user_pref()
#print("Ratings are:",x)
