import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import *#FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.backends.backend_qt4agg import *
from matplotlib.figure import Figure
from tkinter import *
matplotlib.use("TkAgg")


'''
def createWindow(title):
    window = windowLaunch()

    FullScreenApp(window)
    
    window.mainloop()
'''  

class firstFrame():
        
    def __init__(self, userID=-1):#,plot):
        self.root = tk.Tk()
        self.userID = userID
        
        FullScreenApp(self.root)
        
        self.root.title("Explaining Recommendations for Collaborative Filtering")

        title = "Select your user ID to see recommended movies:"
        label = tk.Label(self.root, text=title,fg="white",bg="blue")
        label.grid(row=0,columnspan=2)

        

        tk.Label(self.root, text = "User ID").grid(row=1,column=0)
        entryID = tk.Entry(self.root)
        entryID.grid(row=1,column=1)
        entryID.focus()

        
        
        #self.setUserID(userID)

        b = Button(self.root, text="Submit", command=self.setUserID(entryID)).grid(row=1,column=2)
        c = Button(self.root, text="Close", command=self.quit).grid(row=2,column=2)

        #self.quit
        #self.root.quit()  ->  root.mainloop() will still run in the background
        self.root.mainloop()

        
    def getUserID(self): 
        return self.userID
    def setUserID(self, entryID):
        userID = entryID.get()
        tk.Label(self.root, text = userID,bg="black").grid(row=3,column=0)
        self.userID = userID
    def quit(self):
        self.root.destroy()

        
    def printSomething(userID):
        # button.destroy() or button.pack_forget()
        label = Label(self.root, text=userID.get()).grid(row=1,column=3)
        #str(self.getUserID)
        

'''
        self.frames = {}
        for F in (graphDisplay):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
'''        


    


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

class graphDisplay(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

