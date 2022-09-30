#!/usr/bin/env python
# coding: utf-8

# In[4]:


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


# In[11]:


class Linkedin:
    
    def __init__(self):
        self.x = 'Hello'
        
    @classmethod
    def LINKEDIN_Scrapping(clc,job_search):
      if job_search == "data analysis":
        link1 = 'https://www.linkedin.com/jobs/search?keywords=Data%20Analysis&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
      elif job_search == "machine learning":
        link1 = 'https://www.linkedin.com/jobs/search?keywords=machine%20learning&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
      elif job_search == "software testing":
        link1 = 'https://www.linkedin.com/jobs/search?keywords=software%20testing&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
      
      # FIRST get main informations about jobs

      title = []
      location = []
      country = []
      company_name = []
      post_time = []
      Title =[]
      company_logo =[]
      data  = requests.get(link1)
      soup  = BeautifulSoup(data.text)
      Title = soup.find_all('h3' , {'class': 'base-search-card__title'})
      for x in range(len(Title)):
        t = re.split('[(|-]',Title[x].text)
        title.append(t[0].strip())    
        location.append(soup.find_all('span' , {'class': 'job-search-card__location'})[x].text.replace('\n',' ').strip())
        m = soup.find_all('h4' , {'class': 'base-search-card__subtitle'})[x].text
        company_name.append(m.replace('\n',' ').strip())

        company_logo.append(soup.find_all('img')[x]['data-delayed-url'])
        tt = soup.find_all('time')[x]
        post_time.append(tt.text.replace('\n',' ').strip())
      time.sleep(3)

      # function to get jobs' links 
      def get_links(url):
        links_ =[]
        data  = requests.get(url).text
        soup  = BeautifulSoup(data)
        llinks = soup.find_all('a' , {'class': 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})
        for l in llinks:
          links_.append(l['href'])
        return links_

      # apply links function
      links = get_links(link1)
      # get more about jobs
      Employment_type = []
      Job_function = []
      Seniority_level = []
      Industries = []

      # function to get more about jobs
      def other(urls):
        frames =[]
        for url in urls:
          data1 = requests.get(url)
          soup1 = BeautifulSoup(data1.content)
          j =  soup1.find('ul' , {'class': 'description__job-criteria-list'})
          time.sleep(3)
          jj=j.find_all('h3')
          dic ={}
          for i in range(len(jj)):
            dic[jj[i].text.replace('\n',' ').strip()] = j.find_all('span')[i].text.replace('\n',' ').strip()
          output = pd.DataFrame()
          output = output.append(dic, ignore_index=True) 
          frames.append(output)
        result = pd.concat(frames)
        return result

      # apply Other function
      df = other(links)
      df.fillna('Not_Found',inplace= True)
      df.reset_index(inplace=True, drop=True)


      # function to get job description
          
      def discription(urls):
        nn = pd.DataFrame()
        for link in urls:
          


          try:
            
            dict_desc={}
            heading =[]
            heading_values_final =[]
            data1 = requests.get(link)
            soup1 = BeautifulSoup(data1.text )
            l = soup1.find('div',{'class':'show-more-less-html__markup'})
            time.sleep(4)
            desc = l.find_all('ul')

            # get lists of points req.
            if len(desc) != 0:   
              heading_values =[]
              for i in range(len(desc)):
                desc1 =desc[i].find_all('li')
                time.sleep(3)
                head=[]
                for ii in range(len(desc1)):
                  st=""
                  st='('+str(ii+1) +') '+desc1[ii].text 
                  head.append(st)
                heading_values.append(head)
              heading_values_final.append(heading_values)
              try:
                # get heading of points req.

                    # first get thier location
                c1 =[]
                for a in range(len(desc)):
                  count =0      
                  for i1 in l.children:
                    if type(i1) != bs4.element.NavigableString:
                      count +=1
                      if i1.text == desc[a].text:
                        c1.append(count)
                
                # get the exact heading for each req.
                list11=[]
                for h in c1:
                  llist1=[]
                  flag=0
                  for i in l.children:
                    if type(i) != bs4.element.NavigableString:
                      flag+=1
                      for i2 in l.find_all(['br' and 'strong']) :
                        if (i.text == i2.text) and flag<=h:
                          llist1.append(i.text.strip())
                  list11.append(llist1[-1])
                heading.append(list11)


              except:   # if heading lines are not highlights -_-
                # first get thier req. location
                c1 =[]
                for a in range(len(desc)):
                  count =0      
                  for i1 in l.children:
                    if type(i1) != bs4.element.NavigableString:
                      count +=1
                      if i1.text == desc[a].text:
                        c1.append(count)       

                if (c1[0] ==1)  and (len(c1)==1): # not found any headings
                  heading.append(["***"])
                
                else:
                  list11 =[]
                  
                  for h in c1:
                    llist1=[]
                    flag=0
                    for i in l.children:
                      if type(i) != bs4.element.NavigableString:
                        flag+=1
                        if h == flag+1 :
                          if i.text == "":
                            llist1.append("Description and requirements: ")
                          else:
                            llist1.append(i.text.strip())
                    list11.append(llist1)
                heading.append(list11)
              for j in range(len(heading[0])):
                dict_desc[heading[0][j]] = []
              f =0
              i = len( heading_values_final[0])
              for keys in dict_desc.keys():
                dict_desc[keys] =  heading_values_final[0][f]
                f +=1
                if f == i :
                  break
              nn = nn.append(dict_desc, ignore_index=True, sort=False)

            
            else:    # if we can't get points in description (i will print all the text)
              dict_desc['All_About_Job'] = l.text.replace('\n',' ').strip()
              nn = nn.append(dict_desc, ignore_index=True, sort=False)

          except:  # if we can't acess the job link (i will print not found in its description)
            dict_desc['All_About_Job'] = "Not_Found"
            nn = nn.append(dict_desc, ignore_index=True, sort=False)


        return nn

      

      # apply description function to all links
      df_desc = discription(links)




      # put all together
      df_ml = pd.DataFrame({'Title' : title , 'Location' : location ,'Company_Logo':company_logo,'URLs':links ,'Company_Name' : company_name ,'post_time':post_time})


      result_with_desc = pd.concat([df_ml, df , df_desc], axis=1)
      result_without_desc = pd.concat([df_ml, df ], axis=1)

      result_with_desc.to_excel('LINKEDIN_scrapping_with_description.xlsx',index=False,encoding='utf-8')
      result_without_desc.to_excel('LINKEDIN_scrapping_without_description.xlsx',index=False,encoding='utf-8')




      return result_with_desc , result_without_desc






      


# In[ ]:




