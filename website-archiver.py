import os
import argparse
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class WebsiteArchiver:
    
    def screenshot_url(self,driver,url,output_dir):
        
        # add error handling
        driver.get(url)
        
        # Give the page sometime to render
        driver.implicitly_wait(2)
        
        # get the page dimensions
        total_width = driver.execute_script("return document.body.scrollWidth")
        total_height = driver.execute_script("return document.body.scrollHeight")
        
        # set viewport to full size
        driver.set_window_size(total_width,total_height)
        
        # create a safe filename
        parsed = urlparse(url)
        fname = f"{parsed.netloc}{parsed.path}".replace("/","_").strip("_")
        if not fname:
            fname = "root"
        fname+=".png"
        
        path= os.path.join(output_dir,fname)
        driver.save_screenshot(path)
        print(f"[+] save {url} -> {path}")
        
