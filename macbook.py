from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import mysql.connector as mcon
import streamlit as st
import pandas as pd
import plotly.express as px
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime




st.title("Scrapping Automation Project")

link = "https://www.ebay.com/itm/134638042371?_trkparms=pageci%3Acd839362-65cc-11ee-97da-8aa74efc965f%7Cparentrq%3A0f052b2b18b0acf322cec22dfffed4fc%7Ciid%3A1&var=434175605789"

response= urlopen(link)# it helps to open a link

html_data=response.read() # it helps to read the link data

soup_data = soup(html_data, "html.parser")  # it helps to convert into beautifulsoup

soup_data.prettify()

name = soup_data.find("h1",{"class":"x-item-title__mainTitle"}).text.replace('"',"")[0:18].strip()

price = float(soup_data.find("div",{"class":"x-price-primary"}).text.strip("US $"))

db=mcon.connect(host="localhost",user="root",password="Shashank@098")

cursor = db.cursor() # create a cursor object


cursor.execute("create database if not exists automation")  # helps to create a database in mysql with the help of python

cursor.execute("use automation")

cursor.execute("create table if not exists macbook(date datetime,product_name varchar(255),price float)")

cursor.execute("select * from macbook")
data = pd.DataFrame(cursor.fetchall(),columns = ["Date","Product Name","Price"])

# Making a Line Plot
fig = px.line(data_frame = data,
              x = 'Date',
              y = 'Price'
              ,title='Trend Analysis of Macbook Price')
st.plotly_chart(fig)

# Displaying data which is stored in SQL DataBase
st.table(data)




cursor.execute("select price from automation.macbook order by date desc limit 1")
last_price = cursor.fetchall()[0][0]

# insert a new data into the data base
cursor.execute(f"insert into macbook values(current_timestamp(),'{name}',{price})")

# this helps to show data in streamlit
st.write(f"record({name}, {price}) inserted successfully")

# SENDING MAIL
def send_mail():
    # Outlook SMTP server and port
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    # Your Outlook email address and password
    email_address = 'shashanktheking1997@outlook.com'
    email_password = 'Qwert@123qwert'

    # Recipient's email address
    recipient_email = 'shashanktheking1997@outlook.com'

    # Create the email message
    subject = 'Macbook Current price'
    message = f"""
    # Product Information

    **Date**: {datetime.datetime.now().strftime("%d-%m-%y")},{name},{price}
    **Product**: {name}
    **Price**: ${price:.2f}

    This is the best time to buy!!!!
    the price is dropped from ${last_price} to ${price}
    price difference : ${last_price - price}
    Thanks and Regards
    """

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Establish an SMTP connection with Outlook
    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, recipient_email, msg.as_string())
        server.quit()
        st.write("Email sent successfully.")
    except Exception as e:
        st.write("Error: Could not send email.")
        st.write(e)
if price<last_price:
    send_mail()
else:
    st.write("no price change!!!Email not sent")    


db.commit()

db.close()
#{datetime.datetime.now().strftime("%d-%m-%y")},{name},{price}'


