#!/usr/bin/env python
# coding: utf-8


# In[1]: Documentacion

# ### Monitorea Geoevent a trves de api REST - Valida estado de Inputs
# Consulta el estado de los INPUTS de GeoEvent para su posterior validacion 
# con una plataforma de monitoreo como NAGIOS


# In[2]: Importando librerias
from datetime import datetime
import time
import requests
import http.client
import os
import json
from cryptography.fernet import Fernet
from arcgis.gis import GIS
import sys
import logging
from logging.handlers import RotatingFileHandler

# In[3]: Define funciones
def get_local_path():
    local_path = os.path.realpath('') 
    if os.path.exists(local_path + '\\GE-Monitor.py') == True:
        return local_path
    else:
        local_path = os.path.dirname(__file__)
        return local_path
    
def get_credentials():
    credentials = os.path.realpath('') +'\\'+ 'credentials.json'
    if os.path.exists(credentials) == True:
        pass
    else:
        credentials = os.path.dirname(__file__) +'\\'+ 'credentials.json'

    with open(credentials) as json_data:
        credentials = json.load(json_data)

    key = bytes(credentials['key'].encode())

    ciphered_text = Fernet(key)
    encoded_credentials = credentials['values'].split('-%$&-')
    decoded_credentials = {'portal_desa_user': ciphered_text.decrypt(bytes(encoded_credentials[0].encode())).decode(),
                            'portal_desa_password': ciphered_text.decrypt(bytes(encoded_credentials[1].encode())).decode(),
                            'portal_test_user': ciphered_text.decrypt(bytes(encoded_credentials[2].encode())).decode(),
                            'portal_test_password': ciphered_text.decrypt(bytes(encoded_credentials[3].encode())).decode(),
                            'portal_prod_user': ciphered_text.decrypt(bytes(encoded_credentials[4].encode())).decode(),
                            'portal_prod_password': ciphered_text.decrypt(bytes(encoded_credentials[5].encode())).decode(),
                            'sgip_desa_user': ciphered_text.decrypt(bytes(encoded_credentials[6].encode())).decode(),
                            'sgip_desa_password': ciphered_text.decrypt(bytes(encoded_credentials[7].encode())).decode(),
                            'editor_desa_user': ciphered_text.decrypt(bytes(encoded_credentials[8].encode())).decode(),
                            'editor_desa_password': ciphered_text.decrypt(bytes(encoded_credentials[9].encode())).decode()
    }
    return decoded_credentials


# In[4]: Define variables
# Obtiene credenciales
decoded_credentials = get_credentials()
# Portal Credentials
_portal_user = decoded_credentials['editor_desa_user']
_portal_password = decoded_credentials['editor_desa_password']
portal = 'https://portalgis-desa.domainba.com/portal'
# Variables de LOG
_maxBytes = 10000000 # 10MB
_backupCount = 5 # Mantener 5 archivos

# In[5]: Iniciando y creando logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Creo handlers para loggear en pantallay en un archivo
stdoutHanlder = logging.StreamHandler(sys.stdout)
errHandler = logging.handlers.RotatingFileHandler(f"{get_local_path()}\\error.log", maxBytes=_maxBytes, backupCount=_backupCount)

# Seteo el formato de log
fmt = logging.Formatter(
    "%(filename)s: | %(asctime)s | %(levelname)s | %(lineno)s | %(message)s"
)

# Seteo nivel de error para cada handler
stdoutHanlder.setLevel(logging.DEBUG)
errHandler.setLevel(logging.INFO)

# Seteo el formato de mensaje para cada Handler
stdoutHanlder.setFormatter(fmt)
errHandler.setFormatter(fmt)

# Agrego ambos handler al logger
logger.addHandler(stdoutHanlder)
logger.addHandler(errHandler)

# Ejemplos de LOGS
# logger.debug("Inforcaion de debug")
# logger.info("Importando librerías")
# logger.warning("Importando librerías")
# logger.error("Error generico", exc_info=True)
# logger.critical("Error generico", exc_info=True)

# In[6]: Comienza el script
logger.info("Comenzando")
logger.info("Terminado")
