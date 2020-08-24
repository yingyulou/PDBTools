#!/usr/bin/env python3
# coding=UTF-8

'''
DESCRIPTION

    PDBTools

    Collection of modules for PDB file parsing, linear algebra calculations and
    structure modify.

    See README file for full description and examples.

VERSION

    3.10.0

LATEST UPDATE

<<<<<<< HEAD
    2020.8.24
=======
    2020.8.9
>>>>>>> 66e2b24287e874b0345ac72c0549adc9213cc10f

'''

# Parser
from .src.PDBParser import Load, LoadModel

# Math Util
from .src.MathUtil import Dis, Norm, CalcVectorAngle, CalcRotationMatrix, \
    CalcRotationMatrixByTwoVector, CalcDihedralAngle, CalcRMSD, \
    CalcSuperimposeRotationMatrix, CalcRMSDAfterSuperimpose

# Struct Class
from .src.Protein import Protein
from .src.Chain import Chain
from .src.Residue import Residue
from .src.Atom import Atom

# Const
from .src.Constants import DIH, SIDE, RESIDUE_NAME_THREE_TO_ONE_DICT, \
    RESIDUE_NAME_ONE_TO_THREE_DICT

# Struct Util
from .src.StructUtil import IsH, SplitCompNum, Dumpls, Dumpl, DumpFastals, \
    DumpFastal
