from flask import Blueprint, render_template, request, redirect, abort
from database import SessionLocal
from models import DataPoint

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    session = SessionLocal()
    try:
        data = session.query(DataPoint).all()
    finally:
        session.close()

    return render_template("index.html", data=data)


@web_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        feature1 = request.form.get("feature1")
        feature2 = request.form.get("feature2")
        category = request.form.get("category")

        try:
            feature1 = float(feature1)
            feature2 = float(feature2)
            category = int(category)
        except (ValueError, TypeError):

            return render_template("error400.html"), 400

        session = SessionLocal()
        try:
            new_point = DataPoint(
                feature1=feature1,
                feature2=feature2,
                category=category
            )
            session.add(new_point)
            session.commit()
        finally:
            session.close()

        return redirect("/")


@web_bp.route("/delete/<int:record_id>", methods=["POST"])
def delete(record_id):
    session = SessionLocal()
    try:
        point = session.get(DataPoint, record_id)

        if point is None:
            return render_template("error404.html"), 404

        session.delete(point)
        session.commit()
    finally:
        session.close()

    return redirect("/")
