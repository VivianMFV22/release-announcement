# Release Announcement Generator

## Mô tả
Tool tự động để tạo release announcement từ dữ liệu Jira thô sang format tiếng Nhật có cấu trúc với thuật ngữ chuẩn.

## Cấu trúc thư mục

```
release-announcement/
├── data/
│   ├── processed/           # Dữ liệu đã chia nhỏ theo tháng
│   │   ├── release-data-YYYY-MM-and-YYYY-MM.md
│   │   └── ... (10 files for different month pairs)
│   └── raw/                # Dữ liệu Jira thô (gốc)
│       └── Release announcement .md
├── instructions/
│   ├── processing-prompt.md # Hướng dẫn xử lý cho AI
│   └── terms.md            # Dictionary thuật ngữ tiếng Nhật chuẩn
├── output/                 # Release notes được tạo ra
│   └── release-notes-YYYY-MM-DD-japanese.md
├── scripts/                # Scripts quản lý dữ liệu
│   └── split_data_by_month.py  # Script chia file raw theo tháng
└── templates/
    └── release-announcement-template.md
```

## Quy trình sử dụng

### 1. Chuẩn bị dữ liệu
- Đặt file dữ liệu Jira thô vào thư mục `data/raw/`
- Format: `STL-XXXX, Updated Time: ..., Ticket Type: ..., Epic: ..., Title: ..., Release date: YYYY-MM-DD`

### 2. Chia nhỏ dữ liệu (Tùy chọn)
- Chạy script `python3 scripts/split_data_by_month.py` để chia file raw thành các file nhỏ
- **Logic chia file**: Mỗi file chứa dữ liệu của 2 tháng liên tiếp
  - File `release-data-2025-05-and-2025-06.md` → chứa data tháng 5 + tháng 6
  - File `release-data-2025-06-and-2025-07.md` → chứa data tháng 6 + tháng 7
  - File `release-data-2025-07-and-2025-08.md` → chứa data tháng 7 + tháng 8
- **Kết quả**: 876 tickets → 10 files, tên file sử dụng format số tháng đơn giản
- **Lợi ích**: Tăng tốc độ xử lý, dễ quản lý dữ liệu theo giai đoạn

### 3. Xử lý với AI
- Đọc hướng dẫn trong `instructions/processing-prompt.md`
- **Quan trọng**: AI sẽ sử dụng `instructions/terms.md` làm dictionary chuẩn
- Yêu cầu AI xử lý dữ liệu theo ngày release cụ thể
- **Nguồn dữ liệu**: Có thể sử dụng file raw gốc hoặc file đã chia nhỏ trong `data/processed/`
- AI sẽ tự động:
  - Lọc tickets theo ngày release
  - Phân loại theo Ticket Type (Story/Epic → メイン機能, Technical improvement → 改善, Bug → 不具合)
  - Nhóm theo Epic name trong cùng category
  - Dịch sang tiếng Nhật sử dụng thuật ngữ chuẩn
  - Tạo file output có cấu trúc

### 4. Kết quả
- File release notes tiếng Nhật được tạo trong thư mục `output/`
- Format: `release-notes-YYYY-MM-DD-japanese.md`

## Đặc điểm

### ✅ Tự động hóa
- Không cần code, chỉ cần AI assistant  
- Xử lý dữ liệu thô trực tiếp hoặc từ file đã chia nhỏ
- Tự động phân loại và nhóm tickets
- Script tự động chia file theo tháng (876 tickets → 10 files)

### ✅ Format tiếng Nhật chuẩn
- **Thuật ngữ consistency**: Sử dụng dictionary từ `terms.md`
- Dịch thuật chính xác thuật ngữ chuyên ngành
- Cấu trúc markdown đúng format
- Links đến Jira tickets

### ✅ Phân loại thông minh
- **メイン機能**: Ticket Type: Story, Epic (có Epic name)
- **改善**: Ticket Type: Technical improvement
- **不具合**: Ticket Type: Bug Report, Internal Bug

## Thuật ngữ chuẩn

File `instructions/terms.md` chứa dictionary mapping:
- **English → Japanese**: Thuật ngữ chuyên ngành Cloud Contract
- **Standardization**: Đảm bảo consistency trong translation
- **Examples**:
  - Contract template → 契約テンプレート
  - Workflow → ワークフロー
  - Super admin → 全権限
  - Legal check → 法務案件
  - Multiple currencies → 通貨対応

## Ví dụ Output

```markdown
### 2025年8月5日 リリースノート

**メイン機能**
*   **⭐️通貨対応**
    *   [STL-6267](https://moneyforward.atlassian.net/browse/STL-6267) 全権限として契約テンプレートに通貨フィールドを設定できる
    *   [STL-6272](https://moneyforward.atlassian.net/browse/STL-6272) 申請者として通貨を含む契約金額で契約を申請できる

**改善**
*   [STL-6373](https://moneyforward.atlassian.net/browse/STL-6373) 管理コンソールとの連携フローの改善

**不具合**
*   [STL-6962](https://moneyforward.atlassian.net/browse/STL-6962) PROD上のNavisOfficeID不足の修正
```

## Lưu ý
- **Terminology Priority**: Luôn kiểm tra `terms.md` trước khi dịch
- Tất cả content được dịch hoàn toàn sang tiếng Nhật
- Giữ nguyên emoji trong Epic names (nếu có)
- Phân loại dựa vào Ticket Type, không phụ thuộc emoji
- Links sử dụng domain moneyforward.atlassian.net
- Tự động loại bỏ duplicates và tickets không liên quan
- **Consistency**: Đảm bảo sử dụng thuật ngữ chuẩn từ dictionary 