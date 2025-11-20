from flask import Flask, request, render_template, jsonify

from database import engine
from routes.web import web_bp
from api.api import api_bp
from models import Base

app = Flask(__name__)

Base.metadata.create_all(engine)

app.register_blueprint(web_bp)
app.register_blueprint(api_bp)



@app.errorhandler(400)
def handle_400_error(error):
    if request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]:
        return jsonify({"error": "Invalid data"}), 400

    return render_template("error400.html"), 400


@app.errorhandler(404)
def handle_404_error(error):
    if request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]:
        return jsonify({"error": "Resource not found"}), 404

    return render_template("error404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
