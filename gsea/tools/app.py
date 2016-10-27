#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (C) yanghongshun@gmail.com

import operator
import csv
import types
import os
import sys
import itertools
import getopt
import ConfigParser
import time

from numpy import *



def readCsvDataFromFile(startLine,spliter,csvPath):
	
	data = []
	
	print "reading file: " + csvPath 
	
	if not os.path.isfile(csvPath):
		print "file not exist!"
		sys.exit()
		
	csvfile=csv.reader(open(csvPath, 'r'),delimiter=spliter)
	
	print "storing data"
	
	for line in csvfile:
			data.append(line)
	
	if startLine != '':
		for i in range(startLine):
			#print i
			del data[0]

	return data

def saveCsvDataToFile(title,data,file_path,fmt=''):
	
	print "saving data to file :"+ file_path
	
	if os.path.isfile(file_path):
		os.remove(file_path)
	
	file_handle = open(file_path,'wb')
	if fmt=='':
		csv_writer = csv.writer(file_handle)##delimiter=' ',
	else:
		csv_writer = csv.writer(file_handle,fmt)##delimiter=' ',
	if len(title) >0 :
		csv_writer.writerow(title)
	csv_writer.writerows(data)
	
	file_handle.close()
	
	print "saved ok"

def getObjData(columns,refcolumn,startline,spliter,file_path):
	data=readCsvDataFromFile(startline,spliter,file_path)
	
	cols = [] 
	refcol = 0
	for i in range(len(data[0])):
		if (len(cols)==len(columns)) and (refcol !=0):
			break
		for j in range(len(columns)):
			if cmp(data[0][i],columns[j])==0:
				cols.append(i)
		
		if cmp(data[0][i],refcolumn)==0:
			refcol = i	

	if len(cols)==0:
		print 'please tell me which column you need'
		sys.exit(0)
	if refcol==0:
		print 'please tell me which reference column '
		sys.exit(0)
	
	del data[0]
	objData = []
	objData.append(columns)
	for i in range(len(data)):
		objDataLine = []
		if data[i][refcol] !='':###refcol   '','Unknown'
			for j in range(len(cols)):#cols[j]
				objDataLine.append(data[i][cols[j]])
			
			objData.append(objDataLine)
		
	return objData
		
def computerMedian(column,refcolumn,startline,spliter,file_path):
	data=readCsvDataFromFile(startline,spliter,file_path)
	#column is field name ,col is field index
	col = 0
	refcol = 0
	for i in range(len(data[0])):
		if (col!=0) and (refcol !=0):
			break
		if cmp(data[0][i],column)==0:
			col = i
		elif cmp(data[0][i],refcolumn)==0:
			refcol = i
	#print col
	#print refcol
	if col==0:
		print 'computerMedian:can not find column'
		sys.exit(0)
	if refcol==0:
		print 'computerMedian:can not find refcolumn'
		sys.exit(0)
	
	#print '--column title--'
	print data[0]
	del data[0]	#delete title column
	objMedian = 0
	#objData = []
	objDataColumn = []
	objCount = 0
	#print data[0]
	print '--'+column+'--'
	print col
	print '--'+refcolumn+'--'
	print refcol
	for i in range(len(data)):
		#print  data[i][refcol]	##float
		if data[i][refcol] !='':###refcol   '','Unknown'
			#objData.append(data[i])
			objDataColumn.append(float(data[i][col]))
			objCount +=1
			
	print '--All Line Count(not include column name)--'
	print  len(data)
	print '--Valid Line Count(not include column name)--'
	print objCount
	objDataColumnArray = array(objDataColumn)
	objMedian = median(objDataColumnArray)
	
	print '--Median--'
	print objMedian
	
	return objMedian
	

def normalizeColumn(objColumn,objColumns,objData,objColumn_Median):
	objColumnIndex = -1
	for i in range(len(objColumns)):
		if cmp(objColumns[i],objColumn)==0:
			objColumnIndex = i
	if objColumnIndex ==-1:
		print '--can not find objColumn in objColumns --'
		sys.exit(0)
	
	objDataNormalize = []
	del objData[0]
	objDataNormalize.append(objColumns)
	for i in range(len(objData)):
		objDataNormalizeLine = []
		for j in range(len(objColumns)):
			if j==objColumnIndex:
				objDataNormalizeLine.append(float(objData[i][j])/objColumn_Median)
			else:
				objDataNormalizeLine.append(objData[i][j])
		
		objDataNormalize.append(objDataNormalizeLine)	

	return objDataNormalize

def compatData(input_file_path,compat_files_list,objConnectColumn):
	
	objCompatBaseData=readCsvDataFromFile(0,',',input_file_path)
	
	objCompatListData =[]
	if len(compat_files_list)==0:
		print '--compat files is null--'
		sys.exit(0)
	else :
		#print compat_files_list
		for i in range(len(compat_files_list)):
			#print compat_files_list[i]
			objCompatListData.append(readCsvDataFromFile(0,',',compat_files_list[i]))
			#print objCompatListData[i][0]
			if len(objCompatBaseData) != len(objCompatListData[i]):
				print '--row not be equal--'
				sys.exit(0)
	

	objCompatData = []	
	
	for i in range(len(objCompatBaseData)):
		objCompatDataLine = []
		objCompatDataLine.extend(objCompatBaseData[i])
		for j in range(len(objCompatListData)):#j/6
			objCompatDataLine.extend(objCompatListData[j][i])
		objCompatData.append(objCompatDataLine)	
	
	##check probename
	#for i in range(len(objCompatData)):
		#print objCompatData[i]
	print '--check ProbeName--'
	print objCompatData[1]
	
	objCompatFileList = []
	for i in range(len(compat_files_list)):
		objCompatFileList.append(os.path.basename(compat_files_list[i]))
		
	print '--get compat file list--'
	print objCompatFileList
	objConnectColumnIndex = []
	for i in range(len(objCompatData[0])):
		if cmp(objCompatData[0][i],objConnectColumn)==0:
			objConnectColumnIndex.append(i)
		else :
			objConnectColumnIndex.append(0)
	
	print '--print ProbeName column index--'		
	print objConnectColumnIndex
	#need first objConnectColumn
	#del objConnectColumnIndex[0]
	#print objConnectColumnIndex
	##title
	##	
	j=0
	for i in range(len(objCompatData[0])):
		if (objConnectColumnIndex[i]!=0) and (objConnectColumnIndex[i]!=1):##first 	objConnectColumn = 'ProbeName' show not delete
			objCompatData[0][objConnectColumnIndex[i]+1]=objCompatFileList[j]
			j+=1
	
	print '--change compat file name--'
	print 	objCompatData[0]
	print 	objCompatData[1]
	
	#delete 	objConnectColumn
	objCompatResultData = []
	for i in range(len(objCompatData)):
		objCompatResultDataLine = []
		for j in range(len(objConnectColumnIndex)):
			if (objConnectColumnIndex[j]==0) or (objConnectColumnIndex[j]==1):
				objCompatResultDataLine.append(objCompatData[i][j])
		
		objCompatResultData.append(objCompatResultDataLine)
	print '--check result compat data--'
	print objCompatResultData[0]
	print objCompatResultData[1]

	return objCompatResultData

def expressionData(input_file_path,changeColumns,changeType):
	
	normalizeData=readCsvDataFromFile(0,',',input_file_path)

	changeColumnsIndex = []
	normalizeDataColumnTitle = normalizeData[0]
	for i in range(len(normalizeDataColumnTitle)):
		for j in range(len(changeColumns)):
			if cmp(normalizeDataColumnTitle[i],changeColumns[j])==0:
				changeColumnsIndex.append(i)
	
	if len(changeColumnsIndex) == 0:
		print '--can not find changeColumn--'
		sys.exit(0)
	
	del normalizeData[0]
	
	changedData = []
	changedData.append(normalizeDataColumnTitle)
	for i in range(len(normalizeData)):
		#if i ==0 :
			#print normalizeData[i]
		changedDataLine=[]
		for j in range(len(normalizeDataColumnTitle)):
			if j in changeColumnsIndex:
				if cmp(changeType,'log2')==0:
					#print normalizeData[i][j]
					changeValue = array([float(normalizeData[i][j])])
					#print changeValue
					changedValue = log2(changeValue)
					changedDataLine.append(repr(changedValue[0]))###repr  not str
					#print changedValue
			else :
				changedDataLine.append(normalizeData[i][j])
		#if i ==0 :
			#print changedDataLine
		changedData.append(changedDataLine)	
				
	#print changedData[0]
	#print changedData[1]
	#print changedData[2]
	
	return 	changedData

def getInfoByColumns(input_file_path,infoColumns,info_type="name"):
	info_Data=readCsvDataFromFile(0,',',input_file_path)
	info_columns = infoColumns.split(',')
	
	if len(info_columns)==0:
		print '--please tell me which columns you want  --'
		sys.exit(0)
	info_result =[]
	if cmp(info_type,'name')==0:##means has title
		name_column = info_Data[0]
		for i in range(len(info_columns)):
			info_columns_res = []
			#print '-'*100
			try:
				info_columns_index=name_column.index(info_columns[i])
			except:
				print 'some column not be found in the columns'
				sys.exit(0)
			
			info_columns_data = []
			for r in range(len(info_Data)):
				info_columns_data.append(info_Data[r][info_columns_index])
			
			print '-'*20+info_columns[i]+'-'*20
			print 'total:'+str(len(info_columns_data))
			info_columns_res.append(info_columns_data)
			unique_info_columns_data = {}.fromkeys(info_columns_data).keys()
			print 'unique total:'+str(len(unique_info_columns_data))
			info_columns_res.append(unique_info_columns_data)
		info_result.append(info_columns_res)
	
	##[0] means columns [0][0]:means total [0][1]:means unique total
	return info_result					


def setGeneSetDB(input_file_path):
	geneDb=readCsvDataFromFile(0,',',input_file_path)
	geneSetDB = []
	geneSetDBNotNull =[]
	geneSetDBUnique = []
	for i in range(len(geneDb)):
		if i>1:#1 starts gene name
			geneSetDB.extend(geneDb[i])
	
	#print	geneSetDB
	geneSetDBNotNull = [gene for gene in geneSetDB if gene !='' and gene !='[]' ]  ##'',[] filter
	geneSetDBUnique = {}.fromkeys(geneSetDBNotNull).keys()

	#print len(geneSetDB)
	#print len(geneSetDBNotNull)
	print "Gene SET DB total:"+str(len(geneSetDBNotNull))
	print "Gene SET DB Unique total:"+str(len(geneSetDBUnique))
	
	return geneSetDBUnique 


def saveDataRowAtColumnsByInDatas(input_file_path,atColumns,inDatas,info_type="name"):
	info_Data=readCsvDataFromFile(0,',',input_file_path)
	at_Columns=atColumns.split(',')
	if len(at_Columns)!=len(inDatas):
		print 'atColumn=a,b inDatas=[[column include a],[column include b]] '
		sys.exit(0)
	
	saveData=[]
	
	if cmp(info_type,'name')==0:##means has title
		name_column = info_Data[0]
		at_Columns_index = []
		for i in range(len(at_Columns)):
			try:
				at_Columns_index.append(name_column.index(at_Columns[i]))
			except:
				print 'some column not be found in the columns'
				sys.exit(0)
			
		for r in range(len(info_Data)):
			if r==0:
				saveData.append(info_Data[r])
				#print info_Data[r]
			else:
				for k in range(len(at_Columns_index)):
					try:
						inDatas[k].index(info_Data[r][at_Columns_index[k]])
					except:
						break
					
					if(k==len(at_Columns_index)-1):
						saveData.append(info_Data[r])
						#print info_Data[r]

				continue
				
			
	return saveData


def saveDataRowAtColumnsByExcludeDatas(input_file_path,atColumns,inDatas,info_type="name"):
	info_Data=readCsvDataFromFile(0,',',input_file_path)
	at_Columns=atColumns.split(',')
	if len(at_Columns)!=len(inDatas):
		print 'atColumn=a,b inDatas=[[column include a],[column include b]] '
		sys.exit(0)
	
	saveData=[]
	
	if cmp(info_type,'name')==0:##means has title
		name_column = info_Data[0]
		at_Columns_index = []
		for i in range(len(at_Columns)):
			try:
				at_Columns_index.append(name_column.index(at_Columns[i]))
			except:
				print 'some column not be found in the columns'
				sys.exit(0)
			
		for r in range(len(info_Data)):
			if r==0:
				saveData.append(info_Data[r])
				#print info_Data[r]
			else:
				for k in range(len(at_Columns_index)):
					try:
						inDatas[k].index(info_Data[r][at_Columns_index[k]])
					except:			
						if(k==len(at_Columns_index)-1):
							saveData.append(info_Data[r])
						break
						#print info_Data[r]

				continue
				
			
	return saveData
	
#def convertGeneIDFromGeneName(input_file_path,convert_type="add"):
def convertGeneIDFromGeneName(info_Data,convert_type="add",startConvert=1,find_GeneName_index=-1,name_column=[]):
	#info_Data=readCsvDataFromFile(0,',',input_file_path)
	resData=[]
	convertData=[]
	notconvertData=[]
			
	#print find_GeneName_index
		#print name_column
	if cmp(convert_type,'add')==0:
		if find_GeneName_index >=0 :
			geneID_index = find_GeneName_index+1
			convert_name_column = name_column
			convert_name_column.insert(geneID_index,'GeneID')
			for r in range(len(info_Data)):
				convert_infoData_row=[]
				currentGeneID = ''
				if r<startConvert:
					convertData.append(convert_name_column)
					notconvertData.append(convert_name_column)
				else :
					convert_infoData_row = info_Data[r]

					print info_Data[r][find_GeneName_index]
					#time.sleep(0.1)
					currentGeneID	= getGeneIDFromGeneName(info_Data[r][find_GeneName_index])	
					convert_infoData_row.insert(geneID_index,currentGeneID)
					
					if len(currentGeneID)==0:
						notconvertData.append(convert_infoData_row)
						print '>'*10
						print convert_infoData_row
					#print convert_infoData_row
					convertData.append(convert_infoData_row)
					print '-'*10 
					print convert_infoData_row
					
	elif cmp(convert_type,'change')==0:
		for w in range(len(info_Data)):
			convert_infoData_row = []
			notconvert_infoData_row=[]
			if w<startConvert:##gene name fron third line start
				convert_infoData_row=info_Data[w]
				notconvert_infoData_row=info_Data[w]
			else:
					#convert_infoData_row = info_Data[w]
					for l in range(len(info_Data[w])):
						currentGeneID=[]
						#print info_Data[w][l]
						if	info_Data[w][l] !='':
							print info_Data[w][l]
							#time.sleep(0.1)
							currentGeneID = getGeneIDFromGeneName(info_Data[w][l])
							if len(currentGeneID)==0:
								notconvert_infoData_row.append(info_Data[w][l])
							else:
								notconvert_infoData_row.append([])
						else:
							notconvert_infoData_row.append([])

						convert_infoData_row.append(currentGeneID)
						
			if len(convert_infoData_row)!=0:		
				convertData.append(convert_infoData_row)
			if len(notconvert_infoData_row)!=0:
				notconvertData.append(notconvert_infoData_row)
			#print convert_infoData_row
			#print notconvert_infoData_row
	#print name_column
	resData.append(convertData)
	resData.append(notconvertData)
	
	return resData
	
def getGeneIDFromGeneName(geneName,Organism='Homo'):
	if geneName=='':
		print '--gene name can not be null--'
		sys.exit(0)
	
	geneIDs=[]
	from Bio import Entrez
	Entrez.email = "yanghongshun@gmail.com"
	#(GAB2[Gene Name]) AND HOMO[Organism]
	term_query = geneName+'[Gene Name] AND '+Organism+'[Organism]'
	#print term_query
	handle = Entrez.esearch(db="gene", term=term_query)
	record = Entrez.read(handle)
	handle.close()
	#another try
	if len(record['IdList'])==0:	
		term_query = geneName+' AND '+Organism+'[Organism]'
		handle = Entrez.esearch(db="gene", term=term_query)
		record = Entrez.read(handle)
		handle.close()
	
	if len(record['IdList'])==0:	
		print '-'*20+geneName+'-'*20
		print '--cant be found--'
		print '--no geneID!--'
	else:
		if len(record['IdList'])==1:
				geneIDs.append(record['IdList'][0])
		elif  len(record['IdList']) >1:
			for i in range(len(record['IdList'])):		
				handle_list = Entrez.esummary(db="gene", id=record['IdList'][i])
				record_list = Entrez.read(handle_list)
				handle_list.close()
				
				if  len(record_list)>1:
					print '-'*10+geneName+':'+str(record['IdList'][i])+'-'*10
					print 'one geneID more geneName'
					for k in range(len(record_list)):
						print '-'*5+'gene Name:'+str(record_list[k]['Name'])+'-'*5
				else:	
					#print record_list[0]['Status']
					if cmp(record_list[0]['Name'],geneName)==0:
						#if record_list[0]['Status']=='0':
						if record_list[0]['ChrStart']!=999999999:##999999999 replaced
							geneIDs.append(record['IdList'][i])
			
		#record["Count"] >= 2
		if len(geneIDs)==0:
			print '-'*5+geneName+'-'*5
			print ' no  gene ID'
		elif len(geneIDs)>1:
			print '-'*5+geneName+'-'*5
			print ' more than one gene ID haha'

	return geneIDs


###main
def main(argv):
	
	DIR_RESULT = './../result/'
	#
	temp = ''
	##setting var init
	input_file_path = ''
	#
	output_option = ''
	#
	compat_files = ''
	#
	step = ''
	#
	change_type = ''
	#
	info_columns=''
	gene_db_input_file_path = ""
	convertGeneName_GeneID = ""
	convert_combine = 0
	
	#
	checkrepeat_src = ''
	
	#
	sync_genename_on_geneid=''
	try:
		opts, args = getopt.getopt(argv,"hi:o:c:s:t:n:g:p:r:b:k:y:",["input_file=","output=","compat_files=","step=",'change_type=','info_columns=','gene_db=','temp=','convert=','combine=','check=','sync='])
	except getopt.GetoptError:
		print 'please -h see help'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print '-h,see help list below '
			print '-p just for developer'
			print '	-i setting the input file'
			print '	-o (output option:)median,common'
			print '	-c (compat_files:)a.txt,b.txt'
			print '	-s (step=)expression'
			print '	-t (change type = )log2'
			print '	-n (info_columns=)a,b -g ./../data/0401/gene_setdbfile.csv '
			print '	-r change(add)  -i ../data/0401/gene_setdbfile.csv(../result/0401/result_expression_data.txt) (-b x)'
			print '	-k setdb(expression) -i ../result/0401/result_geneid_result_gene_set_database.txt'
			print '	-i ..file.. -y ..file.. sync -i file same gene name base -y file on geneid'
			print '-'*100
			print '1、	./app.py -i ../data/0401/TWS_1.txt -o median'
			print '2、	./app.py -i ../data/0401/TWS_1.txt -o common'
			print '3、	./app.py -i ../data/0401/result_common_TWS_1.txt	 -c ./../data/0401/result_median_TWS_1.txt,./../data/0401/result_median_TWS_2.txt,./../data/0401/result_median_TWS_3.txt'
			print '4、	./app.py -i ../result/0401/result_single_normalize.txt -s expression -t log2'
			print '5、 ./app.py -i ../result/0401/result_expression_data.txt -n a(,b) -g ../result/0401/result_gene_set_database.gmx'
			print '5-1、 ./app.py -i ../result/0401/result_expression_data.txt -n GeneName -g ../result/0401/result_gene_set_database.txt'
			print '5-2、 ./app.py -i ../result/0401/result_geneid_result_expression_data.txt -n GeneID -g ../result/0401/result_geneid_result_gene_set_database.txt'
			print '6、 ./app.py -i ../data/0401/gene_setdbfile.csv(../result/0401/result_expression_data.txt)  -r change(add)  (-b:combine geneid/files)'
			print '7、./app.py -i ../result/0401/result_geneid_result_gene_set_database.txt -k setdb(expression) :check repeat geneid'
			print '8、./app.py -i ../result/0401/result_unique_result_geneid_result_expression_data.txt -y ../result/0401/result_unique_result_geneid_result_gene_set_database.txt'
			print 'note:>./app.py -i ../result/0401/result_geneid_result_gene_set_database.txt -k setdb	>./app.py -i ../result/0401/result_geneid_result_expression_data.txt -y ../result/0401/result_unique_result_geneid_result_gene_set_database.txt >./app.py -i ../result/0401/result_syn_result_geneid_result_expression_data.txt -n GeneName -g ../result/0401/result_unique_result_geneid_result_gene_set_database.txt ' 
			sys.exit()
		elif opt in ("-i","--input_file"):
			input_file_path = arg
		elif opt in ("-o","--output"):
			output_option = arg
		elif opt in ("-c","--compat_files"):
			compat_files = arg
		elif opt in ("-s","--step"):
			step = arg
		elif opt in ("-t","--change_type"):
			change_type = arg
		elif opt in ("-n","--info_columns"):
			info_columns = arg
		elif opt in ("-g","--gene_db"):
			gene_db_input_file_path = arg
		elif opt in ("-p","--temp"):
			temp = arg
		elif opt in ("-r","--convert"):
			convertGeneName_GeneID = arg##add,change
		elif opt in ("-b","--combine"):
			convert_combine=1
		elif opt in ("-k","--check"):
			checkrepeat_src=arg
		elif opt in ("-y","--sync"):
			sync_genename_on_geneid=arg
	#print convert_genename_geneid
	
	if temp !='':
		geneIDs = getGeneIDFromGeneName(temp)
		print geneIDs
		sys.exit(0)
	
	if cmp(input_file_path,'')!=0:		
		input_file_basename=os.path.basename(input_file_path)
		#print input_file_basename
		input_file_dirname=os.path.split(os.path.dirname(input_file_path))
		#print input_file_dirname
		output_file_dirname = DIR_RESULT+input_file_dirname[1]
		#print	output_file_dirname
		if os.path.exists(output_file_dirname)==False:
			#mkdir dir result
			os.mkdir(output_file_dirname)
	

		if cmp(output_option,'median')==0:
		
			#tempData = []
			objRefColumn = 'Description'
			objColumn = 'gProcessedSignal'	##normalize column
			objColumn_Median = computerMedian(objColumn,objRefColumn,9,'\t',input_file_path) #include title	gProcessedSignal
			#print gProcessedSignal_Median
			objColumns=['ProbeName','gProcessedSignal','gIsPosAndSignif']
			objData = getObjData(objColumns,objRefColumn,9,'\t',input_file_path)
		
			objDataNormalize = normalizeColumn(objColumn,objColumns,objData,objColumn_Median)
	
			file_median_prefix='result_median_'
			output_file_median_path = output_file_dirname+'/'+file_median_prefix+input_file_basename
			#print output_file_path
			saveCsvDataToFile([],objDataNormalize,output_file_median_path)
			#print objDataNormalize[0]
		elif cmp(output_option,'common')==0:
			objCommonRefColumn = 'Description'
			objCommonColumns=['FeatureNum','ProbeName','GeneName', 'SystematicName', 'Description']
			objCommonData = getObjData(objCommonColumns,objCommonRefColumn,9,'\t',input_file_path)
		
			file_common_prefix='result_common_'
			output_file_common_path = output_file_dirname+'/'+file_common_prefix+input_file_basename
			saveCsvDataToFile([],objCommonData,output_file_common_path)
	
			#print objCommonData[1]
		if cmp(compat_files,'') !=0:
			compat_files_list = compat_files.split(',')
						##
			objConnectColumn = 'ProbeName'
			objCompatResultData = compatData(input_file_path,compat_files_list,objConnectColumn)
			##
			file_single_norm_name='result_single_normalize.txt'
			output_file_single_norm_path = output_file_dirname+'/'+file_single_norm_name
			saveCsvDataToFile([],objCompatResultData,output_file_single_norm_path)
		
		if cmp(step,'expression')==0:
			#print normalizeData[1]
			
			changeColumns=[
										'result_median_TWS_1.txt',
										'result_median_TWS_2.txt',
										'result_median_TWS_3.txt',
										'result_median_untreated_1.txt',
										'result_median_untreated_2.txt',
										'result_median_untreated_3.txt'
										]
			if change_type=='':
				print '--set change type (log2) for expression data on change'
				sys.exit(0)
			else:
				changeType = change_type
			
			#print changedDataColumn[0]
			changedData = expressionData(input_file_path,changeColumns,changeType)
			file_normalize_log_name='result_expression_data.txt'
			output_file_normalize_log_path = output_file_dirname+'/'+file_normalize_log_name
			saveCsvDataToFile([],changedData,output_file_normalize_log_path)
		if info_columns!='':##one column once better
			info_columns_result = getInfoByColumns(input_file_path,info_columns)
			#print len(info_columns_result[0][1])##[0] means columns [0][0]:means total [0][1]:means unique total
			
			##get geneset unique
			if gene_db_input_file_path=='':
				print 'dont find gene db file'
				sys.exit(0)
			
			geneSetDB=setGeneSetDB(gene_db_input_file_path)
				
			for i in range(len(info_columns_result)):	 
				#print len(unique_info_columns_data)
				#x=0 #0:means total \ 1:means unique total
				for x in range(2):
					info_columns_result_exist=[]
					for j in range(len(info_columns_result[i][x])):
						#[],''
						if info_columns_result[i][x][j]!='[]' and info_columns_result[i][x][j]!='':							
							try:
								geneSetDB.index(info_columns_result[i][x][j])
								info_columns_result_exist.append(info_columns_result[i][x][j])
							except:
								continue
						
					info_columns_result[i].append(info_columns_result_exist)
			
			#info_columns_result[0][0] 就是info_columns.split(',')所得列表中第一个元素所在列得元素得集合（包含重复）
			#info_columns_result[0][1] 就是info_columns.split(',')所得列表中第一个元素所在列得元素得集合（不包含重复）			
			#info_columns_result[0][2] 就是info_columns_result[0][0]中的gene在genesetdb中出现的元素集合
			#info_columns_result[0][3] 就是info_columns_result[0][1]中的gene在genesetdb中出现的元素集合

			print 'OBJ gene Exist in Gene SET DB:'+str( len(info_columns_result[0][2]))
			#print len({}.fromkeys(info_columns_result[0][2]).keys()) check
			print 'OBJ gene Unique Exist in Gene SET DB:'+str( len(info_columns_result[0][3]) )
			
			inExistDatas=[]
			inExistDatas.append(info_columns_result[0][3])
			
			findSaveData = saveDataRowAtColumnsByInDatas(input_file_path,info_columns,inExistDatas)
			
			##
			file_prefix = 'result_by_'+info_columns+'_'
			##
			file_findgene_name=file_prefix+'result_find_gene.txt'
			output_file_findgene_path = output_file_dirname+'/'+file_findgene_name
			saveCsvDataToFile([],findSaveData,output_file_findgene_path)

			notfindSaveData=saveDataRowAtColumnsByExcludeDatas(input_file_path,info_columns,inExistDatas)

			file_notfindgene_name=file_prefix+'result_notfind_gene.txt'
			output_file_notfindgene_path = output_file_dirname+'/'+file_notfindgene_name
			saveCsvDataToFile([],notfindSaveData,output_file_notfindgene_path)
				
			#print info_columns_result[0][2]
			#convert gene name to gene id
			#for g in range(len(info_columns_result[0][1])):
				#geneIDs = getGeneIDFromGeneName(info_columns_result[0][1][g])
				#print info_columns_result[0][1][g],geneIDs
				
		##convert gene name to gene id
		if cmp(convertGeneName_GeneID,'')!=0:
			geneid_tempdir = output_file_dirname+'/geneid'
			if os.path.exists(geneid_tempdir)==False:
				os.mkdir(geneid_tempdir)
			
			iData=readCsvDataFromFile(0,',',input_file_path)
			find_GeneName_index = -1
			name_column=iData[0]

			#没次计算n个，并保存n_***
			if cmp(convertGeneName_GeneID,'add')==0:
				n=500##compute per cycle
			elif cmp(convertGeneName_GeneID,'change') ==0:
				n=100

			i=0
			meanIData=[iData[i:i+n] for i in range(0,len(iData),n)]
			i=0	
			for i in range(len(meanIData)):	
				
				file_notconvert_geneid_prefix=str(i)+'_'+'result_notfindgeneid_'
				output_file_notconvert_path = geneid_tempdir+'/'+file_notconvert_geneid_prefix+input_file_basename
				
				file_convert_geneid_prefix=str(i)+'_'+'result_geneid_'
				output_file_convert_path = geneid_tempdir+'/'+file_convert_geneid_prefix+input_file_basename
				#debug
				#if convert_combine==0:
				if (os.path.isfile(output_file_convert_path) and os.path.isfile(output_file_notconvert_path))==False:
				#debug
					if convert_combine==1:##-b
						print 'dont compute end of the file to find geneid'
						print 'please dont use -b option to get all geneid about this file'
						sys.exit(0)
					rData=[[],[]]
					if cmp(convertGeneName_GeneID,'add')==0:
						#print convertGeneName_GeneID,input_file_path
						#0 not convert,1start convert
						
						if find_GeneName_index==-1:
							convert_base_column = 'GeneName'
							try:
								find_GeneName_index = name_column.index(convert_base_column)
							except:
								print 'some column not be found in the columns'
								sys.exit(0)	
								
						if i==0:
							currentStartConvert=1
						else:
							currentStartConvert=0
						
						rData=convertGeneIDFromGeneName(meanIData[i],'add',currentStartConvert,find_GeneName_index,name_column)				
					
					elif cmp(convertGeneName_GeneID,'change') ==0:
						#print convertGeneName_GeneID,1
						#0,1 not convert，2start convert
						if i==0:
							currentStartConvert=2
						else:
							currentStartConvert=0
						
						rData=convertGeneIDFromGeneName(meanIData[i],'change',currentStartConvert)	
					
					saveCsvDataToFile([],rData[0],output_file_convert_path)
					saveCsvDataToFile([],rData[1],output_file_notconvert_path)
			if convert_combine==1:
				i=0
				bData=[]
				nbData=[]
				for i in range(len(meanIData)):	
				
					file_notconvert_geneid_prefix=str(i)+'_'+'result_notfindgeneid_'
					output_file_notconvert_path = geneid_tempdir+'/'+file_notconvert_geneid_prefix+input_file_basename
					
					file_convert_geneid_prefix=str(i)+'_'+'result_geneid_'
					output_file_convert_path = geneid_tempdir+'/'+file_convert_geneid_prefix+input_file_basename
					if (os.path.isfile(output_file_convert_path) and os.path.isfile(output_file_notconvert_path))==True:

						ncData=readCsvDataFromFile(0,',',output_file_notconvert_path)
						if cmp(convertGeneName_GeneID,'add')==0:
							titleHas=1
						elif cmp(convertGeneName_GeneID,'change') ==0:
							titleHas =2
							
						if i==0:
							nbData.extend(ncData[0:titleHas])
							del ncData[0:titleHas]
						if len(ncData)>0:
							nbData.extend(ncData)
						
						cData=readCsvDataFromFile(0,',',output_file_convert_path)
						if i==0:
							bData.extend(cData[0:titleHas])
							del cData[0:titleHas]
						if len(cData)>0:
							bData.extend(cData)
				
					
				#print bData
				file_nb_geneid_prefix='result_notfindgeneid_'
				output_file_nb_path = output_file_dirname+'/'+file_nb_geneid_prefix+input_file_basename
					
				file_b_geneid_prefix='result_geneid_'
				output_file_b_path = output_file_dirname+'/'+file_b_geneid_prefix+input_file_basename
				
				saveCsvDataToFile([],bData,output_file_b_path)
				saveCsvDataToFile([],nbData,output_file_nb_path)
			
		if len(checkrepeat_src)!=0:
			file_prefix="result_geneid_"
			genename_input_file_path = output_file_dirname+'/'+input_file_basename[len(file_prefix):]
			if	os.path.exists(genename_input_file_path)==False:
				print 'cant find :'+genename_input_file_path
				sys.exit(0)
			
			ckGeneID_file=readCsvDataFromFile(0,',',input_file_path)
			ckGeneName_file=readCsvDataFromFile(0,',',genename_input_file_path)
			from collections import defaultdict

			if cmp(checkrepeat_src,'setdb')==0:
				ckGeneName_data= ckGeneName_file[2:]		
				ckGeneID_data= ckGeneID_file[2:]		
				#print len(ckGeneID_data)
				T_ckGeneID_data=map(list,zip(*ckGeneID_data))
				#print len(T_ckGeneID_data[0])
				
				print 'check and adjust one gene name one gene id'
				
				for rows in range(len(T_ckGeneID_data)):#rows means columns
					#print '*'*100
					d={}
					s=T_ckGeneID_data[rows]
					d = defaultdict(list)
					for k,va in [(v,i) for i,v in enumerate(s)]:
					    d[k].append(va)
					
					for j in range(len(d.items())):
						ld=[]
						geneids=[]
						ld=list(d.items()[j])
						if cmp(ld[0],'[]')!=0:
							geneids=eval(ld[0])
							###发现同一个gene name 多个gene id，此时处理方式就是只取第一个gene id（很多时候都是对的）
							if len(geneids)>1:
								#print ld[0]+',rows:'+str(ld[1])+',cols:'+str(rows)
								for r in range(len(ld[1])):
									ckGeneID_data[ld[1][r]][rows]="['"+str(geneids[0])+"']"
				##到这里，gene name 只对应一个gene id
				
				#查找全文中是否有重复的geneid
				print 'find same geneid base file'
				F_ckGeneID_data=[]
				F_ckGeneName_data=[]
				F_row_cols=len(ckGeneID_data[0])
				for p in range(len(ckGeneID_data)):
					F_ckGeneID_data.extend(ckGeneID_data[p])
					F_ckGeneName_data.extend(ckGeneName_data[p])
				#sys.exit(0)
				d4={}
				s4=F_ckGeneID_data
				d4 = defaultdict(list)
				for k4,va4 in [(v4,i4) for i4,v4 in enumerate(s4)]:
					d4[k4].append(va4)
				#print d4.items()	
				for j4 in range(len(d4.items())):
					ld4=[]
					ld4=list(d4.items()[j4])
					if cmp(ld4[0],'[]')!=0:
						#print ld4
						if len(ld4[1])>1:
							genename_list_org = []
							geneid_list_org = []
							genename_list_uniq =[]
							for r4 in range(len(ld4[1])):
								#print F_ckGeneName_data[ld4[1][r4]]+'	,index:'+str(ld4[1][r4])
								genename_list_org.append(F_ckGeneName_data[ld4[1][r4]])
								geneid_list_org.append(F_ckGeneID_data[ld4[1][r4]])
							genename_list_uniq = {}.fromkeys(genename_list_org).keys()	
							if len(genename_list_uniq)>1:
								#print	 genename_list_org
								#print geneid_list_org
								#print ld4
								for q in range(len(ld4[1])):
									#print ld4[1][q]/F_row_cols,ld4[1][q]%F_row_cols
									ckGeneName_data[ld4[1][q]/F_row_cols][ld4[1][q]%F_row_cols]=genename_list_org[0]
					
				ckGeneName_data.insert(0,ckGeneName_file[0])
				ckGeneName_data.insert(1,ckGeneName_file[1])
			##下面可以不用执行	
			elif cmp(checkrepeat_src,'expression')==0:
				T_ckGeneID_data= ckGeneID_file[1:]	
				ckGeneID_data=[]
				for i in range(len(T_ckGeneID_data)):
					ckGeneID_data.append(T_ckGeneID_data[i][3])
				d5={}
				s5=ckGeneID_data
				d5 = defaultdict(list)
				for k5,va5 in [(v5,i5) for i5,v5 in enumerate(s5)]:
					d5[k5].append(va5)
				#print d5.items()	
				for j5 in range(len(d5.items())):
					ld5=[]
					ld5=list(d5.items()[j5])
					if cmp(ld5[0],'[]')!=0:
						#print len(ld5[1])				
						if len(ld5[1])>1:
							genename_list_org = []
							geneid_list_org = []
							genename_list_uniq =[]
							for r5 in range(len(ld5[1])):
								#print T_ckGeneID_data[ld5[1][r5]][2]
								#print T_ckGeneID_data[ld5[1][r5]][2],T_ckGeneID_data[ld5[1][r5]][3]
								genename_list_org.append(T_ckGeneID_data[ld5[1][r5]][2])
								geneid_list_org.append(T_ckGeneID_data[ld5[1][r5]][3])
							genename_list_uniq = {}.fromkeys(genename_list_org).keys()
							#print genename_list_uniq	
							if len(genename_list_uniq)>1:
								#print	 genename_list_org
								#print geneid_list_org
								#print ld5
								print '*'*10
								print ld5
								for q in range(len(ld5[1])):
									print T_ckGeneID_data[ld5[1][q]][2]
									T_ckGeneID_data[ld5[1][q]][2] = genename_list_org[0]
									#print T_ckGeneID_data[ld5[1][q]][2]
				
				ckGeneName_data=[]	
				ckGeneName_data=T_ckGeneID_data
				ckGeneName_data.insert(0,ckGeneID_file[0])

			file_u_genename_prefix='result_unique_'
			output_file_unique_path = output_file_dirname+'/'+file_u_genename_prefix+input_file_basename			
			saveCsvDataToFile([],ckGeneName_data,output_file_unique_path)
		if cmp(sync_genename_on_geneid,'')!=0:
			if os.path.exists(input_file_path)==False:
				print 'cant find the file:'+input_file_path
				sys.exit(0)
			unique_expression_geneid_file = input_file_path
			#print unique_expression_geneid_file
			if os.path.exists(sync_genename_on_geneid)==False:
				print 'cant find the file:'+sync_genename_on_geneid
				sys.exit(0)
			unique_gene_setdb_geneid_file = sync_genename_on_geneid
			
			sycGeneExpression_file=readCsvDataFromFile(0,',',unique_expression_geneid_file)
			sycGeneExpression_Data = sycGeneExpression_file[1:]
			sycGeneNameSetDB_file=readCsvDataFromFile(0,',',unique_gene_setdb_geneid_file)
			sycGeneNameSetDB_Data = sycGeneNameSetDB_file[2:]
			
			unique_gene_setdb_geneid_file_basename=os.path.basename(unique_gene_setdb_geneid_file)
			file_prefix="result_unique_"
			geneid_input_file_path = output_file_dirname+'/'+unique_gene_setdb_geneid_file_basename[len(file_prefix):]
			if	os.path.exists(geneid_input_file_path)==False:
				print 'cant find :'+geneid_input_file_path
				sys.exit(0)
			sycGeneIDSetDB_file =readCsvDataFromFile(0,',',geneid_input_file_path)
			sycGeneIDSetDB_Data= sycGeneIDSetDB_file[2:]
			
			F_sycGeneIDSetDB_ROW_COLS=len(sycGeneIDSetDB_Data[0])
			F_sycGeneIDSetDB_Data=[]
			for i in range(len(sycGeneIDSetDB_Data)):
				F_sycGeneIDSetDB_Data.extend(sycGeneIDSetDB_Data[i])
			#print len(F_sycGeneIDSetDB_Data)
			#print F_sycGeneIDSetDB_Data
			
			for j in range(len(sycGeneExpression_Data)):
				if cmp(sycGeneExpression_Data[j][3],'[]')!=0:
					current_geneid=sycGeneExpression_Data[j][3]
					current_index = -1
					current_index_rows = -1
					current_index_cols = -1
					try:
						current_index=F_sycGeneIDSetDB_Data.index(current_geneid)
						#print 'current geneid of expression:'+current_geneid
						#print 'current gene name of expression:'+sycGeneExpression_Data[j][2]
					except:
						continue
					
					current_index_rows=current_index/F_sycGeneIDSetDB_ROW_COLS
					current_index_cols = current_index%F_sycGeneIDSetDB_ROW_COLS
					#print 'one axis of setdb :'+F_sycGeneIDSetDB_Data[current_index]
					#print 'two axis of setdb :'+sycGeneIDSetDB_Data[current_index_rows][current_index_cols]
					#print 'name two axis of setdb :'+sycGeneNameSetDB_Data[current_index_rows][current_index_cols]
					if current_index!=-1:
						sycGeneExpression_Data[j][2]=sycGeneNameSetDB_Data[current_index_rows][current_index_cols]
				
			sycGeneExpression_Data.insert(0,sycGeneExpression_file[0])
			for k in range(len(sycGeneExpression_Data)):
				del sycGeneExpression_Data[k][3]
			
			file_syn_genename_prefix='result_syn_'
			output_file_syn_path = output_file_dirname+'/'+file_syn_genename_prefix+input_file_basename			
			saveCsvDataToFile([],sycGeneExpression_Data,output_file_syn_path)
			'''
			到目前：
			./app.py -i ../result/0401/result_syn_result_geneid_result_expression_data.txt -n GeneName -g ../result/0401/result_unique_result_geneid_result_gene_set_database.txt 
			
			'''

###app

if __name__=='__main__':
	if len(sys.argv) <=1:
		print "please use option -h"
	else :
		main(sys.argv[1:])
