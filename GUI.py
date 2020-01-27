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
from tkinter import *
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
'''
def createWindow(title):
    window = windowLaunch()

    FullScreenApp(window)
    
    window.mainloop()
'''
'''
def firstFrame():

    def returnUserID():
        userID = entryID.get()
        print("userID is:",userID)
        return userID

    def quitGUI():
        root.destroy()
        
    root = Tk() #or tk.Tk()
    #FullScreenApp(root)
        
    root.title("Explaining Recommendations for Collaborative Filtering")

    title = "Select your user ID to see recommended movies:"
    label = tk.Label(root, text=title,fg="white",bg="blue")
    label.grid(row=0,columnspan=2)

        

    tk.Label(root, text = "User ID").grid(row=1,column=0)
    entryID = Entry(root) # or tk.Entry
    entryID.grid(row=1,column=1)
    entryID.focus()

        
    #self.setUserID(userID)

    b = Button(root, text="Submit", command=returnUserID).grid(row=1,column=2)
    c = Button(root, text="Close", command=quitGUI).grid(row=2,column=2)

    #self.quit
    #self.root.quit()  ->  root.mainloop() will still run in the background
    mainloop() #self.root.mainloop()
 
'''

def quitPage(currentPage):
    currentPage.destroy()
    
    
def displayResults(rowTitles, rowGenres, metadata, selectedUser, numberRec):
    if(len(rowTitles)>4):
        rowTitles=rowTitles[:4]
    window = Tk()
    FullScreenApp(window)
    window.title(("Showing",numberRec,"recommendations for user",selectedUser))
    window.configure(background='white')

    title = "Recommended for you"
    label = tk.Label(window, text=title,anchor='w',fg="black",bg="light grey",font=("MS Sans Serif",26))
    label.grid(row=0,columnspan=8,sticky=N+S+E+W)

    colCount = 0
    padx=10
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
            im = PIL.Image.open(io.BytesIO(raw_data))
            image = ImageTk.PhotoImage(im)

        except:
            year = tk.Label(window, text='Data Unavailable!',fg="black",font=("Arial",12))
            duration = tk.Label(window, text='Data Unavailable!',anchor='w',fg="black",font=("Arial",12,"bold"))
            image = PhotoImage(file="movie_metadata/poster/notFound.png")           
            

        images.append(image)
        
        
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

    b = Button(window, text="Next", command= lambda: quitPage(window))
    b.grid(row=5,column=6,columnspan=2,sticky=N+S+E+W)
    mainloop()
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
