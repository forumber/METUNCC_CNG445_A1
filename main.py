from staff import *
from pprint import pprint
from food import *
from animal import *
from observation import *
from feeding import *
from terminaltables import AsciiTable
import datetime
import os
import sys

def loadFile():
    global sourcefile
    if sys.argv[1:]==[]:       #if there is no argument entered in terminal
        sourcefile=input("There is no argument!\nEnter a name for txt file to be created:")
        fo=open(sourcefile,"w+")
        fo.close()
    elif len(sys.argv) == 2:
        print(f"The source txt file name is {sys.argv[1]}")
        sourcefile=sys.argv[1]
    else:
        print("Too many arguments!")
        raise SystemExit
        


def readTxtFile():            #staff read is done, waiting for animal and food add functions to be added to implement them
    fo=open(sourcefile,"r+")
    fl=fo.read().splitlines()
    for ln in fl:
        if ln.startswith("S:"):
            step_2=ln[2:].split(",")
            staffList.append(Staff(step_2[0],step_2[1],step_2[2],step_2[3],step_2[4]))
        elif ln.startswith("A:"):
            step_2=ln[2:].split(",")
            theEnvironment = None
            for environment in environmentList:
                if environment.environmentID == step_2[4]:
                    theEnvironment = environment
            if (theEnvironment == None):
                print("Error while parsing file!")
                print("The environment with no", step_2[4], "is not found!")
                raise SystemExit
            animalList.append(Animal(step_2[0],step_2[1],step_2[2],step_2[3],theEnvironment))
        elif ln.startswith("E:"):
            step_2=ln[2:].split(",")
            environmentList.append(Environment(step_2[0],step_2[1],step_2[2],step_2[3],step_2[4])) 
        elif ln.startswith("F:"):
            step_2=ln[2:].split(",")
            foodList.append(Food(step_2[0],step_2[1],step_2[2]))
        elif ln.startswith("O:"):
            step_2=ln[2:].split(",")
            theStaff = None
            for staff in staffList:
                if staff.id == step_2[5]:
                    theStaff = staff
            if (theStaff == None):
                print("Error while parsing file!")
                print("The staff with no", step_2[5], "is not found!")
                raise SystemExit
            theAnimal = None
            for animal in animalList:
                if animal.no == step_2[6]:
                    theAnimal = animal
            if (theAnimal == None):
                print("Error while parsing file!")
                print("The animal with no", step_2[6], "is not found!")
                raise SystemExit
            #step_2[7] = unixTimeStamp
            theAnimal.observationRecord.append(
                Observation(step_2[0],step_2[1],step_2[2],step_2[3],step_2[4],theStaff, step_2[7]))
        elif ln.startswith("I:"): #feeding
            step_2=ln[2:].split(",")
            theStaff = None
            for staff in staffList:
                if staff.id == step_2[4]:
                    theStaff = staff
            if (theStaff == None):
                print("Error while parsing file!")
                print("The staff with no", step_2[4], "is not found!")
                raise SystemExit
            theAnimal = None
            for animal in animalList:
                if animal.no == step_2[5]:
                    theAnimal = animal
            if (theAnimal == None):
                print("Error while parsing file!")
                print("The animal with no", step_2[5], "is not found!")
                raise SystemExit
            theFood = None
            for food in foodList:
                if food.foodID == step_2[2]:
                    theFood = food
            if (theFood == None):
                print("Error while parsing file!")
                print("The food with no", step_2[2], "is not found!")
                raise SystemExit
            #step_2[6] is the unixTimeStamp which we use to compare dates easily
            theAnimal.feedingRecord.append(Feeding(step_2[0],step_2[1],theFood,step_2[3],theStaff,step_2[6]))
    fo.close()


def addStaff():
    staffList.append(Staff.create(sourcefile))
    

def addAnimal():
    animalList.append(Animal.create(environmentList,sourcefile))


def addEnvironment():
    environmentList.append(Environment.create(sourcefile,environmentList))


def addFood():
    foodList.append(Food.create(sourcefile, foodList))


def addObservation():
    printAnimals(0)
    selection = input("Select an animal by its no (type 0 to create a new one): ")
    foundAnimal = None
    while foundAnimal is None:
        if selection != '0':
            for animal in animalList:
                if selection == animal.no: foundAnimal = animal
            if foundAnimal is None:
                print("This animal doesn't exist in the database.")
                selection = input("Select an animal by its no (type 0 to create a new one): ")
        else:
            foundAnimal = Animal.create(environmentList, sourcefile)
            animalList.append(foundAnimal)
    
    foundAnimal.addObservation(sourcefile,staffList)


def addFeedingReport():
    printAnimals(0)
    selection = input("Select an animal by its no (type 0 to create a new one): ")
    foundAnimal = None
    while foundAnimal is None:
        if selection != '0':
            for animal in animalList:
                if selection == animal.no: foundAnimal = animal
            if foundAnimal is None:
                print("This animal doesn't exist in the database.")
                selection = input("Select an animal by its no (type 0 to create a new one): ")
        else:
            foundAnimal = Animal.create(environmentList, sourcefile)
            animalList.append(foundAnimal)
    
    foundAnimal.addFeeding(sourcefile,staffList,foodList)


def printAnimals(isFromMenu):
    if len(animalList) == 0 and isFromMenu:
        print("There is no animal to show detail of!")
        return
    data = [['Number', 'Gender', 'Date of Birth', 'Color']]
    for a in animalList: data.append([a.no, a.gender, a.doB, a.color])
    print(AsciiTable(data).table)
    if(isFromMenu):
        selection = input("Enter the number of animal whose details you want to see: ")
        found = 0
        while found == 0:
            for a in animalList:
                if a.no == selection:
                    a.printDetails()
                    found = 1
            if found == 0:
                print("This animal doesn't exist in the database.")
                selection = input("Enter the number of animal whose details you want to see: ")



def printStaff(staffList):
    data = [['ID', 'Name', 'Surname', 'Office', 'Tel']]
    for s in staffList: data.append([s.id,s.fName,s.lName,s.office,s.tel])
    print(AsciiTable(data).table)
    selection = input("Type 'E' to export details.\nor, press Enter to continue:")
    if selection == 'e' or selection == 'E':
        with open("staffDetails.txt", "w") as staffDetails:
            staffDetails.write(AsciiTable(data).table)
            print("Export successful.")



def printFood():
    data = [['Food Name', 'Manufacturer']]
    for f in foodList: data.append([f.foodName, f.manufacturer])
    print(AsciiTable(data).table)
    input("Press Enter to continue...")


def printEnvironment():
    data = [['ID', 'Humidity', 'Size', 'Temperature', 'Hours of light']]
    for a in environmentList: data.append([a.environmentID, a.humidity, a.size, a.temperature, a.h_of_light])
    print(AsciiTable(data).table)
    input("Press Enter to continue...")


def menu():
    while 1:
        print("\nWelcome to the Institute Tracking Application!")
        print("---MENU---")
        selection = 1 #need to initialize to make system(clear) work
        print(AsciiTable([['Select', 'Action'],
                ['1', 'Existing Staff Details'],
                ['2', 'Existing Animal Details'],
                ['3', 'Existing Food Details'],
                ['4', 'Existing Environment Details'],
                ['5', 'Create Animal Feeding Report'],
                ['6', 'Create Animal Observation Report'],
                ['7', 'Add a new staff'],
                ['8', 'Add a new animal'],
                ['9', 'Add a new environment'],
                ['10', 'Add a new food item'],
                ['-1', 'Exit']]).table)
        selection = int(input("Selection: "))
        if selection == 1: printStaff(staffList)
        elif selection == 2: printAnimals(1)
        elif selection == 3: printFood()
        elif selection == 4: printEnvironment()
        elif selection == 5: addFeedingReport()
        elif selection == 6: addObservation()
        elif selection == 7: addStaff()
        elif selection == 8: addAnimal()
        elif selection == 9: addEnvironment()
        elif selection == 10: addFood()
        elif selection == -1: raise SystemExit


if __name__ == '__main__':
    staffList = []
    foodList = [] 
    animalList = []
    environmentList = []
    sourcefile = None
    loadFile()     #Finds or creates source txt file
    readTxtFile()  #Reads from source file according to staff,animal or food lists
    menu()
    
 
