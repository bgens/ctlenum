# ctlenum
Enumeration of Certificate Transparency Logs

**Requirements:**
  - ```pip install requests```
  - ```pip install argparse```
  - API Key for sslmate's certspotter:
    - Register an account with sslmate.com (certspotter)
    - Grab API Key from: https://sslmate.com/account/api_credentials
  - Install google chrome or google chromium
  - Download latest version of chrome webdriver from: https://chromedriver.chromium.org/downloads
  - Place webdriver in the ctlenum directory

**Before using:**
  - edit 'config.py' and place your API key in the config file
  - example: ```API_KEY = "legitimate_key"```

**Basic Use:**
If outputting results to a list, for use with nmap and/or other scanning tools, ideal usage will be with no arguments.

```python ctlenum.py --target targetdomain```

**Arguments:**

 --target sets target domain
 
 -s scan
 
 -ss scan & screenshot
  - Example: \*.example.com

**Example w/ Arguments:**

   ```python ctlenum.py -ss --target example.com```
   
