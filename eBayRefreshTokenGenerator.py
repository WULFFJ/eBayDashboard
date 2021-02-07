###### This will only need ran once every 18 months.  The refresh token can be used to get new Auth Tokens for the eBay Dashboard Script.  If you get captcha during this process, re-run this script. It happens about 20% of the time.
###### Everything with YOURWHATEVER will need replaced with your actual informatinn from your own eBay Developer Account.
import pandas as pd
import urllib
import webbrowser
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
import requests
import base64
import time
from pywinauto import application

###### Long list of all the scopes assigned to my API..find under Get a Token from eBay via Your Application...make sure you are in production enviornment, click Get a Token via Your eBay Application, click oAuth at the bottom and click "See All" under "Your branded eBay Production Sign In (OAuth)".  You will needs to copy everything after "scope=" and paste in the line below between the two quotations marks.  This will urlencode the string. 

scopes=urllib.parse.quote('https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/commerce.identity.readonly')



###### #This setups the request to get authorization from the user.  If using my eBay dashboard script, the user will be you, via your eBay sellers account. ****Note***** If you are burdened with captcha (happens about 1/5 times, you will have to re-run this script).

rl=('https://auth.ebay.com/oauth2/authorize?'
    'client_id=YOURCLIENTID&'
    'redirect_uri=YOURREDIRECTURI&'
    'response_type=code&'
    'state=JUSTPUTAVALUEHEREOFWHATEVER&'
    f'scope={scopes}&'
    'prompt=login'
   )

###### Two lines below are only to check that the line is being configured correctly.

link=requests.post(rl)
print(link)

###### Calling Selenium for Chrome to open a pop-up Window for user login.  If using my eBay dashboard script, this will be you signing into your eBay sellers account, with appropriate login.

driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Python\chromedriver_win32\chromedriver.exe')
driver.maximize_window()
driver.get(rl)

###### The time function below, gives you 20 seconds to type your username, password and click the "I agree button".  You will be consenting to give your eBay developer account permission to access your eBay sellers account.

time.sleep(20)

###### After the 20 seconds, (which you can change to be sooner) Selenium will grab the link from the address bar url, which contains the code needed to proceed with granting the codes needed ahead.

aclink=driver.current_url #Selenium captures the URL containing the code for the initial credentials grant

acode=aclink[105:223] #parsed portion of the response that you need
driver.close() #Selenium closes the Chrome Browser

print(aclink) #Just for you to see it is working correctly.  You use the portion that proceeds "code=".

###### Initial access token request.  I do not use this access token but merely use it to get the refresh token.  The refresh token is good for 18 months instead of 2 hours.  The refresh token will generate you a new access token, each time you run the eBay dashboard script.  

###### Access token credentials from your developer account

secret='YOURCLIENTSECRETBETWEENTHESEQUOTES' #Client secret found under "Application Keys in your developer account" *Make sure everything is set for production"
cid=’YOURCLIENTIDBETWEENTHESEQUOTES' #Client id can be found under the same place as Client Secret

#This base 64 encodes the Client ID and Client Secret.  Adds the word "Basic", which requires a space between it and the base64 encoded credentials
aencoded='Basic ' + base64.b64encode((cid + ':' + secret).encode()).decode()

EURL='https://api.ebay.com/identity/v1/oauth2/token?' #oAuth token request URL

###### Headers follow the instruction of the eBay Developer guide

headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization" : aencoded
    }

###### Body of the post request consists of the grant-type, the authorization code from variable (acode) and the redirect uri, that you can find on the User Token Page.  (Make sure you are in production environment and click "Get Token from eBay via your application").  It will be labeled RuName (eBay Redirect URL name).

Rbody=('grant_type=authorization_code&'f'code={acode}&''redirect_uri=REPLACETHISWITHYOURREDIRECTURI')

arequest=requests.post(EURL,headers=headers, data=Rbody).json() #This isi the actual request

print(arequest) #Visual to see the response and different elemtents,so to know what needs parsed

###### Two items needed 1.Access Token and 2.Refresh Token from the response

atoken=(arequest['access_token'])

rtoken=(arequest['refresh_token'])
print(rtoken)

###### Copy the Refresh token, you will need to paste it into the eBay Dashboard script

print(atoken) #Authorization
