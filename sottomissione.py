import csv, sys

etichette = ['FALSE', 'SUBSTRATE_PRODUCT-OF', "PRODUCT-OF", "ANTAGONIST", "SUBSTRATE", "ACTIVATOR", "INHIBITOR", 'AGONIST-INHIBITOR', "INDIRECT-DOWNREGULATOR", "INDIRECT-UPREGULATOR", "AGONIST", "AGONIST-ACTIVATOR", "PART-OF", "DIRECT-REGULATOR"]

opath = input("Percorso file output di predizione (vuoto per output/test_results.tsv): ")
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

i = -1
test = input("File input di predizione (vuoto per test.tsv): ")
test = "test.tsv" if not test else test
with open(test) as test:
    test = csv.reader(test, delimiter="\t")
    with open('sottomissione.tsv', 'xt', encoding='UTF-8', newline='') as sottomissione:
        tsv_writer = csv.writer(sottomissione, delimiter='\t')
        for linea in test:
            # retid = f"{nabs}.{t1}.{t2}"
            (id, arg1, arg2) = linea[0].split('.')
            arg1 = "Arg1:" + arg1
            arg2 = "Arg2:" + arg2
            if i>=0 and Yp[i] != "FALSE":
                tsv_writer.writerow([id, Yp[i], arg1, arg2])
            i += 1