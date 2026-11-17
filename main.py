import os
import pandas as pd
from src.dbscan_model import SeattleDBSCANClustering, predict_new_sample
from src.visualization import generate_interactive_map, plot_clusters_2d

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "kc_house_data.csv")
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Cannot find {csv_file}")

    print("🚀 Đang tải và phân tích dữ liệu BĐS King County Seattle...")
    df = pd.read_csv(csv_file)

    # 1. Huấn luyện mô hình DBSCAN
    clustering = SeattleDBSCANClustering(eps=0.7, min_samples=120)
    clustering.fit(df)
    print(" Huấn luyện mô hình DBSCAN thành công (eps=0.7, min_samples=120)!")

    # 2. Xuất báo cáo tổng quan kinh doanh
    summary_df = clustering.get_cluster_summary()
    print("\n📊 BẢNG TỔNG HỢP CÁC PHÂN KHÚC THỊ TRƯỜNG (BUSINESS SUMMARY):")
    print("=" * 110)
    display_cols = ['cluster', 'segment_name', 'market_share_pct', 'price_median', 'sqft_median', 'price_per_sqft', 'grade', 'top_zipcodes']
    print(summary_df[display_cols].to_string(index=False))
    print("=" * 110)

    # Lưu bảng summary ra CSV
    summary_path = os.path.join(base_dir, "cluster_business_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f" Đã lưu bảng phân tích kinh doanh: {summary_path}")

    # 3. Tạo bản đồ tương tác Seattle
    map_file = os.path.join(base_dir, "seattle_clusters_map.html")
    generate_interactive_map(clustering.df_train, output_path=map_file, sample_size=2000)
    print(f"🗺️  Đã tạo bản đồ tương tác: {map_file} (mở trực tiếp bằng trình duyệt)")

    # 4. Tạo biểu đồ 2D Scatter
    plot_file = os.path.join(base_dir, "clusters_price_size.png")
    plot_clusters_2d(clustering.df_train, output_image=plot_file)
    print(f"📈 Đã xuất biểu đồ tương quan: {plot_file}")

    # 5. Thử nghiệm dự đoán căn nhà mới
    print("\n🏠 THỬ NGHIỆM DỰ ĐOÁN PHÂN KHÚC CHO CĂN NHÀ MỚI:")
    test_cases = [
        {"price": 250000, "sqft": 1100, "grade": 6, "desc": "Nhà nhỏ vùng ven"},
        {"price": 420000, "sqft": 1700, "grade": 7, "desc": "Nhà phố phổ thông"},
        {"price": 550000, "sqft": 2200, "grade": 8, "desc": "Nhà trung cấp gia đình"},
        {"price": 1400000, "sqft": 4200, "grade": 11, "desc": "Biệt thự cao cấp"}
    ]

    for tc in test_cases:
        cl, conf = predict_new_sample(tc['price'], tc['sqft'], tc['grade'])
        print(f" • {tc['desc']} (${tc['price']:,}, {tc['sqft']:,} sqft, Grade {tc['grade']}) -> Cluster {cl} (Độ tin cậy: {conf:.1%})")

    print("\n Toàn bộ quy trình hoàn tất thành công!")

if __name__ == "__main__":
    main()
