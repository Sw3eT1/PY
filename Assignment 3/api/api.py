from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import DataPoint

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/data", methods=["GET"])
def get_all_data():
    session = SessionLocal()
    try:
        items = session.query(DataPoint).all()

        result = [
            {
                "id": item.id,
                "feature1": item.feature1,
                "feature2": item.feature2,
                "category": item.category
            }
            for item in items
        ]

    finally:
        session.close()

    return jsonify(result), 200


@api_bp.route("/data", methods=["POST"])
def add_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    feature1 = data.get("feature1")
    feature2 = data.get("feature2")
    category = data.get("category")

    try:
        feature1 = float(feature1)
        feature2 = float(feature2)
        category = int(category)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data"}), 400

    session = SessionLocal()
    try:
        new_point = DataPoint(
            feature1=feature1,
            feature2=feature2,
            category=category
        )
        session.add(new_point)
        session.commit()

        new_id = new_point.id

    finally:
        session.close()

    return jsonify({"id": new_id}), 201


@api_bp.route("/data/<int:record_id>", methods=["DELETE"])
def delete_data(record_id):
    session = SessionLocal()
    try:
        item = session.get(DataPoint, record_id)

        if item is None:
            return jsonify({"error": "Record not found"}), 404

        session.delete(item)
        session.commit()

    finally:
        session.close()

    return jsonify({"id": record_id}), 200
