import datetime
import logging
import random
import time
from turtle import title

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import chromedriver_autoinstaller
import json
from google.oauth2 import service_account

from googleapiclient.discovery import build
chromedriver_autoinstaller.install()
from seleniumwire import webdriver
import time
import pickle

logged_in=False

class Instabot:
    def __init__(self):
        global driver
        global logged_in
        global SAMPLE_SPREADSHEET_ID
        global SERVICE_ACCOUNT_FILE
        global SCOPES

        
        with open("proxy.txt","r") as file:
            ip_port=file.readlines()[0].replace("\n","").strip()

        # replace 'user:pass@ip:port' with your information
        options = {
            'proxy': {
                'http': ip_port,
                'https': ip_port,
                'no_proxy': 'localhost,127.0.0.1'
            }

        }

        with open("sheetID.txt","r") as file:
            SAMPLE_SPREADSHEET_ID=file.readlines()[0].replace("\n","")
        SERVICE_ACCOUNT_FILE = 'keys.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--lang=en-GB")
        #options.headless = True
        service = ChromeService()
        driver=webdriver.Chrome(seleniumwire_options=options,options=chrome_options)
        self.createSS()
        self.start()

    
    """""
    def starter(self):
        global SAMPLE_SPREADSHEET_ID
        global SERVICE_ACCOUNT_FILE
        global SCOPES

        
        with open("sheetID.txt","r") as file:
            SAMPLE_SPREADSHEET_ID=file.readlines()[0].replace("\n","")
        SERVICE_ACCOUNT_FILE = 'keys.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.createSS()
        self.start()

    """""

    #WHEN PROGRAM STARTS IT CREATES WORKSHEETS
    def createSS(self):

        
        creds=None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)


        try:
            service = build('sheets', 'v4', credentials=creds)
        except:
            DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
            service = build('sheets', 'v4', credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)

        with open("accounts.txt","r")as file:
            title_list=file.readlines()

            
            
        values=[["Date","Followers","Following","Posts"]]
        
        for name in title_list:
            try:
                title= name.split(":")[0].strip().replace("\n","")
                insta_name=name.split(":")[1].replace("\n","").strip()
            except:
                title=name.replace("\n","").strip()
                insta_name=name.replace("\n","").strip()
            instagram=[["Instagram Account:",insta_name]]
            # Call the Sheets API
            sheet = service.spreadsheets()

            request_body = {
                        'requests': [{
                            'addSheet': {
                                'properties': {
                                    'title': title,
                                    'tabColor': {
                                        'red': 0.44,
                                        'green': 0.99,
                                        'blue': 0.50
                                    }
                                }
                            }
                        }]
                    }
            try:
                
                response = service.spreadsheets().batchUpdate(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    body=request_body
                ).execute()

                creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

                try:
                    service = build('sheets', 'v4', credentials=creds)
                except:
                    DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
                    service = build('sheets', 'v4', credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)

                request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"{title}!A1", valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS", body={"values":instagram}).execute()
                request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"{title}!A1", valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS", body={"values":values}).execute()
            except:
                pass

    def writeSS(self,values,title):
        SERVICE_ACCOUNT_FILE = 'keys.json'
        creds=None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)


        try:
            service = build('sheets', 'v4', credentials=creds)
        except:
            DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
            service = build('sheets', 'v4', credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)

        # Call the Sheets API
        sheet = service.spreadsheets()
        #result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                            range="insta!B2").execute()
        #values = result.get('values', [])
        #print(result)
        values=[values]
        
        try:
            request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"{title}!A1", valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS", body={"values":values}).execute()
        except:
            pass

        
    def start(self):
        
        with open("accounts.txt","r")as file:
            inst_list=file.readlines()

        if logged_in==False:

            driver.get(f"https://www.instagram.com/")
            time.sleep(300)
            pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
            
        else:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)

        logged_in=True
        
        today = datetime.datetime.now().strftime("%d %B %Y")
        for link in inst_list:
            #0 date, 1 followers, 2 following, 3 post
            item_list=[]
            
            for i in range(0,5):
                item_list.append("")
            item_list[0]=json.dumps(today, indent=4, sort_keys=True, default=str).replace('"','')
            try:
                search_query=link.split(':')[1].replace('\n','').strip()
            except:
                search_query=link.replace('\n','').strip()

            driver.get(f"https://www.instagram.com/{search_query}/")

            item_list[1]=WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH,"//div[contains(text(),' followers')]/span"))).text
            
            time.sleep(2)
            
            item_list[2]=driver.find_element(By.XPATH,"//div[contains(text(),' following')]/span").text
            
            item_list[3]=driver.find_element(By.XPATH,"//div[contains(text(),' posts')]/span").text
            try:
                title=link.split(":")[0].replace("\n","").strip()
            except:
                title=link.replace("\n","").strip()
            self.writeSS(item_list,title)
 
            
        
  

while True:
    print("\t\tTodays scraping starting")
    ig=Instabot()
    print("\n\n\t\tTodays scraping Finished")
    #time.sleep(86400+random.randint(0,200))
    time.sleep(1)




