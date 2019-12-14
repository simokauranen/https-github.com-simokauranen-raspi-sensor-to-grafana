"""
Author:         Simo Kauranen
Description:    Collection of tool methods

"""

import os.path
import logging

logging.basicConfig(level=logging.DEBUG)

def getPiJSONAddresses():
    """ Read JSON URLs from the default config file ./config/raspberry-pi-addresses
        Returns list of strings like "192.456.78.23:5000/api/v1/kamk_11)
    """

    try:
        fileDir = os.path.dirname(__file__)
        filename = os.path.join(fileDir, './config/raspberry-pi-urls')
        filename = os.path.abspath(os.path.realpath(filename))
        file = open(filename, "r")
        return file.read().splitlines()
    except IOError:
        logging.exception("File not found. Please add file ./config/raspberry-pi-urls.")
    except Exception:
        logging.exception("Trouble with reading config file")
    
logging.debug(getPiJSONAddresses())