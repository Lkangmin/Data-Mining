import numpy as np
import pandas as pd
import sys


class Dtree():
    def __init__(self,df,is_leaf=0):
        self.df = df
        self.attri = None
        self.label = None
        self.child = None
        self.is_leaf = is_leaf
        
        self.make_tree()
        self.label = self.df.iloc[:,-1].value_counts().idxmax()
        
    def make_tree(self):
        if len(self.df.iloc[:,-1].unique()) == 1:
            self.is_leaf = 1;
        
        else:
            att = list(self.df.columns[:-1])
            min_g = float('inf')
            for i in att:
                gain = info_gain(self.df,i)
                if gain <= min_g:
                    min_g = gain
                    self.attri = i
            self.child = dict()
            for i in self.df[self.attri].unique():
                new_input = self.df.loc[self.df[self.attri]==i]
                self.child[i] = Dtree(new_input.drop(self.attri,axis=1))
    
    def classify(self,test):
        if self.is_leaf:
            return self.label
        else:
            try:
                res = self.child[test[self.attri]]
            except:
                return self.label
            return res.classify(test)
            
            
    def print_tree(self,c):
        count = c
        if self.is_leaf:
            for k in range(0,count): print(' ',end='')
            print("  leaf label:",self.label)
        else:
            for k in range(0,count): print('  ',end='')
            print(self.attri)
            for i,j in self.child.items():
                for k in range(0,count): print('  ',end='')
                print(i)
                j.print_tree(c+1)

def entropy(res):
    info = 0
    for i in range(0,len(res)):
        info += -(res[i]/res.sum())*np.log2(res[i]/res.sum())
    return info

def info_gain(df,label):
    gain = 0
    class_ = df.iloc[:,-1]
    data_l = df.shape[0]
    att_dic = df[label].value_counts()
    for i,j in att_dic.items():
        res = df.groupby([label,class_]).size()[i]
        gain += (res.sum()/data_l)*entropy(res)
    return gain

if __name__ == "__main__":
    df = pd.read_table(sys.argv[1],sep='\t')
    test = pd.read_table(sys.argv[2],sep='\t')
    tree = Dtree(df)
    test.loc[:,df.columns[-1]] = None
    temp = test.columns[-1]
    for i in range(0,len(test)):
        test.loc[i,temp] = tree.classify(test.loc[i])
    test.to_csv(sys.argv[3],sep='\t',index = False)
