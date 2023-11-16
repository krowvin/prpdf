# importing modules

import pytesseract
# Wenn tesseract exe nicht im System PATH angegeben, dann:
# pytess= r"/home/detleva/.local/bin"
from PIL import Image
# Wenn poppler/bin  nicht im System PATH angegeben, dann:
# pdftoppm_path = r"/home/detleva/.local/bin/pdftoppm"
import os  # , subprocess
from pdf2image import convert_from_path
from datetime import datetime
import logging
import time
from datetime import datetime, date
import threading
import shutil
import random
import settings
from vars import WORK_DIR, PDF_DIR, TEMP_DIR, ARCH_DIR, UNKN_DIR


os.chdir(WORK_DIR)
# Logging
logging.basicConfig(filename=os.path.join(
    WORK_DIR, '/config/server.log'), level=logging.INFO)

# Filedate
# filedatum=datetime.now().strftime('%d_%m_%Y+0') # filename + Tag_Monat_Jahr_Counter

# SETTINGS

config = settings.loadConfig()

lang = config["lang"]
debug = config["debug"]
updatetime = config["updatetime"]
index = config["index"]


# Ordner anlegen

os.makedirs(ARCH_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(UNKN_DIR, exist_ok=True, mode=0o775)


# CRON THREAD

# CRON Run
def autoscan_cron():
    while True:
        logging.info("STARTING CRONJOB PR PDF AUTOSCAN "+str(datetime.now()))
        print("STARTING CRONJOB PR PDF AUTOSCAN "+str(datetime.now()))
        try:
            run()
        except Exception as e:
            print("An exception occurred "+str(e))
            logging.error("An exception occurred "+str(e))
        time.sleep(updatetime)  # TODO conf updatetime

# aus OCR text indexieren und PDFs in Ordner schieben


def sort(pdf_file, text):
    if debug == "on":
        print("---------------------------------------------------\n\n")
        print(text)
        print("---------------------------------------------------\n\n")

    for archiv_item in index:                 # Schleife uber DICT
        ordner, filename = archiv_item.split(";")
        count = 0
        treffer = 0
        # Schleife uber Keywords in einem Item
        for keywords in index[archiv_item]:
            treffer = text.find(keywords)     # match ein Keyword
            if treffer >= 0:
                count += 1
        if count >= len(index[archiv_item]):    # match auf alle Keywords
            if not os.path.exists(ordner):  # Ordner mit Item aus Dict anlegen
                os.makedirs(ordner)
            filedatum = date.fromtimestamp(os.path.getmtime(
                PDF_DIR+"/"+pdf_file)).strftime('%d_%m_%Y')
            fileneu = filename+"_"+filedatum+"_" + \
                str(random.randint(1111, 9999))+".pdf"

            logging.info(f"MOVE {PDF_DIR}/{pdf_file} to {ordner}/{fileneu}")
            print("MOVE "+PDF_DIR+"/"+pdf_file+" to "+ordner+"/"+fileneu)
            shutil.move(PDF_DIR+"/"+pdf_file, ordner +
                        "/"+fileneu)  # pdf File in Ordner


def run():
    # PDFs in Bilder umwandeln und OCR Texterkennung
    print("Run Dir")
    for pdf_file in os.listdir(PDF_DIR):   # Schleife uber Source Ordner
        try:
            # PDFs der Reihe nach indexieren
            sort(pdf_file, ocr(PDF_DIR, pdf_file))
        except Exception as e:
            logging.error("An exception occurred "+str(e))
            print("An exception occurred "+str(e))
            continue

    print("Run Del")
    for image_file in os.listdir(TEMP_DIR):  # temp Dir loeschen
        os.remove(TEMP_DIR+"/"+image_file)
    print("Move")
    # nicht erkannte PDFs nach unknown kopieren
    for unknown_file in os.listdir(PDF_DIR):
        if os.path.isfile(PDF_DIR+"/"+unknown_file):
            logging.info("MOVE "+PDF_DIR+"/"+unknown_file +
                         " to "+UNKN_DIR+"/"+unknown_file)
            print("MOVE "+PDF_DIR+"/"+unknown_file +
                  " to "+UNKN_DIR+"/"+unknown_file)
            shutil.move(PDF_DIR+"/"+unknown_file, UNKN_DIR+"/"+unknown_file)


def ocr(folder, pdf_file):
    print("---- OCR PDF-File: ", pdf_file, " ----\n")
    if pdf_file.endswith(".pdf"):
        temp = TEMP_DIR+"/"+pdf_file[:-4]
        source = folder+"/"+pdf_file

    # Bilder aus pdf
        try:
            pages = convert_from_path(
                source, dpi=400, first_page=1, last_page=1, grayscale=True)
        except Exception as e:
            logging.error("An exception occurred "+str(e))
            print("An exception occurred "+str(e))
            return ""

        filename = temp+"_1.jpg"
        pages[0].save(filename, 'JPEG')

    # OCR Texterkennung
        try:
            return pytesseract.image_to_string(Image.open(temp+"_1.jpg"), lang=lang)
        except:
            return ""


# Cron Thread start
th = threading.Thread(target=autoscan_cron)
th.start()
