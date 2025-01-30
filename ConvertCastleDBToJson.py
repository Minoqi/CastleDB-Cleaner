# Copyright (c) 2025 Minoqi
# This code is licensed under the MIT License.
# See LICENSE file for details.
import json
import os


# Variables
fileToConvert = ''
locationToSendTo = ''
overrideSameName = ''
overrideEnabled = False
convertedData = {}
originalData = {}
idString = ''


## Intro
print("Welcome to ClassDB Cleaner!")
print("This program will go through each sheet in your .cdb file and turn it into a JSON file.")
print("It will ask for an ID. This is the name of the column you used to mark the ID of the line of data.")
print("This ID has to be the same for all sheets, or you'll have to rerun the script for each unique ID name.")
print("If a sheet does not have the ID name, it will be skipped.")
print("WARNING: In order for a JSON dictionary to work correctly, make sure each ID value for each line in your CastleDB file is unique! You can do this with the 'Unique Identifier' data type option for the column. It will warn you if any of the values are the same.")


# Get the files paths
fileToConvert = input("Enter the Castle DB file path: ").strip()


# Open and load in the original file
try:
    with open(fileToConvert, "r") as file:
        originalData = json.load(file)
    print("SUCCESSFULLY LOADED")
except FileNotFoundError:
    print("ERROR: File not found")
    quit()
except json.JSONDecodeError:
    print("ERROR: Invalid JSON format")
    quit()
except Exception as e:
    print(f"ERROR: {e}")
    quit()


# Get the destination for converted file
useCurrentPath = input("Do you want to store the converted files in the same location this script is located in? (y/n) ").strip()
while useCurrentPath.lower() != "y" and useCurrentPath.lower() != "n":
    print("ERROR: Asnwer given is invalid, please try again.")
    useCurrentPath = input("Do you want to store the converted files in the same location this script is located in? (y/n) ").strip()

if useCurrentPath.lower() == "n":
    useCastleDBPath = input("Do you want to store the converted files in the same location the CastleDB file is located in? (y/n) ").strip()
    while useCastleDBPath.lower() != "y" and useCastleDBPath.lower() != "n":
        print("ERROR: Asnwer given is invalid, please try again.")
        useCastleDBPath = input("Do you want to store the converted files in the same location the CastleDB file is located in? (y/n) ").strip()

if useCurrentPath.lower() == "y":
    locationToSendTo = os.getcwd()
elif useCastleDBPath.lower() == "y":
    locationToSendTo = os.path.dirname(fileToConvert)
else:
    locationToSendTo = input("Enter the file path for the folder you want the conversion stored in: ").strip()

    while os.path.exists(locationToSendTo) == False:
        print("ERROR: That file path does not exist, please try again")
        locationToSendTo = input("Enter the file path for the folder you want the conversion stored in: ").strip()

# Add trailing slash if it's not there
if not locationToSendTo.endswith(os.sep):
    locationToSendTo += os.sep


# Get any other necessary information
overrideSameName = input("If the file already exists should it overrite it? (y/n) ").strip()

while overrideSameName.lower() != "y" and overrideSameName.lower() != "n":
    print("ERROR: Answer given is invalid, please try again.")
    overrideSameName = input("If the file already exists should it overrite it? (y/n) ").strip()

if overrideSameName.lower() == 'y':
    overrideEnabled = True

idString = input("What's the name of the key that's storing the ID value? Keep in mind this is case sensitive! -> ")


# Convert each sheet
for sheet in originalData["sheets"]:
    # Make sure there are lines, otherwise skip sheet (used to skip sheets made from list column types)
    if not sheet["lines"]:
        print(f"Skipping sheet used for column list type... {sheet["name"]}")
        continue

    # Make sure ID exists, otherwise skip sheet
    if idString not in sheet["lines"][0]:
        print(f"ERROR: ID not found in file, skipping sheet {sheet["name"]}... (Given ID: {idString})")
        continue

    # Save to it's own file
    for line in sheet["lines"]:
        convertedData[line[idString]] = line
        del convertedData[line[idString]][idString]
    
    finalPathName = locationToSendTo + sheet["name"] + ".json"
    
    if os.path.exists(finalPathName):
        if overrideEnabled == False:
            print(f"ERROR: File aready exists and override is set to false, skipping... ({finalPathName})")
            continue
        else:
            os.remove(finalPathName)
        
    with open(finalPathName, "w") as file:
        json.dump(convertedData, file, indent=4)
        print(f"File Done: {finalPathName}")
    
    # Reset
    convertedData = {}


print("DONE!")