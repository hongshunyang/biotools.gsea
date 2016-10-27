我们分步来，你先完成下面的步骤，对6个样本做normalization，

1。对每一个文件（TWS_1.txt，TWS_2.txt....），计算出gProcessedSignal这个列的median。注意里面有一些行测的的数据是用于芯片的检验，而不是真正的基因表达。这些行的特点是Description这个列为空。以我上次的数据为例，62,976行里面，只有58,717是基因表达。其余的行可以删除，不可以用于计算median。

2。对于剩下的行（我上次是58,717），保留gProcessedSignal和glsPosandSignif这两个列。gProcessedSignal的数值需要处理一下，用实际测的的数值除以这个文件的median。例如，TWS_1.txt这个文件里面，gProcessedSignal的mean为6.861519。对于A_23_P117082这个prob，原始的信号为435.829900。那么normalize之后的信号就是63.5179907。

3。创建一个新的文件，含有如下的列（这些列在所有文件中应该是一致的）和Description不为空的行。
FeatureNum	ProbeName	GeneName	SystematicName	Description

4。把各个文件中经过normalize之后的gProcessedSignal和glsPosandSignif加入新的文件中。我们一个有6个样本（文件），这样应该加入12行。

5。最后所得的文件应该和data/Single-experiment normalized data/K1297_A4021_intensity_norm.txt类似。

这个文件里面含有初步处理过的6个样本的全基因组表达数据。我们会从这里出发，研究有特异性表达的通路。

下一步是根据这个文件，和之前发给你的其他文件，生成GSEA所需要的三个文件。详细说明见下面的链接和我的简述。

http://www.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats#GMX:_Gene_MatriX_file_format_.28.2A.gmx.29

文件1：根据你生成的这个文件，生成”Expression Data”，用TXT格式比较方便。生成这个文件的时候，记得使用log2来对表达进行变换。原因是表达的测量单位是”fold-change”，一般不符合正态分布。经过变换后会好一些。这里你要把代码写得灵活一些，我们以后可以会使用别的变换，或者是删除一些probe。

文件2：”Phenotype Data”。三个TWS样本是经过treat之后的细胞，一般设定为case，而“untreated”设定为control。用CLS格式

文件3：“Gene Set Database”。用你之前收到的Gene.xls文件生成这个文件。用GMX格式比较方便。这个文件里面有自己定义的gene set。我们之后会用gsea来看哪些gene set里面的基因有差异性表达。

gene name -> gene id

Gene Name:GAB2
Organism: HOMO

(GAB2[Gene Name]) AND HOMO[Organism]

http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=(GAB2[Gene%20Name])%20AND%20HOMO[Organism]

http://biopython.org/DIST/docs/api/Bio.Entrez-module.html

<eSearchResult>
<Count>1</Count>
<RetMax>1</RetMax>
<RetStart>0</RetStart>
<IdList>
	<Id>9846</Id>
</IdList>
<TranslationSet>
<Translation>
<From>HOMO[Organism]</From>
<To>"Homo"[Organism]</To>
</Translation>
</TranslationSet>
<TranslationStack>
<TermSet>
<Term>GAB2[Gene Name]</Term>
<Field>Gene Name</Field>
<Count>85</Count>
<Explode>N</Explode>
</TermSet>
<TermSet>
<Term>"Homo"[Organism]</Term>
<Field>Organism</Field>
<Count>201334</Count>
<Explode>Y</Explode>
</TermSet>
<OP>AND</OP>
</TranslationStack>
<QueryTranslation>GAB2[Gene Name] AND "Homo"[Organism]</QueryTranslation>
</eSearchResult>