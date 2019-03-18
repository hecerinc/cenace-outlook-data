import pandas as pd
import numpy as np
import json


with open('01_01.json', 'r', encoding='utf8') as f:
    c = f.read()
parsed = json.loads(c)
parsed = parsed['Resultados']


# In[21]:


res = pd.DataFrame()
for zone in parsed:
    tmp = pd.DataFrame(zone['Valores'])
    tmp['zona'] = zone['zona_carga']
    res = res.append(tmp, ignore_index = True)


# In[30]:


# res.iloc[:,[0,1,4]] = res.iloc[:,[0,1,4]].apply(pd.to_numeric)


# In[32]:


res['hora'] = res['hora'].astype('int32')
res['region'] = 'BAJA CALIFORNIA SUR'
res.rename(columns={'zona': 'zdc'}, inplace=True)

zones = pd.read_csv('zones2.csv', names=['id','region', 'zdc'], header=None)
tmp = pd.merge(res, zones, how="left", left_on=['region', 'zdc'], right_on=['region', 'zdc'])

# In[39]:


tmp.to_csv("01.csv", index=False)

