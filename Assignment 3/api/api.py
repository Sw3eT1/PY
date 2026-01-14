from flask import Blueprint, request, jsonify
import services

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/data", methods=["GET"])
def get_all_data():
    items = services.get_all_data_points()

    result = [
        {
            "id": i.id,
            "feature1": i.feature1,
            "feature2": i.feature2,
            "category": i.category
        }
        for i in items
    ]
    return jsonify(result), 200


@api_bp.route("/data", methods=["POST"])
def add_data():
    data = request.json

    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    try:
        f1 = float(data.get("feature1"))
        f2 = float(data.get("feature2"))
        cat = int(data.get("category"))

        new_id = services.add_data_point(f1, f2, cat)

        return jsonify({"id": new_id}), 201

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data"}), 400


@api_bp.route("/data/<int:record_id>", methods=["DELETE"])
def delete_data(record_id):
    success = services.delete_data_point(record_id)
    if not success:
        return jsonify({"error": "Record not found"}), 404
    return jsonify({"id": record_id}), 200


@api_bp.route("/predictions", methods=["GET"])
def get_prediction():
    f1_str = request.args.get("feature1")
    f2_str = request.args.get("feature2")

    try:
        if f1_str is None or f2_str is None:
            return jsonify({"error": "Missing parameters"}), 400

        f1 = float(f1_str)
        f2 = float(f2_str)

        category = services.predict_category(f1, f2)
        return jsonify({"category": category}), 200

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data or not enough data to train"}), 400