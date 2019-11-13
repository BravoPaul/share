import re
import pandas as pd



df = pd.DataFrame(columns=['lib', 'qty1', 'qty2'])

df.loc[0] = [1,2,3]
df.loc[1] = [1,2,3]
df.loc[2] = [1,2,3]
df.loc[3] = [1,2,3]
df.loc[4] = [1,2,3]

df.loc[8] = [4,5,6]

print(df)