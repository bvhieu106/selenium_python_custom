import time
from api_automation import *
from Connect_selenium import *
import re
import time
from termcolor import colored
import random
import concurrent.futures
import os
error_profiles = []
used_uuids = set()
def disconnect_and_reconnect(driver, port):
    driver.quit()  # Close the existing Chrome WebDriver instance
    time.sleep(5)  # Wait for 5 seconds before reconnecting
    driver = connect_to_debug_port(port)  # Create a new Chrome WebDriver instance
    return driver
used_uuids = set()
def get_unused_uuid(index):
    global used_uuids
    url = "http://127.0.0.1:5555/profileList?page=1&limit=100"#adjust 

    # Send an HTTP GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Access the "content" key in the JSON data
        uuid_list = [item["uuid"] for item in data["data"]["content"]]
        
        # Find an unused UUID at the specified index
        for i, uuid in enumerate(uuid_list):
            if uuid not in used_uuids:
                used_uuids.add(uuid)
                if i == index:
                    return uuid
    
    return None

error_urls = []



num = list(range(1,1+1)) # list start from 1-100 adjust above  if you have more than 100 profile 




def process_chrome_profile(chrome_profile, uuid):
    if uuid:
    
        print(f'Acc {chrome_profile}')
# URL của yêu cầu POST
        try:
            
            
            
            remote_port = OpenProfile(uuid)
            
            print("Remote port --->  ",remote_port)
           # time.sleep(5)
            driver = connect_to_debug_port(remote_port)
            #ur code here 
           
         
        
  
    

        

        

         
            url = f'http://127.0.0.1:5555/closeProfile?uuid={uuid}'
          #  response = requests.get(url)
           # url = "http://127.0.0.1:5555/delete-profile"
            #data = {
            #"uuid_browser": [uuid]}
        # Gửi yêu cầu DELETE
            #response = requests.delete(url, json=data)
            #print(response.text)
            # #get requets
            # GetRequest(driver) 
         
        except Exception as e:
            print("Error processing Acc", chrome_profile)
            print(str(e))
            error_profiles.append(chrome_profile)
            url = f'http://127.0.0.1:5555/closeProfile?uuid={uuid}'
            response = requests.get(url)




def TestScript():
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for n in num:
            # Subtract 1 to get the correct index since Python lists are zero-based
            index = n - 1
            uuid = get_unused_uuid(index)
            if uuid:
                executor.submit(process_chrome_profile, n, uuid)
                time.sleep(6)

TestScript()
print("Error profiles:", error_profiles)
print("Error url:", error_urls)
