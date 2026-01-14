from flask import Blueprint, render_template, request, redirect
import services

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    data = services.get_all_data_points()
    return render_template("index.html", data=data)


@web_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        try:
            f1 = float(request.form.get("feature1"))
            f2 = float(request.form.get("feature2"))
            cat = int(request.form.get("category"))

            services.add_data_point(f1, f2, cat)

            return redirect("/")
        except (ValueError, TypeError):
            return render_template("error400.html"), 400


@web_bp.route("/delete/<int:record_id>", methods=["POST"])
def delete(record_id):
    success = services.delete_data_point(record_id)
    if not success:
        return render_template("error404.html"), 404
    return redirect("/")


@web_bp.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    if request.method == "POST":
        try:
            f1 = float(request.form.get("feature1"))
            f2 = float(request.form.get("feature2"))

            category = services.predict_category(f1, f2)

            return render_template("prediction_result.html", category=category)
        except (ValueError, TypeError):
            return render_template("error400.html"), 400