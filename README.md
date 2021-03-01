# PDBTools

PDB文件解析与坐标线性代数运算工具集。

PDB文件在PDBTools中将被解析为4个层级：Protein -\> Chain -\> Residue -\> Atom

**本文档中所有的“角度”均指弧度制角度；所有的“旋转矩阵”均指右乘旋转矩阵。**

## 使用说明

- PDBTools依赖Numpy以及Enum（仅Python2）

- 导入"PDBTools"即可使用：

``` Python
import PDBTools
```

- PDBTools的所有接口均位于名称空间PDBTools下

## PDB文件解析函数

### 1. Load

``` Python
Load(pdbFileName, parseHBool = False)
```

将PDB文件解析为Protein对象。

#### 参数：

- \<str\> pdbFilePath：PDB文件路径
- \<bool\> parseHBool：是否开启氢原子解析

#### 返回值：

- \<Protein\> Protein对象

#### 例：

``` Python
proObj = Load('xxxx.pdb')
```

### 2. LoadModel

``` Python
LoadModel(pdbFilePath, parseHBool = False)
```

将含有"MODEL"关键词的PDB文件解析为Protein对象list。

#### 参数：

- \<str\> pdbFilePath：PDB文件路径
- \<bool\> parseHBool：是否开启氢原子解析

#### 返回值：

- \<list\<Protein\>\> Protein对象构成的list

#### 例：

``` Python
proObjList = LoadModel('xxxx.pdb')
```

## 属性

### Protein属性

#### 1. \<str\> name

PDB文件名（不包含".pdb"）。

#### 2. \<int\> model

Model编号。

如果当前Protein对象由Load函数解析得到，或由LoadModel函数解析得到，但其不属于一个Model，则此值为0。

#### 3. \<list\<Chain\>\> sub

self包含的所有链对象。

#### 4. \<dict\<str, Chain\>\> subDict

self包含的所有{链名：链对象}哈希表。

**请注意：如果self包含多条链名一致的链，则此属性的数据不正确（先出现的链将被后出现的链覆盖）。**

#### 5. \<np.ndarray(1 * 3)\> center, 只读

self包含的所有原子的几何中心。

#### 6. \<str\> seq, 只读

self的残基序列。

#### 7. \<str\> fasta, 只读

self的字符串形式的Fasta文件内容，title为self.name。

### Chain属性

#### 1. \<str\> name

链名。

#### 2. \<Protein\> owner

self所属的Protein。

#### 3. \<list\<Residue\>\> sub

self包含的所有残基对象。

#### 4. \<dict\<str, Residue\>\> subDict, 只读

self包含的所有{完整残基编号：残基对象}哈希表。

**请注意：如果self包含多个完整残基编号一致的残基，则此属性的数据不正确（先出现的残基将被后出现的残基覆盖）。**

#### 5. \<np.ndarray(1 * 3)\> center, 只读

self包含的所有原子的几何中心。

#### 6. \<str\> seq, 只读

self的残基序列。

#### 7. \<str\> fasta, 只读

self的字符串形式的Fasta文件内容，title为self.name。

#### 8. \<int\> idx, 只读

self在self.owner.sub中的索引值。

#### 9. \<Chain\> pre, next, 只读

self在self.owner.sub中的前/后一个同级对象，如果不存在这样的对象（self是self.owner.sub中的第一个或最后一个元素），则将抛出IndexError异常。

### Residue属性

#### 1. \<str\> name

残基名。

#### 2. \<int\> num

残基编号。

#### 3. \<str\> ins

残基插入字符。

#### 4. \<Chain\> owner

self所属的Chain。

#### 5. \<list\<Atom\>\> sub

self包含的所有原子对象。

#### 6. \<str\> compNum

同时获取/设定残基对象的num + ins属性。

使用以下方式设定属性：

``` Python
proObj = Load('xxxx.pdb')
proObj[0][0].compNum = (0, '')
```

#### 7. \<dict\<str, Atom\>\> subDict, 只读

self包含的所有{原子名：原子对象}哈希表。

**请注意：如果self包含多个原子名一致的原子，则此属性的数据不正确（先出现的原子将被后出现的原子覆盖）。**

#### 8. \<dict\<str, np.ndarray(1 * 3)\>\> coordDict, 只读

self包含的所有{原子名：原子坐标}哈希表。

**请注意：如果self包含多个原子名一致的原子，则此属性的数据不正确（先出现的原子将被后出现的原子覆盖）。**

#### 9. \<np.ndarray(1 * 3)\> center, 只读

self包含的所有原子的几何中心。

#### 10. \<str\> seq, 只读

self的残基序列。

#### 11. \<str\> fasta, 只读

self的字符串形式的Fasta文件内容，title为self.name。

#### 12. \<int\> idx, 只读

self在self.owner.sub中的索引值。

#### 13. \<Residue\> pre, next, 只读

self在self.owner.sub中的前/后一个同级对象，如果不存在这样的对象（self是self.owner.sub中的第一个或最后一个元素），则将抛出IndexError异常。

### Atom属性

#### 1. \<str\> name

原子名。

#### 2. \<int\> num

原子编号。

#### 3. \<np.ndarray(1 * 3)\> coord

原子坐标。

#### 4. \<str\> alt

备用位置指示符。

#### 5. \<str\> occ

占有。

#### 6. \<str\> tempF

温度因子。

#### 7. \<str\> ele

元素符号。

#### 8. \<str\> chg

电荷。

#### 9. \<Residue\> owner

self所属的Residue。

#### 10. \<int\> idx, 只读

self在self.owner.sub中的索引值。

#### 11. \<Atom\> pre, next, 只读

self在self.owner.sub中的前/后一个同级对象，如果不存在这样的对象（self是self.owner.sub中的第一个或最后一个元素），则将抛出IndexError异常。

## 成员函数

### 构造函数

#### 1. Protein构造函数

``` Python
__init__(self, proteinID = '', modelNum = 0)
```

#### 参数：

- \<str\> proteinID：蛋白名，用于初始化name属性
- \<int\> modelNum：Model编号，用于初始化model属性

#### 例：

``` Python
proObj = Protein('xxxx')
```

#### 2. Chain构造函数

``` Python
__init__(self, chainName = '', owner = None)
```

#### 参数：

- \<str\> chainName：链名，用于初始化name属性
- \<Protein\> owner：self的所属Protein，用于初始化owner属性。如果owner不为None，则构造函数将自动在owner与self之间建立从属关系

#### 例：

``` Python
proObj = Protein('xxxx')
chainObj = Chain('X', proObj)
```

#### 3. Residue构造函数

``` Python
__init__(self, resName = '', resNum = 0, resIns = '', owner = None)
```

#### 参数：

- \<str\> resName：残基名，用于初始化name属性
- \<int\> resNum：残基编号，用于初始化num属性
- \<str\> resIns：残基插入字符，用于初始化ins属性
- \<Chain\> owner：self的所属Chain，用于初始化owner属性。如果owner不为None，则构造函数将自动在owner与self之间建立从属关系

#### 例：

``` Python
chainObj = Chain('X')
resObj = Residue('XXX', 0, '', chainObj)
```

#### 4. Atom构造函数

``` Python
__init__(self, atomName = '', atomNum = 0, atomCoord = array([0., 0., 0.]),
    atomAltLoc = '', atomOccupancy = '', atomTempFactor = '', atomElement = '',
    atomCharge = '', owner = None)
```

#### 参数：

- \<str\> atomName：原子名，用于初始化name属性
- \<int\> atomNum：原子编号，用于初始化num属性
- \<np.ndarray(1 * 3)\> atomCoord：原子坐标，用于初始化coord属性
- \<str\> atomAltLoc：备用位置指示符，用于初始化alt属性
- \<str\> atomOccupancy：占有，用于初始化occ属性
- \<str\> atomTempFactor：温度因子，用于初始化tempF属性
- \<str\> atomElement：元素符号，用于初始化ele属性
- \<str\> atomCharge：电荷，用于初始化chg属性
- \<Residue\> owner：self的所属Residue，用于初始化owner属性。如果owner不为None，则构造函数将自动在owner与self之间建立从属关系

#### 例：

``` Python
resObj = Residue('X')
atomObj = Atom('X', 0, np.array((0., 0., 0.)), '', '', '', '', '', resObj)
```

### 特殊成员函数

#### 1. \_\_iter\_\_（仅限非Atom层级）

``` Python
__iter__(self)
```

获取sub属性的迭代器。

#### 例：

``` Python
proObj = Load('xxxx.pdb')

for chainObj in proObj:
    for resObj in chainObj:
        for atomObj in resObj:
            pass
```

#### 2. \_\_len\_\_（仅限非Atom层级）

``` Python
__len__(self)
```

获取sub属性的长度。

#### 例：

``` Python
proObj = Load('xxxx.pdb')
subLen = len(proObj)
```

#### 3. \_\_getitem\_\_, \_\_setitem\_\_（仅限非Atom层级）

``` Python
__getitem__(self, sliceObj)

__setitem__(self, sliceObj, setValue)
```

通过索引值获取/设定sub属性中的元素。

#### 例：

``` Python
proObj = Load('xxxx.pdb')
atomObj = proObj[0][0][0]
proObj[0] = proObj[1].Copy()
```

#### 4. \_\_sub\_\_（仅限Atom层级）

``` Python
__sub__(self, subAtomObj)
```

获取两原子间的欧几里得距离。

#### 例：

``` Python
proObj = Load('xxxx.pdb')
atomDis = proObj[0][0][0] - proObj[0][0][1]
```

### 所有层级公有成员函数

#### 1. Dump

``` Python
Dump(self, dumpFilePath, fileMode = 'w')
```

将self输出到PDB文件。

#### 参数：

- \<str\> dumpFilePath：输出PDB文件路径
- \<str\> fileMode：文件句柄打开模式

#### 返回值：

- self

#### 例：

``` Python
proObj = Load('xxxx.pdb')
proObj.Dump('xxxx.pdb')
```

#### 2. Dumps

``` Python
Dumps(self)
```

得到字符串形式的PDB文件内容。

#### 参数：

- void

#### 返回值：

- \<str\> 字符串形式的PDB文件内容

#### 例：

``` Python
proObj = Load('xxxx.pdb')
dumpStr = proObj.Dumps()
```

#### 3. Copy

``` Python
Copy(self)
```

得到self的深拷贝。

#### 参数：

- void

#### 返回值：

- self的深拷贝

#### 例：

``` Python
proObj = Load('xxxx.pdb')
copyProObj = proObj.Copy()
```

### 非Atom层级公有成员函数

#### 1. [I]GetResidues

``` Python
GetResidues(self)

IGetResidues(self)
```

跨层级直接返回self包含的所有残基对象。

#### 参数：

- void

#### 返回值：

- \<list\<Residue\>\> 对于GetResidues
- \<Generator\<Residue\>\> 对于IGetResidues

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObjList = proObj.GetResidues()
resObjIter = proObj.IGetResidues()
```

#### 2. [I]GetAtoms, [I]FilterAtoms, [I]GetAtomsCoord, [I]FilterAtomsCoord

``` Python
GetAtoms(self)

IGetAtoms(self)

FilterAtoms(self, atomName = 'CA', *atomNameTuple)

IFilterAtoms(self, atomName = 'CA', *atomNameTuple)

GetAtomsCoord(self)

IGetAtomsCoord(self)

FilterAtomsCoord(self, atomName = 'CA', *atomNameTuple)

IFilterAtomsCoord(self, atomName = 'CA', *atomNameTuple)
```

跨层级直接返回self包含的所有，或按原子的name属性筛选后的原子对象或原子坐标。

#### 参数：

- \<*str\> *atomNameTuple：原子名列表

#### 返回值：

- \<list\<Atom\>\> 对于GetAtoms，FilterAtoms
- \<Generator\<Atom\>\> 对于IGetAtoms，IFilterAtoms
- \<np.ndarray\> 对于GetAtomsCoord，FilterAtomsCoord
- \<Generator\<np.ndarray(1 * 3)\>\> 对于IGetAtomsCoord，IFilterAtomsCoord

#### 例：

``` Python
proObj = Load('xxxx.pdb')

atomObjList = proObj.GetAtoms()
filterAtomObjList = proObj.FilterAtoms('N', 'CA', 'C')
atomCoordList = proObj.GetAtomsCoord()
filterAtomCoordList = proObj.FilterAtomsCoord('N', 'CA', 'C')

atomObjIter = proObj.IGetAtoms()
filterAtomObjIter = proObj.IFilterAtoms('N', 'CA', 'C')
atomCoordIter = proObj.IGetAtomsCoord()
filterAtomCoordIter = proObj.IFilterAtomsCoord('N', 'CA', 'C')
```

#### 3. MoveCenter

``` Python
MoveCenter(self)
```

将self的所有原子坐标减去center向量。

#### 参数：

- void

#### 返回值：

- self

#### 例：

``` Python
proObj = Load('xxxx.pdb')
proObj.MoveCenter()
```

#### 4. DumpFasta

``` Python
DumpFasta(self, dumpFilePath, fileMode = 'w')
```

将self输出到Fasta文件。

#### 参数：

- \<str\> dumpFilePath：输出Fasta文件路径
- \<str\> fileMode：文件句柄打开模式

#### 返回值：

- self

#### 例：

``` Python
proObj = Load('xxxx.pdb')
proObj.DumpFasta('xxxx.fasta')
```

#### 5. RenumResidues, RenumAtoms

``` Python
RenumResidues(self, startNum = 1)

RenumAtoms(self, startNum = 1)
```

对self的所有残基/原子进行重编号。

#### 参数：

- \<int\> startNum：起始编号

#### 返回值：

- self

#### 例：

``` Python
proObj = Load('xxxx.pdb')
proObj.RenumResidues().RenumAtoms()
```

#### 6. Append, Insert

``` Python
Append(self, subObj, copyBool = True)

Insert(self, insertIdx, subObj, copyBool = True)
```

为self追加/插入子结构。所有添加至self的子结构都是原结构对象调用Copy成员函数得到的拷贝，且会与self自动建立从属关系。如果copyBool被设定为False，则拷贝不会发生。

#### 参数：

- \<*SubObj\> subObjTuple：self对应的子结构对象列表
- \<int\> insertIdx：插入位置索引值
- \<bool\> copyBool：是否拷贝subObj

#### 返回值：

- self

#### 例：

``` Python
proObj = Load('xxxx.pdb')
proObj.Append(proObj.sub[0]).Insert(0, proObj.sub[0])
```

#### 7. RemoveAlt

``` Python
RemoveAlt(self)
```

遍历self包含的所有原子对象，如果原子对象的alt属性为''，则忽略，如果为'A'，则修改为''，否则删除当前原子。

#### 参数：

- void

#### 返回值：

- self

#### 例：

``` Python
proObj = Load('xxxx.pdb')
proObj.RemoveAlt()
```

### 非Protein层级公有成员函数

#### 1. Remove

``` Python
Remove(self)
```

从self.owner.sub中删除self。

#### 参数：

- void

#### 返回值：

- void

#### 例：

``` Python
proObj = Load('xxxx.pdb')
proObj.sub[0].Remove()
```

## 残基二面角

残基对象实现了若干对蛋白主/侧链二面角进行计算和旋转相关的成员函数（即以下所有成员函数的self都专指Residue对象）。

### 主链二面角

**对主链进行操作时请注意：N端与C端的两个残基分别无法进行二面角Phi与Psi的计算或调整（因为这两个二面角不存在）。如果出现上述情况，则将抛出IndexError异常。**

#### 1. CalcBBDihedralAngle

``` Python
CalcBBDihedralAngle(self, dihedralEnum)
```

计算主链二面角。

#### 参数：

- \<DIH\> dihedralEnum：主链二面角种类。DIH.PHI或DIH.L表示Phi；DIH.PSI或DIH.R表示Psi

#### 返回值：

- \<float\> 有符号二面角值（-pi ~ pi）

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObj = proObj[0][1]
dihedralAngle = resObj.CalcBBDihedralAngle(DIH.PHI)
```

#### 2. CalcBBRotationMatrixByDeltaAngle, CalcBBRotationMatrixByTargetAngle

``` Python
CalcBBRotationMatrixByDeltaAngle(self, dihedralEnum, sideEnum, deltaAngle)

CalcBBRotationMatrixByTargetAngle(self, dihedralEnum, sideEnum, targetAngle)
```

以旋转角度/目标角度作为参数，计算主链旋转矩阵。

#### 参数：

- \<DIH\> dihedralEnum：主链二面角种类。DIH.PHI或DIH.L表示Phi；DIH.PSI或DIH.R表示Psi
- \<SIDE\> sideEnum：转动侧。SIDE.N或SIDE.L表示转动N端；SIDE.C或SIDE.R表示转动C端
- \<float\> deltaAngle/targetAngle：旋转角度/目标角度

#### 返回值：

- \<np.ndarray(1 * 3)\> 旋转前/后平移向量
- \<np.ndarray(3 * 3)\> 旋转矩阵

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObj = proObj[0][1]
moveCoord, rotationMatrix = resObj.CalcBBRotationMatrixByDeltaAngle(DIH.PHI, SIDE.N, 1.)
moveCoord, rotationMatrix = resObj.CalcBBRotationMatrixByTargetAngle(DIH.PHI, SIDE.N, 0.)
```

#### 3. GetBBRotationAtomObj

``` Python
GetBBRotationAtomObj(self, dihedralEnum, sideEnum)
```

获取以给定参数进行旋转时，所有需要旋转的原子对象列表。

#### 参数：

- \<DIH\> dihedralEnum：主链二面角种类。DIH.PHI或DIH.L表示Phi；DIH.PSI或DIH.R表示Psi
- \<SIDE\> sideEnum：转动侧。SIDE.N或SIDE.L表示转动N端；SIDE.C或SIDE.R表示转动C端

#### 返回值：

- \<list\<Atom\>\> 所有需要旋转的原子对象列表

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObj = proObj[0][1]
rotationAtomObjList = resObj.GetBBRotationAtomObj(DIH.PHI, SIDE.N)
```

#### 4. RotateBBDihedralAngleByDeltaAngle, RotateBBDihedralAngleByTargetAngle

``` Python
RotateBBDihedralAngleByDeltaAngle(self, dihedralEnum, sideEnum, deltaAngle)

RotateBBDihedralAngleByTargetAngle(self, dihedralEnum, sideEnum, targetAngle)
```

以旋转角度/目标角度作为参数直接旋转主链。

#### 参数：

- \<DIH\> dihedralEnum：主链二面角种类。DIH.PHI或DIH.L表示Phi；DIH.PSI或DIH.R表示Psi
- \<SIDE\> sideEnum：转动侧。SIDE.N或SIDE.L表示转动N端；SIDE.C或SIDE.R表示转动C端
- \<float\> deltaAngle/targetAngle：旋转角度/目标角度

#### 返回值：

- self

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObj = proObj[0][1]
resObj.RotateBBDihedralAngleByDeltaAngle(DIH.PHI, SIDE.N, 1.)
resObj.RotateBBDihedralAngleByTargetAngle(DIH.PHI, SIDE.N, 0.)
```

### 侧链二面角

**对侧链进行调整时请注意：GLY、ALA残基由于不存在侧链二面角，不可调用下列成员函数。且不可使用不存在的侧链二面角索引值调用下列成员函数。如果出现上述情况，则将抛出IndexError异常。**

#### 1. CalcSCDihedralAngle

``` Python
CalcSCDihedralAngle(self, dihedralIdx)
```

计算侧链二面角。

#### 参数：

- \<int\> dihedralIdx：侧链二面角索引值。索引值从0开始编号，最大允许索引值根据残基种类而不同。索引值表示某个残基从主链到侧链方向上的第N个侧链二面角

#### 返回值：

- \<float\> 有符号二面角值（-pi ~ pi）

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObj = proObj[0][1]
dihedralAngle = resObj.CalcSCDihedralAngle(0)
```

#### 2. CalcSCRotationMatrixByDeltaAngle, CalcSCRotationMatrixByDeltaAngle

``` Python
CalcSCRotationMatrixByDeltaAngle(self, dihedralIdx, deltaAngle)

CalcSCRotationMatrixByTargetAngle(self, dihedralIdx, targetAngle)
```

以旋转角度/目标角度作为参数，计算侧链旋转矩阵。

#### 参数：

- \<int\> dihedralIdx：侧链二面角索引值。索引值从0开始编号，最大允许索引值根据残基种类而不同。索引值表示某个残基从主链到侧链方向上的第N个侧链二面角
- \<float\> deltaAngle/targetAngle：旋转角度/目标角度

#### 返回值：

- \<np.ndarray(1 * 3)\> 旋转前/后平移向量
- \<np.ndarray(3 * 3)\> 旋转矩阵

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObj = proObj.sub[0].sub[1]
moveCoord, rotationMatrix = resObj.CalcSCRotationMatrixByDeltaAngle(0, 1.)
moveCoord, rotationMatrix = resObj.CalcSCRotationMatrixByTargetAngle(0, 0.)
```

#### 3. GetSCRotationAtomObj

``` Python
GetSCRotationAtomObj(self, dihedralIdx)
```

获取以给定侧链二面角进行旋转时，所有需要旋转的原子对象列表。

#### 参数：

- \<int\> dihedralIdx：侧链二面角索引值。索引值从0开始编号，最大允许索引值根据残基种类而不同。索引值表示某个残基从主链到侧链方向上的第N个侧链二面角

#### 返回值：

- \<list\<Atom\>\> 所有需要旋转的原子对象列表

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObj = proObj[0][1]
rotationAtomObjList = resObj.GetSCRotationAtomObj(0)
```

#### 4. RotateSCDihedralAngleByDeltaAngle, RotateSCDihedralAngleByTargetAngle

``` Python
RotateSCDihedralAngleByDeltaAngle(self, dihedralIdx, deltaAngle)

RotateSCDihedralAngleByTargetAngle(self, dihedralIdx, targetAngle)
```

以旋转角度/目标角度作为参数直接旋转侧链。

#### 参数：

- \<int\> dihedralIdx：侧链二面角索引值。索引值从0开始编号，最大允许索引值根据残基种类而不同。索引值表示某个残基从主链到侧链方向上的第N个侧链二面角
- \<float\> deltaAngle/targetAngle：旋转角度/目标角度

#### 返回值：

- self

#### 例：

``` Python
proObj = Load('xxxx.pdb')
resObj = proObj[0][1]
resObj.RotateSCDihedralAngleByDeltaAngle(0, 1.)
resObj.RotateSCDihedralAngleByTargetAngle(0, 0.)
```

## 数学函数

### 1. Dis

``` Python
Dis(coordA, coordB)
```

计算两个三维坐标之间的欧几里得距离。

#### 参数：

- \<np.ndarray(1 * 3)\> coordA，coordB：两个三维坐标

#### 返回值：

- \<float\> 欧几里得距离

#### 例：

``` Python
coordDis = Dis(np.array((1., 2., 3.)), np.array((4., 5., 6.)))
```

### 2. Norm

``` Python
Norm(coordArray)
```

计算三维向量的二范数。

#### 参数：

- \<np.ndarray(1 * 3)\> coordArray：三维坐标

#### 返回值：

- \<float\> 二范数

#### 例：

``` Python
coordNorm = Norm(np.array((1., 2., 3.)))
```

### 3. CalcVectorAngle

``` Python
CalcVectorAngle(coordA, coordB)
```

计算两向量夹角。

#### 参数：

- \<np.ndarray(1 * 3)\> coordA，coordB：两个三维向量

#### 返回值：

- \<float\> 两向量夹角值（0 ~ pi）

#### 例：

``` Python
vectorAngle = CalcVectorAngle(np.array((1., 2., 3.)), np.array((4., 5., 6.)))
```

### 4. CalcRotationMatrix

``` Python
CalcRotationMatrix(rotationAxis, rotationAngle)
```

计算轴角旋转矩阵。

#### 参数：

- \<np.ndarray(1 * 3)\> rotationAxis：旋转轴向量，无需缩放至单位长度
- \<float\> rotationAngle：旋转角

#### 返回值：

- \<np.ndarray(3 * 3)\> 旋转矩阵

#### 例：

``` Python
rotationMatrix = CalcRotationMatrix(np.array((1., 2., 3.)), 1.)
```

### 5. CalcRotationMatrixByTwoVector

``` Python
CalcRotationMatrixByTwoVector(coordA, coordB)
```

计算从向量A旋转至向量B所需要的旋转矩阵。

#### 参数：

- \<np.ndarray(1 * 3)\> coordA，coordB：两个三维向量

#### 返回值：

- \<np.ndarray(3 * 3)\> 旋转矩阵

#### 例：

``` Python
rotationMatrix = CalcRotationMatrixByTwoVector(np.array((1., 2., 3.)), np.array((4., 5., 6.)))
```

### 6. CalcDihedralAngle

``` Python
CalcDihedralAngle(coordA, coordB, coordC, coordD)
```

计算二面角。

#### 参数：

- \<np.ndarray(1 * 3)\> coordA，coordB，coordC，coordD：四个三维向量

#### 返回值：

- \<float\> 有符号二面角值（-pi ~ pi）

#### 例：

``` Python
dihedralAngle = CalcDihedralAngle(np.array((1., 2., 3.)), np.array((4., 5., 6.)),
    np.array((7., 8., 9.)), np.array((10., 11., 12.)))
```

### 7. CalcRMSD

``` Python
CalcRMSD(coordArrayA, coordArrayB)
```

对两组等长的三维坐标计算RMSD。

#### 参数：

- \<np.ndarray(N * 3)\> coordArrayA，coordArrayB：两组等长的矩阵

#### 返回值：

- \<double\> RMSD值

#### 例：

``` Python
rmsdValue = CalcRMSD(np.array(((1., 2., 3.), (4., 5., 6.))),
    np.array(((7., 8., 9.), (10., 11., 12.))))
```

### 8. CalcSuperimposeRotationMatrix

``` Python
CalcSuperimposeRotationMatrix(sourceCoordArray, targetCoordArray)
```

计算从sourceCoordArray到targetCoordArray的叠合旋转矩阵。

#### 参数：

- \<np.ndarray(N * 3)\> sourceCoordArray, targetCoordArray：两组等长的矩阵

#### 返回值：

- \<np.ndarray(1 * 3)\> 前平移向量
- \<np.ndarray(3 * 3)\> 旋转矩阵
- \<np.ndarray(1 * 3)\> 后平移向量

#### 例：

``` Python
coordArrayA = np.array(((1., 2., 3.), (4., 5., 6.)))
coordArrayB = np.array(((7., 8., 9.), (10., 11., 12.)))

sourceCenterCoord, rotationMatrix, targetCenterCoord = CalcSuperimposeRotationMatrix(
    coordArrayA, coordArrayB)

print((coordArrayA - sourceCenterCoord).dot(rotationMatrix) + targetCenterCoord)
print(coordArrayB)
```

### 9. CalcRMSDAfterSuperimpose

``` Python
CalcRMSDAfterSuperimpose(coordArrayA, coordArrayB)
```

叠合并计算RMSD。

此函数会将coordArrayA通过CalcSuperimposeRotationMatrix函数向coordArrayB进行叠合，然后计算两组坐标之间的RMSD。

#### 参数：

- \<np.ndarray(N * 3)\> coordArrayA，coordArrayB：两组等长的矩阵

#### 返回值：

- \<float\> RMSD值

#### 例：

``` Python
rmsdValue = CalcRMSDAfterSuperimpose(np.array(((1., 2., 3.), (4., 5., 6.))),
    np.array(((7., 8., 9.), (10., 11., 12.))))
```

## 常量

### 1. \<Enum\> DIH

枚举变量，表示主链二面角种类。DIH.PHI或DIH.L表示Phi，DIH.PSI或DIH.R表示Psi。

### 2. \<Enum\> SIDE

枚举变量，表示主链二面角旋转时的转动侧。SIDE.N或SIDE.L表示转动N端，SIDE.C或SIDE.R表示转动C端。

### 3. \<dict\<str, str\>\> RESIDUE_NAME_THREE_TO_ONE_DICT, RESIDUE_NAME_ONE_TO_THREE_HASH

三字母，单字母残基名的相互转换哈希表。

## 其他函数

### 1. IsH

``` Python
IsH(atomName)
```

判断一个原子名是否为氢原子。

#### 参数：

- \<str\> atomName：原子名

#### 返回值：

- \<bool\> 原子名是否为氢原子

#### 例：

``` Python
isHBool = IsH('1H')
```

### 2. SplitCompNum

``` Python
SplitCompNum(compNumStr)
```

将完整残基编号分割为残基编号和残基插入编号。

#### 参数：

- \<str\> compNumStr：完整残基编号

#### 返回值：

- \<int\> 残基编号
- \<str\> 残基插入编号

#### 例：

``` Python
resNum, resIns = SplitCompNum('1A')
```

### 3. Dumpl

``` Python
Dumpl(structObjList, dumpFilePath, fileMode = 'w')
```

将任何对象构成的list输出到PDB文件。

#### 参数：

- \<list\<Obj\>\> structObjList：任何层级对象构成的list
- \<str\> dumpFilePath：输出PDB文件路径
- \<str\> fileMode：文件句柄打开模式

#### 返回值：

- void

#### 例：

``` Python
proObjList = LoadModel('xxxx.pdb')
Dumpl(proObjList, 'xxxx.pdb')
```

### 4. Dumpls

``` Python
Dumpls(structObjList)
```

得到字符串形式的Dumpl函数输出内容。

#### 参数：

- \<list\<Obj\>\> structObjList：任何层级对象构成的list

#### 返回值：

- \<str\> 字符串形式的Dumpl函数输出内容

#### 例：

``` Python
proObjList = LoadModel('xxxx.pdb')
dumpStr = Dumpls(proObjList)
```

### 5. DumpFastal

``` Python
DumpFastal(structObjList, dumpFilePath, fileMode = 'w')
```

将非Atom对象构成的list输出到Fasta文件。

#### 参数：

- \<list\<Obj\>\> structObjList：非Atom对象构成的list
- \<str\> dumpFilePath：输出Fasta文件路径
- \<str\> fileMode：文件句柄打开模式

#### 返回值：

- void

#### 例：

``` Python
proObjList = LoadModel('xxxx.pdb')
DumpFastal(proObjList, 'xxxx.fasta')
```

### 6. DumpFastals

``` Python
DumpFastals(structObjList)
```

得到字符串形式的DumpFastal函数输出内容。

#### 参数：

- \<list\<Obj\>\> structObjList：非Atom对象构成的list

#### 返回值：

- \<str\> 字符串形式的DumpFastal函数输出内容

#### 例：

``` Python
proObjList = LoadModel('xxxx.pdb')
dumpStr = DumpFastals(proObjList)
```

## 补充说明

### 解析函数

- PDB文件解析函数（Load、LoadModel）将完全按照PDB文件内容进行解析，不会对结构进行任何排序、合并或重组操作
- Load函数在解析时会跳过任何非"ATOM"关键词开头的行（包括"MODEL"）；而LoadModel函数会跳过任何非"ATOM"或"MODEL"关键词开头的行
- 解析时会去除所有字符串类型属性双端的空格字符

### 对于创建新对象的判定

#### 1. Load函数：

- Protein：只会在解析开始前创建唯一的一个，并最终返回这个对象
- Chain：解析开始时，以及每次检测到链名发生变化时（从上一个"ATOM"行到当前行），都会创建一个新的链对象
- Residue：解析开始时，创建新链时，以及每次检测到残基名、残基编号或残基插入字符三者之一发生变化时（从上一个"ATOM"行到当前行），都会创建一个新的残基对象
- Atom：每检测到一个新的"ATOM"行都会创建一个新的Atom对象

#### 2. LoadModel函数：

- Protein：解析开始前，以及每次检测到"MODEL"关键词时，都会创建一个新的蛋白对象。如果解析开始前创建的这个蛋白对象在函数返回前仍然为空，则其将在函数返回前被删除
- Chain：解析开始时，创建新Model时，以及每次检测到链名发生变化时（从上一个"ATOM"行到当前行），都会创建一个新的链对象
- Residue：解析开始时，创建新Model时，创建新链时，以及每次检测到残基名、残基编号或残基插入字符三者之一发生变化时（从上一个"ATOM"行到当前行），都会创建一个新的残基对象
- Atom：每检测到一个新的"ATOM"行都会创建一个新的Atom对象

### 空字段

解析时会对所有字符串属性进行strip方法处理，故所有的空字段都会被解析为空字符串。此性质在筛选及属性修改时可能有用。

### \_\_slots\_\_

出于性能的考虑，四个结构类都定义了\_\_slots\_\_，故不可以随意添加限定以外的属性。

### 未定义行为

本文档中未提及的，以及明显不符合层级结构的操作，如给残基追加链对象，迭代原子对象等，其行为都是未定义的。可能会引发错误或其他未知问题。出于性能的考虑，代码中未对调用时的各种不合理行为做全面的类型检查与行为检查。
