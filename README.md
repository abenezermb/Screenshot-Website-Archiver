# Screenshot-Website-Archiver
takes a list of URLs, opens each in a headless browser, and saves full-page screenshots for documentation or auditing.

python3 -m venv env```

Step 2: Activate virtual environment
```bash
source env/bin/activate```

Step 3: Install dependencies
```bash
pip3 install -r requirements.txt```

Step 4: Add list of urls in urls.txt

Step 5: Run website-archiver.py
```bash
python3 website-archiver.py -i urls.txt -o screenshots```