import pandas as pd
from math import log
import os

cwd = os.getcwd()

print("Current working directory: {0}".format(cwd))

print ("os.getcwd() returns an object of type {0}".format(type(cwd)))

# copy the filepath 
os.chdir ("C:\Users\izzyd\OneDrive\Desktop\MIS20080 - Intro to Programming\Task 3 and 4_Loan_Data.csv")

df = pd.read_csv('loan_data_created.csv')

x = df['default'].to_list() # 1 if default else 0 #to_list() converts the pandas series to a list
y = df['fico_score'].to_list()
n = len(x)
print (len(x), len(y))

default = [0 for i in range(851)]
total = [0 for i in range(851)] #makes two lsits of length 851 with all values initialized to 0 

for i in range(n):
    y[i] = int(y[i])
    default[y[i]-300] += x[i] #adds one loan to the count for that FICO score and itterated dover every one 
    total[y[i]-300] += 1 #indexed by FICO score -300 to make it 0 indexed
    
for i in range(0, 551): #prefix sum to make calculations easier later
    default[i] += default[i-1] 
    total[i] += total[i-1]
    
import numpy as np
    
def log_likelihood(n, k):
    p = k/n
    if (p==0 or p==1):
        return 0
    return k*np.log(p)+ (n-k)*np.log(1-p)

r = 10
dp = [[[-10**18, 0] for i in range(551)] for j in range(r+1)]

for i in range(r+1):
    for j in range(551):
        if (i==0):
            dp[i][j][0] = 0
        else:
            for k in range(j):
                if (total[j]==total[k]):
                    continue
                if (i==1):
                    dp[i][j][0] = log_likelihood(total[j], default[j])
                else:
                    if (dp[i][j][0] < (dp[i-1][k][0] + log_likelihood(total[j]-total[k], default[j] - default[k]))):
                        dp[i][j][0] = log_likelihood(total[j]-total[k], default[j]-default[k]) + dp[i-1][k][0]
                        dp[i][j][1] = k
                                                     
print (round(dp[r][550][0], 4))
                                                     
k = 550
l = []
while r >= 0:
    l.append(k+300)
    k = dp[r][k][1]
    r -= 1

print(l)
