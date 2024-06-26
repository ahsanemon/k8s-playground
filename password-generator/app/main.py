from flask import Flask, request, jsonify, render_template
import random
import string
from prometheus_flask_exporter import PrometheusMetrics
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
metrics = PrometheusMetrics(app)

def generate_password(length, special_chars, numbers):
    password = []
    password.extend(random.choices(string.ascii_letters, k=length - special_chars - numbers))
    password.extend(random.choices(string.digits, k=numbers))
    password.extend(random.choices(string.punctuation, k=special_chars))
    random.shuffle(password)
    return ''.join(password)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/generate-passwords', methods=['GET', 'POST'])
def generate_passwords_page():
    if request.method == 'POST':
        min_length = int(request.form['min_length'])
        special_chars = int(request.form['special_chars'])
        numbers = int(request.form['numbers'])
        num_passwords = int(request.form['num_passwords'])

        passwords = []
        for _ in range(num_passwords):
            password = generate_password(min_length, special_chars, numbers)
            passwords.append(password)

        return render_template('generate_passwords.html', passwords=passwords)

    return render_template('generate_passwords.html', passwords=None)

if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 80), app)
    http_server.serve_forever()