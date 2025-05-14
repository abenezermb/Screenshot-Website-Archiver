import os
import argparse
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager,ChromeType
# from webdriver_manager.core.utils import ChromeType


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
    
    def launch_headless_browser(self, urls,output_dir):
        options = webdriver.ChromeOptions()

        # Use the new headless mode (Chrome 109+)
        options.add_argument("--headless=new")

        # Sandbox flags (required in many Linux environments, CI, Docker, etc.)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Needed to get DevToolsActivePort working
        options.add_argument("--remote-debugging-port=9222")

        # Optional: hide logs
        options.add_argument("--log-level=3")

        # If Chrome isn't on your PATH, point directly to its binary:
        # options.binary_location = "/usr/bin/google-chrome-stable"

        # Point at your snap-installed Chromium:
        options.binary_location = "/snap/bin/chromium"

        # Install a Chromium-specific driver instead of the default Google-Chrome one:
        service = Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        )
        driver = webdriver.Chrome(service=service, options=options)

        try:
            for url in urls:
                self.screenshot_url(driver, url,output_dir)
        finally:
            driver.quit()
        
def main():
    parser = argparse.ArgumentParser(
        description="Headless full-page screenshot archiver"
    )
    
    parser.add_argument('-i','--input-file',help="Text file with one url per line")
    parser.add_argument('-o','--output-dir',default='Screenshots',help='Directory to save screenshots (will be created)')
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
        
    if not args.output_dir:
        parser.error("Error! Output directory should be specified.")
        
    # prepare output dir
    os.makedirs(args.output_dir,exist_ok=True)
    
    # create an object
    archiver = WebsiteArchiver()
    archiver.launch_headless_browser(urls,args.output_dir)
    

if __name__ == "__main__":
    main()
    
    


        