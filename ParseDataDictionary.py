# -*- coding: utf-8 -*-
"""
This file is intended to parse the "Basic Monthly CPS" Data Dictionary for
2022 found at the link below, and build a collection of elements to use as a 
guide for parsing the monthly supplements. Some modification may be required to 
work with other years. I intend to extend it to include additonal supplement data.

https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.2022.html#list-tab-1979780401

Created on Sat Aug 26 09:32:30 2023
@author: gabe
"""

from objects import CpsUtil

# configuration
baseDictionaryLocation = "G:\\My Drive\\Grad School\\Code\\CPSDataTools\\DataDictionaries\\2022_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt"
strEndOfElements = "End of Basic CPS Portion of the Record"
strHeaderRowIndicator = "NAME"
descLineIndicators = ["\t", "NOTE: ", " ", "\n", "(", "PERSON"]
sectionLineIndicators = ["A3."]

fileDictionary = open(baseDictionaryLocation,"r")
linesDictionary = fileDictionary.readlines()
numLinesInFile = len(linesDictionary)

def goToNextLine(lineCount, linesDictionary):
    # consolidated this since I will be advancing lines in several different places
    line = linesDictionary[lineCount]
    lineCount += 1
    # Scrub the line - just remove newline for now
    line = line.replace("\n", "")
    while line == "":
        # do nothing and move to the next line
        line = linesDictionary[lineCount]
        lineCount += 1
        line = line.replace("\n", "")
        
    return lineCount, line

def processDescLines(strDescription, lineCount = 0):
    #build one string of description lines
    line = ""
    lineCount, line = goToNextLine(lineCount, linesDictionary)
    if line.startswith(tuple(descLineIndicators)): 
        strDescription = strDescription + line + "\n"
        strDescription, lineCount, line = processDescLines(strDescription, lineCount)
        
    return strDescription, lineCount, line

def parseDataDictionary2020():

    # infrastructure
    # global lineCount        # for tracking
    lineCount = 0
    line = ""
    #tupLine = [0,""]        # testing for recusion
    numLinesInFile = 0      # for instrumentation
    inBody = False          # says we have entered the beinging of lines of interest
    lastLine = False        # says we have hit the end of the lines of interest
    elements = []
    
    try:
  
    
        lineCount, line = goToNextLine(lineCount, linesDictionary)
        
        while not lastLine:
            
            if inBody == False and line.startswith(strHeaderRowIndicator):
                inBody = True
                # print("Found header line {}.".format(line))
                lineCount, line = goToNextLine(lineCount, linesDictionary)
                continue
            elif not inBody:
                #throw out lines until the 'column' specification starts
                lineCount, line = goToNextLine(lineCount, linesDictionary)
                continue
            elif line.startswith(strEndOfElements):
                lastLine = True
            elif inBody:
                if line.startswith(tuple(sectionLineIndicators)):
                    #throw out section headers
                    lineCount, line = goToNextLine(lineCount, linesDictionary)
                    continue
                
                # parse the data line
                splitLine=line.split("\t")
                # print(splitLine)
        
                index = 0 
                name = splitLine[index].strip()
                index += 1
                
                #move through white space
                while splitLine[index].strip() == "":
                    index +=1
                
                size = int(splitLine[index])
                index +=1
                
                #move through white space _should only be once..._
                while splitLine[index] == "":
                    index +=1
                    
                description = splitLine[index]
                index += 1
                maxIndex = len(splitLine)-1
                # everything before the last chunk should be description
                while index < maxIndex:
                    description = description + " " + splitLine[index]
                    index += 1
                
                description = description.strip()
                
                #break out the start / end and -1 so we have zero based indexing
                while(splitLine[maxIndex] =="" or splitLine[maxIndex] ==" "):
                    #step back until we have a value
                    maxIndex -=1 
                
                locations = splitLine[maxIndex].strip().split("-") 
                if(len(locations)==1):
                    locations = splitLine[maxIndex].split("–") # Yes we apparently have multiple types of dashes
                
                start = int(locations[0].strip())-1
                end = int(locations[1].strip())-1
                
                element = CpsUtil.DataDictonaryElement( name, 
                                                   size, 
                                                   description, 
                                                   start, 
                                                   end)
                
                #handle any following description lines 
                element.Description, lineCount, line = processDescLines(element.Description, lineCount)
        
                # print ("Data line {}: \"{}\"".format(lineCount, line))
        
                elements.append(element)
                
        
            # if lineCount >5000:
            #     lastLine = True
               
            continue

        # Print formated output and check the numbers
        checkStart = 0
        #checkEnd = 0
                    
        print("\n********************************************************************")
        for element in elements:
            print("Name: {0:<10}\tStart: {1}\t End: {2}".format(element.Name, element.Start, element.End))
            if not checkStart == element.Start:
                print("*** Misaligned Location: Name: {} Expected Start: {} Found: {}".format(element.Name, checkStart, element.Start))
            if not (element.End - element.Start + 1) == element.Size:
                 print("*** Mismatched Size / Start / End: Name: {} Expected Size: {} Found Size: {} Start: {} End: {}".format(element.Name, element.Size, element.End - element.Start + 1, element.Start, element.End))
            checkStart = element.End + 1
        print("********************************************************************")
        print("End of file processing. Proccessed {} of {} lines, {} elements.".format(lineCount, numLinesInFile, len(elements)))
        
        return elements        
    except:
        print("\n***** Error processing Line {}: \"{}\"\n".format(lineCount, line))
        raise

parseDataDictionary2020()