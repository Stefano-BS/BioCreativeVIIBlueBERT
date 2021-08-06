from sklearn.metrics import classification_report
import csv

etichette = ['FALSE', 'SUBSTRATE_PRODUCT-OF', "PRODUCT-OF", "ANTAGONIST", "SUBSTRATE", "ACTIVATOR", "INHIBITOR", 'AGONIST-INHIBITOR', "INDIRECT-DOWNREGULATOR", "INDIRECT-UPREGULATOR", "AGONIST", "AGONIST-ACTIVATOR", "PART-OF", "DIRECT-REGULATOR"]

Y = []
with open("test.tsv") as test:
    test = csv.reader(test, delimiter="\t")
    for linea in test:
        Y.append(linea[2])

Yp = []
with open("output/test_results.tsv") as output:
    output = csv.reader(output, delimiter="\t")
    for linea in output:
        i=0
        max=0
        imax=0
        for num in linea:
            if float(num) > max:
                max = float(num)
                imax=i
            i+=1
        Yp.append(etichette[imax])
        i+=1

debug = False
if debug:
    for i in range(100):
        print(Y[i+1], Yp[i])

print(classification_report(Y[1:], Yp))