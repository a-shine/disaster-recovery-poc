#!/bin/bash

sudo apt-get update
sudo apt-get install -yq build-essential python3-pip

pip install flask

cat << EOF > app.py
#!/usr/bin/python

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_cloud():
  return 'Hello Cloud!'

app.run(host='0.0.0.0')

EOF

chmod 755 app.py

./app.py