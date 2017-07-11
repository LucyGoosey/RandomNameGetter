import csv, random

boys = [];
girls = [];

with open("bname.csv", 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"');
    for row in reader:
        if(row[1].upper() == "B"):
            boys.append(row[2]);
        else:
            girls.append(row[2]);
            
numNames = int(raw_input("How many names would you like? "));

option = "X";
while option != ""\
    and option.upper() != "B"\
    and option.upper() != "G"\
    and option.upper() != "O":
    option = raw_input("Would you like [b]oys names, [g]irls names, or B[o]th? ");

if(option == ""):
    option = "O";
    
option = option.upper();
if(option == "O"):
    numNames /= 2;

if(option == "B" or option == "O"):
    print "{0} random boys names:".format(numNames);
    for _ in range(numNames):
        print(random.choice(boys));
    
if(option == "G" or option == "O"):
    print "\n{0} random girls names:".format(numNames);
    for _ in range(numNames):
        print(random.choice(girls));