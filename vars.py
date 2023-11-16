# Folder - !!! DO NOT CHANGE FOR DOCKER !!!!

import os

# Get the current working directory if a user does not specify one in their docker environment
print(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = os.path.dirname(os.path.abspath(__file__)) if 'WORKDIR' not in os.environ else  os.environ['WORKDIR']
print("WORK DIR", WORK_DIR)
PDF_DIR  = os.path.join(WORK_DIR, "/static/pdf/")                # Source
TEMP_DIR = r"/tmp/images/"                                      # Temp
ARCH_DIR = os.path.join(WORK_DIR, "/archiv/")                 # Upper folder archive -- underneath storage of the item folders
UNKN_DIR = os.path.join(WORK_DIR, "/static/pdf/unknown/")    # unrecognized PDFs