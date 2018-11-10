#!/bin/env python
# coding=UTF-8

'''
    StructUtil
    ==========
        Utils define.
'''

################################################################################
# Dump Struct Object List To PDB File
################################################################################

def Dumpl(structObjList, dumpFileName, fileMode = 'w'):

    with open(dumpFileName, fileMode) as fo:
        for structObj in structObjList:
            fo.write(structObj.Dumps())