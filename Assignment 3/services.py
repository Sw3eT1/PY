from database import SessionLocal
from models import DataPoint
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np



def get_all_data_points():
    with SessionLocal() as session:
        return session.query(DataPoint).all()


def add_data_point(feature1: float, feature2: float, category: int) -> int:
    with SessionLocal() as session:
        new_point = DataPoint(
            feature1=feature1,
            feature2=feature2,
            category=category
        )
        session.add(new_point)
        session.commit()
        session.refresh(new_point)
        return new_point.id


def delete_data_point(record_id: int) -> bool:
    with SessionLocal() as session:
        point = session.get(DataPoint, record_id)
        if point is None:
            return False
        session.delete(point)
        session.commit()
        return True



def predict_category(feature1: float, feature2: float) -> int:
    with SessionLocal() as session:
        data_points = session.query(DataPoint).all()

        if not data_points:
            raise ValueError("Brak danych w bazie - nie można wytrenować modelu.")

        X = [[dp.feature1, dp.feature2] for dp in data_points]
        y = [dp.category for dp in data_points]

    k = max(1, min(5, len(X)))

    clf = KNeighborsClassifier(n_neighbors=k)
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)
    clf.fit(X_scaled, y)

    input_data = [[feature1, feature2]]
    input_scaled = scaler.transform(input_data)

    prediction = clf.predict(input_scaled)

    return int(prediction[0])