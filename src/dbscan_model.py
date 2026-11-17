import numpy as np
import pandas as pd
from collections import Counter
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from src.preprocessing import clean_house_data, transform_features

class SeattleDBSCANClustering:
    def __init__(self, eps=0.7, min_samples=120):
        self.eps = eps
        self.min_samples = min_samples
        self.model = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        self.scaler = None
        self.features = ['price', 'sqft_living', 'grade']
        self.X_scaled = None
        self.nbrs = None
        self.labels_ = None
        self.df_train = None

    def fit(self, df: pd.DataFrame):
        """Fit DBSCAN model and train NearestNeighbors for inference."""
        self.df_train = clean_house_data(df)
        self.X_scaled, self.scaler, _ = transform_features(self.df_train, self.features)
        
        self.labels_ = self.model.fit_predict(self.X_scaled)
        self.df_train['cluster'] = self.labels_
        
        # Fit NearestNeighbors on scaled training data for new sample predictions
        self.nbrs = NearestNeighbors(n_neighbors=self.min_samples)
        self.nbrs.fit(self.X_scaled)
        return self

    def predict_new_sample(self, price: float, sqft_living: float, grade: int):
        """
        Predict cluster for a new house using KNN majority vote among neighbors.
        Returns:
            (cluster_id, confidence, avg_neighbor_distance)
        """
        if self.scaler is None or self.nbrs is None:
            raise ValueError("Model is not fitted yet. Call fit() first.")

        sample_df = pd.DataFrame([{
            'price': price,
            'sqft_living': sqft_living,
            'grade': grade
        }])
        
        sample_scaled, _, _ = transform_features(sample_df, self.features, scaler=self.scaler)
        distances, indices = self.nbrs.kneighbors(sample_scaled)

        neighbor_labels = self.labels_[indices[0]]
        valid_labels = neighbor_labels[neighbor_labels != -1]

        if len(valid_labels) == 0:
            return -1, 0.0, float(distances[0].mean())

        label_counts = Counter(valid_labels)
        predicted_cluster = label_counts.most_common(1)[0][0]
        confidence = label_counts.most_common(1)[0][1] / len(neighbor_labels)
        avg_distance = float(distances[0].mean())

        return int(predicted_cluster), float(confidence), avg_distance

    def get_cluster_summary(self) -> pd.DataFrame:
        """Computes comprehensive quantitative business statistics per cluster."""
        if self.df_train is None:
            raise ValueError("Model is not fitted yet.")

        df = self.df_train.copy()
        df['price_per_sqft'] = df['price'] / df['sqft_living']
        total = len(df)
        
        cluster_names = {
            -1: "Nhiễu / Bất động sản cá biệt (Outlier)",
            0: "Nhà phổ thông trung bình thấp (Grade 7)",
            1: "Nhà bình dân / Khởi điểm (Grade 6)",
            2: "Nhà trung cấp gia đình (Grade 8)",
            3: "Biệt thự siêu cao cấp (Grade 11)",
            4: "Nhà cao cấp ven đô (Grade 9)",
            5: "Dinh thự sang trọng (Grade 10)"
        }

        records = []
        for cl in sorted(list(set(self.labels_))):
            sub = df[df['cluster'] == cl]
            top_zips = sub['zipcode'].value_counts().head(3).to_dict()
            top_zips_str = ", ".join([f"{int(k)} ({v})" for k, v in top_zips.items()])
            
            records.append({
                "cluster": int(cl),
                "segment_name": cluster_names.get(int(cl), f"Phân khúc {cl}"),
                "count": len(sub),
                "market_share_pct": round(len(sub) / total * 100, 2),
                "price_median": int(sub['price'].median()),
                "price_mean": int(sub['price'].mean()),
                "sqft_median": int(sub['sqft_living'].median()),
                "price_per_sqft": round(float(sub['price_per_sqft'].mean()), 2),
                "grade": int(round(sub['grade'].mean())),
                "top_zipcodes": top_zips_str,
                "center_lat": round(float(sub['lat'].mean()), 4),
                "center_long": round(float(sub['long'].mean()), 4)
            })
            
        return pd.DataFrame(records)

# Module-level convenience functions to support: `from dbscan_model import predict_new_sample`
_singleton_model = None

def _get_or_create_model():
    global _singleton_model
    if _singleton_model is None:
        import os
        csv_path = os.path.join(os.path.dirname(__file__), "..", "kc_house_data.csv")
        if not os.path.exists(csv_path):
            csv_path = "kc_house_data.csv"
        df = pd.read_csv(csv_path)
        _singleton_model = SeattleDBSCANClustering()
        _singleton_model.fit(df)
    return _singleton_model

def predict_new_sample(price: float, sqft_living: float, grade: int):
    """Standalone helper function that matches the README documentation."""
    model = _get_or_create_model()
    cluster, confidence, _ = model.predict_new_sample(price, sqft_living, grade)
    return cluster, confidence
