from flask import Flask
import random
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World",random.choice([200,500])

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
