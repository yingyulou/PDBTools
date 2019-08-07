# PDBTools

PDB文件层级化解析与坐标线性代数运算工具集。

PDB文件在PDBTools中将被解析为4个层级：Protein -> Chain -> Residue -> Atom

**请注意：本文档中所有的“角度”均指弧度制角度；所有的“旋转矩阵”均指右乘旋转矩阵。**

## 基本函数与方法

### 基本函数

#### 1. Load

``` Python
Load(pdbFileName, parseHBool = False)
```

将PDB文件解析为Protein对象。

参数：

- pdbFileName, str：PDB文件名
- parseHBool, bool：是否开启氢原子解析

返回值：

- Protein对象

#### 2. LoadModel

``` Python
LoadModel(pdbFileName, parseHBool = False)
```

将含有MODEL关键词的PDB解析为Protein对象list，这些蛋白对象的name属性将被设置为：PDB文件名（不包含".pdb"）+ '\_MODEL\_' + MODEL编号。参数同Load函数。

如果PDB中不含MODEL关键词，或第一个MODEL关键词之前仍具有ATOM行，则这部分原子将被解析至返回值list的第一个元素中，其name属性将被设置为PDB文件名（不包含".pdb"）。

返回值：

- Protein对象list

#### 3. Dumpl

``` Python
Dumpl(structObjList, dumpFileName, fileMode = 'w')
```

将任何层级对象构成的list输出到PDB文件。

参数：

- structObjList, list：层级对象构成的list
- dumpFileName, str：PDB文件名
- fileMode, str：文件句柄打开模式

#### 4. Dumpls

``` Python
Dumpls(structObjList)
```

得到字符串形式的Dumpl函数输出内容。

#### 5. DumpFastal

``` Python
DumpFastal(structObjList, dumpFileName, fileMode = 'w')
```

将非Atom层级对象构成的list输出到Fasta文件。参数同Dumpl函数。

#### 6. DumpFastals

``` Python
DumpFastals(structObjList)
```

得到字符串形式的DumpFastal函数输出内容。

#### 7. \_\_init\_\_

四种结构对象的构造函数定义如下：

``` Python
Protein(proteinID = '')

Chain(chainName = '', owner = None)

Residue(resName = '', resNum = 0, resIns = '', owner = None)

Atom(atomName = '', atomNum = 0, atomCoord = array([0., 0., 0.]), atomAltLoc = '', atomOccupancy = '', atomTempFactor = '', atomElement = '', atomCharge = '', owner = None)
```

当调用这些构造函数时，如果owner不为None，则构造函数将自动在owner与新结构对象之间建立从属关系。

### 所有层级公有方法

#### 1. Dump

``` Python
Dump(self, dumpFileName, fileMode = 'w')
```

将self输出到PDB文件。返回self。

参数：

- dumpFileName, str：输出文件名
- fileMode, str：文件句柄打开模式

#### 2. Dumps

``` Python
Dumps(self)
```

得到字符串形式的PDB文件内容。

#### 3. Copy

``` Python
Copy(self)
```

得到self的深拷贝。

### 非Atom层级公有方法

#### 1. DumpFasta

``` Python
DumpFasta(self, dumpFileName, fileMode = 'w')
```

将self输出到fasta文件。参数同Dump方法。

#### 2. GetResidues, IGetResidues

``` Python
GetResidues(self)
IGetResidues(self)
```

跨层级直接返回self包含的所有残基对象。其中，GetResidues方法返回list，IGetResidues方法返回生成器。

#### 3. GetAtoms, IGetAtoms

``` Python
GetAtoms(self)
IGetAtoms(self)
```

跨层级直接返回self包含的所有原子对象。其中，GetAtoms方法返回list，IGetAtoms方法返回生成器。

#### 4. FilterAtoms, IFilterAtoms

``` Python
FilterAtoms(self, atomName = 'CA', *atomNameTuple)
IFilterAtoms(self, atomName = 'CA', *atomNameTuple)
```

跨层级直接按一个或多个原子名筛选self包含的所有原子对象。其中，FilterAtoms方法返回list，IFilterAtoms方法返回生成器。例：

``` Python
structObj.FilterAtoms()                 # 筛选CA原子（默认）
structObj.FilterAtoms('N', 'CA', 'C')   # 筛选骨架原子
```

#### 5. GetAtomsCoord

``` Python
GetAtomsCoord(self)
```

跨层级直接返回self包含的所有原子的坐标（N*3 ndarray）。

#### 6. FilterAtomsCoord

``` Python
FilterAtomsCoord(self, atomName = 'CA', *atomNameTuple)
```

跨层级直接按一个或多个原子名筛选self包含的所有原子对象，返回筛选后的所有原子的坐标（N*3 ndarray）。

#### 7. RenumResidues, RenumAtoms

``` Python
RenumResidues(self, startNum = 1)
RenumAtoms(self, startNum = 1)
```

对self包含的所有残基/原子进行重编号。startNum参数用于设定起始编号。返回self。

#### 8. MoveCenter

``` Python
MoveCenter(self)
```

整体平移self，使得self的几何中心平移至原点。返回self。

#### 9. Append, Insert

``` Python
Append(self, *appendObjTuple)
Insert(self, idxNum, *insertObjTuple)
```

为self追加/插入子结构。所有添加至self的子结构都是原结构对象调用Copy方法得到的拷贝，且会与self自动建立从属关系。返回self。

参数：

- *appendObjTuple, *insertObjTuple, *obj：self对应的子结构对象（不定长参数）
- idxNum, int：插入位置索引值

#### 10. RemoveAlt

``` Python
RemoveAlt(self)
```

一个特殊的操作：遍历self包含的所有原子对象，如果原子对象的alt属性为''，则忽略，如果为'A'，则修改为''，否则删除当前原子。返回self。

### 非Protein层级公有方法

#### 1. Remove

``` Python
Remove(self)
```

从结构对象中删除self自身。

## 特殊操作

### 迭代

非Atom对象可直接迭代，从而访问当前层级的子层级对象列表：

``` Python
for chainObj in structObj:
    for resObj in chainObj:
        for atomObj in resObj:
            pass
```

### 切片

非Atom对象可切片：

``` Python
structObj[:]        # 获取链对象
structObj[0][1:]    # 获取残基对象
structObj[0][0][0]  # 获取原子对象
```

### 长度

非Atom对象可调用len函数，求其子结构列表的长度：

``` Python
len(structObj)
```

### 布尔值

非Atom对象的布尔值依据其是否为空结构进行判定。即：如果self.sub为[]，则布尔值为False，否则为True。

Atom对象的布尔值一定为True。

### 欧氏距离

原子对象重载了减法运算符，用于求两原子之间的欧氏距离：

``` Python
atomObjA - atomObjB
```

## 属性

### 所有层级公有属性

#### 1. name, str

此属性对于不同的层级含义不同：

- Protein：PDB文件名（不包含".pdb"）
- Chain：链名
- Residue：残基名
- Atom：原子名

### 非Atom层级公有属性

#### 1. sub, list

self的子层级对象列表

#### 2. center, ndarray (只读)

self的所有原子坐标几何中心。

#### 3. seq, str (只读)

self的残基序列

#### 4. fasta, str (只读)

self的fasta文件字符串

### 非Protein层级公有属性

#### 1. owner, obj

self的父级对象

#### 2. idx, int (只读)

self在其owner的sub中的索引值

#### 3. pre, next, obj (只读)

self的前/后一个同层级对象

如果self没有前/后一个对象，则抛出IndexError

### 其他公有属性

#### 1. subDict, dict (只读)

Protein与Residue层级公有，含义分别为：

- Protein：由self的所有链对象组成的链名-链对象哈希表
- Residue：由self的所有原子对象组成的原子名-原子对象哈希表

#### 2. num, int

Residue与Atom层级公有，含义分别为：

- Residue：不包含插入字符的残基序号
- Atom：原子序号

### Residue独有属性

#### 1. ins, str

残基插入字符

#### 2. compNum, str (特殊方式写)

残基序号 + 残基插入字符

此属性通过(num, ins)二元组进行赋值：

``` Python
resObj.compNum = (1, '')
```

#### 3. coordDict, dict (只读)

由self的所有原子组成的原子名-原子坐标哈希表

### Atom独有属性

#### 1. coord, ndarray

原子坐标

#### 2. alt, str

备用位置指示符

#### 3. occ, str

占有

#### 4. tempF, str

温度因子

#### 5. ele, str

元素符号

#### 6. chg, str

电荷

## 残基二面角

残基对象实现了若干对蛋白主链二面角进行计算、旋转相关的方法（即以下所有方法的self都专指Residue对象）。

### 主链二面角

**对主链进行操作时请注意：最靠近N端与C端的两个残基分别无法进行二面角PHI与PSI的计算或调整（因为这两个二面角不存在）。如果出现上述情况，则抛出IndexError。**

#### 1. CalcBBDihedralAngle

``` Python
CalcBBDihedralAngle(self, dihedralEnum)
```

计算主链二面角。

参数：

- dihedralEnum, DIH：主链二面角种类。DIH.PHI或DIH.L表示Phi，DIH.PSI或DIH.R表示Psi。

#### 2. CalcBBRotationMatrixByDeltaAngle

``` Python
CalcBBRotationMatrixByDeltaAngle(self, dihedralEnum, sideEnum, deltaAngle)
```

以旋转角度作为参数，计算主链旋转矩阵。

参数：

- dihedralEnum, DIH：同CalcBBDihedralAngle方法。
- sideEnum, SIDE：转动侧。SIDE.N或SIDE.L表示转动N端，SIDE.C或SIDE.R表示转动C端。
- deltaAngle, float：转动角度。

返回值：

- moveCoord, ndarray(1*3)：旋转前/后平移向量
- rotationMatrix, ndarray(3*3)：旋转矩阵

#### 3. CalcBBRotationMatrixByTargetAngle

``` Python
CalcBBRotationMatrixByTargetAngle(self, dihedralEnum, sideEnum, targetAngle)
```

以目标角度作为参数，计算主链旋转矩阵。

参数与返回值同CalcBBRotationMatrixByDeltaAngle方法。但targetAngle表示目标角度。

#### 4. GetBBRotationAtomObj

``` Python
GetBBRotationAtomObj(self, dihedralEnum, sideEnum)
```

获取以给定参数进行旋转时，所有需要旋转的原子对象。参数同CalcBBRotationMatrixByDeltaAngle方法。

返回值：

- rotationAtomObjList, list：原子对象list

#### 5. RotateBBDihedralAngleByDeltaAngle

``` Python
RotateBBDihedralAngleByDeltaAngle(self, dihedralEnum, sideEnum, deltaAngle)
```

以旋转角度作为参数直接旋转主链。参数同CalcBBRotationMatrixByDeltaAngle方法。返回self。

#### 6. RotateBBDihedralAngleByTargetAngle

``` Python
RotateBBDihedralAngleByTargetAngle(self, dihedralEnum, sideEnum, targetAngle)
```

以目标角度作为参数直接旋转主链。参数同CalcBBRotationMatrixByTargetAngle方法。返回self。

### 侧链二面角

**对侧链进行调整时请注意：GLY、ALA残基由于不存在侧链二面角，不可调用下列方法。且不可使用不存在的侧链二面角索引值调用下列方法。如果出现上述情况，则抛出IndexError。**

#### 1. CalcSCDihedralAngle

``` Python
CalcSCDihedralAngle(self, dihedralIdx)
```

计算侧链二面角。

参数：

- dihedralIdx, int：侧链二面角索引值。索引值从0开始编号，最大允许索引值根据残基种类而不同。索引值表示某个残基从主链到侧链方向上的第N个侧链二面角。

#### 2. CalcSCRotationMatrixByDeltaAngle

``` Python
CalcSCRotationMatrixByDeltaAngle(self, dihedralIdx, deltaAngle)
```

以旋转角度作为参数，计算侧链旋转矩阵。

参数：

- dihedralIdx：同CalcSCDihedralAngle方法
- deltaAngle：旋转角度

返回值同CalcBBRotationMatrixByDeltaAngle方法。

#### 3. CalcSCRotationMatrixByTargetAngle

``` Python
CalcSCRotationMatrixByTargetAngle(self, dihedralIdx, targetAngle)
```

以目标角度作为参数，计算侧链旋转矩阵。参数与返回值同CalcSCRotationMatrixByDeltaAngle方法。但targetAngle表示目标角度。

#### 4. GetSCRotationAtomObj
``` Python
GetSCRotationAtomObj(self, dihedralIdx)
```

获取以给定侧链二面角进行旋转时，所有需要旋转的原子对象。参数同CalcSCDihedralAngle方法。返回值同GetBBRotationAtomObj方法。

#### 5. RotateSCDihedralAngleByDeltaAngle

``` Python
RotateSCDihedralAngleByDeltaAngle(self, dihedralIdx, deltaAngle)
```

以旋转角度作为参数直接旋转侧链。参数同CalcSCRotationMatrixByDeltaAngle方法。返回self。

#### 6. RotateSCDihedralAngleByTargetAngle

``` Python
RotateSCDihedralAngleByTargetAngle(self, dihedralIdx, targetAngle)
```

以目标角度作为参数直接旋转侧链。参数同CalcSCRotationMatrixByTargetAngle方法。返回self。

## 数学函数

#### 1. Dis

``` Python
Dis(coordA, coordB)
```

计算两个三维坐标之间的欧式距离。

#### 2. Norm

``` Python
Norm(coordArray)
```

计算一个三维坐标的二范数。

#### 3. CalcVectorAngle

``` Python
CalcVectorAngle(coordA, coordB)
```

计算两向量夹角，返回角度（0 ~ pi）。

#### 4. CalcRotationMatrix

``` Python
CalcRotationMatrix(rotationAxis, rotationAngle)
```

计算轴角旋转矩阵。

参数：

- rotationAxis, ndarray(1*3)：旋转轴向量，无需缩放至单位长度
- rotationAngle, float：旋转角

#### 5. CalcRotationMatrixByTwoVector

``` Python
CalcRotationMatrixByTwoVector(coordA, coordB)
```

计算从向量A旋转至向量B所需要的旋转矩阵。

#### 6. CalcDihedralAngle

``` Python
CalcDihedralAngle(coordA, coordB, coordC, coordD)
```

计算二面角。返回有符号角度（-pi ~ pi）。

``` Python
CalcRMSD(coordArrayA, coordArrayB)
```

计算RMSD。

参数：

- coordArrayA, coordArrayB, ndarray(N*3)：两组由三维坐标组成的等长二维数组

#### 7. CalcSuperimposeRotationMatrix

``` Python
CalcSuperimposeRotationMatrix(sourceCoordArray, targetCoordArray)
```

计算从sourceCoordArray到targetCoordArray的叠合旋转矩阵。

参数：

- sourceCoordArray, targetCoordArray, ndarray(N*3)：两组由三维坐标组成的等长二维数组

返回值为平移向量sourceCenterCoord，旋转矩阵rotationMatrix，以及平移向量targetCenterCoord。使得sourceCoordArray通过(sourceCoordArray - sourceCenterCoord).dot(rotationMatrix) + targetCenterCoord这样的平移->旋转->平移操作后，与targetCoordArray形成叠合。

#### 8. CalcRMSDAfterSuperimpose

``` Python
CalcRMSDAfterSuperimpose(coordArrayA, coordArrayB)
```

叠合并计算RMSD。

参数同CalcRMSD函数。

此函数会将coordArrayA通过CalcSuperimposeRotationMatrix函数向coordArrayB进行叠合，然后计算两组坐标之间的RMSD。

## 常量

#### 1. DIH

枚举变量，表示主链二面角种类。DIH.PHI或DIH.L表示Phi，DIH.PSI或DIH.R表示Psi。

#### 2. SIDE

枚举变量，表示主链二面角旋转时的转动侧。SIDE.N或SIDE.L表示转动N端，SIDE.C或SIDE.R表示转动C端。

#### 3. RESIDUE\_NAME\_THREE\_TO\_ONE\_DICT, RESIDUE\_NAME\_ONE\_TO\_THREE\_DICT

三字母，单字母残基名的相互转换哈希表。

## 其他说明

### 解析函数

- 解析函数（Load、LoadModel）将完全按照PDB文件中ATOM行的出现顺序对PDB文件进行解析与存储。不会进行任何排序或重组过程。
- Load函数在解析时会跳过任何非ATOM开头的行。而LoadModel函数会跳过任何非ATOM或MODEL开头的行。

### 对于创建新层级对象的判定

#### 1. Load函数：

- Protein：只会在解析开始前创建唯一的一个，并最终返回这个对象。
- Chain：在解析开始时，以及每次检测到链名发生变化时（从上一个ATOM行到当前行），都会创建新的链对象。
- Residue：在解析开始时，以及每次检测到残基名、残基编号或残基插入字符三者之一发生变化时（从上一个ATOM行到当前行），都会创建新的残基对象。
- Atom：每检测到一个新的ATOM行都会创建一个Atom对象。

#### 2. LoadModel函数：

- Protein：解析开始前，以及每次检测到MODEL关键词时，会创建一个新的蛋白对象。如果解析开始前创建的蛋白对象为空，则会在最后的返回值中被删除。
- Chain：解析开始时，每次检测到链名发生变化时（从上一个ATOM行到当前行），以及一个新的Model出现时，都会创建新的链对象。
- Residue：解析开始时，每次检测到残基名、残基编号或残基插入字符三者之一发生变化时（从上一个ATOM行到当前行），以及一个新的Model出现时，都会创建新的残基对象。
- Atom：每检测到一个新的ATOM行都会创建一个Atom对象。

### 空字段

解析时会对所有字符串属性进行strip方法处理，故所有的空字段都会被解析为空字符串。此性质在筛选及属性修改时可能有用。

### \_\_slots\_\_

出于性能的考虑，四个结构类都定义了\_\_slots\_\_，故不可以随意添加限定以外的属性。

### 未定义行为

本文档中未提及的，以及明显不符合层级结构的操作，如给残基追加链对象，迭代原子对象等，其行为都是未定义的。可能会引发错误或其他未知问题。出于性能的考虑，代码中未对调用时的各种不合理行为做全面的类型检查与行为检查。
