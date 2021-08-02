import sys, os, random, numpy, pandas, csv

numpy.random.seed(2021)
devortrain = input("Dev o Train? ")
if devortrain == "dev":
    DABS = pandas.read_csv('development/drugprot_development_abstracs.tsv', sep='\t', names=['id','titolo','txt'])
    DENT = pandas.read_csv('development/drugprot_development_entities.tsv', sep='\t', names=['id','t','tipo','ini','fin','nome'])
    DREL = pandas.read_csv('development/drugprot_development_relations.tsv', sep='\t', names=['id','tipo','arg1','arg2'])
elif devortrain == "train":
    DABS = pandas.read_csv('training/drugprot_training_abstracs.tsv', sep='\t', names=['id','titolo','txt'])
    DENT = pandas.read_csv('training/drugprot_training_entities.tsv', sep='\t', names=['id','t','tipo','ini','fin','nome'])
    DREL = pandas.read_csv('training/drugprot_training_relations.tsv', sep='\t', names=['id','tipo','arg1','arg2'])
else:
    raise Exception("Scelta non compatibile")

test = input("Test? ")
test = True if test == "si" else False

def componi(nabs = 16618126):
    # Ritorna lista di input per BERT: [(id, testo, classe)]
    ret = []
    retid = ""
    rettxt = ""
    retclass = ""
    i = 0
    for n in DREL.id:
        if n == nabs:
            t1 = DREL.arg1[i].replace("Arg1:", '')
            t2 = DREL.arg2[i].replace("Arg2:", '')
            retid = f"{nabs}.{t1}.{t2}"
            retclass = DREL.tipo[i]
            j=0
            for n2 in DABS.id:
                if n2 == nabs:
                    rettxt = DABS.titolo[j] + DABS.txt[j]
                j+=1
            
            j=0
            indici = [0,0,0,0]
            tipi = ["", ""]
            for n2 in DENT.id:
                if n2 == nabs:
                    #rettxt = rettxt.replace(DENT.tipo[j], f"@{DENT.tipo[j]}$")
                    #rettxt = rettxt[0:DENT.ini[j]-1] + f"@{DENT.tipo[j]}$" + rettxt[DENT.fin[j]-1:]
                    if DENT.t[j] == t1:
                        indici[0] = DENT.ini[j]-1
                        indici[1] = DENT.fin[j]-1
                        tipi[0] = DENT.tipo[j]
                    elif DENT.t[j] == t2:
                        indici[2] = DENT.ini[j]-1
                        indici[3] = DENT.fin[j]-1
                        tipi[1] = DENT.tipo[j]
                j+=1
            
            nuovoinizio = 0
            nuovafine = len(rettxt)
            if indici[0] < indici[2]:
                try:
                    nuovoinizio = rettxt[0:indici[0]].rindex('.')+2
                except ValueError as v:
                    nuovoinizio = 0
                try:
                    nuovafine = rettxt.index('.', indici[3])
                except ValueError as v:
                    nuovafine = len(rettxt)
                rettxt = rettxt[nuovoinizio : nuovafine]
                rettxt = rettxt[0:indici[2]-nuovoinizio] + f"@{tipi[1]}$" + rettxt[indici[3]-nuovoinizio:]
                rettxt = rettxt[0:indici[0]-nuovoinizio] + f"@{tipi[0]}$" + rettxt[indici[1]-nuovoinizio:]
            elif indici[0] > indici[2]:
                try:
                    nuovoinizio = rettxt[0:indici[2]].rindex('.')+2
                except ValueError as v:
                    nuovoinizio = 0
                try:
                    nuovafine = rettxt.index('.', indici[1])
                except ValueError as v:
                    nuovafine = len(rettxt)
                rettxt = rettxt[nuovoinizio : nuovafine]
                rettxt = rettxt[0:indici[0]-nuovoinizio] + f"@{tipi[0]}$" + rettxt[indici[1]-nuovoinizio:]
                rettxt = rettxt[0:indici[2]-nuovoinizio] + f"@{tipi[1]}$" + rettxt[indici[3]-nuovoinizio:]
            
            # rettxt = rettxt[rettxt[0:indici[2]].rindex('.')+2 : rettxt.index('.', indici[1])]
            # rettxt = rettxt.replace(tipi[0], f"@{tipi[0]}$")
            # rettxt = rettxt.replace(tipi[1], f"@{tipi[1]}$")
            # print(f"tipi: {rettxt[indici[0]-nuovoinizio : indici[1]-nuovoinizio]} {rettxt[indici[2]-nuovoinizio : indici[3]-nuovoinizio]} retid: {retid} retclass: {retclass}\n{rettxt}")
            ret.append([retid, rettxt, retclass])
        i+=1
    return ret

def mktrain(test):
    retid = ""
    rettxt = ""
    retclass = ""
    i = 0
    with open('train.tsv', 'xt', encoding='UTF-8', newline='') as train:
        tsv_writer = csv.writer(train, delimiter='\t')
        if test:
            testfile = open('test.tsv', 'xt', encoding='UTF-8', newline='')
            tsv_writertest = csv.writer(testfile, delimiter='\t')
        
        for nabs in DREL.id:
            t1 = DREL.arg1[i].replace("Arg1:", '')
            t2 = DREL.arg2[i].replace("Arg2:", '')
            retid = f"{nabs}.{t1}.{t2}"
            retclass = DREL.tipo[i]
            j=0
            for n2 in DABS.id:
                if n2 == nabs:
                    rettxt = DABS.titolo[j] + DABS.txt[j]
                j+=1
            j=0
            indici = [0,0,0,0]
            tipi = ["", ""]
            for n2 in DENT.id:
                if n2 == nabs:
                    if DENT.t[j] == t1:
                        indici[0] = DENT.ini[j]-1
                        indici[1] = DENT.fin[j]-1
                        tipi[0] = DENT.tipo[j]
                    elif DENT.t[j] == t2:
                        indici[2] = DENT.ini[j]-1
                        indici[3] = DENT.fin[j]-1
                        tipi[1] = DENT.tipo[j]
                j+=1
            nuovoinizio = 0
            nuovafine = len(rettxt)
            if indici[0] < indici[2]:
                try:
                    nuovoinizio = rettxt[0:indici[0]].rindex('.')+2
                except ValueError as v:
                    nuovoinizio = 0
                try:
                    nuovafine = rettxt.index('.', indici[3])
                except ValueError as v:
                    nuovafine = len(rettxt)
                rettxt = rettxt[nuovoinizio : nuovafine]
                rettxt = rettxt[0:indici[2]-nuovoinizio] + f"@{tipi[1]}$" + rettxt[indici[3]-nuovoinizio:]
                rettxt = rettxt[0:indici[0]-nuovoinizio] + f"@{tipi[0]}$" + rettxt[indici[1]-nuovoinizio:]
            elif indici[0] > indici[2]:
                try:
                    nuovoinizio = rettxt[0:indici[2]].rindex('.')+2
                except ValueError as v:
                    nuovoinizio = 0
                try:
                    nuovafine = rettxt.index('.', indici[1])
                except ValueError as v:
                    nuovafine = len(rettxt)
                rettxt = rettxt[nuovoinizio : nuovafine]
                rettxt = rettxt[0:indici[0]-nuovoinizio] + f"@{tipi[0]}$" + rettxt[indici[1]-nuovoinizio:]
                rettxt = rettxt[0:indici[2]-nuovoinizio] + f"@{tipi[1]}$" + rettxt[indici[3]-nuovoinizio:]
            
            if test:
                if random.randint(1, 3) > 2:
                    tsv_writertest.writerow([retid, rettxt, retclass])
                else:
                    tsv_writer.writerow([retid, rettxt, retclass])
            else:
                tsv_writer.writerow([retid, rettxt, retclass])
            i+=1

def mktrain2():
    with open('train.tsv', 'xt', encoding='UTF-8', newline='') as train:
        tsv_writer = csv.writer(train, delimiter='\t')
        ultimonabs = 0
        for nabs in DREL.id:
            if nabs != ultimonabs:
                ultimonabs = nabs
                tsv_writer.writerows(componi(nabs))

mktrain(test)