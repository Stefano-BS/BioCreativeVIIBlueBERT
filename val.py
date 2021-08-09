from sklearn.metrics import classification_report
import csv

etichette = ['FALSE', 'SUBSTRATE_PRODUCT-OF', "PRODUCT-OF", "ANTAGONIST", "SUBSTRATE", "ACTIVATOR", "INHIBITOR", 'AGONIST-INHIBITOR', "INDIRECT-DOWNREGULATOR", "INDIRECT-UPREGULATOR", "AGONIST", "AGONIST-ACTIVATOR", "PART-OF", "DIRECT-REGULATOR"]

Y = []
with open("test.tsv") as test:
    test = csv.reader(test, delimiter="\t")
    for linea in test:
        Y.append(linea[2])

opath = input("Percorso file output (vuoto per output/test_results.tsv): ")
opath = "output/test_results.tsv" if not opath else opath
Yp = []
with open(opath) as output:
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

csvout = input("Fare csv? ")
if csvout:
    ocsv = opath[0:len(opath)-3] + "csv"
    with open(ocsv, 'xt', encoding='UTF-8', newline='') as ocsv:
        csv_writer = csv.writer(ocsv, delimiter=';')
        dict = classification_report(Y[1:len(Yp)+1], Yp, output_dict=True)
        for k in dict:
            riga = [k]
            if type(dict[k]) == float:
                riga.append(dict[k])
            else:
                for val in dict[k]:
                    riga.append(dict[k][val])
            csv_writer.writerow(riga)
else:
    print(classification_report(Y[1:len(Yp)+1], Yp))