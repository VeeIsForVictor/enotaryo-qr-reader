from datetime import datetime
from json import JSONDecoder
import logging
import os
from fastapi import FastAPI, UploadFile
import cv2

server = FastAPI()

LOGGER = logging.getLogger(__name__)

@server.get("/")
async def root():
    return {"serverName": "enotaryo-qr-reader"}

@server.post('/document/')
async def signatures(file: UploadFile):
    os.makedirs("dump", exist_ok=True)
    filename = f"dump/{datetime.now()}-{file.filename}"
    image_file = open(filename, "xb+")
    data = await file.read()
    image_file.write(data)
    image_file.flush()
    img = cv2.imread(filename)
    qrd = cv2.QRCodeDetector()
    retval, decoded_info, _, _ = qrd.detectAndDecodeMulti(img)
    ret_info = []

    for info in decoded_info:
        ret_info.append(JSONDecoder().decode(info))

    os.remove(filename)
    
    return {
        "qrCodeResult": retval,
        "signatures": ret_info
    }
