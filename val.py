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
        Yp.append(etichette[linea.index(max(linea))])

print(classification_report(Y[1:], Yp, target_names=etichette))