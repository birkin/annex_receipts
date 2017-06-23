# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Part of LAS-to-Josiah code.
Convert names.
"""

import datetime, logging, os, pprint, string, sys

log = logging.getLogger(__name__)

## add project parent-directory to sys.path
parent_working_dir = os.path.abspath( os.path.join(os.getcwd(), os.pardir) )
sys.path.append( parent_working_dir )

from annex_eod_project import FileHandler






class NameConverter( object ):



    def makeTrueOrigToArchiveOrigDictionary(self, inputList, timeStamp):

        log.debug( 'starting makeTrueOrigToArchiveOrigDictionary()' )
        builtDict = {}
        for fileName in inputList:
            key = fileName
            # import string
            underscorePosition = string.find(fileName, "_")
            rootSlice = fileName[:underscorePosition]
            value = "ORIG_" + rootSlice + "_" + timeStamp + ".dat"
            builtDict[key] = value

        return builtDict



    def makeArchiveOrigToArchiveParsedDictionary(self, inputDictionary, timeStamp):

        builtDict = {}
        for fileName in inputDictionary.values(): # the value in the incoming dictionary becomes the key in this built dictionary
            key = fileName
            rootSlice = fileName[5:10]
            value = "PARSED_" + rootSlice + "_" + timeStamp + ".dat"
            builtDict[key] = value

        return builtDict



    def convertInputToOriginal(self, inputFileName):

        if(inputFileName[:4] == "ORIG"):
            root = inputFileName[5:10]
            month = inputFileName[16:18]
            day = inputFileName[19:21]
            returnValue = root + "_" + month + day + ".txt"
        elif(inputFileName[:4] == "PARS"):
            root = inputFileName[7:12]
            month = inputFileName[18:20]
            day = inputFileName[21:23]
            returnValue = root + "_" + month + day + ".txt"
        else:
            returnValue = inputFileName

        return returnValue


    # def prepareFinalDestinationDictionary(self, archive_original_to_archive_parsed_dictionary, destination_directory):
    #     """ Takes  most recently used dictionary (with references to empty files removed)
    #             and creates the new dictionary for copying the parsed files to their final destination.
    #         Also checks for pre-existing files, and if found, appends a suffix to the file name to prevent overwriting.
    #         Called by Controller.py """
    #     built_dct = {}
    #     for filename in archive_original_to_archive_parsed_dictionary.values():
    #         key = filename  # destinationFileName in inputDictionary becomes sourceFileName in outputDictionary
    #         root = filename[7:12].lower()
    #         year_str = filename[13:17]
    #         month_str = filename[18:20]
    #         day_str = filename[21:23]
    #         hour_str = filename[24:26]
    #         minute_str = filename[27:29]
    #         new_filename = '{rt}{yr}{mo}{dy}T{hr}{mn}'.format(
    #             rt=root, yr=year_str, mo=month_str, dy=day_str, hr=hour_str, mn=minute_str )
    #         built_dct[key] = new_filename
    #     log.debug( 'built_dct, ```{0}```'.format( pprint.pformat(built_dct) ) )
    #     return built_dct


    def prepareFinalDestinationDictionary(self, archive_original_to_archive_parsed_dictionary, destination_directory):
        """ Takes  most recently used dictionary (with references to empty files removed)
                and creates the new dictionary for copying the parsed files to their final destination.
            Also checks for pre-existing files, and if found, appends a suffix to the file name to prevent overwriting.
            Called by Controller.py """
        built_dct = {}
        for filename in archive_original_to_archive_parsed_dictionary.values():
            key = filename  # destinationFileName in inputDictionary becomes sourceFileName in outputDictionary
            root = filename[7:12].lower()
            ( year_str, month_str, day_str, hour_str, minute_str ) = self.make_datetime_strings( filename )
            new_filename = '{rt}{yr}{mo}{dy}T{hr}{mn}'.format(
                rt=root, yr=year_str, mo=month_str, dy=day_str, hr=hour_str, mn=minute_str )
            built_dct[key] = new_filename
        log.debug( 'built_dct, ```{0}```'.format( pprint.pformat(built_dct) ) )
        return built_dct

    def make_datetime_strings( self, filename ):
        """ Extracts timestamp info from filename.
            Called by prepareFinalDestinationDictionary() """
        year_str = filename[13:17]
        month_str = filename[18:20]
        day_str = filename[21:23]
        hour_str = filename[24:26]
        minute_str = filename[27:29]
        data_tpl = ( year_str, month_str, day_str, hour_str, minute_str )
        log.debug( 'data_tpl, ```{0}```'.format( pprint.pformat(data_tpl) ) )
        return data_tpl


    # def prepareFinalDestinationDictionary(self, archive_original_to_archive_parsed_dictionary, destination_directory):
    #     """ Takes  most recently used dictionary (with references to empty files removed)
    #             and creates the new dictionary for copying the parsed files to their final destination.
    #         Also checks for pre-existing files, and if found, appends a suffix to the file name to prevent overwriting.
    #         Called by Controller.py """
    #     built_dct = {}
    #     for filename in archive_original_to_archive_parsed_dictionary.values():
    #         key = filename  # destinationFileName in inputDictionary becomes sourceFileName in outputDictionary
    #         root = filename[7:12].lower()
    #         year_str = filename[13:17]
    #         month_str = filename[18:20]
    #         day_str = filename[21:23]
    #         hour_str = filename[24:26]
    #         minute_str = filename[27:29]
    #         second_str = filename[30:32]
    #         new_filename = '{rt}{yr}{mo}{dy}T{hr}{mn}{sc}.txt'.format(
    #             rt=root, yr=year_str, mo=month_str, dy=day_str, hr=hour_str, mn=minute_str, sc=second_str )
    #         built_dct[key] = new_filename
    #     log.debug( 'built_dct, ```{0}```'.format( pprint.pformat(built_dct) ) )
    #     return built_dct


#     def prepareFinalDestinationDictionary(self, archiveOriginalToArchiveParsedDictionary, destinationDirectory):
#         '''
#         - Takes the most recently used dictionary (with references to empty files removed) and creates the new dictionary for
#         copying the parsed files to their final destination.
#         - Also checks for pre-existing files, and if found, appends a suffix to the file name to prevent overwriting.
#         '''
#         builtDict = {}
#         for parsedFileName in archiveOriginalToArchiveParsedDictionary.values():

#             key = parsedFileName # destinationFileName in inputDictionary becomes sourceFileName in outputDictionary

#             root = parsedFileName[7:12]
#             # import string
#             root = string.lower(root)

#             month = parsedFileName[18:20]
#             day = parsedFileName[21:23]

#             basicCreatedName = root + month + day + ".txt" # this will be the destinationFileName *if* the file doesn't already exist.

#             # check for existence of pre-existing files with same root name.
# #               Remember, I'm iterating through a list now.
# #               The logic is that I start a loop, take my basicCreatedName and look for a match anywhere in the destinationDirectory.
# #               If no match, I'm golden (add to new dict), but if there is a match, add a suffix_number to the basicCreatedName and
# #               check again for a match in the destinationDirectory.

#             fileHandlerInstance = FileHandler.FileHandler()
#             log.debug( 'calling scanDirectory()' )
#             destinationFileList = fileHandlerInstance.scanDirectory(destinationDirectory)

#             hopefulFinalName = basicCreatedName
#             suffixNumeral = 1
#             flag = "continue"
#             sanityCheck = 0
#             while ( (flag == "continue") & (sanityCheck < 1000) ):
#                 sanityCheck = sanityCheck + 1 # no endless loops while developing

#                 comparisonResult = "initialize"
#                 for existingFileName in destinationFileList:
#                     if (existingFileName == hopefulFinalName):
#                         comparisonResult = "matchFound"

#                 if (comparisonResult == "initialize"):
#                     realFinalName = hopefulFinalName
#                     flag = "stop"
#                 else: # life is trickier
#                     suffixNumeral = suffixNumeral + 1
#                     hopefulFinalName = basicCreatedName + "_" + str(suffixNumeral)

#             # overwrite check done, new destination file name ready; update dictionary
#             builtDict[key] = realFinalName

#         return builtDict



# bottom
