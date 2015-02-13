# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 08:57:47 2014

@author: mkunc

Program to scrape the historical premier league tables
and combine into a single data frame. The purpose of which will
be to perform analysis on the points for each position.

e.g. "How many points on average will I need to avoid the drop?"
 
"How many points does it take to make it to the Champion's League"

"Which position on the table has the widest std deviation?"

"""
#importing neede librarires
from urllib2 import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series, DataFrame

#the years that will be analyzed

years = ['1995','1996','1997','1998','1999','2000','2001','2002','2003'
        ,'2004','2005','2006','2007','2008','2009','2010','2011','2012',
        '2013','2014']
#the season names
        
seasons=['95-96','96-97','97-98','98-99','99-00','00-01','01-02',
         '02-03','03-04','04-05','05-06','06-07','07-08','08-09','09-10',
         '10-11','11-12','12-13','13-14']

#scraping and appending the data

data = []
x = 0
y = len(years)-1
while x < y:
    yr1, yr2 = years[x],years[x+1]
    url ='http://www.premierleague.com/en-gb/matchday/league-table.html?season=%s-%s&month=MAY&timelineView=date&toDate=831250800000&tableView=CURRENT_STANDINGS' %(yr1,yr2)
    page = urlopen(url)
    soup = BeautifulSoup(page.read())
    table = soup.findAll('table')[0]
    pts = table.findAll('td',{'class':'col-pts'})
    for p in pts:
        data.append(p.string)
    x = x+1

#list comprehension to force strings to ints.
data = [int(i) for i in data]
#creating a list of lists to correspond to every premier league season.
#dividing the list into 20 equal pieces as  there are 20 teams in the premier league
splits = [data[i:i+20] for i in xrange(0, len(data),20)]

#create the DataFrame and transpose it so it looks like a football table
df = DataFrame(splits).T
df.columns = seasons
df.index = range(1,21)

#couple of things that I'd like to do
#    1. generate the list of years dynamically
#    2. generate the list of seasons dynamically
#    3. seriously cut down on the amount of Soup that I have here. 
#    4. grab other data points (wins, losses, draws, f, a,) and create a hierarchy
#    5. much further down the road - gather the data by month