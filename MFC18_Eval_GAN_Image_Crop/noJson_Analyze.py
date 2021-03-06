# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

import csv
import json
import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from collections import Counter
#'./probeHistory.json'
#'./FinalScores/UnifiPRNUTime_1_CameraVideoImg.csv'
#'./Reference/MFC18_EvalPart1-camera-ref.csv'
def CSVreader(path):
	with open(path) as f:
		reader = csv.reader(f,delimiter='|', quoting=csv.QUOTE_NONE)
		rows = []
		for row in reader:
			rows.append(row)
	return rows

def printInColumn(A):
	for i in range(len(A)):
		print(A[i])

def findNOJSON(scorePath,ReferencePath,opHistoryPath):

	# Leggo json
	with open(opHistoryPath) as f:
		data = json.load(f)

	# Leggo csv FinalScores
	A = CSVreader(scorePath)
	A.remove(A[0])  #Rimuovo l'intestazione
	# Leggo csv ManipReference
	B = CSVreader(ReferencePath)
	B.remove(B[0]) #Rimuovo l'intestazione

	noJSON = []
	tmp = []
	count = 0
	match = False
	for i in range(len(A)):
		for j in range(len(data['probesFileID'])):
			if A[i][0] == data['probesFileID'][j]['probeID']:
				match = True
		if match == False:
			count = count + 1
			tmp.append(A[i][0])
			tmp.append(A[i][1])
			noJSON.append(tmp)
			tmp = []
		match = False

	# noJSON è una matrice contenente: ProbeID,score,isManipulated/notManipulated raggruppata per Y(yes is manipulated)
	finalNoJSON = []
	for i in range(len(noJSON)):
		for j in range(len(B)):
			if(noJSON[i][0] == B[j][1]):
				tmp.append(noJSON[i][0])
				tmp.append(noJSON[i][1])
				tmp.append(B[j][2].split(".", 1)[1])
				finalNoJSON.append(tmp)
				tmp = []
	return finalNoJSON 

def NoJsonAnalyze(noJSON,optout,threshold,target):
	countOptout = 0
	countOverThresh = 0
	countUnderTresh = 0
	countTarget = 0
	countOptTarget = 0
	countUnderTreshTarget = 0
	countOverThreshTarget = 0 

	for i in range(len(noJSON)):
		if noJSON[i][2] == target:
			countTarget = countTarget + 1
		if float(noJSON[i][1]) == optout:
			countOptout = countOptout + 1
			if noJSON[i][2] == target:
				countOptTarget = countOptTarget + 1
		elif float(noJSON[i][1]) >= threshold:
			countOverThresh = countOverThresh + 1
			if noJSON[i][2] == target:
				countOverThreshTarget = countOverThreshTarget + 1			
		elif (float(noJSON[i][1])) < threshold and (float(noJSON[i][1]))>= 0:
			countUnderTresh = countUnderTresh + 1
			if noJSON[i][2] == target:
				countUnderTreshTarget = countUnderTreshTarget + 1	

	print('numero elementi totali non trovati nel file JSON:  ',len(noJSON))
	print("")
	print('numero elementi non trovati nel file JSON con formato '+target+':',str(countTarget))
	print("")
	print('numero elementi non trovati nel file JSON con score uguale al valore optout '+ str(optout) +': '+ str(countOptout)+', avente inoltre formato '+target+' '+str(countOptTarget))
	print("")
	print('numero elementi non trovati nel file JSON con score maggiore o uguale del valore soglia '+ str(threshold) +': '+ str(countOverThresh)+', avente inoltre formato '+target+' '+ str(countOverThreshTarget))
	print("")
	print('numero elementi non trovati nel file JSON con score minore del valore soglia '+ str(threshold) +': '+ str(countUnderTresh)+', avente inoltre formato '+target+' '+ str(countUnderTreshTarget))
	print("")

noJSON = findNOJSON('./FinalScores/UnifiGLCM_1_GANImageCrop.csv','./Reference/MFC18_Eval-manipulation-image-ref.csv','./probeHistory.json')
NoJsonAnalyze(noJSON,-1,0.3,'jpg')
#printInColumn(noJSON)

#