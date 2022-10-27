#!/usr/bin/env python3
# coding=UTF-8

'''
    Util
    ====
        Utility functions define.
'''

# Import PDBTools
from .Constants import __H_RE, __COMP_NUM_RE

########################################################################################################################
# If An Atom Name is H
########################################################################################################################

def IsH(atomName):

    return __H_RE.match(atomName)


########################################################################################################################
# Split CompNum To (ResNum, ResIns)
########################################################################################################################

def SplitCompNum(compNumStr):

    resNum, resIns = __COMP_NUM_RE.match(compNumStr).groups()

    return int(resNum), resIns


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
