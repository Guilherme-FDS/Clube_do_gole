from flask import Flask
import os
from routes.views import routes
from flask import session
app = Flask(__name__)

app.secret_key =  os.urandom(24)
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)