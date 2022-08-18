# ============================= FORM ============================= #
#@markdown <br><center><img src='https://www.v2ray.com/resources/v2ray_1024.png' height="100" alt="V2Ray"/></center>
#@markdown <center><h3>V2Ray<br />An free and open-source proxy server</h3></center><br>
USE_FREE_TOKEN = True  # @param {type:"boolean"}
TOKEN = ""  # @param {type:"string"}
REGION = "JP" #@param ["US", "EU", "AP", "AU", "SA", "JP", "IN"]
ID=""  # @param {type:"string"}
DEFAULT_SET = True  # @param {type:"boolean"}
PORT_FORWARD = "argotunnel" #@param ["ngrok", "localhost", "argotunnel"]
RUN_WITH_LATEST = False  # @param {type:"boolean"}
# ================================================================ #

import json
import base64
import uuid
import os
import urllib.request
import re

from subprocess import Popen
import pandas as pd
import requests

HOME = os.path.expanduser("~")



def v2ray(id=None, port=9999):
  if RUN_WITH_LATEST:
    found = findPackageR('v2fly/v2ray-core', 'v2ray-linux-64.zip', all_=True)
    downUrl = found['assets']['browser_download_url']
    tagName = found['tag_name']
  else:
    downUrl = 'https://github.com/v2fly/v2ray-core/releases/download/v4.45.2/v2ray-linux-64.zip'
    tagName = 'v4.45.2'
  
  print(f"Installing v2ray {tagName} ...")
  if not os.path.exists("tools/v2raybin"):
    os.system(f'mkdir -p -m 777 tools/v2raybin && cd tools/v2raybin  && curl -L -H "Cache-Control: no-cache" -o v2ray.zip {downUrl} && unzip v2ray.zip  && chmod +x v2ray  && rm -rf v2ray.zip  && chgrp -R 0 ../  && chmod -R g+rwX ../')
  CONFIG_JSON1="{\"log\":{\"access\":\"\",\"error\":\"\",\"loglevel\":\"warning\"},\"inbound\":{\"protocol\":\"vmess\",\"port\":"
  CONFIG_JSON2=",\"settings\":{\"clients\":[{\"id\":\""
  CONFIG_JSON3="\",\"alterId\":64}]},\"streamSettings\":{\"network\":\"ws\"}},\"inboundDetour\":[],\"outbound\":{\"protocol\":\"freedom\",\"settings\":{}}}"
  with open("tools/v2raybin/config.json", "w") as f:
    f.write(CONFIG_JSON1+str(port)+CONFIG_JSON2+id+CONFIG_JSON3)
  
  
  Popen("./v2ray run".split(), cwd='tools/v2raybin/', env={'V2RAY_VMESS_AEAD_FORCED':'false'})

port=9910

if not ID:
  ID=str(uuid.uuid4())
print("Setting up v2ray server ... ")
v2ray(ID,port)
print("Setting up tunnel ... ")
Server = PortForward_wrapper(
    PORT_FORWARD, TOKEN, USE_FREE_TOKEN, [['v2ray', port, 'http']],
    REGION.lower(), [f"{HOME}/.ngrok2/V2ray.yml", 8097]
).start('v2ray', displayB=False)

d=json.loads('{"add":"{0}","aid":"64","host":"","id":"{1}","net":"ws","path":"","port":"80","ps":"1","tls":"","type":"none","v":"2"}')
d["add"]=re.search("(?<=//).*?(/|$)",Server["url"]).group()
d["id"]=ID
clear_output()
# print(d)
config="vmess://"+base64.b64encode(json.dumps(d).encode()).decode("utf-8")
print(config)



