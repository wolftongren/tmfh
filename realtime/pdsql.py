import pandas as pd
import numpy as np

df1 = pd.DataFrame([1,2,3,4], columns=list('ABCD'))
df2 = pd.DataFrame([1,2,3,4],columns=list('ABCD'))

print df1

print df2

df = pd.merge([df1, df2])

print df

