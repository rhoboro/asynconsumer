import hashlib


def to_byte(bytes_or_str, enc='utf-8'):
    """byteに変換して返す"""
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode(enc)
    else:
        value = bytes_or_str or b''
    return value


def to_md5(data):
    return hashlib.md5(to_byte(data)).hexdigest()


from .gcs_downloader import fetch_gcs_objects
from .http_downloader import fetch_http_resources

__all__ = ['fetch_gcs_objects', 'fetch_http_resources']
