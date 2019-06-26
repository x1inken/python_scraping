#!/usr/bin/env python
# coding: utf-8

# In[9]:


import urllib.request
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import time
import socket


# In[16]:


def connection():
    return create_engine('mysql+mysqldb://root@localhost/sake?charset=utf8&use_unicode=1')
engine = connection()


# In[17]:


def insSake(shuzo, kana, ken ,mizu ,address, tel, web):
    return "insert into sake(shuzo, kana, ken ,mizu ,address, tel, web) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(shuzo, kana, ken ,mizu ,address, tel, web)


# In[18]:


def getSake(address):
    return "select id from sake where address='{0}'".format(address)


# In[19]:


headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}


# In[40]:


i=1
end=1842
while i < end:
    url = 'http://www.sake-sennin.com/fbo/web/app.php/user/brewers/{0}'.format(i)
    i=i+1
    
    try:
        print(url)
        time.sleep(1)
        req = urllib.request.Request(url , headers=headers)
        soup = BeautifulSoup(urllib.request.urlopen(req).read())
        
        kuramoto = soup.find(id='kuramoto-box1')
        kana = kuramoto.find(id='caption').text
        shuzo = kuramoto.find('h4').text
        ken = kuramoto.find(id='area').text
        
        td = kuramoto.find('table').findAll('td')
        mizu = td[9].text.strip()
        address = td[10].text
        tel = td[11].text
        web = td[13].text
        print(shuzo, kana, ken ,mizu ,address, tel, web)
        
        s = engine.execute( getSake(address)).fetchone()
        if s is None:
            engine.execute( insSake(shuzo, kana, ken ,mizu ,address, tel, web))
        
    except urllib.error.HTTPError as err:
        print(err.code)
    except urllib.error.URLError as err:
        print(err.reason)
    except socket.error as err:
        print("timeout")


# In[ ]:




