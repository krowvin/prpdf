# Folder - !!! DO NOT CHANGE FOR DOCKER !!!!

import os

WORK_DIR = '.' if 'WORKDIR' not in os.environ else  os.environ['WORKDIR']
PDF_DIR  = os.path.join(WORK_DIR, "/static/pdf/")                # Source
TEMP_DIR = r"/tmp/images/"                                      # Temp
ARCH_DIR = os.path.join(WORK_DIR, "/archiv/")                 # Upper folder archive -- underneath storage of the item folders
UNKN_DIR = os.path.join(WORK_DIR, "/static/pdf/unknown/")    # unrecognized PDFs
