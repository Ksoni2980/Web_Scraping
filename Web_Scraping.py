from bs4 import BeautifulSoup
import requests 
import pandas as pd
from datetime import date,timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

stocks = []
dates = []
for j in range(1,4):
    URL = "https://www.moneycontrol.com/broker-research/stocks-" + str(j) + ".html"
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    all = soup.findAll('p', attrs={'class':'MT5'})
    stocks += [x.text.rstrip() for x in all[:20]]
    
    all = soup.findAll('p', attrs={'class':'op_gl12'})
    dates += [x.text[10:] for x in all[:20]]

Call = []
Name = []
Target = []
Madeby = []

i = 0
to_delete = []
for stock in stocks:
    if ';' not in stock or ':' not in stock or 'target of' not in stock: 
        to_delete.append(i)
        continue

    stock = stock.split(';')

    first = stock[0].split()
    Call.append(first[0])
    Name.append(" ".join(first[1:]))
    
    Target.append(stock[1].split(':')[0][10:])
    Madeby.append(stock[1].split(':')[1])
    dates = pd.to_datetime(dates)
    i+=1

current = (date.today()-timedelta(days=0)).isoformat()
dates = list(dates)

for i in to_delete[::-1]:
    del dates[i]


d = {'Call':Call,'Stock':Name,'Target':Target,'Caller':Madeby,'Date':dates}
df = pd.DataFrame(d)
df = df[df['Date'] == current]



recipients = ["""comma separated emails"""] 
emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = "Daily tips"
msg['From'] = 'ksoni2980@gmail.com'


html = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(df.to_html())

part1 = MIMEText(html, 'html')
msg.attach(part1)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()  
server.login("enter sender's email addressemail-address", "enter password") 
server.sendmail(msg['From'], emaillist , msg.as_string())
server.quit()