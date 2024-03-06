#!/usr/bin/env python3
#
# Author: Dylan Boland
#
# ==== Description of Script ====
# This script prints out the meaning of a prefix or suffix
# that is supplied by the user on the command line.
#
# The prefixes and suffixes that are used throughout the RTL are stored
# in rtl_dictionary.json, a file located in <ADD PATH>.
#
# There are two main reasons for having this script and the rtl_dictionary.json file:
#
# (1) Should someone be thinking of introducing a new prefix or suffix for, say, the word “request”, they can check this 
# file to see if there is already one in use. They might have been thinking of using “_rqst”, but soon see that “_req” is 
# already being used to indicate a request signal. They decide to use this suffix too, and a consistency begins to build up.
#
# (2) A new member of the team (or a long-standing one, as the case may be!) might be wondering what a certain prefix or suffix means. 
# Say, for example, “PQ_”. They could then search the list of prefixes in the file (from anywhere in their environment and without 
# opening the file – details of how this can be done are in <ADD DOCUMENT>) and see that “PQ_” indicates that 
# whatever signal they are looking at is somehow related to the “Placement Queue”.

# Modules that we will need:
import os
import sys
import json
import argparse

# ==== Some General-info Strings ====
# Tags - define these here so they can be quickly and easily changed
errorTag   = """\t***Error: """
successTag = """\t***Success: """
infoTag    = """\t***Info: """

prefixHelpMsg = infoTag + """Call the script with the --prefix switch and supply the
prefix whose meaning you want to know. For example,

    check_rtl_meaning.py --prefix pq_

"""

suffixHelpMsg = infoTag + """Call the script with the --suffix switch and supply the
suffix whose meaning you want to know. For example,

    check_rtl_meaning.py --suffix _req

"""

listAllHelpMsg = infoTag + """Call the script with the --list_all switch in order
to see all of the prefixes and suffixes used in the RTL, as well as their explanations.
"""

pathToDictHelpMsg = infoTag + """Call the script with the --path_to_dict switch if you want
to search a RTL dictionary JSON file on a specific path
"""

noArgsMsg  = errorTag + """No input arguments were specified."""

fileReadAttemptMsg = infoTag + """Trying to read in {}"""

fileEmptyMsg = infoTag + """The file at {} is empty... creating the dictionary from scratch"""

unsupportedScriptUsageMsg = errorTag + """Only one switch (--prefix, --suffix, or --list_all) should be supplied at a time"""

prefixSuffixNotFoundMsg = infoTag + """The {} {} could not be found in {}"""

explanationMsg = """{}: {}"""

prefixSectionHeader = """=======================================
            Prefixes
=======================================\n\n"""

suffixSectionHeader = """\n=======================================
            Suffixes
=======================================\n\n"""


# Function to handle the input arguments
def parsingArguments():
    parser = argparse.ArgumentParser(description = "Theme for the new wallpaper.")
    parser.add_argument('--prefix', type = str, help = prefixHelpMsg)
    parser.add_argument('--suffix', type = str, help = suffixHelpMsg)
    # Below, we use 'action = 'store_true'' so that we do not need to supply
    # any argument alongside the '--list_all' switch. If we supply the '--list_all'
    # switch then "True" will be stored for the 'list_all' argument. It acts like
    # a boolean variable
    parser.add_argument('--list_all', action = 'store_true', help = listAllHelpMsg)
    parser.add_argument('--path_to_dict', type = str, help = pathToDictHelpMsg)
    return parser.parse_args()

def readInDictionary(pathToFile):
    with open(pathToFile) as p:
        try:
            print(fileReadAttemptMsg.format(pathToFile))
            dictionary = json.load(p)
        except:
            print(fileEmptyMsg.format(pathToFile))
            dictionary = {
                "Prefixes" : {
                "aref_": """Indicates that the signal is to do with the auto-refresh logic.""",
                "mmu_": """Indicates that the signal is coming from the memory-management unit."""
                },
                "Suffixes" : {
                "_req": """Indicates a request line.""",
                "_ctrl": """Indicates a control signal or a signal from a control block."""
                }
            }
    return dictionary

if __name__ == "__main__":

    # ==== Check if any Arguments were Supplied ====
    if len(sys.argv) == 1:
        print(noArgsMsg)
        exit()

    args = parsingArguments() # parse the input arguments (if there are any)
    
    # ==== Check if All the Prefixes and Suffixes are to be listed ====
    printOutDictionary = False
    if args.list_all:
        printOutDictionary = True
    
    # ==== Check if the user is wanting to check a prefix meaning ====
    lookUpPrefix = False
    if args.prefix:
        prefix = args.prefix
        lookUpPrefix = True

    # ==== Check if the user is wanting to check a suffix meaning ====
    lookUpSuffix = False
    if args.suffix:
        suffix = args.suffix
        lookUpSuffix = True

    # ==== Check if the user has supplied a path to the folder with the RTL dictionary ====
    pathSupplied = False
    if args.path_to_dict:
        filePath = args.path_to_dict
        pathSupplied = True

    fileName = "rtl_dictionary.json" # name of the file with all the RTL prefixes and suffixes
    if not pathSupplied: # first, check that no path argument was supplied
         # For now, we will store the file in the same directory as this script.
         # Should the rtl_dictionary.json file be moved to a different directory, then the
         # filePath variable below should be updated
         filePath = "./"

    # ==== Step 1: Read in the RTL dictionary ====
    rtlDictionary = readInDictionary(filePath + fileName)
    
    # ==== Step 2: Check if the prefix or suffix exists and print the explanation if it does ====
    if (lookUpPrefix):
        prefixList = rtlDictionary["Prefixes"] # extract the prefix segment of the dictionary
        if prefix in prefixList: # check if the prefix is in the list
            prefixExplanation = prefixList[prefix] # extract the comment or explanation
            print(explanationMsg.format(prefix, prefixExplanation))
        else:
            print(prefixSuffixNotFoundMsg.format("prefix", prefix, fileName))
    if (lookUpSuffix):
        suffixList = rtlDictionary["Suffixes"] # extract the suffix segment of the dictionary
        if suffix in suffixList: # check if the suffix is in the list
            suffixExplanation = suffixList[suffix] # extract the comment or explanation
            print(explanationMsg.format(suffix, suffixExplanation))
        else:
            print(prefixSuffixNotFoundMsg.format("suffix", suffix, fileName))
    if (printOutDictionary):
        outputMsg = prefixSectionHeader
        prefixList = rtlDictionary["Prefixes"] # extract the prefix segment of the dictionary
        suffixList = rtlDictionary["Suffixes"] # extract the suffix segment of the dictionary
        # ==== Add the prefixes and their explanations first ====
        for key, value in prefixList.items():
            outputMsg += f"""{key}: {value}\n"""
        
        outputMsg += suffixSectionHeader
        
        # ==== Add the suffixes next ====
        for key, value in suffixList.items():
            outputMsg += f"""{key}: {value}\n"""    
        
        # ==== Print the string to the console ====
        print(outputMsg)
    exit()
