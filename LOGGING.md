# PDBTools更新日志

### Version 3.9.0

1. [PDBParser] 修复Load与LoadModel函数在某些情况下产生的解析错误

2. [StructClass] 增加Move与MoveInsert函数

### Version 3.8.0

1. [StructUtil] 增加IsH函数

### Version 3.6.0

1. [Chain] 为Chain类增加subDict函数

2. [StructUtil] 增加SplitCompNum函数

### Version 3.5.0

1. [PDBParser] 修改LoadModel函数对于Protein对象的name属性的创建规则

### Version 3.4.6

1. 重新组织项目代码分布

2. 重写README

3. 重写LOGGING

4. [StructClass]为__NotAtomStructBase类增加IGetAtomsCoord，IFilterAtomsCoord方法

### Version 3.4.4

1. [MathUtil] 增加CalcRMSDAfterSuperimpose函数

### Version 3.4.2

1. [StructClass] 为Dump，RotateBBDihedralAngleByDeltaAngle，RotateBBDihedralAngleByTargetAngle，RotateSCDihedralAngleByDeltaAngle，RotateSCDihedralAngleByTargetAngle方法增加return self

### Version 3.4.0

1. [StructClass] 为__NotAtomStructBase类增加RemoveAlt方法

### Version 3.2.0

1. [StructClass] 为MoveCenter，RenumResidues，RenumAtoms，Append，Insert方法增加return self

2. [StructClass] 修复GetBBRotationAtomObj方法的错误行为

### Version 3.0.0

1. [StructClass] 将StructBaseClass_py2，StructBaseClass_py3与StructClass合并

### Version 2.16.4

1. [StructUtil] 增加Dumpls和DumpFastals函数

### Version 2.16.2

1. [PDBParser] 修改LoadModel函数对于"PDBID_Model_0"的命名行为。原"PDBID_Model_0"命名行为修改为直接命名为"PDBID"

### Version 2.16.0

1. [StructConst, StructClass] 为StructConst增加枚举变量DIH与SIDE，将所有“主链二面角种类”参数限定为DIH枚举变量中的值，将所有“主链二面角转动侧”参数限定为SIDE枚举变量中的值

### Version 2.15.0

1. [StructClass] 去除MoveCenter、RenumResidues、RenumAtoms方法的return self

### Version 2.14.12

1. [StructClass] chainDict，atomDict属性均更名为subDict

### Version 2.14.10

1. [StructClass] 为Protein类增加chainDict属性

### Version 2.14.8

1. [PDBParser, StructClass] 修改Load与LoadModel函数，将原子的occ和tempF属性解析类型由float修改至str。并修改Atom类的Dumps方法的格式字符串，以适用于新类型

2. [StructClass] Atom类的ins属性更名为alt，e属性更名为chg

3. [MathUtil] 增加CalcRMSD函数

### Version 2.14.6

1. [StructBaseClass] 修改__StructBase中的布尔逻辑，去除原基类中__nonzero__与__bool__方法，将布尔值的判定托管至__len__函数。这样做将使得空结构对象（sub属性长度为0）的布尔值为False，而Atom对象由于失去了所有布尔值判定方法，其布尔值一定为True

2. [PDBParser] 修改LoadModel函数，使其能够正确解析不含有MODEL关键词的PDB

### Version 2.14.4

1. [StructClass] 为__NotProteinStructBase类增加pre与next方法

2. [StructClass] 为Residue类增加atomsDict与coordDict方法

3. [StructClass] 修改关于主链二面角的多个方法的报错逻辑，将两端残基的计算直接视为IndexError

### Version 2.14.2

1. [StructClass] 将Atom类的following属性拆分为四个属性：occ，tempF，ele，e

### Version 2.14.0

1. [StructClass, StructConst] 为C_ResidueStruct类增加方法：CalcSCDihedralAngle，CalcSCRotationMatrixByDeltaAngle，CalcSCRotationMatrixByTargetAngle，GetSCRotationAtomObj，RotateSCDihedralAngleByDeltaAngle，RotateSCDihedralAngleByTargetAngle，同时，为StructConst增加常量_RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT，用于残基侧链的旋转调整

2. [StructClass] C_ResidueStruct类的CalcBBRotationMatrix，GetRotationAtomObj，ModifyBBDihedralAngleByDeltaAngle，ModifyBBDihedralAngle方法，分别更名为：CalcBBRotationMatrixByTargetAngle，GetBBRotationAtomObj，RotateBBDihedralAngleByDeltaAngle，RotateBBDihedralAngleByTargetAngle

3. [StructClass, StructBaseClass] 类：__C_StructBase，__C_NotAtomStructBase，__C_NotProteinStructBase，C_ProteinStruct, C_ChainStruct, C_ResidueStruct,C_AtomStruct分别更名为：__StructBase，__NotAtomStructBase，__NotProteinStructBase，Protein，Chain，Residue，Atom

### Version 2.12.4

1. [StructClass, PDBParser] 为C_AtomStruct类增加了ins属性，用于存储转变位置指示符。同时修改了C_AtomStruct类的__slots__、__init__、__repr__、__str__、Copy、Dumps方法，以及PDBParser中的Load、LoadModel函数，以支持该属性

2. [StructClass] 为__C_NotAtomStructBase类增加RenumResidues与RenumAtoms方法，分别用于对残基和原子进行重编号

### Version 2.12.2

1. [StructClass] 为C_ResidueStruct类增加fasta属性，用于生成默认格式的fasta文件样式字符串（readonly property属性）

2. [StructClass] 为__C_NotAtomStructBase非原子抽象基类增加DumpFasta方法，用于fasta文件的输出

3. [StructUtil] 增加DumpFastal函数，用于将包含多个结构对象的list输出成一个fasta文件

### Version 2.12.0

1. 重构StructClass与StructClass_py2，将抽象基类__C_StructBase的定义模块单独分离为StructBaseClass_py2与StructBaseClass_py3，其他继承类定义统一归入StructClass文件

2. [PDBParser] 增加LoadModel解析器函数，用于解析含有多个MODEL的PDB
