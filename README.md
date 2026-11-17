# 🏡 Phân Khúc Thị Trường Bất Động Sản Seattle Bằng Thuật Toán DBSCAN
*(Seattle Housing Market Segmentation & Pricing Analytics using DBSCAN)*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)](https://scikit-learn.org)
[![Folium](https://img.shields.io/badge/Folium-Interactive%20Maps-green.svg)](https://python-visualization.github.io/folium/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Dự án phân tích dữ liệu và phân khúc thị trường bất động sản King County (Seattle, Washington) với hơn **21,000 giao dịch**. Bằng việc áp dụng thuật toán phân cụm dựa trên mật độ **DBSCAN** kết hợp mô hình suy luận **K-Nearest Neighbors (KNN)**, hệ thống tự động nhận diện **6 phân khúc thị trường cốt lõi** và cô lập các bất động sản cá biệt (Outliers) để tối ưu hóa chiến lược định giá và danh mục đầu tư.

📄 **Đọc toàn bộ báo cáo phân tích kinh doanh tại:** [BÁO CÁO BUSINESS CASE](BUSINESS_CASE.md)

---

## 🌟 Điểm Nổi Bật Của Dự Án

* **Khám phá phân khúc tự nhiên:** Không ép buộc dữ liệu vào số cụm định trước (như K-Means), DBSCAN tự động tìm ra 6 phân khúc chuẩn dựa trên mật độ thực tế của Giá bán (`price`), Diện tích (`sqft_living`), và Chất lượng xây dựng (`grade`).
* **Lọc bỏ điểm dị biệt (Noise/Outliers):** Nhận diện chính xác 388 bất động sản bất thường (tỷ lệ 1.81%) có giá đột biến (lên tới \$7.7M) để đưa vào quy trình thẩm định thủ công.
* **Cơ chế suy luận mẫu mới (Inductive Inference):** Tự xây dựng module `predict_new_sample()` bằng thuật toán K-Nearest Neighbors với cơ chế bỏ phiếu đa số (Majority Voting) để gán nhãn phân khúc cho các căn nhà mới ký gửi.
* **Trực quan hóa không gian:** Tích hợp bản đồ tương tác `seattle_clusters_map.html` thể hiện sự tương quan mật thiết giữa phân khúc xây dựng và vị trí địa lý (từ vùng bình dân Nam Seattle đến khu nhà giàu Bellevue & Mercer Island).

---

## 📊 Tóm Tắt Các Phân Khúc Thị Trường (Market Segments)

| Cụm | Tên phân khúc đề xuất | Thị phần | Giá trung vị (USD) | Diện tích TB | Đơn giá (\$/sqft) | Grade | Khu vực tiêu biểu |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | Nhà bình dân / Khởi điểm | 9.29% | **\$275,000** | 1,188 sqft | \$271 | 6 | Nam Seattle, Tukwila (98118, 98168) |
| **0** | Phổ thông trung bình thấp | 41.50% | **\$375,000** | 1,689 sqft | \$252 | 7 | Bắc Seattle, Kirkland (98034, 98115) |
| **2** | Trung cấp gia đình | 28.18% | **\$510,000** | 2,184 sqft | \$258 | 8 | Redmond, Green Lake (98052, 98103) |
| **4** | Cao cấp ven đô | 12.13% | **\$720,500** | 2,872 sqft | \$276 | 9 | Sammamish, Bellevue (98074, 98006) |
| **5** | Dinh thự sang trọng | 5.26% | **\$915,000** | 3,527 sqft | \$307 | 10 | Somerset, Sammamish (98075, 98006) |
| **3** | Biệt thự siêu cao cấp | 1.83% | **\$1,280,000** | 4,376 sqft | \$342 | 11 | Mercer Island, Downtown Bellevue (98040, 98004) |
| **-1** | Bất động sản cá biệt (Outlier) | 1.81% | **\$280,000** | 2,312 sqft | \$327 | 1–13 | Nhà giá siêu cao (tới \$7.7M) hoặc đặc thù |

---

## 📁 Cấu Trúc Dự Án

```text
Clustering-house-prices-using-the-DBSCAN-algorithm/
│
├── DataMining_Main.ipynb          # Notebook nghiên cứu, thử nghiệm & EDA chi tiết
├── BUSINESS_CASE.md               # Báo cáo phân tích kinh doanh chuẩn Business Analyst
├── README.md                      # Tài liệu giới thiệu & hướng dẫn sử dụng dự án
├── requirements.txt               # Danh sách thư viện phụ thuộc
├── kc_house_data.csv              # Tập dữ liệu gốc King County Housing
├── main.py                        # Script thực thi toàn bộ pipeline huấn luyện & xuất báo cáo
│
├── src/                           # Mã nguồn module chuẩn hóa
│   ├── __init__.py                # Khởi tạo package
│   ├── preprocessing.py           # Làm sạch dữ liệu, Log transform, RobustScaler
│   ├── dbscan_model.py            # Model DBSCAN & hàm dự đoán mẫu mới (KNN Inference)
│   └── visualization.py           # Xuất bản đồ tương tác Folium & biểu đồ phân tích
│
├── cluster_business_summary.csv   # Bảng tổng hợp số liệu kinh doanh từng cụm
├── seattle_clusters_map.html      # Bản đồ tương tác vệ tinh Seattle (Mở bằng trình duyệt)
└── clusters_price_size.png        # Biểu đồ phân bổ Giá vs. Diện tích
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Dự Án

### 1. Khởi tạo môi trường ảo

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường (Windows)
.venv\Scripts\activate

# Kích hoạt môi trường (Linux/Mac)
# source .venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2. Chạy pipeline hoàn chỉnh

```bash
python main.py
```

Lệnh trên sẽ tự động:
1. Huấn luyện mô hình DBSCAN ($eps=0.7$, $min\_samples=120$).
2. Xuất bảng phân tích định lượng kinh doanh ra file `cluster_business_summary.csv`.
3. Sinh bản đồ tương tác `seattle_clusters_map.html`.
4. Xuất biểu đồ tương quan `clusters_price_size.png`.
5. Chạy thử nghiệm hàm dự đoán cho 4 căn nhà mẫu mới.

---

## 💻 Sử Dụng Mô Hình Trong Code

Bạn có thể dễ dàng import và sử dụng hàm dự đoán phân khúc cho căn nhà mới:

```python
from src.dbscan_model import predict_new_sample

# Dự đoán phân khúc cho một căn nhà mới ký gửi
cluster_id, confidence = predict_new_sample(
    price=450000,       # Giá nhà (USD)
    sqft_living=2000,   # Diện tích sinh hoạt (sqft)
    grade=8             # Chất lượng xây dựng (1-13)
)

print(f"Căn nhà thuộc Cluster: {cluster_id}")
print(f"Độ tin cậy của mô hình: {confidence:.1%}")
```

---

## 📈 Trực Quan Hóa Tương Tác
Dự án cung cấp file **`seattle_clusters_map.html`**. Bạn chỉ cần mở trực tiếp file này bằng bất kỳ trình duyệt nào (Chrome, Edge, Firefox) để:
* Khám phá tọa độ từng căn nhà trên bản đồ địa lý Seattle.
* Xem phân bố màu sắc theo từng phân khúc.
* Nhấp vào từng điểm để xem chi tiết: Giá bán, Diện tích, Grade, và Mã Zipcode.
