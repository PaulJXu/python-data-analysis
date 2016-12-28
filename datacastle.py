
# coding: utf-8

# In[1]:

import pandas as pd


# In[52]:

import numpy as np


# In[2]:

user_info = pd.read_csv('C:\\Users\\Administrator\\Desktop\\新建文件夹\\个人征信\\train\\user_info_train.txt',header=None,names=['user_id','sex','occupation','education','marriage','household'])


# In[49]:

user_info.dtypes


# In[3]:

bank_detail = pd.read_csv('C:\\Users\\Administrator\\Desktop\\新建文件夹\\个人征信\\train\\bank_detail_train.txt',header=None,names=['user_id','tm_encode','trade_type','trade_amount','salary_tag'])


# In[4]:

grouped0 = bank_detail.groupby(['user_id','trade_type']) 


# In[5]:

income = grouped0['trade_amount'].sum().unstack()


# In[6]:

income.rename(columns={0:'shouru',1:'zhichu'},inplace = True)


# In[7]:

income['netincome'] = income['shouru']-income['zhichu']


# In[8]:

incomes = income['netincome']#合并表


# In[9]:

tag1 = bank_detail.loc[bank_detail['salary_tag']==1]


# In[10]:

salary = tag1.groupby('user_id')['trade_amount'].mean()#salary合并表


# In[11]:

bank = pd.concat([incomes,salary],axis=1)


# In[12]:

new_bank = bank.reset_index()#合并到总表


# In[13]:

bill_detail = pd.read_csv('C:\\Users\\Administrator\\Desktop\\新建文件夹\\个人征信\\train\\bill_detail_train.txt',header=None,names=['user_id','tm_encode','bank_id','last_bill','last_return','credit_amount','this_bill_left','minreturn_bill','use_times','this_bill_amount','adjust_amount','recircle_rate','left_amount','load_amount','return_item'])


# In[14]:

bill_detail.head()


# In[15]:

bill_detail['last_return_diff']=bill_detail['last_return']-bill_detail['last_bill']


# In[16]:

bill_detail = bill_detail.drop(['tm_encode','last_bill','last_return','minreturn_bill','use_times','adjust_amount'],axis=1)


# In[17]:

bill_detail.head()


# In[73]:

bill_detail.loc[bill_detail['user_id']==2]


# In[18]:

grouped2 = bill_detail.groupby('user_id')


# In[19]:

crdits = grouped2['bank_id'].unique()


# In[36]:

c = pd.DataFrame(columns=['user_id','cards'])
for index in crdits.index:
    c = c.append(pd.Series({'user_id':index,'cards':len(crdits[index])}),ignore_index=True)


# In[57]:

c['user_id']=c['user_id'].astype(np.int64)


# In[58]:

c.dtypes


# In[59]:

c.head()#合并表 每个用户拥有的信用卡数量


# In[61]:

grouped1 = bill_detail.groupby(['user_id','bank_id'])


# In[75]:

credit_amount = (grouped1['credit_amount'].sum())/(grouped1['credit_amount'].size())


# In[84]:

credit_amounts = pd.DataFrame(credit_amount).reset_index()


# In[89]:

credit_amounts.rename(columns={0:'edu'},inplace=True)


# In[92]:

user_credit_amount = pd.DataFrame(credit_amounts.groupby('user_id')['edu'].sum())


# In[95]:

user_credit_amount = user_credit_amount.reset_index()#合并表  每个用户所有信用卡总额度


# In[ ]:

#每个用户循环利息总额 与 每个用户上次还款借款总差额


# In[105]:

user_rate = grouped2['recircle_rate','last_return_diff'].sum().reset_index() #合并表


# In[108]:

user_loan = pd.DataFrame(grouped2['load_amount'].mean()).reset_index() #每个用户平均预借现金额度 合并表


# In[111]:

d = pd.merge(c,user_credit_amount,on='user_id')


# In[112]:

e = pd.merge(d,user_rate,on='user_id')


# In[113]:

f = pd.merge(e,user_loan,on='user_id') #合并到总表


# In[ ]:



