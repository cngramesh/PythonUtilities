########################################################################################################################################################
#Created on Feb 01, 2014
#Author: By PaNa Infotech for Corventis Inc

#Objective: SearchText_Replacer tool does the following multi-task by scanning the input directory/file path, 
#1. Replaces text given in "Search Text:" field with text in "Replace With:" field. 
#2. Finds and displays the line number and line data for user input text in "Search Text:" field.

#Input: A valid directory/file path containing zero or more files and text to search and replace.

#Output: If "Replace All" button is clicked by inputting dir/file path, then the old text (in "Search Text" field) will be replaced with the new text
#(in "Replace With" field) in all the file(s) of input directory or single file depending on the path specified. 
#If "Find Text" button is clicked by inputting dir/file path and search text then the "Text Area" will display the line number and line data if search
#text found in the input file/in file(s) of input directory. 

#Run Method: Double clicking on Explorer program
########################################################################################################################################################

from Tkinter import *
import tkFileDialog as tkfd
import ttk,tkMessageBox
import os

txtReplacerWindow = Tk() 
txtReplacerWindow.title("SearchText_Replacer")
#txtReplacerWindow.iconbitmap(default='textReplacer.ico')
txtReplacerWindow.resizable(width=False, height=False)

#Reset screen to original position
def clearScreen():
    global dirPathEntry,searchTxtEntry,replaceWithTxtEntry,displayTextArea
    
    dirPathEntry.delete(0, END)
    searchTxtEntry.delete(0, END)
    replaceWithTxtEntry.delete(0, END)
    displayTextArea.delete(1.0, END)
    dirPathEntry.focus_set()

#Replaces I/P text with new value
def replaceFileText(filePath,searchText,replaceText):
    fileTxtSearch = 0
    inFileReader = open(filePath,'r+')
    inputFileData = inFileReader.readlines()
    inFileReader.close()
    outFileWriter = open(filePath,'w')
    for line in inputFileData:
        if searchText in line:
            line = line.replace(searchText,replaceText)
            fileTxtSearch += 1 
        outFileWriter.write(line)
    outFileWriter.close()
    
    return fileTxtSearch

#Searches a text in a file
def searchFileText(filePath,searchText):
    lineNumList = []
    lineDataList = []
    ipFileReader = open(filePath,'r')
    ipFileData = ipFileReader.readlines()
    ipFileReader.close()
    for lineNum,lineData in enumerate(ipFileData):
        if searchText in lineData:
            lineNumList.append(lineNum+1)
            lineDataList.append(lineData)

    return lineNumList,lineDataList

#Validates user input    
def validateInput():
    global dirPathEntry,searchTxtEntry,replaceWithTxtEntry 
    global dirPath,filePath
    
    dirPath=filePath=None
    scanPath = dirPathEntry.get()
    
    if scanPath != "":
        if not os.path.exists(scanPath):
            tkMessageBox.showwarning(title='Warning', message="Input directory/file path doesn't exist.")
            dirPathEntry.focus_set()
            return 0
        else:
            if os.path.isfile(scanPath):
                filePath = scanPath
            if os.path.isdir(scanPath):
                dirPath = scanPath 
            
            if filePath == None and dirPath == None:
                tkMessageBox.showwarning(title='Warning', message="Input directory/file path is invalid.")
                dirPathEntry.focus_set()
                return 0
            else:
                return 1
    else:
        tkMessageBox.showwarning(title='Warning', message="Please input directory/file path.")
        dirPathEntry.focus_set()
        return 0

#Replaces I/P text in all files of a dir/in a file 
def txtReplacer():
    global searchTxtEntry,replaceWithTxtEntry
    global dirPath,filePath
    
    displayTextArea.delete(1.0, END)
    searchText = searchTxtEntry.get() 
    replaceText = replaceWithTxtEntry.get()
    
    #Call to validate I/P
    validateState = validateInput()
    
    if validateState == 0: return
    
    if searchText=="":
        tkMessageBox.showwarning(title='Warning', message="Please input text to search.")
        searchTxtEntry.focus_set()
        return
    
    if replaceText=="":
        tkMessageBox.showwarning(title='Warning', message="Please input Replace With text.")
        replaceWithTxtEntry.focus_set()
        return
    
    #Replace in specified text file
    if filePath != None:
        fileTxtSearch = replaceFileText(filePath,searchText,replaceText)
        tkMessageBox.showinfo(title='Replacer Info', message=str(fileTxtSearch) + " occurrence(s) was replaced in the input file.")
        replaceWithTxtEntry.focus_set()
        return
    
    #Replace text in all files of specified directory
    if dirPath != None:
        fileCount = 0
        for fileName in os.listdir(dirPath):
            try:
                fileName.split(".",1)
                filePath = dirPath + "\\" + fileName
                fileTxtSearch = replaceFileText(filePath,searchText,replaceText)
                if fileTxtSearch > 0:
                    fileCount += 1
            except:
                continue
            
        if fileCount == 0:
            tkMessageBox.showinfo(title='Replacer Info', message="Replaced text in " + str(fileCount) + " files.")
        else:
            tkMessageBox.showinfo(title='Replacer Info', message="Replaced successfully text in " + str(fileCount) + " files.")
        replaceWithTxtEntry.focus_set()
        return
    
#Searches for I/P text in I/P dir/file
def findText():
    global searchTxtEntry,displayTextArea
    global dirPath,filePath,dirPathEntry
    
    searchText = searchTxtEntry.get() 
    
    #Call to validate I/P
    validateState = validateInput()
    if validateState == 0: return
    
    if searchText=="":
        tkMessageBox.showwarning(title='Warning', message="Please input the text to search.")
        searchTxtEntry.focus_set()
        return
    
    #Replace in specified text file
    if filePath != None:
        lineNumList,lineDataList = searchFileText(filePath,searchText)
        if len(lineNumList)==0:
            fileTxtSearch = 0
        else:
            fileTxtSearch = len(lineNumList)
            displayTextArea.delete(1.0, END)
            displayTextArea.insert(INSERT,"Text '" + str(searchText) + "' search result in file " + os.path.basename(filePath))
            displayTextArea.insert(INSERT,"\n=================================================================")
            for index,value in enumerate(lineNumList):
                lineData = str(lineDataList[index]).strip()
                if len(lineData)>67:
                    lineData = lineData[0:68] + "\n" + lineData[68:]
                displayTextArea.insert(INSERT,"\nLine " + str(value) + ": " + lineData + "\n")
                     
        tkMessageBox.showinfo(title='Text Search Info', message=  "Text '" + str(searchText) + "' was found at "+ str(fileTxtSearch) + " line(s) in the input file.")
        searchTxtEntry.focus_set()
        return
    
    #Replace text in all files of specified directory
    if dirPath != None:
        txtSearchFileCount = 0
        totTxtSearchCount = 0
        displayTextArea.delete(1.0, END)
        displayTextArea.insert(INSERT,"Text '" + str(searchText) + "' search result in below file(s)")
        displayTextArea.insert(INSERT,"\n=================================================================")
        
        fileCount = 0
        for fileName in os.listdir(dirPath):
            try:
                fileName.split(".",1)
                filePath = dirPath + "\\" + fileName
                fileCount += 1
                lineNumList,lineDataList = searchFileText(filePath,searchText)
                if len(lineNumList)>0:
                    txtSearchFileCount += 1
                    totTxtSearchCount += len(lineNumList)
                    displayTextArea.insert(INSERT,"\n\nFile Name: " + fileName)
                    displayTextArea.insert(INSERT,"\n---------------------------------------------")
                    
                    for index,value in enumerate(lineNumList):
                        lineData = str(lineDataList[index]).strip()
                        if len(lineData)>67:
                            lineData = lineData[0:68] + "\n" + lineData[68:]
                        displayTextArea.insert(INSERT,"\nLine " + str(value) + ": " + lineData + "\n")
                    
                    displayTextArea.insert(INSERT,"\n")
            except:
                continue
       
        if totTxtSearchCount==0 and txtSearchFileCount==0:
            displayTextArea.delete(1.0, END)
        
        if fileCount==0:
            tkMessageBox.showwarning(title='Text Search Info', message=  "Sorry no files were found in the input directory.")
            dirPathEntry.focus_set()
        else:
            tkMessageBox.showinfo(title='Text Search Info', message=  "Text '" + str(searchText) + "' was found at "+ str(totTxtSearchCount) + " line(s) in " + str(txtSearchFileCount) + " file(s) of input directory.")
            searchTxtEntry.focus_set() 
        return

#Closes txtReplacer screen
def closeTxtReplacer():
    global txtReplacerWindow
    txtReplacerWindow.destroy()

#Browsing for required path
def folderSelection():
    global dirPathEntry,txtReplacerWindow
    
    dirname = tkfd.askdirectory(parent=txtReplacerWindow,initialdir="/",title='Please select a directory')
    dirname = dirname.replace("/","\\")
    dirPathEntry.delete(0, END)
    dirPathEntry.insert(END,dirname)
    dirPathEntry.focus_set()

#Handling keyboard actions
def browseFolderKeyAction(event):
    folderSelection()

def findKeyAction(event):
    findText()

def replaceAllKeyAction(event):
    txtReplacer()

def resetKeyAction(event):
    clearScreen()

def closeKeyAction(event):
    closeTxtReplacer()
    
#Launches Text Replacer GUI screen            
def autoTxtReplacerMain():
    global txtReplacerWindow,dirPathEntry,displayTextArea
    global dirPathEntry,searchTxtEntry,replaceWithTxtEntry
    
    style = ttk.Style()
    style.configure("TxtReplace.TButton", font = ('syatem',9,"bold"))
    
    #Centering Window position
    txtReplacerWindow.update_idletasks()
    x = (txtReplacerWindow.winfo_screenwidth() - txtReplacerWindow.winfo_reqwidth())/3
    y = (txtReplacerWindow.winfo_screenheight() - txtReplacerWindow.winfo_reqheight())/3
    txtReplacerWindow.geometry("+%d+%d" % (x,y))
    
    replacerFrame = Frame(txtReplacerWindow,bg="cornsilk")
    replacerFrame.grid(row=0, column=0, sticky=N+W)
    
    dirPathLabel = Label(replacerFrame, text= "Directory/File Path * :", bg="cornsilk")
    dirPathLabel.grid(row=0, column=0, padx=5, pady=17, sticky=N+W)
    
    dirPathEntry = ttk.Entry(replacerFrame,width=65, font = ('syatem',10,"bold"))
    dirPathEntry.grid(row=0, column=1, padx=3, pady=15, ipady=1, sticky=N+W)
    dirPathEntry.focus_set()
    
    browseButton = ttk.Button(replacerFrame, text="Browse Folder", style="TxtReplace.TButton", command=folderSelection)
    browseButton.grid(row=0, column=2, ipadx=3, ipady=3,padx=5, pady=10, sticky=N+W)
    browseButton.bind("<Return>",browseFolderKeyAction)
          
    searchLabel = Label(replacerFrame, text= "Search Text * :", bg="cornsilk")
    searchLabel.grid(row=1, column=0, padx=5, pady=5, sticky=N+W)
    
    findButton = ttk.Button(replacerFrame, text="Find Text", style="TxtReplace.TButton", command=findText)
    findButton.grid(row=1, column=2, ipadx=5, ipady=3,padx=5, pady=1, sticky=N+W)
    findButton.bind("<Return>",findKeyAction)
    
    searchTxtEntry = ttk.Entry(replacerFrame,width=65, font = ('syatem',10,"bold"))
    searchTxtEntry.grid(row=1, column=1, padx=3, pady=5, sticky=N+E)
    
    replaceLabel = Label(replacerFrame, text= "Replace With * :", bg="cornsilk")
    replaceLabel.grid(row=2, column=0, padx=5, pady=5, sticky=N+W)
    
    replaceWithTxtEntry = ttk.Entry(replacerFrame,width=65, font = ('syatem',10,"bold"))
    replaceWithTxtEntry.grid(row=2, column=1, padx=3, pady=5, sticky=N+E)
        
    replaceButton = ttk.Button(replacerFrame, text="Replace All", style="TxtReplace.TButton", command=txtReplacer)
    replaceButton.grid(row=3, column=1, padx=50, pady=10, ipadx=5, sticky=N+W)
    replaceButton.bind("<Return>",replaceAllKeyAction)
    
    resetButton = ttk.Button(replacerFrame, text="Reset", style="TxtReplace.TButton", command=clearScreen)
    resetButton.grid(row=3, column=1, padx=170, pady=10, ipadx=1, sticky=N+W)
    resetButton.bind("<Return>",resetKeyAction)
    
    quitButton = ttk.Button(replacerFrame, text="Quit", style="TxtReplace.TButton", command=closeTxtReplacer)
    quitButton.grid(row=3, column=1, padx=100, pady=10, ipadx=1, sticky=N+E)
    quitButton.bind("<Return>",closeKeyAction)
    
    textAreaFrame = Frame(txtReplacerWindow, bg="cornsilk")
    textAreaFrame.grid(row=2, column=0, sticky=N+W)
    
    displayTextArea = Text(textAreaFrame)
    displayTextScrollBar = ttk.Scrollbar(displayTextArea, orient=VERTICAL)
    displayTextScrollBar.pack(side=RIGHT, fill=Y)
    displayTextScrollBar.config(command=displayTextArea.yview)
    displayTextArea.configure(yscrollcommand=displayTextScrollBar.set)
    displayTextArea.grid(row=0, column=0, padx=10, pady=15, ipadx=327, ipady=75, sticky=N+W)
    
    txtReplacerWindow.mainloop()
    
autoTxtReplacerMain()