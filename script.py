import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import uuid
import datetime
import requests

proxy_username = "sumexxx"  # Your ProxyMesh username
proxy_password = "12345678"  # Your ProxyMesh password
proxy_host = "open.proxymesh.com"
proxy_port = 31280
PROXY_URL = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"

# Set OS-level proxy environment variables
# os.environ['http_proxy'] = PROXY_URL
# os.environ['https_proxy'] = PROXY_URL

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['stir']
collection = db['trends']

# Twitter credentials
t_username = "SumanDebna2627"
t_password = "12345678stir"

def filter_trends(trends):
    dup_rem_trends = []
    last = ""
    for i in trends:
        if i.text != last:
            dup_rem_trends.append(i.text)
            last = i.text
    final = [i for i in dup_rem_trends if "Show more" not in i and "posts" not in i and "Trending" not in i and "happening" not in i]
    return [i for i in final]


def serialize_document(doc):
    doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    doc['dateTime'] = doc['dateTime'].strftime("%Y-%m-%d %H:%M:%S")
    return doc

def run_script():
    unique_id = str(uuid.uuid4())
    firefox_options = Options()
    firefox_options.binary_location = "/usr/bin/firefox-esr"
    # Use manual proxy configuration
    # firefox_options.set_preference("network.proxy.type", 1)

    # firefox_options.set_preference("network.proxy.http", proxy_host)  # HTTP Proxy
    # firefox_options.set_preference("network.proxy.http_port", proxy_port)  # HTTP Proxy Port
    # firefox_options.set_preference("network.proxy.ssl", proxy_host)  # SSL Proxy
    # firefox_options.set_preference("network.proxy.ssl_port", proxy_port)  # SSL Proxy Port
    # firefox_options.set_preference("network.proxy.ftp", proxy_host)  # FTP Proxy
    # firefox_options.set_preference("network.proxy.ftp_port", proxy_port)  # FTP Proxy Port
    # firefox_options.set_preference("network.proxy.socks", proxy_host)  # SOCKS Proxy
    # firefox_options.set_preference("network.proxy.socks_port", proxy_port)  # SOCKS Proxy Port
    # firefox_options.set_preference("network.proxy.socks_version", 5)  # SOCKS version

    # firefox_options.set_preference("network.proxy.authentication_enabled", True)

    service = Service("./firefox/geckodriver")
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        driver.get("https://x.com/login")

        # Log in to Twitter
        sleep(5)
        username = driver.find_element(By.NAME, "text")
        username.send_keys(t_username)
        username.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        password = driver.find_element(By.NAME, "password")
        password.send_keys(t_password)
        password.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//section[contains(., 'What’s happening')]"))
        )
        sleep(5)
        # Fetch top 5 trending topics
        trends = driver.find_elements(By.XPATH, "//section[contains(., 'What’s happening')]//span")
        trending_topics = filter_trends(trends)
        
        # Get IP address used
        ip_response = requests.get("http://ipinfo.io/json", proxies={"http": PROXY_URL, "https": PROXY_URL})
        ip_address = ip_response.json().get("ip")

        # Store data in MongoDB
        end_time = datetime.datetime.now()
        document = {
            "uniqueID": unique_id,
            "trend1": trending_topics[0] if len(trending_topics) > 0 else None,
            "trend2": trending_topics[1] if len(trending_topics) > 1 else None,
            "trend3": trending_topics[2] if len(trending_topics) > 2 else None,
            "trend4": trending_topics[3] if len(trending_topics) > 3 else None,
            "dateTime": end_time,
            "ipAddress": ip_address
        }

        collection.insert_one(document)
        serialized_document = serialize_document(collection.find_one({"uniqueID": unique_id}))
    
        return serialized_document
    finally:
        driver.quit()