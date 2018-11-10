# PDBTools

PDBTools
========
PDB文件层级化解析与坐标线性代数运算工具集。

结构的表示
----------
PDB文件在PDBTools中将被解析为4个层级：Protein -> Chain -> Residue -> Atom

每一个层级都有一个或多个层级对象与之对应。除ATOM层级以外，其余层级均存储了属于此
层级的所有下一层级对象，可通过层级关系进行逐层遍历访问。且除了Protein层级以外，
其余层级均可通过owner属性访问到其父层级对象。


PDB文件的I/O
------------
首先导入PDBTools：

import PDBTools

通过调用Load函数，以文件名作为其第一参数，可将一个PDB文件导入并解析为Struct对象：

structObj = PDBTools.Load('xxx.pdb')  # 导入并解析PDB文件

Load函数也可接受默认值为False的第二参数，用于显式的打开氢原子的解析。如果此参数
被指定为True，则PDB文件中所有的氢原子将也被解析，否则在默认情况下氢原子将被忽略：

structObj = PDBTools.Load('xxx.pdb', True)  # 开启氢原子解析

任何层级对象可通过调用Dump方法，将层级对象输出为一个新的PDB文件。Dump方法以PDB
文件名作为其第一参数。其也可接受第二参数，用于指定文件句柄的打开模式（一般为w或
a模式），此参数默认值为w。例：

structObj.Dump('xxx.pdb')  # 输出结构对象到PDB文件

与pickle模块类似，任何层级对象也可调用Dumps方法，得到字符串形式的PDB文件内容：

structObj.Dumps()  # 得到结构对象的字符串表示

StructUtil模块中实现了Dumpl函数，可接受由任意层级对象组成的list与输出文件名作为
参数，将list中所有的层级对象依次输出到文件。其也可接受默认值为w的第三参数，用于
指定文件句柄的打开模式：

PDBTools.Dumpl(structObjList, 'xxx.pdb')  # 将structObjList输出到PDB文件


层级的访问
----------
在所有四个层级中，除Atom层以外，其余层均实现了迭代器。当迭代这些层级的对象时，将
委托迭代当前层级的子层级对象列表。下例展示了从最顶层的Struct对象一直遍历到最底层
的Atom对象的过程：

for chainObj in structObj:
    for resObj in chainObj:
        for atomObj in resObj:
            pass

除Atom层以外，其余层也实现了基于列表切片(slice)的访问。可像访问list元素一样，通
过索引和切片获取子结构列表：

structObj[:]        # 获取所有的链对象列表
structObj[0][1:]    # 获取第一条链的第二个到最后一个的残基对象
structObj[0][0][0]  # 获取第一条链的第一个残基的第一个原子对象

Residue层级的所有父层级(Protein, Chain)均可通过调用GetResidues方法，跨层级直接
获取所有的残基对象列表。Atom层级的所有父层级(Protein, Chain, Residue)均可通过调
用GetAtoms方法，跨层级直接获取所有的原子对象列表。IGetResidues与IGetAtoms方法分
别是上述两个方法的迭代器版本，其将返回一个生成器：

structObj.GetAtoms()         # 获取所有的原子对象列表
structObj[0].GetResidues()   # 获取所有的残基对象列表
structObj.IGetAtoms()        # 获取所有的原子对象迭代器
structObj[0].IGetResidues()  # 获取所有的残基对象迭代器

Atom层级的所有父层级(Protein, Chain, Residue)均可通过调用GetAtomsCoord方法，跨
层级直接获取所有原子的坐标矩阵，该方法的返回值是一个二维的ndarray：

structObj.GetAtomsCoord()  # 获取所有原子的坐标矩阵

除Atom层以外，其余层对象可通过Python的len()函数获取当前对象的子结构对象的数量
（即子结构列表的长度）：

len(structObj[0])  # 获取这条链所含有的残基数量


各层级属性访问与修改
--------------------
首先，每一层级都有name属性，对于Protein层级对象而言，其表示PDB文件名（不包含
".pdb"扩展名），而对于Chain层级对象而言，其表示链名，对于Residue层级对象，其
表示残基名，而对于Atom层级对象，其表示原子名。

除Protein层以外，其余所有层级对象都有owner属性，可访问到当前对象的父级对象。

除Atom层以外，其余所有层级对象都有sub属性，可访问到当前对象的子层级对象列表。

除Protein层以外，其余所有层级对象都有idx属性，表示当前对象在其owner的子结构列表
中的索引值。此属性通过@property装饰器实现，为只读属性，不可修改。

除Atom层级外，其余层级均可访问center属性，其计算了当前结构对象所有原子的坐标几
何中心。此属性通过@property装饰器实现，为只读属性，不可修改。

除Atom层级外，其余层级均可访问seq属性，访问此属性可得到当前结构对象所含有的所有
残基的单字母序列字符串。此属性通过@property装饰器实现，为只读属性，不可修改。

Residue与Atom层级具有num属性，对于Residue层级，其表示残基序号（不包含插入字符），
对于Atom层级，其表示原子序号。这个属性是int类型的。

Residue层级具有ins属性，表示残基插入字符。以及compNum属性，可访问到完整的残基序
号，包含残基序号+残基插入字符。

Atom层级具有coord属性，表示当前原子的坐标，这个属性是numpy的ndarray类型。以及
following属性，保存了ATOM行3个坐标以后的所有信息，存储为一个字符串。一般无需对
此属性进行访问与修改。

除Residue层级的compNum属性外，其他所有属性均可通过赋值方式进行修改，修改时应
注意保证数据类型的前后一致性。

Residue层级的compNum属性通过@property装饰器进行访问与修改，在修改此属性时，属性
应接受一个含有两个元素的list或tuple，分别指定为残基编号与插入字符：

resObj.compNum = ('ALA', '')  # 将当前残基完整编号修改为ALA（无插入字符）


结构的分析与调整
----------------
除Atom层级外，其余层级均可调用MoveCenter方法，将当前结构的坐标几何中心平移至原点。此方法对结
构对象进行原地修改，同时返回修改后的结构对象本身：

structObj.MoveCenter()  # 移动structObj的坐标几何中心至原点

两个原子对象之间可通过减法运算得到这两个原子之间的欧氏距离：

structObj[0][0][0] - structObj[0][0][1]  # 得到两个原子之间的欧氏距离

残基对象实现了若干与主链二面角调整相关的API，说明如下：

* CalcBBDihedralAngle(self, dihedralSideStr)
传入残基主链二面角种类字符串：l/phi表示二面角PHI，其余字符串表示二面角PSI，不区
分大小写。返回弧度制二面角。

* CalcBBRotationMatrixByDeltaAngle(self, dihedralSideStr, modifySideStr, rotationAngle)
传入二面角种类字符串（见上），调整端侧字符串：l/n表示对N端进行旋转，其余字符串
表示对C端进行旋转，不区分大小写，以及一个弧度制角度，返回一个平移向量以及一个右
乘旋转矩阵。使得某个坐标A在经过平移与旋转后，相当于绕给定的主链旋转轴，在原角度
基础上旋转了给定角度。

* CalcBBRotationMatrix(self, dihedralSideStr, modifySideStr, targetAngle)
参数与返回值同上。区别在于，当一个坐标在经过此函数得到的旋转矩阵进行变换后，相
当于绕给定的主链旋转轴直接转到给定角度，而与原角度取值无关。

* GetRotationAtomObj(self, dihedralSideStr, modifySideStr)
传入二面角种类字符串与调整端侧字符串（见上），返回一个原子对象list。此方法会根据
主链二面角的种类与调整端侧的组合情况，取出一条链上所有以给定组合进行调整时，需要
进行坐标旋转的原子对象，从而配合上述两个方法得到的旋转矩阵进行坐标修改。

* ModifyBBDihedralAngleByDeltaAngle(self, dihedralSideStr, modifySideStr, rotationAngle)
参数同CalcBBRotationMatrixByDeltaAngle。调用此接口后，与参数给出的主链二面角种类
以及转动侧相关的全部需要转动的原子都会直接进行转动。转动角度参数表示在当前二面角
基础上进行转动的角度。

* ModifyBBDihedralAngle(self, dihedralSideStr, modifySideStr, targetAngle)
参数同CalcBBRotationMatrix。调用此接口后，与参数给出的主链二面角种类以及转动侧相
关的全部需要转动的原子都会直接进行转动。转动角度参数表示转动后的目标二面角角度。


结构的编辑
----------
四个层级的对象新建均可通过对应层级的类：C_ProteinStruct, C_ChainStruct, C_ResidueStruct,
C_AtomStruct实例化得到。四个类在实例化时的所有参数均可选，类原型分别为：

PDBTools.C_ProteinStruct(proteinID = '')
PDBTools.C_ChainStruct(chainName = '', owner = None)
PDBTools.C_ResidueStruct(residueName = '', residueNum = 0, residueInsertChar = '', owner = None)
PDBTools.C_AtomStruct(atomName = '', atomNum = 0, atomCoordArray = np.array([0., 0., 0.]), atomFollowingInfo = '', owner = None)

除Protein层级外，其余层级的最后一个参数均可指定为一个当前层级的owner对象，如果
这样做，则当前实例化得到的新对象将自动与其owner产生关联（当前对象加入owner对象
的子结构列表，当前对象的owner属性被设置为参数给定的owner），如果owner为None，
则不会进行与owner有关的操作。

除Atom层级外，每一个层级均可通过Append方法，对当前层级对象追加一个或多个子层级对
象。此方法的参数被声明为不定长形参，可传入一至多个子层级对象进行追加。追加对象的
同时，两个层级之间将自动产生层级上下关联。在此操作中，所有被追加的子层级对象都会
被自动调用Copy方法，从而追加一个原对象的拷贝，不会影响到原对象自身的位置与从属关
系。例：

structObj.Append(*structObj[:])       # 对Protein对象追加此Protein对象的所有链对象（需要实参解包）
structObj[0].Append(structObj[0][0])  # 对一个链对象追加一个残基对象

除Atom层级外，每一个层级可通过调用Insert方法，对当前对象进行子层级的插入。其参数
由索引值（对应于当前层级的子结构列表），与一至多个子层级对象组成（同样被声明为不
定长形参）。与追加过程类似，在此操作中，所有被插入的子层级对象都会被自动调用Copy
方法，从而插入一个原对象的拷贝，不会影响到原对象自身的位置与从属关系。例：

structObj.Insert(3, *structObj[:])       # 在子结构列表的索引值为3的位置插入所有的链对象（需要实参解包）
structObj[0].Insert(3, structObj[0][0])  # 在子结构列表的索引值为3的位置插入一个残基对象

所有层级对象均可调用Copy方法，返回一个当前对象的复制（深拷贝）。返回的对象只会
保留从当前层级往下的所有从属关系，其自身的owner为None。例：

structObj.Copy()           # 生成一个Protein对象的深拷贝
structObj[0][0][0].Copy()  # 生成一个Atom对象的深拷贝

除Protein层级外，其余层级对象可调用Remove方法删除其本身。本质上是删除了当前对象
在其owner的子结构列表中的记录，故无从属关系的对象不能进行这样的操作。例：

structObj[0].Remove()  # 删除这条链自身


层级对象的筛选
--------------
层级对象的筛选有多种方式。由于除了Atom层以外的其他层级均实现了迭代器，故推荐使用
filter函数对层级进行筛选：

filter(lambda x: x.name == 'ALA', structObj[0])  # 筛选出一条链中所有的ALA

除上述通用方法外，除了Atom层级以外的其他层级可调用FilterAtoms方法，此方法以至少
一个的原子名作为不定长参数，进行基于原子名的原子对象筛选。此方法常用于筛选出某层
级中所有的CA原子或所有的骨架原子(N, CA, C)。此方法返回筛选后的原子对象list。此外，
IFilterAtoms方法为上述方法的迭代器版本，将返回一个原子对象生成器，FilterAtomsCoord
方法将直接返回筛选后原子的ndarray坐标矩阵。上述三个方法的原子名默认值均为'CA'：

structObj.FilterAtoms('CA')             # 筛选并返回蛋白质中所有的CA原子列表
structObj.IFilterAtoms('N', 'CA', 'C')  # 筛选并返回蛋白质中所有的骨架原子迭代器
structObj.FilterAtomsCoord()            # 筛选并返回蛋白质中所有的CA原子坐标矩阵


MathUtil线性代数模块
--------------------
MathUtil中实现了一些基于numpy的线性代数运算API，可传入原子坐标进行计算。各API
的函数原型及功能如下：

* Dis(coordA, coordB)
三维坐标专用的高性能函数。用于计算两个三维坐标之间的距离，可用于替代numpy.linalg.norm函数。

* Norm(coordArray)
三维坐标专用的高性能函数。用于计算一个三维坐标的二范数，可用于替代numpy.linalg.norm函数。

* PDBTools.CalcVectorAngle(coordA, coordB)
传入两个ndarray形式的向量，用于计算两向量夹角，返回弧度制角度（0 ~ pi）。

* PDBTools.CalcRotationMatrix(rotationAxis, rotationAngle)
传入任意的（无需缩放至单位长度）旋转轴向量，与弧度制角度，用于计算右乘旋转矩阵。

* PDBTools.CalcRotationMatrixByTwoVector(coordA, coordB)
传入两个向量坐标，返回从向量A旋转至向量B所需要的右乘旋转矩阵。

* PDBTools.CalcDihedralAngle(coordA, coordB, coordC, coordD)
传入四个点的ndarray形式坐标，用于计算由这四个点构成的二面角，返回有符号弧度制角度（-pi ~ pi）

* PDBTools.CalcSuperimposeRotationMatrix(sourceCoordArray, targetCoordArray)
传入两个等长的（由相同数量的点的坐标得到的）二维坐标ndarray矩阵，用于计算从sourceCoordArray
到targetCoordArray的叠合旋转矩阵。函数返回平移向量A、旋转矩阵B与平移向量C，从而
使得sourceCoordArray通过(sourceCoordArray - A).dot(B) + C计算后，与targetCoordArray
之间的RMSD取到最小值，形成叠合。


其他
----
* Load函数的解析顺序
Load函数将完全按照PDB文件中ATOM行的出现顺序，对PDB文件进行解析与存储。不会进行
任何排序过程。此外，解析时将忽略所有非ATOM关键字行，包括TER等。

* 对于创建新层级对象的判定
Protein：只会在解析开始前创建唯一的一个，并最终返回这个对象。
Chain：在解析开始时，以及每次检测到链名发生变化时（从上一个ATOM行到当前行），都
会创建新的链对象。
Residue：在解析开始时，以及每次检测到残基名、残基编号或残基插入字符三者之一发生
变化时（从上一个ATOM行到当前行），都会创建新的残基对象。
Atom：每检测到一个新的ATOM行都会创建一个Atom对象

* 空字段
由于解析时会对所有字符串字段（包括链名、残基名、残基插入字符、原子名）进行strip
方法处理，故所有的空字段，如空链名，空插入字符等，都会被解析为空字符串。此性质在
筛选及属性修改时可能有用。

* 布尔值
任何结构对象的布尔值都为True。

* __slots__
出于性能的考虑，四个结构类都定义了__slots__，故不可以随意添加限定以外的属性。

* 序列化与进程池
所有层级对象均支持2号及以上序列化协议进行序列化。故其可作为进程池函数的参数进行
传递，且由于multiprocessing模块的特性，默认情况下传入各进程池函数的结构对象是彼
此独立的，不会出现由于内存共享带来的问题。

* 三字符、一字符氨基酸名的相互转换
StructConst中定义了两个哈希表常量，其键值对相反。分别对应于20种α-氨基酸的三字符
与一字符名称，可用于两种名称之间的相互转换。这两个全局变量可通过PDBTools.RES_NAME_THREE_TO_ONE_DICT
与PDBTools.RES_NAME_ONE_TO_THREE_DICT访问到。

* MODEL关键词
解析时不会关注含有多个MODEL的PDB。除ATOM以外的任何关键词都将被忽略。

* 未定义行为
本文档中未提及的，以及明显不符合层级结构的操作，如给残基追加链对象，迭代原子对象
等，其行为都是未定义的。可能会引发错误或其他未知问题。出于性能的考虑，代码中未对
调用时的各种不合理行为做全面的类型检查与行为检查。
