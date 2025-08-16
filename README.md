# Release Announcement Generator

## Mô tả
Tool tự động để tạo release announcement từ dữ liệu Jira thô sang format tiếng Nhật có cấu trúc với thuật ngữ chuẩn. Hỗ trợ tạo release announcement từ nhiều project Jira (STL và SFM) đồng thời.

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
- **Multi-project support**: Lấy release version trên cả 2 project STL (Cloud Contract) và SFM (Stampless Frontend Migration)
- Đặt file dữ liệu Jira thô vào thư mục `data/raw/`
- Format: `STL-XXXX, Updated Time: ..., Ticket Type: ..., Epic: ..., Title: ..., Release date: YYYY-MM-DD`
- **Jira MCP Integration**: Sử dụng Jira MCP để lấy thông tin release version và tickets từ cả STL và SFM projects

### 2. Chia nhỏ dữ liệu với filtering (Tùy chọn)
- Chạy script `python3 scripts/split_data_by_month.py` để chia file raw thành các file nhỏ
- **Logic filtering**: 
  - **Release Date**: Chỉ lấy tickets có release date từ hiện tại đến 2 tháng trong tương lai
- **Logic chia file**: Mỗi file chứa dữ liệu của 2 tháng liên tiếp
  - File `release-data-2025-07-and-2025-08.md` → chứa data tháng 7 + tháng 8
  - File `release-data-2025-08-and-2025-09.md` → chứa data tháng 8 + tháng 9
- **Kết quả**: 1604 tickets → ~123 filtered tickets, chỉ tạo 2-3 files relevant
- **Lợi ích**: 
  - Tăng tốc độ xử lý đáng kể (giảm 92%+ data không cần thiết)
  - Chỉ xử lý tickets có release date sắp tới
  - Dễ quản lý dữ liệu theo giai đoạn

### 3. Xử lý với AI
- Đọc hướng dẫn trong `instructions/processing-prompt.md`
- **Quan trọng**: AI sẽ sử dụng `instructions/terms.md` làm dictionary chuẩn
- Yêu cầu AI xử lý dữ liệu theo ngày release cụ thể
- **Nguồn dữ liệu**: Có thể sử dụng file raw gốc hoặc file đã chia nhỏ trong `data/processed/`
- AI sẽ tự động:
  - Lấy thông tin release version từ cả STL và SFM projects qua Jira MCP
  - Lọc tickets theo ngày release và ticket type rules
  - **Filtering rules mới**: 
    - ✅ **Bao gồm**: Story, Bug Report, Technical improvement
    - ❌ **Loại bỏ**: Internal Bug, Task (tất cả Task, không có ngoại lệ)
  - Phân loại theo Ticket Type (Story/Epic → メイン機能, Technical improvement → 改善, Bug Report → 不具合)
  - Nhóm theo Epic name trong cùng category
  - Dịch sang tiếng Nhật sử dụng thuật ngữ chuẩn từ file `terms.md`
  - Tạo file output có cấu trúc cho multi-project

### 4. Kết quả
- File release notes tiếng Nhật được tạo trong thư mục `output/`
- Format: `release-notes-YYYY-MM-DD-japanese.md`

## Đặc điểm

### ✅ Tự động hóa
- Không cần code, chỉ cần AI assistant  
- **Filtering thông minh**: Tự động lọc tickets theo release date (2 tháng tương lai)
- Xử lý dữ liệu thô trực tiếp hoặc từ file đã chia nhỏ
- Tự động phân loại và nhóm tickets
- Script tự động chia file theo tháng với filtering (1604 → ~123 tickets relevant)

### ✅ Format tiếng Nhật chuẩn
- **Thuật ngữ consistency**: Sử dụng dictionary từ `terms.md`
- Dịch thuật chính xác thuật ngữ chuyên ngành
- Cấu trúc markdown đúng format
- Links đến Jira tickets

### ✅ Phân loại thông minh với Multi-project support
- **Multi-project data**: Tự động merge data từ STL và SFM projects
- **Filtering rules được cập nhật**: 
  - ✅ **Bao gồm**: Story, Bug Report, Technical improvement
  - ❌ **Loại bỏ**: Internal Bug, Task (tất cả Task, không có ngoại lệ)
- **メイン機能**: Ticket Type: Story, Epic (có Epic name)
  - Format: **【Epic Name】（一般公開する予定日：未定）**
  - Bao gồm thông tin hạn chế môi trường (STG/PROD) theo template
- **改善**: Ticket Type: Technical improvement
- **不具合**: Ticket Type: Bug Report (chỉ Bug Report, KHÔNG bao gồm Internal Bug hoặc Task)

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
### 2025年7月22日 リリースノート

**メイン機能**
*   **【複数通貨】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6363](https://moneyforward.atlassian.net/browse/STL-6363) ユーザーとして、締結済み契約リストで通貨による並べ替えが可能
    *   [STL-6266](https://moneyforward.atlassian.net/browse/STL-6266) [通常フロー] 申請者として、通貨を含む契約を申請できます

*   **【Slack通知（法務チェック）】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6522](https://moneyforward.atlassian.net/browse/STL-6522) [FE] (React移行) Cloud Contractユーザーとして、新しい通知設定ページを見ることができます
    *   [STL-6759](https://moneyforward.atlassian.net/browse/STL-6759) Slack通知ユーザーとして、Cloud ContractとのSlackアカウントのリンクを解除できます

**改善**
*   [STL-6521](https://moneyforward.atlassian.net/browse/STL-6521) [BE] LightPDFの使用にフィーチャーフラグを使用
*   [STL-6712](https://moneyforward.atlassian.net/browse/STL-6712) [Improvement][BE][DocumentType,StampType,CustomFields] ユーザーはリストの上部から最新の項目を見ることができます

**不具合**
*   [STL-6863](https://moneyforward.atlassian.net/browse/STL-6863) 締結証明書PDFで簡体字中国語のフォントが表示されます
*   [STL-6900](https://moneyforward.atlassian.net/browse/STL-6900) [BE]ユーザーグループに基づいて権限が設定されている場合、支払側は契約を表示できません
```

## Lưu ý
- **Multi-project Integration**: Hỗ trợ lấy data từ cả STL và SFM projects qua Jira MCP
- **Terminology Priority**: **BẮT BUỘC** kiểm tra `terms.md` trước khi dịch mọi thuật ngữ
- Tất cả content được dịch hoàn toàn sang tiếng Nhật
- **Format chuẩn cho メイン機能**:
  - Sử dụng 【】thay vì ⭐️ emoji
  - Thêm thông tin ngày release: （一般公開する予定日：未定）
  - **STG/PROD info theo template**: 
    - STG: Stampless with Biz - 事業者番号：8297-0083
    - PROD: Stampless 6789 事業者番号：6033-6255
- **Filtering Rules mới (cập nhật)**:
  - ✅ **Bao gồm**: Story, Bug Report, Technical improvement
  - ❌ **Loại bỏ**: Internal Bug, Task (tất cả Task, không có ngoại lệ)
- Phân loại dựa vào Ticket Type, không phụ thuộc emoji
- Links sử dụng domain moneyforward.atlassian.net
- Tự động loại bỏ duplicates và tickets không liên quan
- **Terminology Consistency**: **BẮT BUỘC** sử dụng thuật ngữ chuẩn từ `terms.md` dictionary