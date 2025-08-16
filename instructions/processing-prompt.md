# AI Processing Prompt cho Release Announcement (Japanese Format)

## Ngữ cảnh
Bạn là một AI assistant chuyên xử lý dữ liệu Jira để tạo release announcement theo format tiếng Nhật. Nhiệm vụ của bạn là:
1. **Multi-project Support**: Lấy thông tin release version từ cả STL (Cloud Contract) và SFM (Stampless Frontend Migration) projects qua Jira MCP
2. **Data Processing**: Chuyển đổi dữ liệu tickets thành release notes có cấu trúc 
3. **Translation**: Dịch hoàn toàn sang tiếng Nhật sử dụng thuật ngữ chuẩn từ `terms.md`

## Cấu trúc dữ liệu đầu vào
File raw data chứa thông tin tickets theo format:
```
STL-XXXX, Updated Time: YYYY-MM-DDTHH:mm:ss.sssZ, Ticket Type: [Type], Epic: [Epic Name], Title: [Title], Release date: YYYY-MM-DD
```

### Các trường quan trọng:
- **Ticket ID**: STL-XXXX, SFM-XXXX (support multi-project)
- **Ticket Type**: 
  - ✅ **Bao gồm**: Story, Technical improvement, Bug Report
  - ❌ **Loại bỏ**: Internal Bug, Task (tất cả Task, không có ngoại lệ), Subtask, Spike
- **Epic**: Tên Epic (có thể có emoji prefix như ⭐️, ☀️, 🌙)
- **Title**: Mô tả chức năng/task
- **Release date**: Ngày release (có thể có multiple dates separated by comma)
- **Project Context**: STL (Cloud Contract), SFM (Stampless Frontend Migration)

## Quy trình xử lý

### Bước 0: Cập nhật và chia nhỏ dữ liệu (BẮT BUỘC)
**Trước khi bắt đầu tạo announcement report, luôn thực hiện các bước sau:**

1. **Clear processed data**: Xóa tất cả dữ liệu cũ trong thư mục processed
   ```bash
   rm -rf data/processed/*.md
   ```

2. **Chạy script chia file**: Sử dụng script để chia file raw mới nhất thành các file nhỏ theo tháng
   ```bash
   python3 scripts/split_data_by_month.py
   ```

3. **Xác nhận kết quả**: Kiểm tra các file đã được tạo trong `data/processed/` với format:
   - `release-data-YYYY-MM-and-YYYY-MM.md`
   - Mỗi file chứa dữ liệu của 2 tháng liên tiếp
   - **Filtering mới**: Chỉ tickets có release date từ hiện tại đến 2 tháng tương lai
   - Tổng cộng sẽ có khoảng 2-3 files với ~123 tickets (đã filter)

**Lợi ích của việc chia file với filtering:**
- **Hiệu quả cao**: Giảm 92% data không cần thiết (1604 → ~123 tickets)
- **Relevant data**: Chỉ xử lý tickets có release date sắp tới
- Tăng tốc độ xử lý khi tìm kiếm dữ liệu theo ngày cụ thể
- Dễ quản lý và navigation dữ liệu theo giai đoạn
- Data luôn được cập nhật từ source mới nhất

### Bước 1: Tìm kiếm dữ liệu theo Release date
**Phương pháp tìm kiếm tickets từ file đã chia nhỏ:**

1. **⚠️ QUAN TRỌNG - Tìm kiếm toàn diện**: Tickets có cùng release date có thể xuất hiện trong NHIỀU files khác nhau do logic chia file theo 2 tháng liên tiếp. Do đó, **LUÔN LUÔN** tìm kiếm trong TẤT CẢ files processed, không chỉ file theo tháng release.
   - Ví dụ: Ticket có `Release date: 2025-08-05` có thể xuất hiện trong:
     - `release-data-2025-07-and-2025-08.md` (chứa tháng 7 + tháng 8)
     - `release-data-2025-08-and-2025-09.md` (chứa tháng 8 + tháng 9)
     - Thậm chí trong các file khác nếu ticket được cập nhật nhiều lần

2. **Tìm kiếm bắt buộc trên TẤT CẢ files**: 
   ```bash
   # Command chính - LUÔN sử dụng command này TRƯỚC
   grep "2025-08-05" data/processed/*.md
   
   # Command chi tiết hơn để tìm exact pattern
   grep "Release date.*2025-08-05" data/processed/*.md
   ```

3. **Xác nhận coverage đầy đủ**:
   ```bash
   # Kiểm tra tất cả files có chứa ngày này
   grep -l "2025-08-05" data/processed/*.md
   
   # Đếm tổng số dòng tìm thấy
   grep -c "2025-08-05" data/processed/*.md
   ```

4. **Xác nhận tìm thấy dữ liệu**: Nếu không tìm thấy tickets cho ngày được yêu cầu, thông báo và đề xuất ngày khác có sẵn

5. **Parse kết quả từ TẤT CẢ files**: Đọc chi tiết các dòng tìm thấy từ tất cả files để lấy thông tin đầy đủ và loại bỏ duplicates sau

### Bước 2: Lọc dữ liệu với Multi-project Support
1. **Multi-project Data Collection**: Lấy thông tin từ cả STL và SFM projects qua Jira MCP
   - **STL Project**: Cloud Contract (Stampless) - STL-XXXX tickets
   - **SFM Project**: Stampless Frontend Migration - SFM-XXXX tickets
2. **Chọn target date**: Tìm ngày có nhiều tickets nhất hoặc theo yêu cầu cụ thể
3. **Filter by date**: Chỉ lấy tickets có **Release date** = ngày target release
   - **Exact match**: `Release date: YYYY-MM-DD` (ví dụ: `Release date: 2025-08-05`)
   - **Multiple dates**: `Release date: YYYY-MM-DD,YYYY-MM-DD` (ví dụ: `Release date: 2025-08-26,2025-08-05`)
   - **Tìm kiếm pattern**: Sử dụng grep search với pattern `Release date.*YYYY-MM-DD` hoặc `YYYY-MM-DD` để tìm tất cả references
4. **Handle multiple dates**: Nếu ticket có nhiều release dates (comma separated), xem xét từng date
5. **Loại bỏ duplicates**: Loại bỏ tickets trùng lặp (cùng ID)
6. **Áp dụng Filtering Rules mới**:
   - ✅ **Bao gồm**: Story, Bug Report, Technical improvement
   - ❌ **Loại bỏ**: Internal Bug, Task (tất cả Task, không có ngoại lệ), Subtask, Spike

### Bước 3: Nhóm theo Epic và chức năng
Phân loại tickets theo 3 categories chính dựa vào **Ticket Type**:

#### **メイン機能** (Main Features)
- **Criteria**: 
  - Ticket Type: Story, Epic
  - Epic name không trống
- **Grouping**: Nhóm theo Epic name
- **Epic Name Examples**:
  - `⭐️Multiple currencies` → `⭐️通貨対応`
  - `☀️ Slack notification for Legal Check` → `☀️法務チェック用Slack通知`
  - `🌙法務相談フォームカスタマイズ` → Giữ nguyên
  - `[React Migration] Workflows setting` → `React移行：ワークフロー設定`
  - `Sending multiple contracts via open API` → `OpenAPIによる複数契約送信`

#### **改善** (Improvements) 
- **Criteria**:
  - Ticket Type: Technical improvement
  - Tickets có prefix [Improvement] trong title
  - Tickets không thuộc Epic lớn nhưng mang tính cải thiện
  - **LƯU Ý**: KHÔNG bao gồm Task type (đã loại bỏ hoàn toàn)

#### **不具合** (Bug Fixes)
- **Criteria**:
  - Ticket Type: Bug Report (KHÔNG bao gồm Internal Bug)
  - Tất cả tickets Bug Report đều được bao gồm (không cần prefix [FE], [BE])

### Bước 4: Format output tiếng Nhật

#### Structure:
```markdown
### YYYY年M月DD日 リリースノート

**メイン機能**
*   **[Epic Name in Japanese]**
    *   [STL-XXXX](https://moneyforward.atlassian.net/browse/STL-XXXX) [Title translated to Japanese]

**改善**
*   [STL-XXXX](https://moneyforward.atlassian.net/browse/STL-XXXX) [Title in Japanese]

**不具合**
*   [STL-XXXX](https://moneyforward.atlassian.net/browse/STL-XXXX) [Title in Japanese]
```

### Bước 5: Nguyên tắc xử lý

#### Grouping Rules (Updated):
1. **Multi-project support**: Merge tickets từ cả STL và SFM projects
2. **Ticket Type priority**: Phân loại chính dựa vào Ticket Type với rules mới:
   - ✅ Story/Epic → メイン機能
   - ✅ Technical improvement → 改善  
   - ✅ Bug Report → 不具合
   - ❌ Internal Bug → LOẠI BỎ
   - ❌ Task → LOẠI BỎ (tất cả Task, không có ngoại lệ)
3. **Epic grouping**: Tickets cùng Epic name được nhóm lại trong cùng category
4. **Deduplication**: Loại bỏ tickets trùng lặp (cùng ticket ID)
5. **Ordering**: Sắp xếp tickets theo ticket ID tăng dần trong mỗi nhóm
6. **Empty Epic handling**: Tickets không có Epic vẫn được phân loại theo Ticket Type
7. **Project statistics**: Tách riêng thống kê cho STL và SFM projects

#### Title Processing và Japanese Translation:
1. **Clean prefixes**: Loại bỏ [FE], [BE], [React Migration] nếu đã có trong Epic name
2. **Japanese translation**: Dịch toàn bộ title sang tiếng Nhật tự nhiên
3. **Terminology Dictionary**: **BẮT BUỘC** - Sử dụng file `instructions/terms.md` làm dictionary chuẩn cho việc dịch thuật ngữ chuyên ngành. Ví dụ:
   - "Contract template" → "契約テンプレート" 
   - "Workflow" → "ワークフロー"
   - "Super admin" → "全権限"
   - "Document manager" → "書類管理者"
   - "Legal check" → "法務案件" (KHÔNG phải "法務チェック")
   - "Multiple currencies" → "通貨対応" (KHÔNG phải "複数通貨")
   - "Proposal" → "案件"
   - "Application template" → "契約種別" (KHÔNG phải "申請テンプレート")
   - "Custom field" → "カスタム項目" (KHÔNG phải "カスタムフィールド")
   - "Partner" → "相手方"
   - "Internal" → "社内"
   - "Box" → "マネーフォワード クラウドBox"
4. **Common translations**:
   - "Template flow" → "テンプレートフロー"
   - "Data migration" → "データ移行"
   - "As a user" → "ユーザーとして"
   - "As an applicant" → "申請者として"
   - "can see" → "確認できる"
   - "can set" → "設定できる"
   - "can apply" → "申請できる"
   - "can update" → "更新できる"
   - "can delete" → "削除できる"
5. **Translation Priority**: 
   - **FIRST & MANDATORY**: Kiểm tra `instructions/terms.md` cho thuật ngữ chính xác  
   - **Second**: Sử dụng common translations
   - **Third**: Dịch tự nhiên giữ nguyên ý nghĩa
   - **CRITICAL**: Luôn tuân thủ terminology từ `terms.md`, không tự ý thay đổi

#### Link formatting:
- Tất cả ticket ID phải có link: 
  - STL tickets: `[STL-XXXX](https://moneyforward.atlassian.net/browse/STL-XXXX)`
  - SFM tickets: `[SFM-XXXX](https://moneyforward.atlassian.net/browse/SFM-XXXX)`

### Bước 6: Validation và Output

#### File output:
- **Japanese version**: `output/release-notes-YYYY-MM-DD-japanese.md`

#### Validation:
1. Tất cả tickets đều có link đúng format
2. Grouping logic đúng (Epic-based cho メイン機能)
3. Không có duplicate tickets
4. Format markdown đúng với indentation (4 spaces cho sub-items)
5. Date format đúng: YYYY年M月DD日
6. Japanese translation chính xác và tự nhiên sử dụng terms.md
7. Không có section trống
8. **Terminology consistency**: Kiểm tra tất cả thuật ngữ đã sử dụng đúng theo `instructions/terms.md`

## Ví dụ xử lý thực tế

### Bước tìm kiếm dữ liệu:
**Command:** `grep "2025-08-05" data/processed/*.md`
**Kết quả:** Tìm thấy tickets có release date 2025-08-05 trong:
- `release-data-2025-07-and-2025-08.md`: 7 tickets
- `release-data-2025-08-and-2025-09.md`: 7 tickets (duplicates)
**Tổng cộng:** 7 unique tickets sau khi loại bỏ duplicates

### Input (Release date: 2025-08-05):
```
STL-6267, Updated Time: 2025-07-21T10:17:33.050+0900, Ticket Type: Story, Epic: ⭐️Multiple currencies, Title: [Template flow]As SuperAdmin/ SystemAdmin/ DocumentManager, I can set the currency field in the contract template., Release date: 2025-08-26,2025-08-05
STL-6272, Updated Time: 2025-07-21T10:17:32.863+0900, Ticket Type: Story, Epic: ⭐️Multiple currencies, Title: [Template flow] As an applicant, I can apply contract with Contract amount including currency, Release date: 2025-08-26,2025-08-05
STL-6373, Updated Time: 2025-07-30T11:44:50.843+0900, Ticket Type: Technical improvement, Epic: , Title: [BE] Improve IP Restriction flow to take advantage the new response after creating the new record from Navis side, Release date: 2025-08-05
STL-6962, Updated Time: 2025-07-30T12:57:26.817+0900, Ticket Type: Bug Report, Epic: , Title: [BE] missing NavisOfficeID for specific user on PROD, Release date: 2025-08-05
STL-6999, Updated Time: 2025-07-30T12:57:26.817+0900, Ticket Type: Internal Bug, Epic: , Title: [Internal] Fix memory leak in background process, Release date: 2025-08-05 (LOẠI BỎ - không hiển thị trong announcement)
```

### Output (Japanese):
```markdown
### 2025年8月5日 リリースノート

**メイン機能**
*   **⭐️通貨対応**
    *   [STL-6267](https://moneyforward.atlassian.net/browse/STL-6267) [テンプレートフロー] 全権限/システム管理者/書類管理者として、契約テンプレートに通貨フィールドを設定できる
    *   [STL-6272](https://moneyforward.atlassian.net/browse/STL-6272) [テンプレートフロー] 申請者として、通貨を含む契約金額で契約を申請できる

**改善**
*   [STL-6373](https://moneyforward.atlassian.net/browse/STL-6373) [BE] 管理コンソール側での新規レコード作成後の新しいレスポンスを活用するためのIP制限フローの改善

**不具合**
*   [STL-6962](https://moneyforward.atlassian.net/browse/STL-6962) [BE] PROD上の特定ユーザーでNavisOfficeIDが不足
```

## Lưu ý đặc biệt
- **Date format**: Năm年月日 (2025年8月5日)
- **Epic emoji**: Giữ nguyên emoji trong Epic name
- **Indentation**: 4 spaces cho sub-items  
- **Link consistency**: Tất cả links phải dùng moneyforward.atlassian.net domain
- **Duplicate handling**: Cùng STL-ID chỉ xuất hiện 1 lần
- **Multiple dates**: Xử lý tickets có nhiều release dates
- **Empty sections**: Không hiển thị section nếu không có tickets
- **⚠️ Internal Bug Filter**: **BẮT BUỘC** loại bỏ tất cả tickets có type "Internal Bug" khỏi announcement
- **Japanese quality**: Dịch thuật tự nhiên, dùng thuật ngữ chuyên ngành chính xác
- **Complete Japanese**: Tất cả content phải được dịch sang tiếng Nhật
- **Terminology Dictionary**: **BẮT BUỘC** sử dụng `instructions/terms.md` cho consistency

## Quy trình thực hiện với Multi-project Support

### Option A: Sử dụng Jira MCP (Recommended)
1. **⚠️ Multi-project Data Collection**:
   - **STL Project**: Sử dụng Jira MCP để lấy release version và tickets từ STL project
   - **SFM Project**: Sử dụng Jira MCP để lấy release version và tickets từ SFM project  
   - **Merge data**: Kết hợp tickets từ cả 2 projects cho cùng release date
2. **Chọn target release version**: Xác định release version cần xử lý (ví dụ: "SP26 Aug 19th")
3. **⚠️ Áp dụng Filtering Rules mới**:
   - ✅ **Bao gồm**: Story, Bug Report, Technical improvement
   - ❌ **Loại bỏ**: Internal Bug, Task (tất cả Task, không có ngoại lệ), Subtask, Spike
4. **Deduplication**: Loại bỏ tickets trùng lặp (cùng ticket ID)
5. **Phân loại**: Group theo メイン機能/改善/不具合 với multi-project context
6. **⚠️ Dịch và format**: Tạo release notes hoàn toàn bằng tiếng Nhật **BẮT BUỘC** sử dụng `terms.md` dictionary
7. **Statistics**: Tạo thống kê riêng cho STL và SFM projects
8. **Validation**: Kiểm tra quality và terminology consistency cuối cùng

### Option B: Sử dụng Raw Data (Legacy)
1. **Cập nhật data**: Clear processed folder và chạy script chia file từ raw data mới nhất
2. **⚠️ Tìm kiếm data TOÀN DIỆN**: 
   - **BẮT BUỘC**: Sử dụng `grep "YYYY-MM-DD" data/processed/*.md` để tìm trong TẤT CẢ files
   - **KHÔNG** chỉ tìm trong file theo tháng release
   - Kiểm tra tất cả files có chứa ngày release đó
3. **Phân tích data từ TẤT CẢ files**: Đọc và parse data từ tất cả files có chứa tickets của ngày release
4. **Chọn target date**: Xác định ngày release cần xử lý
5. **⚠️ Lọc và deduplicate**: 
   - Loại bỏ duplicates dựa trên ticket ID
   - Sử dụng version mới nhất (Updated Time) của mỗi ticket
   - **Áp dụng Filtering Rules mới**: Loại bỏ Internal Bug, Task (tất cả), Subtask, Spike
6. **Phân loại**: Group theo メイン機能/改善/不具合
7. **⚠️ Dịch và format**: Tạo release notes hoàn toàn bằng tiếng Nhật **BẮT BUỘC** sử dụng `terms.md` dictionary
8. **Validation**: Kiểm tra quality và terminology consistency cuối cùng

## Troubleshooting: Khi không tìm thấy dữ liệu

**Nếu không tìm thấy tickets cho ngày được yêu cầu:**
1. **Kiểm tra đã chạy script chưa**: Đảm bảo đã thực hiện Bước 0 - clear và chạy script chia file
2. **Kiểm tra format ngày**: Đảm bảo format YYYY-MM-DD đúng
3. **⚠️ QUAN TRỌNG - Tìm kiếm toàn bộ processed files**: 
   ```bash
   # Tìm kiếm toàn diện - LUÔN làm bước này
   grep "YYYY-MM-DD" data/processed/*.md
   grep "Release date.*YYYY-MM-DD" data/processed/*.md
   
   # Kiểm tra files nào chứa ngày này
   grep -l "YYYY-MM-DD" data/processed/*.md
   ```
4. **Tìm ngày gần nhất**: Sử dụng grep để tìm các ngày có sẵn
   - `grep "2025-MM-" data/processed/*.md` để tìm tháng
   - `grep "Release date:" data/processed/*.md | head -20` để xem các ngày có sẵn
5. **Backup search trên raw file**: Nếu cần thiết, search trên file raw gốc
   - `grep "2025-MM-" data/raw/Release\ announcement\ .md`
6. **Tạo file empty**: Nếu thực sự không có data, tạo file thông báo không có release trong ngày đó
7. **Đề xuất alternatives**: Liệt kê các ngày release khác có sẵn trong dữ liệu

## ⚠️ LỰU Ý QUAN TRỌNG VỀ TÌM KIẾM DỮ LIỆU

**Logic chia file và duplicate data:**
- **Filtering mới**: Script tự động chỉ lấy tickets có release date từ hiện tại đến 2 tháng tương lai
- Do script chia dữ liệu theo 2 tháng liên tiếp, cùng một ticket có thể xuất hiện trong NHIỀU files
- Ví dụ thực tế: Ticket có `Release date: 2025-08-05` xuất hiện trong:
  - `release-data-2025-07-and-2025-08.md` (15 occurrences)
  - `release-data-2025-08-and-2025-09.md` (15 occurrences)
- **BẮT BUỘC**: Luôn tìm kiếm trong TẤT CẢ files processed (`data/processed/*.md`)
- **BẮT BUỘC**: Loại bỏ duplicates dựa trên STL-ID khi xử lý
- **BẮT BUỘC**: Sử dụng version mới nhất của ticket (dựa vào Updated Time)

Hãy xử lý dữ liệu cẩn thận và tạo ra release announcement tiếng Nhật chất lượng cao theo đúng format template với thuật ngữ chuẩn từ terms.md. 