import tkinter as tk
import spreadsheet as sp
from tkinter import messagebox
import audio as a
import os
from copy import deepcopy
#import csv
import copy
import tkinter.filedialog as filedialog

from copy import deepcopy

import csv
class DataProcessor():
         def __init__(self,layout,line_count):     
                self.data_fname=layout.filename
                self.out_fname=layout.dirname
                self._line_count=line_count
                self.layout=layout
                self.items=[]
                self.IF_HEADER=False
         def load_and_populate_table(self):
               with open(self.data_fname,encoding="utf8") as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter='|')
                        self.line_count = 0
                        for row in csv_reader:
                           try:    
                                if(self.IF_HEADER):
                                        if self.line_count == 0:
                                                print(f'Column names are {", ".join(row)}')
                                        self.line_count += 1
                                else:
                                        
                                                print(f'\t{row[0]+self.layout._prefix.get()}       {row[1]} ')
                                                #print("Layout:", self.layout.layout)
                                                self.items.append([row[0]+self.layout._prefix.get(),row[2]])
                                                #self.layout.layout["table"].set_data([1,2,3],[1,2,3])
                                                #self.layout.layout["table"].cell(0,0, " a fdas fasd fasdf asdf asdfasdf asdf asdfa sdfas asd sadf ")
    
                                                #self.layout.layout["table"].insert_row([1,2,3])
                                                #self.layout.layout["right_frame"].update()
                                                #self.layout.window.update()
                                                self.line_count += 1
                                                
                           except:
                                  continue
                           if self.line_count==self._line_count:
                                   break     
                        
                        print(f'Processed {self.line_count} lines.')  
                        #self.layout.layout["table"].update()        

class Layout():
    def __init__(self):
        self.dirname=None
        self.filename=None
        self._active_row=None
        self._isRecording=False
        self._debug=False
        self._audio= a.Audio()
        self._temp_bg=[]
        self.window = tk.Tk()
        self.window.title("My GUI")
        self.window.geometry("1200x800") 
        
        self._num_entries=tk.IntVar(value=10)
        self._prefix=tk.StringVar()
        #self.window.resizable(False, False)
        self.layout={}
        self.layout["left_frame"]=tk.Frame(self.window,borderwidth=3,padx=12,pady=12,relief=tk.RAISED)
        self.layout["left_down1_frame"]=tk.Frame(self.layout["left_frame"])
        self.layout["left_down2_frame"]=tk.Frame(self.layout["left_frame"],relief=tk.SOLID)
        self.layout["left_down3_frame"]=tk.Frame(self.layout["left_frame"],relief=tk.SOLID)
        self.layout["left_up1_frame"]=tk.Frame(self.layout["left_frame"],relief=tk.SOLID)
        self.layout["left_up2_frame"]=tk.Frame(self.layout["left_frame"],relief=tk.SOLID)
        self.layout["right_frame"]=tk.Frame(self.window,borderwidth=3,padx=2,pady=1,relief=tk.SUNKEN)

        # Create all widgets within containers
        self.layout["dataset_widget"]=tk.LabelFrame(self.layout["left_frame"],text="Output Directory",bd=4,padx=3,pady=3)
        
        self.layout["file_loaded"]=tk.Label(self.layout["dataset_widget"],text="Directory",padx=9,pady=5,justify=tk.LEFT,width=70,height=1,bg='white',relief=tk.SUNKEN, anchor="w")
        self.layout["btn_loaddir"]=tk.Button(self.layout["dataset_widget"], text = "Browse", command =  self.loaddirectory, width = 10,padx=0)
        
        
        self.layout["read_text_frame"]=tk.LabelFrame(self.layout["left_down2_frame"],text="Text ...",bd=4,padx=3,pady=3)
        self.layout["btn_frame"]=tk.LabelFrame(self.layout["left_down3_frame"],text="Buttons ...",bd=4,padx=3,pady=3)
        
        self.layout["num_entries_frame"]=tk.LabelFrame(self.layout["left_up1_frame"],text="Num Entries  ...",bd=4,padx=3,pady=3)
        self.layout["num_entries"]=tk.Entry(self.layout["num_entries_frame"],textvariable = self._num_entries,selectborderwidth=24,width=10,bg='white',relief=tk.SUNKEN)
        self.layout["lbl_num_entries"]=tk.Label(self.layout["num_entries_frame"],text="# Entries",padx=1,pady=1,justify=tk.LEFT,width=10,height=1,bg='#EEEEEE', anchor="nw")
        

        self.layout["prefix_frame"]=tk.LabelFrame(self.layout["left_up2_frame"],text="Prefix to add to IDs",bd=4,padx=3,pady=3)
        self.layout["prefix"]=tk.Entry(self.layout["prefix_frame"],textvariable =  self._prefix,selectborderwidth=24,width=10,bg='white',relief=tk.SUNKEN)
        self.layout["lbl_prefix"]=tk.Label(self.layout["prefix_frame"],text="# Entries",padx=1,pady=1,justify=tk.LEFT,width=10,height=1,bg='#EEEEEE', anchor="nw")



        #self.layout["prefix"]=tk.Entry(self.layout["read_text_frame"],textvariable = self._prefix,selectborderwidth=24,width=20,bg='orange',relief=tk.SUNKEN)
        
        self.layout["read_text"]=tk.Text(self.layout["read_text_frame"],padx=3,pady=1,width=60,height=20,bg='linen',relief=tk.SUNKEN,wrap=tk.WORD)
        
#        tk.Entry()
        self.layout["data_file_widget"]=tk.LabelFrame(self.layout["left_down1_frame"],text="Dataset File, csv",bd=4,padx=3,pady=3)
        
        
        self.layout["data_file_loaded"]=tk.Label(self.layout["data_file_widget"],text="File",padx=3,pady=5,justify=tk.LEFT,width=70,height=1,bg='white',relief=tk.SUNKEN, anchor="w")
        self.layout["btn_loadfile"]=tk.Button(self.layout["data_file_widget"], text = "Browse", command =  self.loadDataFile, width = 5)
        self.layout["btn_fetch"]=tk.Button(self.layout["data_file_widget"], text = "Fetch", command =  self.Fetch, width = 5)
        self.layout["btn_fetch"]["state"]=tk.DISABLED
        
        
        
        
        
        # Specify where to layout
        
        self.layout["btn_Prev"]=tk.Button(self.layout["btn_frame"], text = "Prev.", command =  self.prev_action, width = 10,padx=0)
        self.layout["btn_Next"]=tk.Button(self.layout["btn_frame"], text = "Next", command =  self.next_action, width = 10,padx=0)
        self.layout["btn_Record"]=tk.Button(self.layout["btn_frame"], text = "Rec.", command =  self.rec_action, width = 10,padx=0)
        self.layout["btn_Play"]=tk.Button(self.layout["btn_frame"], text = "Play", command =  self.play_action, width = 10,padx=0)
        self.layout["btn_Del"]=tk.Button(self.layout["btn_frame"], text = "Delete", command =  self.del_action, width = 10,padx=0)
        self.layout["btn_DumpNewCSV"]=tk.Button(self.layout["btn_frame"], text = "DumpNewCSV", command =  self.DumpCSV, width = 15,padx=0)
        
        
        #self.layout["left_frame"].pack(side=tk.LEFT,anchor='nw',expand=1,fill=tk.X)
        self.layout["left_frame"].pack(side=tk.LEFT,anchor='nw')
        
        self.layout["dataset_widget"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.X)
        self.layout["left_down1_frame"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.X)
        self.layout["left_up1_frame"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.X)
        self.layout["num_entries_frame"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.X)
        
        self.layout["left_up2_frame"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.X)
        self.layout["prefix_frame"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.X)
        
        
        self.layout["left_down2_frame"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.X)
        self.layout["left_down3_frame"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.X)
        self.layout["btn_frame"].pack(side=tk.BOTTOM,anchor='nw',expand=1,fill=tk.BOTH)
        
        
        self.layout["file_loaded"].pack(side=tk.LEFT,anchor='nw',expand=1,fill=tk.X)
        
        self.layout["btn_loaddir"].pack(side=tk.LEFT,anchor='nw')
        
        self.layout["data_file_widget"].pack(side=tk.LEFT,anchor='nw',expand=1,fill=tk.X)
        self.layout["data_file_loaded"].pack(side=tk.LEFT,anchor='nw',expand=1,fill=tk.X)
        
        self.layout["btn_loadfile"].pack(side=tk.LEFT,anchor='nw')
        self.layout["btn_fetch"].pack(side=tk.LEFT,anchor='nw')
        
        
        
        self.layout["num_entries"].pack(side=tk.LEFT,anchor='nw')
        self.layout["lbl_num_entries"].pack(side=tk.LEFT,anchor='nw')
        self.layout["prefix"].pack(side=tk.LEFT,anchor='nw')


        self.layout["read_text_frame"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.BOTH)
        self.layout["read_text"].pack(side=tk.TOP,anchor='nw',expand=1,fill=tk.BOTH)
        self.layout["btn_Prev"].pack(side=tk.LEFT,anchor='nw')
        self.layout["btn_Next"].pack(side=tk.LEFT,anchor='nw')
        self.layout["btn_Record"].pack(side=tk.LEFT,anchor='nw')
        self.layout["btn_Play"].pack(side=tk.LEFT,anchor='nw')
        self.layout["btn_Del"].pack(side=tk.LEFT,anchor='nw')
        self.layout["btn_DumpNewCSV"].pack(side=tk.LEFT,anchor='nw')
        
        


        self.layout["right_frame"].pack(side=tk.RIGHT,anchor='nw',expand=1,fill=tk.BOTH)
        
        self.layout["table"] = sp.Table(self.layout["right_frame"], ["#", "ID", "Sentence"], padx=3,pady=3,column_weights=[0,1,3],column_minwidths=[5,90,None],height=1000)
        
        self.layout["table"].pack(padx=1,pady=1,expand=True,fill=tk.BOTH)


        self.layout["right_frame"].update()
     
        
        self.window.mainloop()
        
    def  mockup(self):
        return

    def DumpCSV(self):
        answer = filedialog.asksaveasfilename(
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=[('all files', '.*'), ('text files', '.txt'),('csv files', '.csv')])
        
        
        print(answer)
        #if isfile.
        with open(answer, 'w') as myfile:
            wr = csv.writer(myfile,delimiter="|",lineterminator='\n')
            for j in self._DataProcessor.items:
                wr.writerow(j)
                
        

    def Fetch(self):
            #self.layout["table"].insert_row([22,23,24])
              
#            if self._active_row:
                
            if self.active_row is not None:
                nr= self.layout["table"].number_of_rows
                self._active_row=0
              #  self.layout["table"].clear()       
                self.layout["table"]._pop_n_rows(nr)    
              
              
            try:
                   num_entries=self._num_entries.get()
  
 
                   if num_entries<=0:
                       raise ValueError
                   
            except Exception as e:
                   messagebox.showerror("Error", 'Please enter numerical value in the box')    
                   return
                   
            self.layout["btn_Play"]["state"]=tk.NORMAL
            
            
            self._DataProcessor=DataProcessor(self,num_entries)
            self._DataProcessor.load_and_populate_table()
            for i,item in enumerate(self._DataProcessor.items):
                    self.layout["table"].insert_row([i,item[0],item[1]])
            
            self._active_row=0
            self.setActiveCell(self._active_row)
            self.layout["read_text"].insert(tk.INSERT,self.layout["table"].cell(self._active_row,2))
            self.layout["read_text"]["state"]=tk.DISABLED
            self._audio._WAVE_OUTPUT_FILENAME=self.layout["table"].cell(self._active_row,1)+".wav"


    
    @property
    def active_row(self):
        return self._active_row

  

    def next_action(self):
        self.layout["read_text"]["state"]=tk.NORMAL
        old_row=self._active_row
        if(self.isValidIndex(self._active_row+1)):
            
            self._active_row +=1    
            self._audio._WAVE_OUTPUT_FILENAME=self.layout["table"].cell(self._active_row,1)+".wav"
            self.layout["read_text"].delete('1.0', tk.END)
            self.layout["read_text"].insert(tk.INSERT,self.layout["table"].cell(self._active_row,2))
            for i in range(3):
                self.layout["table"].allCells[self.active_row*3+i]._message_widget.configure(bg='slate gray')
                self.layout["table"].allCells[old_row*3+i]._message_widget.configure(bg=self.layout["table"]._stripped_rows[old_row%2])
                
        self.layout["read_text"]["state"]=tk.DISABLED       
    
    
    @property 
    def isRecording(self):
        return self._isRecording
        #return True if  self.layout["btn_Record"]["text"]=="Stop" else False
    
    @isRecording.setter
    def isRecording(self, value):
        self._isRecording=value
        
    def play_action(self):
           self.layout["btn_Play"]["state"]=tk.DISABLED     
           try:
               self._audio.play_file(self,self.dirname)
           except  FileNotFoundError:
               if self.dirname:  
                   messagebox.showerror("Error", f'File not Found:  {os.path.join(self.dirname,  self._audio._WAVE_OUTPUT_FILENAME)}')    
               else:
                   messagebox.showerror("Error", f'File not Found:  {os.path.join("",  self._audio._WAVE_OUTPUT_FILENAME)}')    
               self.layout["btn_Play"]["state"]=tk.NORMAL
               
           print("Done playing")
           self.layout["btn_Play"]["state"]=tk.NORMAL
        
    
    
    def rec_action(self):
      #if isValidIndex(self._active_row):  
      
      
      if self.isRecording:
          self.layout["btn_Record"].config(text="Rec.",bg="#EEEEEE")
          self.isRecording=False
          if self._active_row is not None:
              
              self._audio._WAVE_OUTPUT_FILENAME=self.layout["table"].cell(self._active_row,1)+".wav"
          #self._audio.isRecording=False
          self._audio.stop()
          #self._audio.trim(self._audio._frames)
          while not self._audio.isSaved:
              pass
              
              
          self._audio.write_to_file(self.dirname)
          
          
          if self._debug:
              print("Pressing",self.layout["btn_Record"]["text"],self.isRecording)
      else:
          self.layout["btn_Record"].config(text="Stop",bg="red")
          self.isRecording=True
          self._audio.isRecording=True
          self._audio.start_recording()
          
          if self._debug:
              print("Pressing",self.layout["btn_Record"]["text"],self.isRecording)
          
    def del_action(self):
        if not self.dirname:
            if self._audio.del_file(""):
                messagebox.showinfo("Delete ", f'File  {os.path.join("",  self._audio._WAVE_OUTPUT_FILENAME)}  Deleted ')
            else:
                messagebox.showerror("Error", f'Error Deleting file:  {os.path.join("",  self._audio._WAVE_OUTPUT_FILENAME)}')
        else:    
            if self._audio.del_file(self.dirname):
                messagebox.showinfo("Delete ", "File Deleted")
            else:
                messagebox.showerror("Error", f'Error Deleting file:  {os.path.join(self.dirname,  self._audio._WAVE_OUTPUT_FILENAME)}')    
            
            
    
    
    
    def prev_action(self):
        self.layout["read_text"]["state"]=tk.NORMAL
        old_row=self._active_row
        if(self.isValidIndex(self._active_row-1)):
            self._active_row -=1    
            self._audio._WAVE_OUTPUT_FILENAME=self.layout["table"].cell(self._active_row,1)+".wav"
            self.layout["read_text"].delete('1.0', tk.END)
            self.layout["read_text"].insert(tk.INSERT,self.layout["table"].cell(self._active_row,2))
            for i in range(3):
                self.layout["table"].allCells[self.active_row*3+i]._message_widget.configure(bg='slate gray')
                self.layout["table"].allCells[old_row*3+i]._message_widget.configure(bg=self.layout["table"]._stripped_rows[old_row%2])
                
        self.layout["read_text"]["state"]=tk.DISABLED            
    
    
  
    def isValidIndex(self,index):
       return  True if index < self.layout["table"].number_of_rows and index >= 0 else False

    def setActiveCell(self,index):
          if self.isValidIndex(index):
              
            for i in range(3):
                self.layout["table"].allCells[index+i]._message_widget.configure(bg='slate gray')
          else:
             messagebox.showerror("Error", "Error setting next")


    def loaddirectory(self): 
                self.dirname = filedialog.askdirectory()

                if self.dirname: 
                        try: 
                                self.layout["file_loaded"]['text']=self.dirname
                                
                                self.layout["file_loaded"].update()
                        except: 
                                messagebox.showerror("Error", "Error getting Directory")
                                self.dirname=None
                                self.layout["file_loaded"]['text']="None"
    def loadDataFile(self): 
                self.filename = filedialog.askopenfilename(filetypes = (("CSV files", "*.csv")
                                                                   ,("All files", "*.*") ))

                if self.filename: 
                        try: 
                                self.layout["data_file_loaded"]['text']=self.filename
                                self.layout["btn_fetch"]["state"]=tk.NORMAL
                                self.layout["data_file_loaded"].update()
                                
                                
                        except: 
                                messagebox.showerror("Error", "Error loading Data File")
                                self.layout["btn_fetch"]["state"]=tk.DISABLED
                                self.filename=None
                                self.layout["data_file_loaded"]['text']="None"
                                

                        


    
if __name__ == "__main__":
    
    layout=Layout()
    print("i'm here")