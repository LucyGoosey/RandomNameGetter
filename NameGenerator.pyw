import math, random, csv

from Tkinter import *

class GenerateDialog:
    def __init__(self, parent, namearray):
        self.top = Toplevel(parent);
        self.top.title("Generate");
        
        self.names = namearray;
                                            
        self.top.lift(aboveThis=parent);
        
        self.top.grab_set();
        self.top.focus_set();
        
        self.top.attributes("-toolwindow",1);
        
        self.top.bind("<Return>", self.OK);
        self.top.protocol("WM_DELETE_WINDOW", self.top.destroy);
        
        self.InitUI();
        
        self.top.update();
        
        width = self.top.winfo_width();
        height = self.top.winfo_height();
        self.top.geometry("+{0}+{1}".format((parent.winfo_x() + (parent.winfo_width() / 2)) - (width / 2),\
                                            (parent.winfo_y() + (parent.winfo_height() / 2)) - (height / 2)));
        self.top.update();
        
    def InitUI(self):
        topFrame = Frame(self.top);
        bottomFrame = Frame(self.top);
        
        topFrame.grid(column=0, row=0);
        bottomFrame.grid(column=0, row=1);
        
        numLabel = Label(topFrame, text="Total number of names to generate: ");
        self.numNames = StringVar();
        self.numNames.set("25");
        self.numEntry = Entry(topFrame, textvariable=self.numNames, width=5,\
                            validate='key', validatecommand=(self.ValidateInput, '%P'));
        self.numEntry.select_range(0, END);
        self.numEntry.focus();
        
        optLabel = Label(topFrame, text="Do you want male names, female names, or both?");
        self.optVar = IntVar();
        self.optVar.set(2);
        maleRadio = Radiobutton(topFrame, text="Male", variable=self.optVar, value=0);
        femaleRadio = Radiobutton(topFrame, text="Female", variable=self.optVar, value=1);
        bothRadio = Radiobutton(topFrame, text="Both", variable=self.optVar, value=2);
        bothRadio.select();
        
        ok = Button(bottomFrame, text="OK", command=self.OK, width=15);
        cancel = Button(bottomFrame, text="Cancel", command=self.top.destroy, width=15);
        
        numLabel.grid(column=0, row=0);
        self.numEntry.grid(column=1, row=0);
        
        optLabel.grid(column=0, row=1);
        
        maleRadio.grid(column=1, row=1);
        femaleRadio.grid(column=2, row=1);
        bothRadio.grid(column=3, row=1);
        
        ok.grid(column=0, row=0);
        cancel.grid(column=1, row=0);
        
        return;
        
    def ValidateInput(self, text):
        try:
            int(text);
            return True;
        except ValueError:
            return False;
        
    def OK(self, event=None):
        if(not self.ValidateInput(self.numNames.get())):
            self.numEntry.select_range(0, END);
            self.numEntry.focus();
            return;
        
        GenerateNames(self.optVar.get(), int(self.numNames.get()));
        
        self.top.destroy();
        return;

males = [];
females = [];
namelist = [];
root = None;
entry = None;

LONGEST_NAME = 27;

lastOpt = None;
lastNum = None;

def LoadNames(filename):
    global males, females;
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"');
        for row in reader:
            if(row[1].upper() == "B"):
                males.append(row[2]);
            else:
                females.append(row[2]);
                
def GetRandomNames(nameArr, numNames):
    return random.sample(nameArr, numNames if numNames < len(nameArr) else len(nameArr));
    
def GetRandomMaleNames(numNames):
    return GetRandomNames(males, numNames);
    
def GetRandomFemaleNames(numNames):
    return GetRandomNames(females, numNames);

def ShowGenerateDialog():
    global namelist;
    namelist = [];
    GenerateDialog(root, namelist);
    return;
    
def GenerateNames(opt, num):
    global lastOpt, lastNum;
    
    lastOpt = opt;
    lastNum = num;
    
    males = [];
    females = [];

    if(opt == 2):
        num = int(math.floor(num / 2));
        
    if(opt == 0 or opt == 2):
        males = GetRandomMaleNames(num);
    if(opt == 1 or opt == 2):
        females = GetRandomFemaleNames(num);
        
    DisplayNameList(males, females);
    return;
    
def GenerateAgain():
    if(lastOpt and lastNum):
        GenerateNames(lastOpt, lastNum);
        
    
def SetEntryText(text):
    global entry;
    entry.config(state=NORMAL);
    entry.delete(1.0, END);
    entry.insert(INSERT, text);
    entry.config(state=DISABLED);
    return;
    
def FormatNameList(list, text):
    counter = 0;
    for name in list:
        text += name;
        
        counter += 1;
        if(counter > 2):
            text += "\n";
            counter = 0;
        else:
            for i in range(len(name), LONGEST_NAME):
                text += " ";
            
    return text;

def DisplayNameList(males, females):
    namelist = "";
    
    if(males):
        namelist += "{0} Male names:\n".format(len(males));
        namelist = FormatNameList(males, namelist);        
        
    if(females and males):
        namelist += "\n\n";
        namelist += "********************************************************************************";
        namelist += "\n\n";
    
    if(females):
        namelist += "{0} Female names:\n".format(len(females));
        namelist = FormatNameList(females, namelist);
        
    SetEntryText(namelist);
    return;
    
def InitUI():    
    global entry;
    
    root.title("Random Name Generator");
    root.resizable(0, 1);
    
    mainframe = Frame(root);
    bottomframe = Frame(root);
    
    scrollbar = Scrollbar(mainframe);
    scrollbar.pack(side=RIGHT, fill=Y);
    
    mainframe.pack(fill=BOTH, expand=1);
    bottomframe.pack(side=BOTTOM);
    
    genButton = Button(bottomframe, text="Generate!", command=ShowGenerateDialog);
    genAgainButton = Button(bottomframe, text="Generate Again!", command=GenerateAgain);
    genButton.pack(side=LEFT);
    genAgainButton.pack(side=LEFT);

    entry = Text(mainframe, state=DISABLED);
    entry.pack(side=LEFT, fill=BOTH);
    
    entry.config(yscrollcommand=scrollbar.set);
    scrollbar.config(command=entry.yview);
        
def main():
    global root;
    LoadNames("bname.csv");
    
    root = Tk();

    root.geometry("{0}x{1}".format(*(665, 415)));

    root.update();
    
    InitUI();

    root.mainloop();

if __name__ == '__main__':
    main();