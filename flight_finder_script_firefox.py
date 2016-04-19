import urllib2, re, sys, smtplib
from ConfigParser import SafeConfigParser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os
# import selenium.webdriver.chrome.service as service
from pyvirtualdisplay import Display
from selenium import webdriver


"""Login to Gmail and send notification email with body (msg)."""
def sendGmailMessage(username,password,msg_price):
    # print (username)
    # print (password)

    fromaddr = username
    toaddrs  = ['tstilwell@gmail.com']

    msg = "\r\n".join([
    "From: "+username,
    "To: "+toaddrs[0],
    "Subject: Flight to Chicago 4th of July!",
    "",
    msg_price
    ])

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def checkOpodo(searchURL,maxPrice,username,password):
    minPrice=10
    price = selenium_test(searchURL)
    print ("lowest price is",price)
    # if price < minPrice: minPrice = price
    if price < maxPrice:
        message = "Time to check the flight company; the flight is available for "+str(price)+" kroner.\nFollow this link for the search results: "+searchURL+"\nGo, go, go!"
        print (message)
        sendGmailMessage(username,password,message)
        return 
    print ('Min price for search was '+str(maxPrice)+'... better luck next time!')
    return 


def print_elm(element):
    try:    
        print ("len price_elem inside:",len(element))
        # print ("price_elem:",element)
        for i in range(len(element)):
            print ("element:",i,element[i])
            print ("element:",i,element[i].text)
            print ("element:",i,element[i].tag_name)
            print ("element:",i,element[i].parent)
            print ("element:",i,element[i].location)
            print ("element:",i,element[i].size)
    except:
        print ("element:",element.text)
        print ("element:",element.tag_name)
        print ("element:",element.parent)
        print ("element:",element.location)
        print ("element:",element.size)
        out = element.text
        out = out.replace("kr", "")
        out = out.replace(" ", "")
        print (out)
        # print ("element:",element)
    return out

def selenium_test(searchURL):

    display = Display(visible=0, size=(1024, 768))
    display.start()
    
    browser = webdriver.Firefox()#'/usr/bin/firefox/firefox'
    time.sleep(3)
    yahoo = browser.get(searchURL)
    time.sleep(5)
    price_elem =  browser.find_element_by_class_name('MHNSJI-d-zb')
    price = print_elm(price_elem)
    browser.quit()
    try:
        return_price = int(price)
    except:
        return_price = price
    return return_price

if __name__ == "__main__":

    parser = SafeConfigParser()
    config = os.path.normpath(os.path.join(os.path.realpath(__file__),"..","config.txt"))
    print (config)
    parser.read(config)
    
    try:
        gmailUser = parser.get('emailSettings','gmailUsername')
        gmailPassword = parser.get('emailSettings','gmailPassword')
    except Exception:
        sys.exit('Could not find/parse email settings in config.txt')
    
    try:
        priceMax= parser.getfloat('searchSettings',"flightMaxPriceForEmail")
        searchURL= parser.get('searchSettings',"searchURL",1)
    except Exception:
        sys.exit('Could not find/parse search settings in config.txt')

    checkOpodo(searchURL,priceMax,gmailUser,gmailPassword)
