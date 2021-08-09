import sys, os, random, numpy, pandas, csv

numpy.random.seed(2021)
devortrain = input("Dev o Train? [dev train] ")
if devortrain == "dev":
    DR = pandas.read_csv('development/drugprot_development_relations.tsv', sep='\t', names=['id','tipo','arg1','arg2'])
    DE = pandas.read_csv('development/drugprot_development_entities.tsv', sep='\t', names=['id','t','tipo','ini','fin','nome'])
elif devortrain == "train":
    DR = pandas.read_csv('training/drugprot_training_relations.tsv', sep='\t', names=['id','tipo','arg1','arg2'])
    DE = pandas.read_csv('training/drugprot_training_entities.tsv', sep='\t', names=['id','t','tipo','ini','fin','nome'])
else:
    raise Exception("Scelta non compatibile")
tutti = input("Generare tutti i casi negativi (altrimenti, uno su trenta)? [si no] ")
tutti = True if tutti == "si" else False

#os.remove('relations2.tsv')
with open('relations2.tsv', 'xt', encoding='UTF-8', newline='') as DREL:
    tsv_writer = csv.writer(DREL, delimiter='\t')
    
    idattuale = DR.id[0]
    imax = len(DR.id)
    relazionipositive = []
    for i in range(0, imax):
        if imax == i+1 or DR.id[i] != idattuale:
            if imax == i+1:
                relazionipositive.append((
                    int(DR.arg1[i].replace("Arg1:T", '')),
                    int(DR.arg2[i].replace("Arg2:T", ''))
                ))
                tsv_writer.writerow([idattuale, DR.tipo[i], DR.arg1[i], DR.arg2[i]])
            j = 0
            ultimochem = 0
            ultimogen = 0
            for n2 in DE.id:
                if n2 == idattuale:
                    if DE.tipo[j] == "GENE":
                        ultimogen = int(DE.t[j].replace("T", ''))
                    else:
                        ultimochem = int(DE.t[j].replace("T", ''))
                j+=1
            #print(f"idattuale: {idattuale}, chem: {ultimochem}, gen: {ultimogen}")
            for nchem in range(1, ultimochem+1):
                for ngen in range(ultimochem+1, ultimogen+1):
                    presente = False
                    for t1, t2 in relazionipositive:
                        if nchem==t1 and ngen==t2:
                            presente = True
                            break
                    if not presente:
                        if tutti or random.randint(0, 30) == 30:
                            tsv_writer.writerow([idattuale, "FALSE", f"Arg1:T{nchem}", f"Arg2:T{ngen}"])
                    # print(f"nchem{nchem} ngen{ngen} presente: {presente}")
                    # print(relazionipositive)
            if imax != i+1:
                relazionipositive = []
                idattuale = DR.id[i]
                relazionipositive.append((
                    int(DR.arg1[i].replace("Arg1:T", '')),
                    int(DR.arg2[i].replace("Arg2:T", ''))
                ))
                tsv_writer.writerow([idattuale, DR.tipo[i], DR.arg1[i], DR.arg2[i]])
        else:
            relazionipositive.append((
                int(DR.arg1[i].replace("Arg1:T", '')),
                int(DR.arg2[i].replace("Arg2:T", ''))
            ))
            tsv_writer.writerow([idattuale, DR.tipo[i], DR.arg1[i], DR.arg2[i]])