# abbiamo il json , lo score, e le manipolazioni
# dobbiamo raggruppare per -1 e per i probe che non si trovano nel json

import csv
import json
import re


# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from collections import Counter

def CSVreader(path):
    with open(path) as f:
        reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        rows = []
        for row in reader:
            rows.append(row)
    return rows


def printInColumn(A):
    for i in range(len(A)):
        print(A[i])


def scoreFilter1(scoreMatrix, opHistory, scorelist, opFilter):

    score = int(re.findall("[-+]?\d*\.\d+|[-+]?\d+",scorelist[0])[0])
    function = re.findall("[=]?[<=]?[>=]?[<]?[>]?",scorelist[0])[0]

    print(score)
    print(function)
    if(len(scorelist) > 1):
        scorelist.remove(scorelist[0])
        print(scorelist)
        scoreFilter1(scoreMatrix,opHistory,scorelist,opFilter)

    # init >> Faccio i join tra le probe nello score del csv e le probe presenti nell'history
    tmp = []
    result = []
    tmpMatrix = []
    for i in range(len(scoreMatrix)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                tmp.append(scoreMatrix[i][0]) #ProbeID
                tmp.append(scoreMatrix[i][1]) #Camera
                tmp.append(opFilter)  # opFiltro
                tmp.append(scoreMatrix[i][3]) #Score
                tmp.append(opHistory['probesFileID'][j]['operations']) #[opHistory]
                tmpMatrix.append(tmp) #ProbeID|Camera|opFiltro|Score|[opHistory]
                tmp = []

    p = 0
    c = 1
    oF = 2
    s = 3
    oH = 4
    # end >> Ho costruito tmpMatrix ProbeID|Camera|opFiltro|Score|[opHistory]

    tmp = []
    tmpMatrix2 = []
    countOperations = 0
    objPosition = -1
    firstMatched = False

    if (score != -1) and (score < 0):
        print('errore,valore inserito non corretto')
        return 0

    elif (function == '=') and (score == -1):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][s]) == -1:  #Score ==-1
                for j in range(len(tmpMatrix[i][oH])): #[opHistory]
                    countOperations = countOperations + 1
                    if (opFilter == tmpMatrix[i][oH][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][p]) #ProbeID
                tmp.append(tmpMatrix[i][c]) #Camera
                tmp.append(tmpMatrix[i][oF]) #opFiltro
                #tmp.append(tmpMatrix[i][s])  #Score
                tmp.append(objPosition) #posOpFilter
                tmp.append(countOperations) #numOp
                tmpMatrix2.append(tmp) # ProbeID|Camera|opFilter|posOpFilter|numOp
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)): # se opFilter non è presente opFilter=-1
            if tmpMatrix2[i][3] != -1: #opFilter
                result.append(tmpMatrix2[i])
        return result


    elif (function) == '>' and (score == -1):
        print('dashara ritenta')
        return 0


    elif (function == '>') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][s]) >= score:  #Score
                for j in range(len(tmpMatrix[i][oH])):
                    countOperations = countOperations + 1
                    if (opFilter == tmpMatrix[i][oH][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][p])  # ProbeID
                tmp.append(tmpMatrix[i][c])  # Camera
                tmp.append(tmpMatrix[i][oF])  # opFiltro
                # tmp.append(tmpMatrix[i][s])  #Score
                tmp.append(objPosition)  # posOpFilter
                tmp.append(countOperations)  # numOp
                tmpMatrix2.append(tmp)  # ProbeID|Camera|opFilter|posOpFilter|numOp
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):
            if tmpMatrix2[i][3] != -1:
                result.append(tmpMatrix2[i])
        return result

    elif (function == '<') and (score >= 0):
        for i in range(len(tmpMatrix)):
            if (float(tmpMatrix[i][s]) < score) and (float(tmpMatrix[i][s]) != -1):
                for j in range(len(tmpMatrix[i][oH])):
                    print(tmpMatrix[i][oH][j]['name'])
                    countOperations = countOperations + 1
                    if (opFilter == tmpMatrix[i][oH][j]['name']) and (firstMatched == False):
                        objPosition = countOperations
                        firstMatched = True
                tmp.append(tmpMatrix[i][p])  # ProbeID
                tmp.append(tmpMatrix[i][c])  # Camera
                tmp.append(tmpMatrix[i][oF])  # opFiltro
                # tmp.append(tmpMatrix[i][s])  #Score
                tmp.append(objPosition)  # posOpFilter
                tmp.append(countOperations)  # numOp
                tmpMatrix2.append(tmp)  # ProbeID|Camera|opFilter|posOpFilter|numOp
                print('')
                tmp = []
            firstMatched = False
            objPosition = -1
            countOperations = 0
        for i in range(len(tmpMatrix2)):
            if tmpMatrix2[i][3] != -1:
                result.append(tmpMatrix2[i])
        return result

    elif (function == '<') and (score == -1):
        print('Error')
        return 0


def scoreFilter2(scoreMatrix, opHistory, scorelist, opFilter, function='null', maxPreviousOp=0):
    tmp = []
    result = []
    tmpMatrix = []
    match = False
    for i in range(len(scoreMatrix)):
        for j in range(len(opHistory['probesFileID'])):
            if scoreMatrix[i][0] == opHistory['probesFileID'][j]['probeID']:
                for k in range(len(opHistory['probesFileID'][j]['operations'])):
                    if opFilter == opHistory['probesFileID'][j]['operations'][k]['name']:
                        match = True
                        break
                if match == True:
                    tmp.append(scoreMatrix[i][0])
                    tmp.append(scoreMatrix[i][1])
                    tmp.append(scoreMatrix[i][3])
                    tmp.append(opHistory['probesFileID'][j]['operations'])
                    tmpMatrix.append(tmp)
                tmp = []
                match = False

    tmp = []
    tmpOp = []
    countOperations = 0

    if (scorelist != -1) and (scorelist < 0):
        print('errore,valore inserito non corretto')
        return 0

    elif (function == 'null') and (scorelist == -1):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) == -1:
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != opFilter:
                        countOperations = countOperations + 1
                        if countOperations <= maxPreviousOp:
                            tmpOp.append(tmpMatrix[i][3][j]['name'])
                    else:
                        break
                tmp.append(tmpOp)
                tmp.append(countOperations)
                result.append(tmp)
                tmp = []
                tmpOp = []
                countOperations = 0

    elif (function == 'over') and (scorelist == -1):
        print('errore,inserire parametri corretti')
        return 0

    elif (function == 'over') and (scorelist >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) >= scorelist:
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != opFilter:
                        countOperations = countOperations + 1
                        if countOperations <= maxPreviousOp:
                            tmpOp.append(tmpMatrix[i][3][j]['name'])
                    else:
                        break
                tmp.append(tmpOp)
                tmp.append(countOperations)
                result.append(tmp)
                tmp = []
                tmpOp = []
                countOperations = 0

    elif (function == 'under') and (scorelist >= 0):
        for i in range(len(tmpMatrix)):
            if float(tmpMatrix[i][2]) < scorelist and (float(tmpMatrix[i][2]) != -1):
                tmp.append(tmpMatrix[i][0])
                for j in range(len(tmpMatrix[i][3])):
                    if tmpMatrix[i][3][j]['name'] != opFilter:
                        countOperations = countOperations + 1
                        if countOperations <= maxPreviousOp:
                            tmpOp.append(tmpMatrix[i][3][j]['name'])
                    else:
                        break
                tmp.append(tmpOp)
                tmp.append(countOperations)
                result.append(tmp)
                tmp = []
                tmpOp = []
                countOperations = 0

    elif (function == 'under') and (scorelist == -1):
        print('errore,inserire parametri corretti')
        return 0

    if result != []:
        for i in range(len(result)):
            if float(result[i][2]) == 0:
                result[i][2] = 'First Operation'
        return result


# Leggo json
with open('./myoperations.json') as f:
    opHistory = json.load(f)
# Leggo csv FinalScores
finalScore = CSVreader('./FinalScores/UnifiPRNUTime_1_CameraVideoVideo.csv')
finalScore.remove(finalScore[0])  # Rimuovo l'intestazione
# Leggo csv ManipReference
camera_ref = CSVreader('./Reference/MFC18_EvalPart1-camera-ref.csv')
camera_ref.remove(camera_ref[0])  # Rimuovo l'intestazione
with open('./Reference/operations.json') as f:
    allOperations = json.load(f)

#METODO CON re.
scorelist = ['-1']
#scorelist = ['<50']
#scorelist = ['>50']

result1 = scoreFilter1(finalScore, opHistory, scorelist, 'AddAudioSample')
printInColumn(result1)
print(len(result1))

# result2 = scoreFilter2(finalScore, opHistory, scorelist, 'AddAudioSample', 'null', 2)
# printInColumn(result2)