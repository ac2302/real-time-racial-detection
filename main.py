from flask import Flask, request, render_template
from flask.json import jsonify
import sys
import os
import json
import threading
import webbrowser

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=['POST'])
def start():
    # try:
    if 1:
        options = json.dumps({
            'render-frames': bool(request.form.get('render-frames')),
            'render-box': bool(request.form.get('render-box')),
            'render-text': bool(request.form.get('render-text')),
            'render-percentage': bool(request.form.get('render-percentage')),
            'text-color': request.form.get('text-color'),
            'box-color': request.form.get('box-color'),
        }, indent=4)

        with open('settings.json', 'w') as f:
            print(options, file=f)
            f.flush()

        os.system(f"{sys.executable} racial_detection.py")

        return render_template("index.html")
    # except:
    #     return jsonify({"message": "error"})


if __name__ == '__main__':
    # starting the flask app
    threading.Thread(target=app.run).start()
    webbrowser.open('http://localhost:5000')
