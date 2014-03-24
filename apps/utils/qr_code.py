# coding: utf-8
from StringIO import StringIO
import urllib

import qrcode


def generate_qrcode(field, url):
    img = qrcode.make(url)
    img_bytes = StringIO()
    img.save(img_bytes, 'png')
    img_bytes.seek(0)
    field.put(img_bytes, content_type='image/png')
