from flask import Flask, request, render_template, redirect, make_response
import jwt
import time
import os
import base64
import json

app = Flask(__name__)

SECRET_KEY = os.environ.get('JWT_SECRET', 'default_secret') 
FLAG = os.environ.get('FLAG', 'grey{no_flag_set}')         

def parse_jwt(token):
    header_b64, payload_b64, *_ = token.split('.')

    padded_header = header_b64 + '=' * (-len(header_b64) % 4)
    header = json.loads(base64.urlsafe_b64decode(padded_header))

    alg = header.get('alg', 'HS256') 

    if alg == 'none':
        padded_payload = payload_b64 + '=' * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded_payload))
        return payload
    else:
        return jwt.decode(token, SECRET_KEY, algorithms=[alg])

@app.route('/', methods=['GET', 'POST'])
def index():
    token = request.cookies.get('token')
    if token:
        try:
            payload = parse_jwt(token)
            if payload.get('admin'):
                return render_template('welcome.html',
                                       title='Welcome admin!',
                                       message='Here is your flag:',
                                       flag=FLAG)
            else:
                return render_template('welcome.html',
                                       title='Welcome my friend!',
                                       message='You are not admin.',
                                       flag=None)
        except jwt.exceptions.InvalidTokenError:
            return render_template('welcome.html',
                                   title='Invalid token!',
                                   message='Your token could not be verified.',
                                   flag=None)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'testuser' and password == 'test123123':
            payload = {
                'username': username,
                'admin': False,
                'iat': int(time.time())
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            resp = make_response(redirect('/'))
            resp.set_cookie('token', token)
            return resp
        else:
            return render_template('welcome.html',
                                   title='Invalid credentials!',
                                   message='Wrong username or password.',
                                   flag=None)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3334)
