#!/usr/bin/env python3
# coding=UTF-8

'''
    StructUtil
    ==========
        Utils define.
'''

################################################################################
# Get Dump String Of Struct Object List
################################################################################

def Dumpls(structObjList):

    return ''.join(structObj.Dumps() for structObj in structObjList)


################################################################################
# Dump Struct Object List To PDB File
################################################################################

def Dumpl(structObjList, dumpFilePath, fileMode = 'w'):

    with open(dumpFilePath, fileMode) as fo:
        for structObj in structObjList:
            fo.write(structObj.Dumps())


################################################################################
# Get Fasta String Of Struct Object List
################################################################################

def DumpFastals(structObjList):

    return ''.join(structObj.fasta for structObj in structObjList)


################################################################################
# Dump Struct Object List To Fasta File
################################################################################

def DumpFastal(structObjList, dumpFilePath, fileMode = 'w'):

    with open(dumpFilePath, fileMode) as fo:
        for structObj in structObjList:
            fo.write(structObj.fasta)
