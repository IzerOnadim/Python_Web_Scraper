# Scrapes price of given amazon product and sends you an email when price falls
# below a given point. Checks the price once a day.
import pandas as pd
import requests
import smtplib
import time
from bs4 import BeautifulSoup

# this is a book on Steve Jobs. You can use any the URL of any amazon product.
URL = ("https://www.amazon.co.uk/"
       "dp/034914043X/?coliid=I3FQBX38L6G2AZ&colid=3AFQK0FN3MIJI&psc=1")

headers = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          "AppleWebKit/537.36 (KHTML, like Gecko)"
                          "Chrome/78.0.3904.97 Safari/537.36")}

def check_price(minThreshold):
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(class_="a-size-base a-color-price a-color-price").get_text()
    # convert to float so that you can compare
    convertedPrice = float(price.strip()[1:5])

    if (convertedPrice < minThreshold):
        send_mail()

def send_mail():
    # start start up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # to do this set up a google app password so you are not using your normal
    # password
    server.login('someone@gmail.com', 'generate a password to go here')

    # this is what the email will contain.
    subject = f"The price has fallen"
    body = ("check the amazon link https://www.amazon.co.uk/"
            "dp/034914043X/?coliid=I3FQBX38L6G2AZ&colid=3AFQK0FN3MIJI&psc=1")
    msg = f"Subject: {subject}\n\n{body}"

    #send the email
    server.sendmail(
        'someone@gmail.com',
        'email to send alert to.',
        msg
    )
    # print confirmation message.
    print('Email has been sent.')
    # exit server
    server.quit()

while(True):
    # checks price once a day.
    check_price(8.00)
    time.sleep(60*60*24)
