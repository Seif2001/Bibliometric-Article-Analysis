from concurrent.futures import ThreadPoolExecutor
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
from math import ceil
from optparse import Values
from turtle import title
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import matplotlib as plt
import plotly.express as px
import plotly
from datetime import datetime
import plotly.graph_objects as go
import json
import dateutil.parser
import babel
import logging
from logging import Formatter, FileHandler
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import sys
from multiprocessing.pool import Pool
import concurrent.futures
import math
s = req.Session()
doi_global=" "
citation_doi = []
articles_names = []
new_doi = []
barselect=""
df_citations = pd.DataFrame()
app = Flask(__name__)
@app.route('/error',methods=['GET','POST'])
def error():
    if request.method=='POST':
        return redirect(url_for('home'))
    
    return render_template('error.html')
@app.route('/',methods=['GET','POST'])
def home():
    try:
        if request.method=='POST':
            global doi_global
            doi_global = request.form['doi']
            return redirect(url_for("article"))
        return render_template('index.html')
    except:
        return redirect(url_for('error'))

@app.route('/articleanalysis',methods=['GET','POST'])
def article():
    try:

        global new_doi
        global articles_names
        global citation_doi
        new_doi.clear()
        articles_names.clear()
        citation_doi.clear()
        flag =False;
        crossreflink= 'https://api.crossref.org/works/'+doi_global+'.xml'
        r = s.get(crossreflink)
        soup = bs(r.content,features="html.parser")
        if soup.find_all('citation') != None:
            citation_list = soup.find_all('citation')

        if soup.find_all('titles') != None:
            Article_name = soup.find_all('titles')
        else:
            Article_name='unknown'

        if soup.find_all('crm-item', {'name':'citedby-count'}) !=None:
            Article_cites = soup.find_all('crm-item', {'name':'citedby-count'})
        else:
            Article_cites='unknown'

        if soup.find('full_title') != None:
            Article_journal = soup.find('full_title').text
            flag=True 
        else:
            Article_journal='unknown'   


        if soup.find('person_name') != None:
            Author = soup.find('person_name')
        else:
            Author='unknown'

        #if Author.find('given_name') !=None and Author.find('surname') !=None:

        try:
            name = Author.find('given_name').text + ' ' + Author.find('surname').text
        except:
            name='unknown'

        if soup.find('crm-item', {'name':'created'}):
            Year = datetime.strptime(soup.find('crm-item', {'name':'created'}).text[2:], '%y-%m-%dT%H:%M:%SZ')
        else:
            Year='unknown'


        for item in citation_list:
            citation_doi.append(item.find('doi'))
            articles_names.append(Article_name[0].text)




        for doi in citation_doi:
            if(doi != None):
                new_doi.append(doi.text)
            else:
                new_doi.append('unknown')
        journal = 'https://journalsearches.com/journal.php?title=' + Article_journal
        r = s.get(journal)
        soup = bs(r.content)
        table = soup.find('table')
        if table != None and len(table.find_all('td')) >=11:
            if(table.find_all('td')[7].text == " YES" or table.find_all('td')[7].text== " NO"):
                Open_Access = table.find_all('td')[7].text
            else:
                Open_Access = 'unknown'
            try:
                CiteScore = float(table.find_all('td')[11].text)
            except:
                CiteScore = 'unknown'
            Quartile = table.find_all('td')[-1].text
        else:
            Open_Access = 'unknown'
            CiteScore = 'unknown'
            Quartile = 'unknown'

        global barselect
        barselect=Quartile






        df_article = pd.DataFrame([[name, Article_name[0].text[1:-1], Article_journal, Year.year, CiteScore, Quartile, Article_cites[0].text, Open_Access]])
        df_article.columns = ['Authors', 'Title','Journal', 'Year', 'CiteScore', 'Quartile', 'Cited-By','Open Access']
        df_article = df_article.transpose()

        global df_plot
        df_plot = df_article
        if request.method=='POST':
            return redirect(url_for("resourceanalysis"))


        return render_template('test.html',  tables=[df_article.to_html(classes='data')], titles=df_article.columns.values)
    except:
        return redirect(url_for('error'))


titles = []
journals = []
journalsLinks = []

leng = 0
def webScrape(link):



    #df_citations['Cross Ref Links'][i] = 'https://api.crossref.org/works/' + str(df_citations['doi'][i])+ '.xml'
    if(link!= "unknown"):
        r = s.get(link)
        soup = bs(r.content)
        temp1=soup.find('title')
        temp2=soup.find('full_title')
        if(temp1!=None):
            titles.append(temp1.text)
        else:
            titles.append('unknown')
        if(temp2!=None):
            journals.append(temp2.text)
            journalsLinks.append('https://journalsearches.com/journal.php?title=' + temp2.text)
        else:
            journals.append('unknown')
            journalsLinks.append('https://journalsearches.com/journal.php?title=' + 'unknown')
    else:
        titles.append('unknown')
        journals.append('unknown')
        journalsLinks.append('https://journalsearches.com/journal.php?title=' + 'unknown')
    
    leng = len(journals)
   


def secWebScrape(link):

    #df_citations['links'][i] = 'https://journalsearches.com/journal.php?title=' + df_citations['Journal'][i]
    #link = df_citations['links'][i]
    linko = link[1]
    if(linko != 'https://journalsearches.com/journal.php?title=unknown'):
        r2 = s.get(linko)
        soup2 = bs(r2.content)
        table = soup2.find('table')
        if table != None and len(table.find_all('td')) >=11:
            if(table.find_all('td')[7].text == " YES" or table.find_all('td')[7].text== " NO"):
                OpenAccess[link[0]] = (table.find_all('td')[7].text)
            else:
                OpenAccess[link[0]] = 'unknown'
            try:
                CiteScore[link[0]] = table.find_all('td')[11].text
            except:
                CiteScore[link[0]] ='unknown'
            try:
                Quartile[link[0]] =table.find_all('td')[-1].text 
            except:
                Quartile[link[0]] ='unknown'

                
        else:
           
            OpenAccess[link[0]] ='unknown'
            CiteScore[link[0]] ='unknown'
            Quartile[link[0]] ='unknown'
        
    else:
        OpenAccess[link[0]] ='unknown'
        CiteScore[link[0]] = 'unknown'
        Quartile[link[0]] ='unknown'
    
    
        

      

    
    
    


@app.route('/articleanalysis/citations', methods=['GET','POST'])
def resourceanalysis():
    try:
        df_citations=pd.DataFrame([])
        df_citations = pd.DataFrame([articles_names,  new_doi])
        df_citations = df_citations.transpose()
        df_citations.columns = ['AUC Article Title', 'doi']
        df_citations.fillna("unknown", inplace =True)




        df_citations['Title']=""
        df_citations['Journal']=""
        df_citations['CiteScore'] = 0
        df_citations['Open Access'] = ''
        df_citations['Quartile'] = 0
        df_citations['links']=''
        df_citations['Cross Ref Links'] = ''

        df_citations.drop_duplicates(subset = ['doi'], inplace=True)
        df_citations = df_citations.reset_index()




        df_citations['Cross Ref Links'] = 'https://api.crossref.org/works/' + df_citations['doi'].astype(str)+ '.xml'
        links1 = df_citations['Cross Ref Links'].values.tolist()

        with concurrent.futures.ThreadPoolExecutor() as executer:
            executer.map(webScrape,links1)

        df_citations = pd.DataFrame([titles, journals])
        df_citations = df_citations.transpose()
        df_citations.columns = ['Title','Journal']


        df_citations['links'] = 'https://journalsearches.com/journal.php?title=' + df_citations['Journal'].astype(str)



        #journalsLinks = df_citations['links'].values.tolist()
        journalsLinks = df_citations['links'].values.tolist()

        for i in range(len(journalsLinks)):
            journalsLinks[i] = [i,journalsLinks[i]]

        #with concurrent.futures.ThreadPoolExecutor() as executer:
        #    executer.map(secWebScrape, journalsLinks)
        #for link in links1:
        #    webScrape(link)
        #   
#   
#   
   #    

        global OpenAccess
        global CiteScore 
        global Quartile

        OpenAccess = [0]*len(df_citations)
        CiteScore = [0]*len(df_citations)
        Quartile = [0]*len(df_citations)

        #for link in journalsLinks:
        #    secWebScrape(link)

        with concurrent.futures.ThreadPoolExecutor() as executer:
            executer.map(secWebScrape,journalsLinks)


        df_citations['CiteScore'] = CiteScore
        df_citations['Open Access'] = OpenAccess
        df_citations['Quartile'] = Quartile

        titles.clear()
        journals.clear()
        CiteScore.clear()
        OpenAccess.clear()
        Quartile.clear()
        links1.clear()
        journalsLinks.clear()

        df_citations.drop('links', axis = 1, inplace=True)
    
        full_list = len(df_citations)

        for i in range(len(df_citations)):
            if(df_citations['Title'][i]=='unknown' and df_citations['Journal'][i]=='unknown' and df_citations['CiteScore'][i]=='unknown'  and df_citations['Open Access'][i]=='unknown' and df_citations['Quartile'][i]=='unknown'):
                df_citations.drop([i],axis=0,inplace=True)

        accurateList= len(df_citations)







    



        if(len(df_citations)==0):
            return "SORRY, the information about your citations is not available"
            #return render_template('citations.html',  tables=[df_citations.to_html(classes='data')], titles=df_citations.columns.values)
        else:
            global df
            df = df_citations


            if request.method=='POST':
                return redirect(url_for('showAnalysis'))


            return render_template('citations.html',  tables=[df_citations.to_html(classes='data')], titles=df_citations.columns.values, full_list = full_list, accurateList = accurateList )
    except:
        return redirect(url_for('error'))





@app.route('/articleanalysis/citations/sorting', methods=['GET','POST'])
def showAnalysis():
    try:

        df['CiteScore'] = df['CiteScore'].replace('unknown', 0)
        df['CiteScore'] = df['CiteScore'].replace('No', 0)
        df['CiteScore'] = df['CiteScore'].replace('Yes', 0)
        df['CiteScore'] = df['CiteScore'].astype(np.float16)

        df.sort_values('CiteScore', ascending= False, inplace=True)


        df['CiteScore'] = df['CiteScore'].replace(0,'unknown')
       



        if request.method=='POST':
            return redirect(url_for('showsuggestion'))



        return render_template('sorting.html',  tables=[df.to_html(classes='data')], titles=[df.columns.values])
    except:
        return redirect(url_for('error'))

@app.route('/articleanalysis/citations/sorting/suggestions',methods=['GET','POST'])
def showsuggestion():
    try:

        df_best=[]
        df_best2=[]

        df_best.clear()
        df_best2.clear()
        df_best=pd.DataFrame(df_best)

        dff=df[df['Open Access']==' YES']
        dfff=df
        dff = dff.drop_duplicates(subset='Journal', keep="first")
        dfff = dfff.drop_duplicates(subset='Journal', keep="first")

        dff=dff.reset_index(drop=True)
        dfff=dfff.reset_index(drop=True)
        countyes=len(dff[dff['Open Access']==' YES'])
        print(countyes)
        rangee=math.ceil(countyes/2.0)

        if rangee>0:
            if countyes>=2:
                df_best=[dff.iloc[0],dff.iloc[1]]
                df_best=pd.DataFrame(df_best)
            else:
                print(rangee)
                for i in range(rangee):
                    df_best.append(dff.iloc[i])
                df_best=pd.DataFrame(df_best)

            print(len(df_best))
            
        rangeee=math.ceil(len(dfff)/2.0)
        if rangeee>0:
            if len(dfff)>=2:
                df_best2=[dfff.iloc[0],dfff.iloc[1]]
                df_best2=pd.DataFrame(df_best2)
            else:
                print(rangee)
                for i in range(rangee):
                    df_best2.append(dfff.iloc[i])
                df_best2=pd.DataFrame(df_best2)
            df_best2.drop('Title', axis=1, inplace=True)
        
        
        


        

        if request.method=='POST':
            return redirect(url_for('showPlots'))

        if len(df_best)>0:
            df_best.drop('Title', axis=1, inplace=True)
            return render_template('suggest.html', tables2=[df_best.to_html(classes='data')],tables3=[df_best2.to_html(classes='data')], titles2=[df_best.columns.values],titles3=[df_best2.columns.values],mytitle='The top two Open Access journals based on article cite score')
        else:
            return render_template('suggest.html',tables3=[df_best2.to_html(classes='data')],titles3=[df_best2.columns.values],mytitle='no open access journals found for you')


    except:
        return redirect(url_for('error'))
    

@app.route('/articleanalysis/citations/sorting/plots', methods=['GET','POST'])
def showPlots():
    try:
        df.sort_values('Quartile', ascending= True, inplace=True)

        fig = px.scatter(df, y="Open Access", x="CiteScore", opacity=0.4, hover_data=['Journal','CiteScore'], size_max = 60, title = "Open Access vs Cite Score ScatterPlot")
        fig.update_traces(marker_size=20)
        try:
            fig.add_trace(go.Scatter(x=[float(df_plot.loc['CiteScore'])], y=[str(df_plot.loc['Open Access'][0])], mode = 'markers', marker=dict(
                color='Black',
                size=20), visible='legendonly',
        name="Your article"))
        except:
            fig.add_trace(go.Scatter(x=[0], y=[str(df_plot.loc['Open Access'][0])], mode = 'markers', marker=dict(
                color='Black',
                size=20), visible='legendonly',
        name="Your article"))



        graphjson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 

        bar_data = df["Quartile"].value_counts()
        bar_data = pd.DataFrame(bar_data)
        bar_data = bar_data.reset_index()
        bar_data.rename(columns = {'index':'Quartile', 'Quartile':'Count'}, inplace = True)
        bar_data = bar_data.astype({'Quartile':'str'})

        # colors = ['RGB(61, 78, 107)',] *5 
        # try:
        #     colors[int(df_plot.loc['Quartile'])-1] = 'RGB(246, 176, 0)'
        # except:
        #     colors[-1]='RGB(246, 176, 0)'



        default_color = 'RGB(61, 78, 107)'
        colors = {barselect: 'RGB(246, 176, 0)'}



        color_discrete_map = {
            c: colors.get(c, default_color) 
            for c in bar_data.Quartile.unique()}

        figBar = px.bar(bar_data, x='Quartile', y='Count', color='Quartile',
                     color_discrete_map=color_discrete_map)

    



        barjson = json.dumps(figBar, cls=plotly.utils.PlotlyJSONEncoder) 

        if request.method=='POST':
            return redirect(url_for('home'))



        return render_template('plot.html',graphjson = graphjson, barjson = barjson)
    except:
        return redirect(url_for('error'))

    

    






if __name__ == '__main__':
    app.run(debug=True)