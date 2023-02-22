#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route('/')
def view_count():
    count_file = 'count.txt'
    with open(count_file, 'r') as f:
        stored_count = f.read()

    count = int(stored_count)
    count += 1

    with open(count_file, 'r+') as f:
        f.write(str(count))

    return 'The current view count is: ' + str(count)


app.run(host='0.0.0.0')
