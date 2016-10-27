# How to use

## Python Version

* 2.x

## Python Dependencies

* Numpy

## Options

* -i setting the input file
* -o (output option:)median,common
* -c (compat_files:)a.txt,b.txt
* -s (step=)expression
* -t (change type = )log2
* -n (info_columns=)a,b -g ./../data/0401/gene_setdbfile.csv
* -r change(add)  -i ../data/0401/gene_setdbfile.csv(../result/0401/result_expression_data.txt) (-b x)
* -k setdb(expression) -i ../result/0401/result_geneid_result_gene_set_database.txt
* -i ..file.. -y ..file.. sync -i file same gene name base -y file on geneid

## Examples
```shell
1../app.py -i ../data/0401/TWS_1.txt -o median
2../app.py -i ../data/0401/TWS_1.txt -o common
> 3../app.py -i ../data/0401/result_common_TWS_1.txt -c ./../data/0401/result_median_TWS_1.txt,./../data/0401/result_median_TWS_2.txt,./../data/0401/result_median_TWS_3.txt
> 4../app.py -i ../result/0401/result_single_normalize.txt -s expression -t log2
> 5../app.py -i ../result/0401/result_expression_data.txt -n a(,b) -g ../result/0401/result_gene_set_database.gmx
> 	* ./app.py -i ../result/0401/result_expression_data.txt -n GeneName -g ../result/0401/result_gene_set_database.txt
>	* ./app.py -i ../result/0401/result_geneid_result_expression_data.txt -n GeneID -g ../result/0401/result_geneid_result_gene_set_database.txt
> 6../app.py -i ../data/0401/gene_setdbfile.csv(../result/0401/result_expression_data.txt)  -r change(add)  (-b:combine geneid/files)
> 7../app.py -i ../result/0401/result_geneid_result_gene_set_database.txt -k setdb(expression) :check repeat geneid
> 8../app.py -i ../result/0401/result_unique_result_geneid_result_expression_data.txt -y ../result/0401/result_unique_result_geneid_result_gene_set_database.txt
> 9.note:>./app.py -i ../result/0401/result_geneid_result_gene_set_database.txt -k setdb     >./app.py -i ../result/0401/result_geneid_result_expression_data.txt -y ../result/0401/result_unique_result_geneid_result_gene_set_database.txt >./app.py -i ../result/0401/result_syn_result_geneid_result_expression_data.txt -n GeneName -g ../result/0401/result_unique_result_geneid_result_gene_set_database.txt
```
