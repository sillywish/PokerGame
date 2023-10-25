from tkinter import *
from tkinter import ttk
  
class ScrollbarApp(Frame):
    """use pack"""
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        
        
        self.canvas = Canvas(self,highlightthickness=0,width=self.winfo_width(),height=self.winfo_height(),bg="red")
        self.canvas.pack(side = LEFT,fill=BOTH,expand=1)
        
        self.scrollbar = ttk.Scrollbar(self,orient=VERTICAL,command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.interior = Frame(self.canvas,bg="green")
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)   
        self.count = 0
        
    def _configure_interior(self, event):
    # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
    
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
            
    def clear_interior(self):
        for widget in self.interior.winfo_children():
            widget.destroy()
        
        self.canvas.yview_moveto(0)
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=(0, 0, 200,400))
        #When you destroy the last widget within a frame, 
        #the frame size is no longer managed by pack or grid. Therefore, 
        #neither pack nor grid knows it is supposed to shrink the frame.
        #simple way to resize is create a tmp widget with (1,1) size to shrink the frame
        if len(self.interior.winfo_children()) == 0:
            tmp = Frame(self.interior, width=1, height=1, borderwidth=0, highlightthickness=0)
            tmp.pack()
            self.interior.update_idletasks()
            tmp.destroy()        
            
class AutoScrollbarApp(Frame):
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        
        self.scrollbar = AutoScrollbar(self) 
        self.scrollbar.grid(row=0, column=1, sticky=N+S) 
        self.canvas = Canvas(self,highlightthickness=0,yscrollcommand=self.scrollbar.set) 
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W) 

        self.scrollbar.config(command=self.canvas.yview)
        
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1) 

        # creating canvas contents 
        self.interior = Frame(self.canvas,bg="green") 
        self.interior.rowconfigure(1, weight=1) 
        self.interior.columnconfigure(1, weight=1) 
        
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)   
        self.count = 0
        
    def _configure_interior(self, event):
    # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
    
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
    
    def clear_interior(self):
        for widget in self.interior.winfo_children():
            widget.destroy()
        
        self.canvas.yview_moveto(0)
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=(0, 0, 200,400))
        #When you destroy the last widget within a frame, 
        #the frame size is no longer managed by pack or grid. Therefore, 
        #neither pack nor grid knows it is supposed to shrink the frame.
        #simple way to resize is create a tmp widget with (1,1) size to shrink the frame
        if len(self.interior.winfo_children()) == 0:
            tmp = Frame(self.interior, width=1, height=1, borderwidth=0, highlightthickness=0)
            tmp.pack()
            self.interior.update_idletasks()
            tmp.destroy()
# Creating class AutoScrollbar 
class AutoScrollbar(Scrollbar): 
	
	# Defining set method with all 
	# its parameter 
	def set(self, low, high): 
		
		if float(low) <= 0.0 and float(high) >= 1.0: 
			
			# Using grid_remove 
			self.tk.call("grid", "remove", self) 
		else: 
			self.grid() 
		Scrollbar.set(self, low, high) 
	
	# Defining pack method 
	def pack(self, **kw): 
		
		# If pack is used it throws an error 
		raise (TclError,"pack cannot be used with this widget") 
	
	# Defining place method 
	def place(self, **kw): 
		
		# If place is used it throws an error 
		raise (TclError, "place cannot be used with this widget") 
 
class TestFrame(Frame):
    def __init__(self, parent,*args, **kwargs):
        Frame.__init__(self, parent,*args, **kwargs)
        self.scrollbar = AutoScrollbar(self) 

        # Calling grid method with all its 
        # parameter w.r.t vertical scrollbar 
        self.scrollbar.grid(row=0, column=1, 
                        sticky=N+S) 
        self.canvas = Canvas(self, 
				yscrollcommand=self.scrollbar.set, 
				) 

        self.canvas.grid(row=0, column=0, sticky=N+S+E+W) 

        self.scrollbar.config(command=self.canvas.yview)
        
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1) 

        # creating canvas contents 
        self.frame = Frame(self.canvas) 
        self.frame.rowconfigure(1, weight=1) 
        self.frame.columnconfigure(1, weight=1) 

        # Defining number of rows and columns 
        rows = 5
        for i in range(1,rows): 
            for j in range(1,9): 
                button = Button(self.frame, padx=8, pady=8, 
                                text="[%d,%d]" % (i,j)) 
                button.grid(row=i, column=j, sticky='news') 

        # Creating canvas window 
        self.canvas.create_window(0, 0, anchor=NW, window=self.frame) 

        # Calling update_idletasks method 
        self.frame.update_idletasks() 

        # Configuring canvas 
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  
        #horiscrollbar.config(command=canvas.xview) 
    
def add_sth(app: ScrollbarApp):

    btn = Button(app.interior,text="test")
    btn.grid(row=app.count)
    app.count+=1
    
    #update_idletasks is necessary to call before move
    app.canvas.update_idletasks()
    app.canvas.yview_moveto(1)
    
    size = (app.interior.winfo_reqwidth(), app.interior.winfo_reqheight())
    print(size)

def clear(app: ScrollbarApp):
    for widget in app.interior.winfo_children():
        widget.destroy()
       
    app.canvas.yview_moveto(0)
    app.canvas.update_idletasks()
    app.canvas.config(scrollregion=(0, 0, 200,400))
    
    #When you destroy the last widget within a frame, 
    #the frame size is no longer managed by pack or grid. Therefore, 
    #neither pack nor grid knows it is supposed to shrink the frame.
    #simple way to resize is create a tmp widget with (1,1) size to shrink the frame
    if len(app.interior.winfo_children()) == 0:
        tmp = Frame(app.interior, width=1, height=1, borderwidth=0, highlightthickness=0)
        tmp.pack()
        app.interior.update_idletasks()
        tmp.destroy()
    size = (app.interior.winfo_reqwidth(), app.interior.winfo_reqheight())
    print(size)  

if __name__ == "__main__":
    root=Tk()
    root.geometry("200x600")
    app = AutoScrollbarApp(root)
    app.pack(fill=BOTH,expand=1)
    
    button = Button(root,text="ADD_SOMETHING",command= lambda:add_sth(app))
    button.pack()
    
    clear_button = Button(root,text="clear",command= app.clear_interior)
    clear_button.pack()
    # a=TestFrame(root,height=400,width=200)
    # a.pack(fill=BOTH,expand=1)
    root.mainloop()
    
    
    # root = tk.Tk()
    # window = Window(root)
    # root.mainloop()
    