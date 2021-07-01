#!/usr/bin/env python3
# coding=UTF-8

'''
    Math
    ====
        Math functions define.
'''

# Import Python Lib
from math import sqrt, sin, cos, acos
from numpy import array, cross
from numpy.linalg import svd, det

################################################################################
# Calc Distance Between Two 3D-Coord (Instead of np.linalg.norm)
################################################################################

def Dis(coordA, coordB):

    return sqrt(
        (coordA[0] - coordB[0])**2 +
        (coordA[1] - coordB[1])**2 +
        (coordA[2] - coordB[2])**2)


################################################################################
# Calc Norm of A 3D-Coord (Instead of np.linalg.norm)
################################################################################

def Norm(coordArray):

    return sqrt(coordArray[0]**2 + coordArray[1]**2 + coordArray[2]**2)


################################################################################
# Calc Vector Angle
################################################################################

def CalcVectorAngle(coordA, coordB):

    return acos(coordA.dot(coordB) / (Norm(coordA) * Norm(coordB)))


################################################################################
# Calc Rotation Matrix (Right Multiply Matrix)
################################################################################

def CalcRotationMatrix(rotationAxis, rotationAngle):

    x, y, z = rotationAxis / Norm(rotationAxis)
    s, c = sin(rotationAngle), cos(rotationAngle)
    one_c = 1 - c

    rotationMatrix = array([
        [c + x**2 * one_c, x * y * one_c + z * s, x * z * one_c - y * s],
        [x * y * one_c - z * s, c + y**2 * one_c, y * z * one_c + x * s],
        [x * z * one_c + y * s, y * z * one_c - x * s, c + z**2 * one_c],
    ])

    return rotationMatrix


################################################################################
# Calc Rotation Matrix By Two Vector (From A To B, Right Multiply Matrix)
################################################################################

def CalcRotationMatrixByTwoVector(coordA, coordB):

    rotationAxis   = cross(coordA, coordB)
    rotationAngle  = CalcVectorAngle(coordA, coordB)
    rotationMatrix = CalcRotationMatrix(rotationAxis, rotationAngle)

    return rotationMatrix


################################################################################
# Calc Dihedral Angle
################################################################################

def CalcDihedralAngle(coordA, coordB, coordC, coordD):

    AB = coordB - coordA
    AC = coordC - coordA
    DB = coordB - coordD
    DC = coordC - coordD

    ABAC = cross(AB, AC)
    DBDC = cross(DB, DC)

    dihedralAngle = CalcVectorAngle(ABAC, DBDC)

    # Calc Sign
    OA = coordA - coordB
    OC = coordC - coordB
    OD = coordD - coordB

    rotationAngle = CalcVectorAngle(OC, array([1, 0, 0]))

    if rotationAngle != 0:
        rotationAxis   = cross(OC, array([1, 0, 0]))
        rotationMatrix = CalcRotationMatrix(rotationAxis, rotationAngle)
        OA = OA.dot(rotationMatrix)
        OD = OD.dot(rotationMatrix)

    OA[0] = 0
    OD[0] = 0

    rotationAngle = CalcVectorAngle(OA, array([0, 0, 1]))

    if rotationAngle != 0:
        rotationAxis   = cross(OA, array([0, 0, 1]))
        rotationMatrix = CalcRotationMatrix(rotationAxis, rotationAngle)
        OD = OD.dot(rotationMatrix)

    if OD[1] > 0:
        dihedralAngle = -dihedralAngle

    return dihedralAngle


################################################################################
# Calc RMSD (Root-mean-square Deviation)
################################################################################

def CalcRMSD(coordArrayA, coordArrayB):

    return sqrt(((coordArrayA - coordArrayB)**2).sum() / len(coordArrayA))


################################################################################
# Calc Superimpose Rotation Matrix (Kabsch Algorithm)
################################################################################

def CalcSuperimposeRotationMatrix(sourceCoordArray, targetCoordArray):

    sourceCenterCoord = sourceCoordArray.mean(0)
    targetCenterCoord = targetCoordArray.mean(0)

    U, E, V = svd((sourceCoordArray - sourceCenterCoord).transpose().dot(
        targetCoordArray - targetCenterCoord))

    if det(U) * det(V) < 0:
        U[:,-1] = -U[:,-1]

    rotationMatrix = U.dot(V)

    return sourceCenterCoord, rotationMatrix, targetCenterCoord


################################################################################
# Calc RMSD After Superimpose A => B
################################################################################

def CalcRMSDAfterSuperimpose(coordArrayA, coordArrayB):

    sourceCenterCoord, rotationMatrix, targetCenterCoord = CalcSuperimposeRotationMatrix(
        coordArrayA, coordArrayB)

    return CalcRMSD((coordArrayA - sourceCenterCoord).dot(rotationMatrix) +
        targetCenterCoord, coordArrayB)
