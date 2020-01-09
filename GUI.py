import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT

from matplotlib.figure import Figure
from tkinter import *
matplotlib.use("TkAgg")


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
    
    
def displayResults(mostCommon,selectedUser,numberRec):
    window = Tk()
    window.title(("Showing",numberRec,"recommendations for user",selectedUser))

    title = "Your top recommendations are:"
    label = tk.Label(window, text=title,fg="black",bg="royalblue1",font=("Helvetica",16))
    label.grid(row=0,columnspan=3,sticky=N+S+E+W)

    recCount = 1
    '''
    #Due to poor formatting of the rows, we need to reformat
    formattedRows = []
    currentRow = ""
    for row in mostCommon:
        if startsWithNumb(row):
            if (currentRow != ""):
                formattedRows+=currentRow
            currentRow = row
        else:
            currentRow += currentRow
    '''  
    for recom in mostCommon:
        recomText = str(recCount)+". "+recom
        label = tk.Label(window, text=recomText,fg="blue4",font=("Helvetica",16))
        label.grid(row=recCount,columnspan=3,sticky="W")
        recCount += 1

    b = Button(window, text="Next", command= lambda: quitPage(window))
    b.grid(row=recCount+1,column=2,sticky=N+S+E+W)
    mainloop()

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

def graphDisplay(fig):
    window = Tk()
    FullScreenApp(window)
    window.title(("Explaining Recommendations"))
    label = tk.Label(window, text="Graph representing movies likely to interest you", font=("Helvetica",16))
    label.pack(pady=10,padx=10)#grid(row=0,columnspan=3)

    #f = Figure(figsize=(5,5), dpi=100)
    #a = f.add_subplot(111)
    #a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)#grid(row=1,rowspan=3,columnspan=3,sticky=N+S+E+W)

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)#grid(row=4,columnspan=3,sticky=N+S+E+W)

