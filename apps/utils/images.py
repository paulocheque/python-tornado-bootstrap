# coding: utf-8
from mimetypes import MimeTypes
from StringIO import StringIO
import requests


def save_from_file(field, filepath):
    img = open(filepath, 'r')
    content_type = None
    mime = MimeTypes()
    content_type = mime.guess_type(filepath)[0]
    field.replace(img, content_type=content_type)
    img.seek(0)


def save_from_url(field, url):
    r = requests.get(url)
    img = StringIO(r.content)
    content_type = r.headers['content-type']
    field.replace(img, content_type=content_type)
    img.seek(0)


def save_from_request(field, fileinfo):
    content = fileinfo['body']
    content_type = fileinfo['content_type']
    field.replace(StringIO(content), content_type=content_type)
