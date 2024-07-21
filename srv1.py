from os import curdir 
from os.path import join as pjoin 
from http.server import BaseHTTPRequestHandler, HTTPServer 
import urllib.request
import gzip
import ssl
from urllib.parse import urlencode
import re
import string

import re
import json
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import base64
import yt_dlp

class StoreHandler (BaseHTTPRequestHandler): 
  def do_GET (self) : 
    if  '/gettube' in self.path : 
              url = self.path[8:]
              self.send_response (200) 
              self.send_header('Content-type', 'text/html') 
              self.end_headers()
              ydl_opts = {'format': 'best'}
              with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                lnk = info['url']
                self.wfile.write('<html><head><meta http-equiv="refresh" content="0; url=' + lnk + '"></head></html>')   
    
    elif self.path == '/': 
          store_path = pjoin (curdir, 'link.html') 
          with open (store_path) as fh: 
              self.send_response (200) 
              self.send_header('Content-type', 'text/html') 
              self.end_headers() 
              self.wfile.write(fh.read().encode() ) 
    elif self.path == '/watchurl11111111111': 
          store_path = pjoin (curdir, 'link.html') 
          with open (store_path) as fh: 
              self.send_response (200) 
              self.send_header('Content-type', 'text/html') 
              self.end_headers() 
              self.wfile.write(fh.read().encode() )

    elif '/elahmad/' in self.path : 
       ssl._create_default_https_context = ssl._create_unverified_context


       params = self.path[9:]
       print(params)


       headers = {
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Accept-Language': 'en-US,en;q=0.9',
          'Connection': 'keep-alive',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'Origin': 'http://www.elahmad.com',
          'Referer': 'http://www.elahmad.com/tv/watchtv.php?id='+params,
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
          'X-Requested-With': 'XMLHttpRequest',
       }

       req = urllib.request.Request(
          'https://www.elahmad.com/tv/mobiletv/glarb.php?id='+params,
          headers=headers,data=None)
       res = urllib.request.urlopen(req, timeout=10).read().decode('cp1252')
       res=res.replace("'",'"');
       
       chids=res.split('"'+params+'"')[0].split('"')
       chid=chids[len(chids)-2]
       key=res.split('my_crypt')[1].split('"')[1].split('"')[0]
       iv=res.split(key+'"')[1].split('"')[1].split('"')[0]

       #iv=iv.encode('utf-8')[:16]
       #Format the payload 
       data_payload={f'{chid}':params}
       data = urlencode(data_payload).encode("utf-8")


       req = urllib.request.Request('https://www.elahmad.com/tv/mobiletv/glarb.php',headers=headers, data=data)
       res = urllib.request.urlopen(req, timeout=10).read().decode('cp1252')

       aes_encrypted=res.split(':"')[1].split('"')[0]

       if 1>0:
        iv =  iv.encode('utf-8') #16 char for AES128
        enc = base64.b64decode(aes_encrypted)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        url = unpad(cipher.decrypt(enc),16)
        url=url.decode('utf-8')
        str =  url+ " "
        if 2>1: 
              self.send_response (200) 
              self.send_header('Content-type', 'text/html') 
              self.end_headers()
              str = '<html><head><meta http-equiv="refresh" content="0; url=' + str  + '"></head></html>'
              self.wfile.write(str.encode()) 
              
    else: 
      store_path = pjoin(curdir, 'link.html') 
      with open (store_path, 'w') as fh: 
         fh.write('<html><head><meta http-equiv="refresh" content="0; url=' + self.path[11:]  + '"></head></html>') 
         self.send_response (200) 
server = HTTPServer (('',  7775), StoreHandler)
server.serve_forever()
