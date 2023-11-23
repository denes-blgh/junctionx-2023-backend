import os
import sys
import hashlib

def get_port(branch: str):
    return int(hashlib.sha256(branch.encode()).digest()) % 50000 + 10000

branches = []
with open("/etc/nginx/branches", "r") as file:
    for branch in file.read().split("\n"):
        if branch != "":
            branches.append(branch)

new = sys.argv[1]
new_port = get_port(new)

if new not in branches:
    branches.append(new)

print(branches)

config = ""

os.system(f"docker stop junctionx_{new}")
os.system(f"docker rm junctionx_{new}")

os.system(f"docker build -t junctionx .")
os.system(f"docker run -d -p {new_port}:7000 --name junctionx_{new} junctionx")

for branch in branches:
    port = get_port(branch)

    config += """
        location ~ ^/junctionx/%s/(.*)$ {
            rewrite ^/junctionx/%s/(.*) /$1 break;
            proxy_pass http://127.0.0.1:%s;
        }
    """ % branch, branch, port

with open("/etc/nginx/nginx.conf", "w") as file:

    with open("/etc/nginx/nginx.conf.begin", "r") as begin:
        file.write(begin.read())

    file.write(config)

    with open("/etc/nginx/nginx.conf.end", "r") as end:
        file.write(end.read())

os.system("systemctl restart nginx")

with open("/etc/nginx/branches", "w") as file:
    for branch in branches:
        file.write(branch + "\n")
