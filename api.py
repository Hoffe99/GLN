from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/uhrzeit', methods=['GET'])
def get_uhrzeit():
    uhrzeit = datetime.now().strftime('%H:%M:%S')
    return jsonify({'uhrzeit': uhrzeit})

if __name__ == '__main__':
    app.run(debug=True)