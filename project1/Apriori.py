from itertools import chain,combinations
import math
import sys
from collections import defaultdict


def read_input(input_file):
    f = open('./'+input_file)
    lines = f.readlines()
    a = []
    for i in range(0,len(lines)):
        a.append(list(map(int,lines[i].strip().split('\t'))))
    return a


def scan(tdb,c,min_sup):
    cand = defaultdict(int)
    for i in tdb:
        for j in c:
            if type(j) == int:
                if {j}.issubset(i):
                    cand[j]+=1
            elif set(j).issubset(i):
                if len(j)==2:
                    cand[tuple(sorted(j))] += 1
                else:
                    cand[tuple(j)] += 1
    ret = dict()
    for i,j in cand.items():
        if j/len(tdb) >= min_sup:
            ret[i] = j/len(tdb)
    return ret
    
    
def join_cand(c,k):
    new = []
    ret = []
    if k == 2:
        new = list(combinations(list(c.keys()),k))
    else:
        for i in c.keys():
            for j in c.keys():
                if len(set(i).union(j)) == k:
                    new.append(tuple(sorted(set(i).union(j))))
    new = list(set(new))
    return  new


def associate_rule(total):
    result = ''
    for length,item in total.items():
        if length >= 2:
            for i in item.keys():
                item_set = [combinations(i,j) for j in range(1,length)]
                for element in map(list,chain(*item_set)):
                    comple = set(i) - set(element)
                    support = sup(total,i)
                    confidence = sup(total,i) / sup(total,element)
                    result += '%s\t%s\t%.2f\t%.2f\n' % ('{{{}}}'.format(','.join(map(str,element))),'{{{}}}'.format(','.join(map(str,comple))),round(support*100,2),round(confidence*100,2))
    return result


def sup(total,element):
    ori = 0
    if len(element)==1:
        temp = element[0]
        ori = total[len(element)][temp]
    else:
        temp = tuple(sorted(element))
        ori = total[len(element)][temp]
    return ori

def write_output(output_file,result):
    f = open(output_file,'w')
    f.write(result)
    f.close()

if __name__ == "__main__":
    min_sup = float(sys.argv[1])/100

    total = dict()
    c = []
    k = 1
    tdb = read_input(sys.argv[2])
    c = list(set(chain(*tdb)))
    while c:
        temp = scan(tdb,c,min_sup)
        total[k] = temp
        c = join_cand(temp,k+1)
        k += 1 
    result = associate_rule(total)
    write_output(sys.argv[3],result)
