# BÁO CÁO PHÂN TÍCH KINH DOANH (BUSINESS CASE STUDY)
## Phân Khúc Thị Trường Bất Động Sản Seattle & Chiến Lược Định Giá Bằng DBSCAN

---

### 1. TỔNG QUAN DỰ ÁN (EXECUTIVE SUMMARY)
* **Bối cảnh kinh doanh:** Thị trường bất động sản King County (Seattle, Washington) có tính phân hóa cực kỳ cao với hơn 21,000 giao dịch. Việc định giá thủ công phụ thuộc nhiều vào cảm tính của môi giới, dẫn đến tình trạng định giá lệch so với thị trường, kéo dài thời gian thanh khoản hoặc làm mất biên lợi nhuận của chủ nhà.
* **Mục tiêu phân tích (Business Objective):** 
  * Khám phá các phân khúc tự nhiên của thị trường dựa trên tổ hợp **Giá bán (Price) - Quy mô sinh hoạt (Sqft Living) - Chất lượng xây dựng (Grade)**.
  * Nhận diện các bất động sản cá biệt (Outliers/Anomalies) để cảnh báo rủi ro định giá sai.
  * Đề xuất chiến lược danh mục sản phẩm và khuyến nghị hành động cụ thể cho Sàn môi giới và Nhà đầu tư.

---

### 2. PHÂN TÍCH BẢN CHẤT DỮ LIỆU & Ý NGHĨA KINH DOANH CỦA CÁC PHÂN CỤM

Sau khi làm sạch dữ liệu và tối ưu hóa tham số mật độ ($eps=0.7$, $min\_samples=120$), thuật toán DBSCAN đã phân loại thành công **21,436 giao dịch** thành **6 phân khúc chủ đạo** và **1 nhóm bất động sản cá biệt (Outlier)** với tỷ lệ nhiễu cực kỳ thấp (chỉ **1.81%**).

#### Bảng Tổng Hợp Chỉ Số Kinh Doanh Chi Tiết:

| Cluster | Tên phân khúc thị trường | Thị phần (%) | Số lượng | Giá trung vị (USD) | Diện tích TB (sqft) | Đơn giá TB (\$/sqft) | Grade chuẩn | Khu vực tập trung (Top Zipcodes) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | Nhà bình dân / Khởi điểm (Entry-level) | **9.29%** | 1,992 | **\$275,000** | 1,188 | \$271 | 6 | 98118, 98168, 98106 (Nam Seattle & Ven đô) |
| **0** | Nhà phổ thông trung bình thấp (Mass Market) | **41.50%** | 8,895 | **\$375,000** | 1,689 | \$252 | 7 | 98034, 98115, 98133 (Bắc Seattle & Kirkland) |
| **2** | Nhà trung cấp gia đình (Family Core) | **28.18%** | 6,040 | **\$510,000** | 2,184 | \$258 | 8 | 98052 (Redmond), 98103 (Green Lake) |
| **4** | Nhà cao cấp ven đô (Suburban Premium) | **12.13%** | 2,601 | **\$720,500** | 2,872 | \$276 | 9 | 98074, 98052, 98006 (Sammamish & Bellevue) |
| **5** | Dinh thự sang trọng (Executive Luxury) | **5.26%** | 1,127 | **\$915,000** | 3,527 | \$307 | 10 | 98075 (Sammamish), 98006 (Somerset) |
| **3** | Biệt thự siêu cao cấp (Ultra Luxury) | **1.83%** | 393 | **\$1,280,000** | 4,376 | \$342 | 11 | 98006 (Bellevue), 98040 (Mercer Island), 98004 |
| **-1** | Bất động sản cá biệt (Outliers / Specials) | **1.81%** | 388 | **\$280,000** | 2,312 | \$327 | 1–13 | 98056, 98006 (Nhà siêu đắt tới \$7.7M hoặc đất cực lớn) |

---

### 3. CHÂN DUNG KHÁCH HÀNG & SẢN PHẨM MỤC TIÊU (PERSONAS)

#### 🎯 Phân khúc Khối lượng lớn (Chiếm 69.68% thị phần - Cụm 0 & Cụm 2)
* **Đối tượng:** Gia đình trẻ có 1–2 con, nhân viên văn phòng, kỹ sư công nghệ tại Microsoft/Amazon.
* **Đặc tính:** Tìm kiếm nhà từ 1,600 – 2,200 sqft, chất lượng xây dựng đạt chuẩn (Grade 7–8), mức giá dao động \$375,000 – \$510,000.
* **Chiến lược môi giới:** Đây là phân khúc có tính thanh khoản cao nhất. Chiến lược marketing nên tập trung vào tiện ích trường học, giao thông công cộng và kết nối nhanh tới khu trung tâm công nghệ.

#### 💎 Phân khúc Thượng lưu & Siêu sang (Chiếm 7.09% thị phần - Cụm 5 & Cụm 3)
* **Đối tượng:** Giám đốc điều hành, doanh nhân, nhà đầu tư quốc tế.
* **Đặc tính:** Diện tích lớn (> 3,500 sqft), Grade từ 10–11, đơn giá vượt ngưỡng \$340/sqft. Tập trung tại đảo Mercer Island (98040) và trung tâm Bellevue (98004).
* **Chiến lược môi giới:** Bán hàng theo hình thức Private Listing (kín tiếng), dịch vụ tư vấn cá nhân hóa cao cấp.

#### ⚠️ Nhóm Outlier (-1) - Giá trị độc nhất của thuật toán DBSCAN
* **Ý nghĩa:** Trong khi K-Means ép buộc mọi ngôi nhà phải vào một cụm nào đó, DBSCAN đã cô lập được **388 căn nhà dị biệt** (giá lên tới 7.7 triệu USD, hoặc các căn nhà có chất lượng cực thấp Grade 1-3).
* **Giá trị thực tế:** Đối với nhóm này, **tuyệt đối không áp dụng định giá tự động bằng AI/Model**, mà phải gắn cờ cảnh báo (Flag for manual appraisal) để chuyên gia thẩm định giá trực tiếp.

---

### 4. ĐỀ XUẤT HÀNH ĐỘNG KINH DOANH (ACTIONABLE RECOMMENDATIONS)

1. **Tích hợp Mô hình Phân Cụm vào Cổng thông tin Khách hàng (CRM & Website):**
   * Cho phép khách hàng nhập thông số căn nhà (Giá dự kiến, diện tích, chất lượng) $\rightarrow$ Hệ thống tự động gán nhãn phân khúc và đề xuất 10 căn nhà tương đồng nhất trong cùng cụm.
2. **Chiến lược Đầu tư "Sửa nhà bán lướt sóng" (House Flipping Strategy):**
   * Lọc ra các căn nhà thuộc **Cluster 1 (Grade 6)** có vị trí giáp ranh khu vực **Cluster 0/2 (Grade 7–8)**. Đầu tư nâng cấp cải tạo (renovation) để nâng Grade từ 6 lên 7/8, gia tăng giá trị tài sản từ \$275k lên \$400k+ với biên lợi nhuận tối ưu.
3. **Cơ chế Cảnh báo sớm Rủi ro Thẩm định (Appraisal Risk Guardrail):**
   * Nếu căn nhà mới được phân loại là Outlier (`Cluster = -1`), hệ thống tự động khóa báo giá tự động và chuyển hồ sơ sang bộ phận Thẩm định rủi ro nội bộ.

---

### 5. LỘ TRÌNH TRIỂN KHAI VÀ CHỈ SỐ ĐO LƯỜNG (METRICS & ROADMAP)
* **Chỉ số theo dõi (KPIs):**
  * *Days on Market (DOM):* Giảm thời gian chờ bán của căn nhà xuống dưới 30 ngày nhờ định giá đúng phân khúc.
  * *Conversion Rate:* Tăng tỷ lệ chốt cọc thêm 15% khi tư vấn đúng giỏ hàng mục tiêu của khách.
  * *Pricing Variance:* Giữ biên độ chênh lệch giữa giá rao bán và giá chốt hợp đồng trong khoảng $\pm 3\%$.
