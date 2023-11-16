# PR PDF - scan documents explorer and automation 
Preview and Rename PDF Explorer\ A webbased document explorer and automation. For easy view, rename and move scanned PDF files.
  
## Background and Motivation:  
I was searching for a easy to use solution to get my letters and paper digital.  
Since I was searching for a solution for my unraid NAS, solutions like paperwork dont work as docker/in web or on many computer.  
Programs like Paperless and Papermerge are great but much to heavy with database etc.  
I like to keep my files in a normal folder structure to share and access them from every pc.  
Thats how PR PDF started. As an lightwight easy to use web based application to make it easy to preview, rename and move scanned documents.  
  
## BETA Note:  
This program is very new and theres a lot to test. Please report issues to the issues tab on github.

## Functions:
* PDF OCR Autoscan will move known documents based on keywords
* Preview and Rename documents from a web browser
* PDF Merge let you merge documents (1+1 and front and back pages)
* Split documents 
* Manual rename and move

## How it works:
1. Documents get scanned to a scan-folder 
2. these documents will be autoscanned and moved to the specific locations
3. Any files that are not recognized by autoscan will be moved to the subfolder "unknown" of the scan-folder
4. The Webbased PR PDF Explorer lists all documents of the "unknown" folder.

## How it looks like:

![Explorer](https://i.ibb.co/b723gYv/Explorer.jpg)
![OCR](https://i.ibb.co/JQb8Frf/OCR.jpg)

# Install and run

## Run as docker
` docker pull knex666/prpdf`

` docker run -d --name='PRPDF' -p 80:80 -v '/mnt/user/Share':'/Archiv/':'rw' -v '/mnt/user/SCAN':'/source/static/pdf/':'rw' -v '/mnt/user/appdata/prpdf/':'/source/config':'rw' 'knex666/prpdf' python3 /source/main.py`

* Note 1: remember to setup the network to map the port of your configuration ` -p 80:80` you can choose any port you want see config
* Note 2: besited a folder structure for documents in a folder you mount to /Archiv/ you can volume mount any directory you want to /Archiv/ to build you own virtual folder structure
` -v '/mnt/user/Files/Accounting':'/Archiv/Accounting':'rw'` etc.

## Run with python on linux
Note: Please ensure to run it from /source/ 
create a folder /Archiv for your files 
and a folder /source/static/pdf/ as location for you scanned pdfs
otherwise feel free to edit the sourcecode on vars.py etc.

* ` python3 -m pip install -r requirements.txt`
* ` sudo apt-get install tesseract-ocr poppler-utils`
* ` python3 main.py`

## Run as systemd service on Fedora
* ` clone to /opt/prpdf (or adapt path below)`
* ` sudo dnf install tesseract-tools tesseract-devel poppler`
* ` python3 -m pip install -r requirements.txt`
* Adapt Homepath in the following two commands (default /opt/prpdf) 
* ` adduser -M -r -s /usr/bin/nologin -d /opt/prpdf`
* ` chown prpdf:prpdf /opt/prpdf`
* Edit prpdf.service to reflect your WORKDIR (/opt/prpdf by default)
* ` cp prpdf.service /lib/systemd/system `
* ` systemctl enable --now prpdf`

## Run on TrueNAS Scale via TrueCharts
1. Create a dataset in your drive pool called prpdf
2. Add 3 more datasets to the newly created prpdf
3. Set storage limits and permissions if you wish, enable windows shares to these if you wish
4. Click the primary prpdf dataset you created in 1 and set the permissions to propagate to child shares
5. Add the TrueCharts catalog
6. Enable all the catalog items (Dev/stable/incubator/etc)
7. Search for prpdf
8. Click Install
9. Fill out the settings (Optionally, go back and create permanent)
10. If the port is not created / open then make sure to create a container port of 30380 to 80 for the web UI
11. Wait for it to deploy and navigate to https://your-truenas-ip:30380 (or whatever the port is set to in truecharts)
12. 
# Configuration
A default config will be creating within the first start of PR PDF.
For Docker please mount the config folder to make it persistent.
An example: https://github.com/maschhoff/prpdf/blob/main/config/config.json

    "port":80, - choose any port you want
    "debug":"off", set so on or off to see ocr results while autoscan
    "lang":"deu", set the ocr language see https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
    "updatetime":1800, uptime in seconds

# Donate
If you like what you see please buy me a Pizza -> https://www.buymeacoffee.com/maschhoff

