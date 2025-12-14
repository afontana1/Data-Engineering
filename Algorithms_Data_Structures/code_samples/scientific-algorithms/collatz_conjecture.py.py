import matplotlib.pyplot as plt
%matplotlib inline

import pandas as pd
import numpy as np
import random
import string

class Collatz():
    '''class for collatz'''
    def __init__(self,number):
        self.n = number
        
        self.out = [self.n]
        self.cache = {}
        
        self.results = []
        self._cache = {}

    def CollatzRecursive(self):
        n = self.out[-1]
        if n == 1:
            return self.out
        elif n % 2==0:
            if n in self.cache:
                self.out.append(self.out[n])
                return self.CollatzRecursive()
            else:
                self.cache[n] = n//2
                self.out.append(n//2)
                return self.CollatzRecursive()
        else:
            if n in self.cache:
                self.out.append(self.cache[n])
                return self.CollatzRecursive()
            else:
                self.cache[n] = 3*n+1
                self.out.append(3*n+1)
                return self.CollatzRecursive()
                

    def CollatzConjecture(self):
        self.results.append(self.n)
        n = self.n
        while n > 1:
            if n%2==0:
                if n in self._cache:
                    self.results.append(self._cache[n])
                else:
                    self.cache[n] = n//2
                    self.results.append(n//2)
                    n = n//2
            else:
                if n in self._cache:
                    self.results.append(self._cache[n])
                else:
                    self._cache[n] = (3*n)+1
                    self.results.append((3*n)+1)
                    n = (3*n)+1
        return self.results
    
    def plotConjecture(self):
        results = self.CollatzConjecture()
        plt.figure(figsize=(10,10))
        plt.title('CollatzConjecture for n = {}'.format(self.n))
        plt.plot(results)
        plt.show()

def _test(m,n):
    recurse,iterative = [], []
    for num in [random.randint(1,m) for _ in range(1,n)]:
        c = Collatz(num)
        recurse.append(c.CollatzRecursive())
        iterative.append(c.CollatzConjecture())
        
    for l1,l2 in zip(recurse,iterative):
        assert l1 == l2
    return recurse, iterative

def pascalsTriangle(n):
    '''n: number of rows'''
    '''first row is one, so input n+1'''
    out = []
    for i in range(1,n+1):
        if i==1:
            out.append([1])
        elif i==2:
            out.append([1,1])
        else:
            temp = []
            temp.append(1)
            for j in range(len(out[-1])-1):
                temp.append(out[-1][j]+out[-1][j+1])
            temp.append(1)
            out.append(temp)
    return out

#Initialize Fake Data
alphabet = list(string.ascii_lowercase)

dcc = {
    str(i): alphabet[random.randint(0,len(alphabet)-1)] for i in range(50)
}

df = pd.DataFrame(
    [tuple([str(random.randint(0,3)) for _ in range(50)]) for j in range(500)],
    columns = [str(i) for i in range(50)]
)



#check map function
def inMap(col1,col2):
    thing = dcc.get(col1,{})
    return col1 == col2

def dotheneedful(df):
    df['col_3'] = df.apply(lambda x: inMap(x['48'], x['49']), axis=1)
    return (df[df['col_3']==True],df[df['col_3']==False])

def compareToThis(df):
    gimme = []
    badbois = []
    for idx,row in df.iterrows():
        thing = dcc.get(row['48'],{})
        if row['48'] == row['49']:
            gimme.append(True)
        else:
            badbois.append(False)
    return {
        'badbois':badbois,
        'goodbois':gimme
    }