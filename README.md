# Phân cụm giá nhà Seattle sử dụng thuật toán DBSCAN

Dự án này thực hiện phân tích và phân cụm dữ liệu giá nhà tại Seattle, Washington sử dụng thuật toán DBSCAN (Density-Based Spatial Clustering of Applications with Noise) để phân loại các căn nhà thành các nhóm có đặc điểm tương tự về giá cả, diện tích và chất lượng xây dựng.

## Mô tả Dataset

Dataset `kc_house_data.csv` bao gồm thông tin về các căn nhà tại Seattle với các thông tin chính:
- Giá nhà (price)
- Diện tích sinh hoạt (sqft_living)
- Số phòng ngủ và phòng tắm
- Chất lượng xây dựng (grade)
- Vị trí (latitude, longitude)
- Và nhiều thông tin khác

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
- So sánh K-Means, OPTICS và DBSCAN
- Phân tích ưu/nhược điểm của mỗi thuật toán
- Lựa chọn DBSCAN vì khả năng xử lý outliers và phát hiện clusters có hình dạng tự nhiên

### 4. Tối ưu hóa Tham số DBSCAN
- Sử dụng K-Distance Graph để xác định epsilon
- Grid Search để tìm tham số tối ưu
- Đánh giá mô hình với nhiều metrics khác nhau

### 5. Kết quả và Đánh giá
- Silhouette Score: 0.321
- Calinski-Harabasz Index: 7605.998
- Davies-Bouldin Index: 6.509
- Balance Ratio: 22.8x
- Noise Ratio: 1.8%

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

## Cách sử dụng

1. Cài đặt các thư viện cần thiết:
```python
pip install pandas numpy scikit-learn seaborn matplotlib folium
```

2. Chạy notebook theo thứ tự các cell
3. Sử dụng hàm predict_new_sample() để dự đoán cluster cho nhà mới:
```python
predict_new_sample(price, sqft_living, grade)
```

## Thư viện sử dụng
- pandas
- numpy
- sklearn
- matplotlib
- seaborn
- folium
