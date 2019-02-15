import csv
import json
import argparse
import sys

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

#Da linea di comando
if sys.argv[1:] != []:
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--probejournaljoin", required=True,help="insert probejournalname path")
    ap.add_argument("-j", "--journalmask", required=True, help="insert journalmask path")
    ap.add_argument("-o", "--operations", required=True, help="insert json file contains all operations")

    args = vars(ap.parse_args())

    probePath = args["probejournaljoin"]
    journalPath = args["journalmask"]
    operationsPath = args["operations"]


#In modalità interattiva
else:
    print("Enter the path of probejournaljoin :")
    probePath = input().strip()

    print("Enter the path of journalmask :")
    journalPath = input().strip()

    print("Enter the path of operations :")
    operationsPath = input().strip()


A = CSVreader(probePath)
# creo il bigArray
pastValue = A[1]
Operations = []
k = 0
B = []
bigArray = []

for i in range(1, len(A)):
    currentValue = A[i]
    if currentValue[0] == pastValue[0]:
        B.append(currentValue)
    else:
        bigArray.append(B)
        B = []
        B.append(currentValue)  # risolve il problema che non printa la 1°
    pastValue = currentValue

# ordino secondo Sequence che è la quarta posizione della tabella
tmpRows = []
for i in range(len(bigArray)):
    for j in range(len(bigArray[i])):
        for k in range(j, len(bigArray[i])):
            if bigArray[i][j][4] < bigArray[i][k][4]:
                tmpRows = bigArray[i][j]
                bigArray[i][j] = bigArray[i][k]
                bigArray[i][k] = tmpRows
                tmpRows = []

# confronto con l'altro csv per stampare l' Operation.  Inserisco tutto dentro C
B = CSVreader(journalPath)
C = []
C2 = []
tmpOP = []
for i in range(len(bigArray)):
    for j in range(len(bigArray[i])):
        for k in range(len(B)):
            if (bigArray[i][j][1] == B[k][0]) and (bigArray[i][j][2] == B[k][1]) and ((bigArray[i][j][3] == B[k][2])):
                # print(B[k][0],B[k][3],B[k][5],B[k][6])
                tmp = [bigArray[i][j][0], B[k][3], B[k][5], B[k][6], ""]
                tmpOP.append([bigArray[i][j][0], B[k][3], B[k][5], B[k][6], ""])
                C.append(tmp)
    C2.append(tmpOP)
    tmpOP = []

# apro il JSON e inserisco la descrizione dentro l'array C.
with open(operationsPath) as f:
    data = json.load(f)
# pprint(data)  #stampa tutto
# print(data.keys()) # stampa tutte le keys principali
# print(data['operations'][0].keys()) # stampa tutte le keys di operations[0]
# print(data['operations'][0]['name'])  #stampa il valore della key name dentro operations[0]
# print(len(data['operations'])) #stampa il numero di operation presenti in operations

for i in range(len(C2)):
    for k in range(len(C2[i])):
        for j in range(len(data['operations'])):
            if C2[i][k][1] == data['operations'][j]['name']:
                C2[i][k][4] = data['operations'][j]['description']
            # print(i, B[k][3], B[k][5], B[k][6], B[k][7])

# Creo un file JSON
totalProbes = []
probes = {}
tmpOperations = {}
for i in range(len(C2)):
    probeOperations = []
    for j in range(len(C2[i])):
        tmpOperations = {
            "name": C2[i][j][1],
            "purpose": C2[i][j][2],
            "operationArgument": C2[i][j][3],
            "description": C2[i][j][4]
        }
        probeOperations.append(tmpOperations)

    probes = {

        "probeID": C2[i][0][0],
        "operations": probeOperations
    }
    totalProbes.append(probes)

probesFile = {

    "probesFileID": totalProbes
}
with open('./probeHistory.json', 'w') as fp:
    json.dump(probesFile, fp, indent=4, ensure_ascii=False)

print('JSON file has been created')