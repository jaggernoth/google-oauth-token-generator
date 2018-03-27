"""Parsing cmd parameters"""
import argparse
import hashlib
import hmac
import time
import base64


def parse_params():
    """returns cmd parameters"""
    parser = argparse.ArgumentParser(
        description='Generates token for given token arguments')
    parser.add_argument('--email',
                        dest='email',
                        required=True,
                        help='user email')
    parser.add_argument('--host',
                        dest='host',
                        required=True,
                        help='host')
    parser.add_argument('--secret',
                        dest='secret',
                        required=True,
                        help='token secret')
    parser.add_argument('--expire',
                        dest='expire',
                        required=False,
                        help='expire')
    return parser.parse_args()


def make_digest(message, key):

    key = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')

    digester = hmac.new(key, message, hashlib.sha1)
    signature1 = digester.digest()
    signature2 = base64.b64encode(signature1)
    return str(signature2, 'UTF-8')


def generate():
    params = parse_params()
    expire = params.expire
    if not expire:
        expire = int(time.time()) + 60*60*24*256
    msg = '{}{}{}'.format(params.host, params.email, expire)
    secret = params.secret
    token = make_digest(msg, secret)
    print(" Expire: {}".format(expire))
    print("  Email: {}".format(params.email))
    print("   Host: {}".format(params.host))
    print("  Token: {}".format(token))


generate()
