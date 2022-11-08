import base64

def base64_encode(string):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')