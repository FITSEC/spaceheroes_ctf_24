import subprocess
import os
import random

import socket
import requests
import hashlib
from flask import Flask, request, redirect

app = Flask(__name__)

get_md5 = lambda s: hashlib.md5(s.encode('utf-8')).hexdigest()

def get_random_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return port

@app.route('/')
def start_container():
    port_inside = 3000
    user_ip = request.remote_addr
    container_name = f"mars_{user_ip}"
    external_ip = "74.207.229.213" # External IP address
    key = get_md5(user_ip)
    port_outside = subprocess.run(f"docker ps | awk -F \'[: -]\' \'/{user_ip}/{{print $32}}\' ", shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip("\n")
    if port_outside is None or port_outside == '': port_outside = get_random_unused_port()

    subprocess.run(f"cp -r /root/martiansonly/docker/src/www/profiles /root/profiles/{key}; rm -f /root/martiansonly/docker/src/www/profiles/profiles", shell=True, check=False)
    
    docker_command = f"docker run -v \"/root/profiles/{key}/:/src/www/profiles/\" -e \"KEY={key}\" --name {container_name} --rm -d -p {port_outside}:{port_inside} martions"
    
    print(docker_command)
    subprocess.run(f"docker kill {container_name}", shell=True, check=False)
    #try:
    subprocess.run(docker_command, shell=True, check=False)
    return redirect(f"http://{external_ip}:{port_outside}/{key}/")
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

