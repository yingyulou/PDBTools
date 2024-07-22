#!/usr/bin/env python3
# coding=UTF-8

'''
    Util
    ====
        Utility functions define.
'''

########################################################################################################################
# If An Atom Name is H
########################################################################################################################

def IsH(atomName):

    return (0x100000e000000000000 >> ord(atomName[0])) & 0x1


########################################################################################################################
# Split CompNum To (ResNum, ResIns)
########################################################################################################################

def SplitCompNum(compNumStr):

    if compNumStr[-1].isalpha():
        return int(compNumStr[:-1]), compNumStr[-1]
    else:
        return int(compNumStr), ''


########################################################################################################################
# Get Dump String Of Struct Object List
########################################################################################################################

def Dumpls(structObjList):

    return ''.join(structObj.Dumps() for structObj in structObjList)


########################################################################################################################
# Dump Struct Object List To PDB File
########################################################################################################################

def Dumpl(structObjList, dumpFilePath, fileMode = 'w'):

    with open(dumpFilePath, fileMode) as fo:
        for structObj in structObjList:
            fo.write(structObj.Dumps())


########################################################################################################################
# Get Fasta String Of Struct Object List
########################################################################################################################

def DumpFastals(structObjList):

    return ''.join(structObj.fasta for structObj in structObjList)


########################################################################################################################
# Dump Struct Object List To Fasta File
########################################################################################################################

def DumpFastal(structObjList, dumpFilePath, fileMode = 'w'):

    with open(dumpFilePath, fileMode) as fo:
        for structObj in structObjList:
            fo.write(structObj.fasta)
