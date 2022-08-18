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
from IPython.display import HTML, clear_output
from subprocess import Popen
import pandas as pd
import requests

HOME = os.path.expanduser("~")
if not os.path.exists(f"{HOME}/.ipython/ocr.py"):
    hCode = "https://raw.githubusercontent.com/biplobsd/" \
                "OneClickRun/master/res/ocr.py"
    urllib.request.urlretrieve(hCode, f"{HOME}/.ipython/ocr.py")

from ocr import PortForward_wrapper, findPackageR, textAn, findProcess

def show_qr(text, v=True):
  try:
    from MyQR import myqr
  except:
    Popen("pip install myqr".split()).wait()
  Popen(["myqr",text]+"--version 5 --level H -n qrcode.png -d /tmp".split()).wait()
  if v:
    from PIL import Image
    im = Image.open("/tmp/qrcode.png")
    os.remove("/tmp/qrcode.png")
    im.show()
    import matplotlib.pyplot as plt
    plt.figure(figsize=(5,5))
    plt.imshow(im)
    plt.axis('off')
    plt.show()
  else:
    with open("/tmp/qrcode.png", "rb") as imageFile:
      imgb64 = base64.b64encode(imageFile.read())
    os.remove("/tmp/qrcode.png")
    return imgb64

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
  
  if not findProcess('./v2ray','run'):
    return Popen("./v2ray run".split(), cwd='tools/v2raybin/', env={'V2RAY_VMESS_AEAD_FORCED':'false'})

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
# print(config)
imgb64 = show_qr(config, v=False).decode()
df_marks = pd.Series(d).to_frame("V2Ray Config")
html = df_marks.to_html(classes="zui-table blueBG")
display(HTML("""<style>@import url('https://fonts.googleapis.com/css?family=Source+Code+Pro:200,900');  :root {   --text-color: hsla(210, 50%, 85%, 1);   --shadow-color: hsla(210, 40%, 52%, .4);   --btn-color: hsl(210, 80%, 42%);   --bg-color: #141218; }  * {   box-sizing: border-box; } button { position:relative; padding: 10px 20px;     border: none;   background: none;      font-family: "Source Code Pro";   font-weight: 900;font-size: 100%;     color: var(--text-color);      background-color: var(--btn-color);   box-shadow: var(--shadow-color) 2px 2px 22px;   border-radius: 4px;    z-index: 0;overflow: hidden; -webkit-user-select: text;-moz-user-select: text;-ms-user-select: text;user-select: text;}  button:focus {   outline-color: transparent;   box-shadow: var(--btn-color) 2px 2px 22px; }  .right::after, button::after {   content: var(--content);   display: block;   position: absolute;   white-space: nowrap;   padding: 40px 40px;   pointer-events:none; }  button::after{   font-weight: 200;   top: -30px;   left: -20px; }   .right, .left {   position: absolute;   width: 100%;   height: 100%;   top: 0; } .right {   left: 66%; } .left {   right: 66%; } .right::after {   top: -30px;   left: calc(-66% - 20px);      background-color: var(--bg-color);   color:transparent;   transition: transform .4s ease-out;   transform: translate(0, -90%) rotate(0deg) }  button:hover .right::after {   transform: translate(0, -47%) rotate(0deg) }  button .right:hover::after {   transform: translate(0, -50%) rotate(-7deg) }  button .left:hover ~ .right::after {   transform: translate(0, -50%) rotate(7deg) }  /* bubbles */ button::before {   content: '';   pointer-events: none;   opacity: .6;   background:     radial-gradient(circle at 20% 35%,  transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),     radial-gradient(circle at 75% 44%, transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),     radial-gradient(circle at 46% 52%, transparent 0, transparent 4px, var(--text-color) 5px, var(--text-color) 6px, transparent 6px);    width: 100%;   height: 300%;   top: 0;   left: 0;   position: absolute;   animation: bubbles 5s linear infinite both; }  @keyframes bubbles {   from {     transform: translate();   }   to {     transform: translate(0, -66.666%);   } }.zui-table {border: solid 1px #DDEEEE;    border-collapse: collapse;    border-spacing: 0;    font: normal 13px;}.zui-table thead th {    background-color: #DDEFEF;    border: solid 1px #DDEEEE;    color: #0000009e;    padding: 10px;    text-align: left;}.zui-table tbody td {border: solid 1px #effff97a;color: #ffffffd1;    padding: 10px;}</style><center><button style="width: 60%" onclick="copy_text_fun()"><img style="width: 40%;" src="data:image/png;base64, """+imgb64+""""/><div style="text-align: -webkit-center;">"""+html+"""</div><a target="_blank" style="text-decoration: none;color: hsla(210, 50%, 85%, 1);font-size: 10px;" href="https://bit.ly/34E09QG">NB. How to setup this's config. [Click ME]</a></button><center>"""))
display(HTML("""<script type="text/javascript">function copy_text_fun() {var copyText = document.getElementById("copy_txt"); var input = document.createElement("textarea");input.value = copyText.textContent;document.body.appendChild(input);input.select();document.execCommand("Copy");input.remove();}</script><p hidden id="copy_txt">"""+config+"""</p>"""))
