# coding: utf-8
import json
import hmac
import hashlib
import base64


def generate_signature(secret_key, serializable_data):
    string = json.dumps(serializable_data)
    sha256hash = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    signature = base64.urlsafe_b64encode(sha256hash)
    return signature
