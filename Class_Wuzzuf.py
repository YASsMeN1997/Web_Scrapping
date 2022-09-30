#!/usr/bin/env python
# coding: utf-8

# In[26]:


import warnings
warnings.filterwarnings("ignore")
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import bs4
from urllib.request import urlopen
import time
import re
import time


# In[27]:


Data_analysis_jobs = ['Data', 'analysis']
machine_learning_jobs = ['machine', 'learning']
software_testing_jobs = ['software' , 'testing']


# In[23]:


class WUZZUF:
    def __init__(self):
        self.x = 'Hello'
        
    
    def Wuzzuf_scrapping(clc,job_type , pages_num):
        
      if job_type.lower() == "data analysis":
          link1 = 'https://wuzzuf.net/search/jobs/?a=navbl&q='+Data_analysis_jobs[0]+'%20'+Data_analysis_jobs[1]
      elif job_type.lower() == "machine learning":
          link1 = 'https://wuzzuf.net/search/jobs/?a=navbl&q='+machine_learning_jobs[0]+'%20'+machine_learning_jobs[1]
      elif job_type.lower() == "software testing":
          link1 = 'https://wuzzuf.net/search/jobs/?a=navbl&q='+software_testing_jobs[0]+'%20'+software_testing_jobs[1]
      title = []
      location = []
      country = []
      job_description = []
      Job_Requirements =[]
      company_name = []
      links = []
      Jop_type = []
      Career_Level = []
      company_logo = []
      Job_Categories = []
      Skills_And_Tools = []
      Experience_Needed =[]
      post_time = []
      Title = []
      for i in range(int(pages_num) ):
        link_new = link1 +'&start='+str(i)
        data  = requests.get(link_new)
        soup  = BeautifulSoup(data.content)
        Title = soup.find_all('h2' , {'class': 'css-m604qf'})
        for x in range(0,len(Title)):
          t = re.split('\(|\-',Title[x].find('a').text)
          title.append(t[0].strip())
          loc = re.split(',' , soup.find_all('span' , {'class': 'css-5wys0k'})[x].text)
          r = ""
          for i in range(len(loc[:-1])):
            r= r+ ', ' +loc[:-1][i].strip()
          location.append(r.replace(',', '', 1).strip())
          country.append(loc[-1].strip())
          links.append('https://wuzzuf.net' + Title[x].find('a').attrs['href'])
          m = " ".join(re.findall("[a-zA-Z\d+]+", (soup.find_all('div' , {'class': 'css-d7j1kk'})[x].find('a').text)))
          company_name.append(m)
          c = soup.find_all('div' ,{'class':'css-1lh32fc'})[x].find_all('span')
          if len(c) ==1:
            Jop_type.append(c[0].text)
          else:
            n =[]
            for i in range(len(c)):
              n.append(c[i].text)
            Jop_type.append(n)
          n =soup.find_all('div' ,{'class':'css-y4udm8'})[x].find_all('div')[1].find_all(['a','span'])
          Career_Level.append(n[0].text)
          yy = n[1].text.replace('·',' ').strip()
          yy = re.findall('[0-9-+]*',yy)
          y1 =""
          for i in range(len(yy)):

            if any(yy[i]):
              y1 = y1+yy[i]
          Experience_Needed.append(y1)
          time = (soup.find_all('div' ,{'class':'css-d7j1kk'}))[x].find('div')
          post_time.append(time.text)

      # to get the logo of the company

          data1  = requests.get(links[x])
          soup1 = BeautifulSoup(data1.content)
          company_logo.append(soup1.find_all('meta',{'property':"og:image"})[0]['content'])
          #time.sleep(4)

      df = pd.DataFrame({'Title' : title , 'Location' : location ,'country':country,'URLs':links ,'Company_Name' : company_name,'Career_Level':Career_Level,'post_time':post_time,'Experience_Needed':Experience_Needed,'Company_Logo':company_logo})
      df.to_excel('WUZZUF_scrapping.xlsx',index=False,encoding='utf-8')
      return df


# In[24]:


#test_class = WUZZUF()


# In[25]:


#test_class.Wuzzuf_scrapping("machine learning" , 2)


# In[ ]:




