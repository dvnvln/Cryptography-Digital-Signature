import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename
from Signature import *
import os

class UtilityFunction:
    @staticmethod
    def open_file():
        file_path = askopenfilename(filetypes=[('Files', '*')])
        if file_path is not None:
            pass
        return file_path

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tugas 5 Kripto (13518003 | 13518116)")
        self.resizable(False, False)

        options = {'padx': 5, 'pady': 0}

        #################
        ## TITLE FRAME ##
        #################
        titleFrame = tk.Frame(self, padx=25, pady=15)
        titleFrame['borderwidth'] = 3
        titleFrame['relief'] = 'groove'
        titleFrame.grid(row=0, column=0, padx=5, pady=(10, 0))

        self.titleLabel = ttk.Label(titleFrame, text="DIGITAL SIGNATURE SOFTWARE")
        self.titleLabel.grid(column=0, row=0, **options)

        ################
        ## MAIN FRAME ##
        ################
        mainFrame = tk.Frame(self, padx=25, pady=15)
        mainFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.inputLabel = ttk.Label(mainFrame, text='Input Text')
        self.inputLabel.grid(column=0, row=0, sticky='w', **options)
        self.inputText = tk.Text(mainFrame, height=25, width=30)
        self.inputText.grid(column=0, row=1, **options)

        self.signedLabelText = tk.StringVar()
        self.signedLabelText.set('Signed Text')
        self.signedLabel = ttk.Label(mainFrame, textvariable=self.signedLabelText)
        self.signedLabel.grid(row=0, column=1, sticky='w', **options)
        self.signedText = tk.Text(mainFrame, height=25, width=30)
        self.signedText.grid(column=1, row=1, sticky='w', **options)
        self.signedText.configure(state='disabled')

        ####################
        ## FUNCTION FRAME ##
        ####################
        functionFrame = tk.Frame(mainFrame, padx=25, pady=15)
        functionFrame.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        self.signBtn = ttk.Button(functionFrame, text='Sign Text', width=25)
        self.signBtn.grid(column=0, row=0, sticky='nsew')
        self.signBtn.configure(command=self.signFile)

        self.validBtn = ttk.Button(functionFrame, text='Check Validity', width=25)
        self.validBtn.grid(column=0, row=1, sticky='nsew')
        self.validBtn.configure(command=self.validateSignature)

        self.import_button = ttk.Button(functionFrame, text='Import File', width=25)
        self.import_button.grid(column=0, row=2, sticky='nsew', pady=(10,0))
        self.import_button.configure(command=self.importFile)
        self.import_label = tk.Text(functionFrame, height=1, width=25)
        self.import_label.grid(column=0, row=3, sticky='nsew', pady=(0,10))
        self.import_label.configure(state='disabled')

        self.importKey_button = ttk.Button(functionFrame, text='Import Public Key File', width=25)
        self.importKey_button.grid(column=0, row=4, sticky='nsew', pady=(10,0))
        self.importKey_button.configure(command=self.importKeyFile)
        self.importKey_label = tk.Text(functionFrame, height=1, width=25)
        self.importKey_label.grid(column=0, row=5, sticky='nsew', pady=(0,10))
        self.importKey_label.configure(state='disabled')

    def signFile(self, event=None):
        self.signedLabelText.set('Signed Text')
        self.signedText.configure(state='normal')
        self.signedText.delete('1.0', 'end')

        inputText = self.inputText.get('1.0', 'end-1c')
        sign = Signature(inputText)
        signedText = sign.signFile()

        self.signedText.insert(tk.INSERT, signedText)
        self.signedText.configure(state='disabled')

    def validateSignature(self, event=None):
        self.signedLabelText.set('Signature Validity')
        self.signedText.configure(state='normal')
        self.signedText.delete('1.0', 'end')

        inputText = self.inputText.get('1.0', 'end-1c')
        newlineCount = 0
        testInputText = inputText
        while(testInputText[-1] == '\n'):
            newlineCount += 1
            testInputText = testInputText[:-1]
        keys = self.importKey_label.get('1.0', 'end-1c')
        pubN,pubE = keys.replace(" ","").split(",")
        pubN,pubE = int(pubN), int(pubE)
        
        sign = Signature(inputText, n=pubN, e=pubE)
        valid = sign.validateSign()

        if(valid):
            self.signedText.insert(tk.INSERT, 'Signature is Valid!')
        else:
            self.signedText.insert(tk.INSERT, 'Signature is Invalid!')
        
        self.signedText.configure(state='disabled')
    
    def importKeyFile(self, event=None):
        self.importKey_label.configure(state='normal')
        f = UtilityFunction.open_file()
        fName, self.fileExtension = fileName, fileExtension = os.path.splitext(f)
        readFile = open(f, 'rb')
        fileReaded = readFile.read()
        b = bytearray(fileReaded)
        result = b.decode('latin-1')
        self.importKey_label.delete('1.0', 'end')
        self.importKey_label.insert(tk.INSERT, result)
        self.importKey_label.configure(state='disabled')

    def importFile(self, event=None):
        f = UtilityFunction.open_file()
        fName, self.fileExtension = fileName, fileExtension = os.path.splitext(f)
        readFile = open(f, 'rb')
        fileReaded = readFile.read()
        b = bytearray(fileReaded)
        result = b.decode('latin-1')
        self.inputText.delete('1.0', 'end')
        self.inputText.insert(tk.INSERT, result)


if __name__ == "__main__":
    app = App()
    app.mainloop()