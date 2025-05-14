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
        
def main():
    parser = argparse.ArgumentParser(
        description="Headless full-page screenshot archiver"
    )
    
    parser.add_argument('-i','--input-file',help="Text file with one url per line")
    parser.add_argument('-o','output-dir',default='Screenshots',help='Directory to save screenshots (will be created)')
    parser.add_argument('urls',nargs="*",help = "One or more urls (ignored if -i/--input-file is used)")
    
    args = parser.parse_args()
    # collect urls
    if args.input_file:
        with open(args.input_file) as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        urls = args.urls
        
    if not urls:
        parser.error("No urls provided (either via -i or positional args)")
        
    # prepare output dir
    os.makedirs(args.output_dir,exist_ok=True)
    
