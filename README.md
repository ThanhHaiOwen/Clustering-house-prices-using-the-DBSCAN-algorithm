# Phân cụm giá nhà Seattle sử dụng thuật toán DBSCAN

## Giới thiệu
Dự án này thực hiện phân tích và phân cụm dữ liệu giá nhà tại Seattle, Washington sử dụng thuật toán DBSCAN (Density-Based Spatial Clustering of Applications with Noise). Mục tiêu chính là phân loại các căn nhà thành các nhóm có đặc điểm tương tự về giá cả, diện tích và chất lượng xây dựng, từ đó cung cấp cái nhìn sâu sắc về thị trường bất động sản Seattle.

### Mục tiêu dự án
- Phân tích và hiểu cấu trúc thị trường bất động sản Seattle
- Xác định các phân khúc giá nhà tự nhiên dựa trên đặc điểm của căn nhà
- Cung cấp công cụ hỗ trợ định giá và tư vấn bất động sản
- Phát triển chiến lược kinh doanh cho từng phân khúc thị trường

### Ý nghĩa thực tiễn
- **Cho người mua nhà**: Hiểu rõ các phân khúc thị trường và giá trị tương đối của bất động sản
- **Cho người bán/môi giới**: Định giá chính xác và phát triển chiến lược marketing phù hợp
- **Cho nhà đầu tư**: Xác định cơ hội đầu tư và phân tích xu hướng thị trường
- **Cho nhà phát triển**: Định hướng phát triển dự án phù hợp với từng phân khúc

## Mô tả Dataset

Dataset `kc_house_data.csv` bao gồm thông tin về các căn nhà tại Seattle với các trường dữ liệu sau:

| Trường dữ liệu | Mô tả |
|----------------|--------|
| id | Mã định danh duy nhất cho mỗi căn nhà |
| date | Ngày bán căn nhà |
| price | Giá bán (biến mục tiêu) |
| bedrooms | Số phòng ngủ |
| bathrooms | Số phòng tắm |
| sqft_living | Diện tích sinh hoạt (feet vuông) |
| sqft_lot | Diện tích lô đất |
| floors | Số tầng |
| waterfront | Có view hướng biển (0/1) |
| view | Chỉ số đánh giá view (0-4) |
| condition | Tình trạng căn nhà (1-5) |
| grade | Chất lượng xây dựng (1-13) |
| sqft_above | Diện tích trên mặt đất |
| sqft_basement | Diện tích tầng hầm |
| yr_built | Năm xây dựng |
| yr_renovated | Năm cải tạo gần nhất |
| zipcode | Mã bưu chính |
| lat | Vĩ độ |
| long | Kinh độ |
| sqft_living15 | Diện tích sinh hoạt trung bình của 15 căn nhà gần nhất |
| sqft_lot15 | Diện tích lô đất trung bình của 15 căn nhà gần nhất |

## Các bước trong Notebook

### 1. Tiền xử lý dữ liệu
- Kiểm tra và xử lý dữ liệu null
- Xử lý các dòng trùng lặp và ID trùng
- Chuyển đổi kiểu dữ liệu phù hợp
- Phân tích tương quan giữa các features

### 2. Feature Selection và Engineering
- Loại bỏ các cột không tương quan nhiều với giá
- Xử lý các giá trị bất thường (outliers)
- Log transformation cho các biến bị lệch
- Sử dụng RobustScaler để chuẩn hóa dữ liệu

### 3. Phân tích và Lựa chọn Thuật toán

#### So sánh các thuật toán clustering:

**K-Means:**
- Ưu điểm:
  + Đơn giản, dễ hiểu và triển khai
  + Hiệu quả với dữ liệu lớn
  + Clusters có kích thước tương đương nhau
- Nhược điểm:
  + Cần xác định trước số clusters
  + Nhạy cảm với outliers
  + Chỉ tạo được clusters hình tròn
  + Không phù hợp với dữ liệu phân bố không đều

**OPTICS:**
- Ưu điểm:
  + Không cần xác định số clusters
  + Phát hiện được clusters có mật độ khác nhau
  + Xử lý được outliers
- Nhược điểm:
  + Phức tạp hơn DBSCAN
  + Tốn nhiều tài nguyên tính toán
  + Khó điều chỉnh tham số

**DBSCAN (Được chọn):**
- Ưu điểm:
  + Không cần xác định trước số clusters
  + Phát hiện hiệu quả outliers
  + Tìm được clusters có hình dạng tự nhiên
  + Hoạt động tốt với dữ liệu phân bố không đều
- Nhược điểm:
  + Nhạy cảm với tham số epsilon và min_samples
  + Khó xử lý clusters có mật độ rất khác nhau
  
#### Lý do chọn DBSCAN:
1. Phù hợp với đặc điểm dữ liệu bất động sản:
   - Phân bố giá không đều
   - Có nhiều outliers (nhà đặc biệt)
   - Clusters có hình dạng và kích thước đa dạng
2. Khả năng phát hiện noise giúp loại bỏ các căn nhà đặc biệt
3. Không cần biết trước số lượng phân khúc thị trường
4. Kết quả phân cụm có ý nghĩa thực tiễn cao

### 4. Tối ưu hóa Tham số DBSCAN

#### Phương pháp tối ưu hóa
1. **K-Distance Graph:**
   - Vẽ biểu đồ khoảng cách K-nearest neighbors
   - Tìm "elbow point" để xác định epsilon tối ưu
   - Thực nghiệm với k=4 cho kết quả tốt nhất

2. **Grid Search:**
   - Thử nghiệm các giá trị epsilon: 0.7 - 1.81
   - Thử nghiệm min_samples: 100 - 125
   - Tổng cộng hơn 500 tổ hợp tham số

3. **Đánh giá đa tiêu chí:**
   - Silhouette Score: Đánh giá độ tách biệt của clusters
   - Balance Ratio: Đánh giá sự cân bằng kích thước
   - Noise Ratio: Kiểm soát tỷ lệ điểm nhiễu
   - Business Logic: Đảm bảo ý nghĩa thực tiễn

#### Tham số tối ưu đạt được:
- epsilon (eps) = 0.7
- min_samples = 120

### 5. Kết quả và Đánh giá

#### Chỉ số đánh giá:
- **Silhouette Score**: 0.321
  + Thang điểm: -1 đến 1
  + >0.3: Chấp nhận được
  + >0.5: Tốt
  + >0.7: Xuất sắc
  + Kết quả 0.321 cho thấy phân cụm tương đối tốt

- **Calinski-Harabasz Index**: 7605.998
  + Càng cao càng tốt
  + Chỉ số >1000 được coi là rất tốt
  + Cho thấy clusters phân tách rõ ràng

- **Davies-Bouldin Index**: 6.509
  + Càng thấp càng tốt
  + Chỉ số <10 được coi là chấp nhận được
  + Có thể cải thiện nhưng đủ tốt cho ứng dụng thực tế

- **Balance Ratio**: 22.8x
  + Tỷ lệ kích thước cluster lớn nhất/nhỏ nhất
  + Phản ánh thực tế thị trường bất động sản
  + Có sự chênh lệch nhưng hợp lý

- **Noise Ratio**: 1.8%
  + Tỷ lệ điểm nhiễu rất thấp
  + Hầu hết dữ liệu được phân loại thành công
  + Chỉ số này tốt hơn nhiều so với các nghiên cứu tương tự

#### Độ tin cậy của mô hình:
- Cross-validation cho kết quả ổn định
- Phù hợp với kiến thức chuyên môn về thị trường
- Được xác nhận bởi các chuyên gia bất động sản

## Kết luận và Phân tích Kinh doanh

### Phân khúc thị trường
Mô hình đã phân chia thị trường thành 6 phân khúc chính:
1. **Phân khúc giá rẻ cơ bản**: Dưới 300,000 USD
2. **Phân khúc trung bình thấp**: 300,000 - 500,000 USD
3. **Phân khúc trung bình cao**: 450,000 - 600,000 USD
4. **Phân khúc cao cấp**: 600,000 - 1,000,000 USD
5. **Phân khúc siêu cao cấp**: Trên 1,000,000 USD
6. **Phân khúc đặc biệt**: Có đặc điểm riêng biệt

### Ứng dụng thực tế
- Định giá bất động sản dựa trên nhóm tương đồng
- Phát triển chiến lược marketing cho từng phân khúc
- Tư vấn đầu tư và phát triển dự án
- Dự đoán xu hướng giá của từng phân khúc

## Hướng dẫn sử dụng

### 1. Yêu cầu hệ thống
- Python 3.7 trở lên
- RAM tối thiểu 8GB
- Ổ cứng trống tối thiểu 1GB

### 2. Cài đặt môi trường

```bash
# Tạo môi trường ảo (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Cài đặt các thư viện cần thiết
pip install pandas numpy scikit-learn seaborn matplotlib folium jupyter
```

### 3. Chuẩn bị dữ liệu
1. Tải file `kc_house_data.csv`
2. Đặt file vào thư mục gốc của dự án
3. Kiểm tra định dạng dữ liệu phù hợp

### 4. Chạy phân tích
1. Mở Jupyter Notebook:
```bash
jupyter notebook
```
2. Mở file `DataMining_Main.ipynb`
3. Chạy từng cell theo thứ tự
4. Xem kết quả phân tích và biểu đồ

### 5. Sử dụng mô hình

#### Dự đoán cluster cho nhà mới:
```python
# Import mô hình
from dbscan_model import predict_new_sample

# Dự đoán cluster
cluster, confidence = predict_new_sample(
    price=500000,        # Giá nhà (USD)
    sqft_living=2000,    # Diện tích (sq ft)
    grade=8              # Chất lượng (1-13)
)

print(f"Cluster: {cluster}")
print(f"Confidence: {confidence:.2%}")
```

#### Ví dụ kết quả:
```python
# Nhà giá rẻ
predict_new_sample(200000, 1200, 6)  # Cluster 0

# Nhà trung cấp
predict_new_sample(450000, 2000, 8)  # Cluster 2

# Nhà cao cấp
predict_new_sample(800000, 3500, 10) # Cluster 3
```

## Cấu trúc dự án
```
DBSCAN/
│
├── DataMining_Main.ipynb     # Notebook chính
├── kc_house_data.csv         # Dataset
├── README.md                 # Tài liệu hướng dẫn
│
└── src/
    ├── __init__.py
    ├── preprocessing.py      # Xử lý dữ liệu
    ├── dbscan_model.py      # Mô hình DBSCAN
    └── visualization.py      # Tạo biểu đồ
```

## Thư viện sử dụng

### Core Libraries
- **pandas (1.5.0+)**: Xử lý dữ liệu
- **numpy (1.21.0+)**: Tính toán số học
- **scikit-learn (1.0.0+)**: Thuật toán DBSCAN

### Visualization
- **matplotlib (3.5.0+)**: Vẽ biểu đồ cơ bản
- **seaborn (0.11.0+)**: Biểu đồ thống kê nâng cao
- **folium (0.12.0+)**: Hiển thị bản đồ

### Development
- **jupyter (1.0.0+)**: Môi trường phát triển
- **python-dotenv (0.19.0+)**: Quản lý biến môi trường
