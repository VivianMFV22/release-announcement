# Release Announcement Generator

## Description
Automated tool to generate Japanese release announcements from Jira data with structured formatting and standardized terminology. Supports creating release announcements from multiple Jira projects (STL and SFM) simultaneously.

## Directory Structure

```
release-announcement/
├── data/                        # Legacy data (not used in new workflow)
│   ├── processed (not use)/     # Split data (not used)
│   └── raw/                     # Raw Jira data (not used)
├── instructions/
│   ├── processing-prompt.md     # AI processing instructions
│   └── terms.md                 # Standard Japanese terminology dictionary
├── output/                      # Generated release notes
│   └── release-announcement-YYYY-MM-DD-japanese.md
├── scripts/                     # Legacy scripts (not used in new workflow)
│   └── split_data_by_month(not_use).py
├── templates/
│   └── release-announcement-template.md
└── README.md
```

## Usage Workflow

### 1. Preparation
- **Multi-project support**: Access both STL (Cloud Contract) and SFM (Stampless Frontend Migration) projects via Jira MCP
- **Jira MCP Integration**: Use Jira MCP to retrieve release version info and tickets directly from Jira API
- **Real-time data**: No raw data files needed, everything retrieved from Jira API

### 2. AI Processing
- Read instructions in `instructions/processing-prompt.md`
- **Important**: AI will use `instructions/terms.md` as the standard dictionary
- Request AI to process data for specific release date
- **Data Source**: Use Jira MCP to access Jira data directly

#### 🔧 **CRITICAL Jira MCP Tools Usage**
**⚠️ To avoid getting stuck, use these EXACT tool names:**

1. **List Release Versions**:
   ```
   mcp_jira-cloud_listProjectVersions
   - projectKey: "STL" or "SFM"
   - includeArchived: false
   ```

2. **Search Tickets by Fix Version**:
   ```
   mcp_jira-cloud_searchIssues
   - projectKey: "STL" or "SFM"  
   - jql: "fixVersion = \"SP26 Aug 19th\""
   - maxResults: 100
   - includeHierarchy: true
   - includeProgress: true
   ```

**❌ NEVER use non-existent tools like:**
- `mcp_jira-cloud_searchTickets`
- `mcp_jira-cloud_getTickets`
- Any tool not starting with `mcp_jira-cloud_`

- AI will automatically:
  - Retrieve release version info from both STL and SFM projects via Jira MCP
  - Filter tickets by release version and ticket type rules
  - **New filtering rules**: 
    - ✅ **Include**: Story, Bug Report, Technical improvement
    - ❌ **Exclude**: Internal Bug, Task (all Tasks, no exceptions)
  - Categorize by Ticket Type (Story/Epic → メイン機能, Technical improvement → 改善, Bug Report → 不具合)
  - Group by Epic name within same category
  - Translate to Japanese using standard terminology from `terms.md` file
  - Create structured output file for multi-project

### 3. Results
- Japanese release notes file created in `output/` directory
- Format: `release-announcement-YYYY-MM-DD-japanese.md`

## Features

### ✅ Automation
- No coding required, only AI assistant with Jira MCP
- **Smart filtering**: Automatically filter tickets by release version
- Direct Jira data access via MCP integration
- Automatic ticket classification and grouping
- Real-time data processing from Jira API

### ✅ Standard Japanese Format
- **Terminology consistency**: Use dictionary from `terms.md`
- Accurate translation of technical terminology
- Proper markdown structure format
- Links to Jira tickets

### ✅ Smart Classification with Multi-project Support
- **Multi-project data**: Automatically merge data from STL and SFM projects
- **Updated filtering rules**: 
  - ✅ **Include**: Story, Bug Report, Technical improvement
  - ❌ **Exclude**: Internal Bug, Task (all Tasks, no exceptions)
- **メイン機能**: Ticket Type: Story, Epic (with Epic name)
  - **⚠️ CRITICAL Epic Grouping Rule**: Tickets with same Epic name MUST be grouped together under that Epic
  - Format: **【Epic Name】（一般公開する予定日：未定）**
  - Include environment restriction info (STG/PROD) per template
  - **Epic sub-listing**: All tickets belonging to the same Epic are listed as sub-items under the Epic heading
  - **NO individual listing**: Story/Epic tickets must NOT be listed individually in メイン機能 - they must be grouped by Epic
  - **STL tickets without Epic**: Move to 改善 section
  - **SFM tickets**: Group in separate "【React 移行】" section
- **改善**: 
  - Ticket Type: Technical improvement
  - STL Story/Epic tickets without Epic
- **不具合**: Ticket Type: Bug Report (Bug Report only, NOT including Internal Bug or Task)

## Standard Terminology

The `instructions/terms.md` file contains dictionary mapping:
- **English → Japanese**: Cloud Contract technical terminology
- **Standardization**: Ensure consistency in translation
- **Examples**:
  - Contract template → 契約テンプレート
  - Workflow → ワークフロー
  - Super admin → 全権限
  - Legal check → 法務案件
  - Multiple currencies → 通貨対応

## Output Example

```markdown
### 2025年7月22日 リリースノート

**メイン機能**
*   **【通貨対応】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6363](https://moneyforward.atlassian.net/browse/STL-6363) ユーザーとして、締結済み契約リストで通貨による並べ替えが可能
    *   [STL-6266](https://moneyforward.atlassian.net/browse/STL-6266) [通常フロー] 申請者として、通貨を含む契約を申請できます

*   **【法務チェック用Slack通知】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6522](https://moneyforward.atlassian.net/browse/STL-6522) [FE] (React移行) Cloud Contractユーザーとして、新しい通知設定ページを見ることができます
    *   [STL-6759](https://moneyforward.atlassian.net/browse/STL-6759) Slack通知ユーザーとして、Cloud ContractとのSlackアカウントのリンクを解除できます

> **Epic Grouping Example**: Notice how tickets with the same Epic are grouped together under the Epic heading, not listed individually

**改善**
*   [STL-6521](https://moneyforward.atlassian.net/browse/STL-6521) [BE] LightPDFの使用にフィーチャーフラグを使用
*   [STL-6712](https://moneyforward.atlassian.net/browse/STL-6712) [Improvement][BE][DocumentType,StampType,CustomFields] ユーザーはリストの上部から最新の項目を見ることができます

**不具合**
*   [STL-6863](https://moneyforward.atlassian.net/browse/STL-6863) 締結証明書PDFで簡体字中国語のフォントが表示されます
*   [STL-6900](https://moneyforward.atlassian.net/browse/STL-6900) [BE]ユーザーグループに基づいて権限が設定されている場合、支払側は契約を表示できません
```

## Important Notes
- **Multi-project Integration**: Support data retrieval from both STL and SFM projects via Jira MCP
- **Terminology Priority**: **MANDATORY** check `terms.md` before translating any terminology
- All content must be completely translated to Japanese
- **Standard format for メイン機能**:
  - Use 【】instead of ⭐️ emoji
  - Add release date info: （一般公開する予定日：未定）
  - **STG/PROD info per template**: 
    - **STL features**: 
      - STG: Stampless with Biz - 事業者番号：8297-0083
      - PROD: Stampless 6789 事業者番号：6033-6255
    - **React 移行 (SFM features)**:
      - STG: Migration R Co.Ltd (Middle plan) - 事業者番号：2966-8562
      - PROD: ReactJS migration (Middle) - 事業者番号：8769-0293
- **⚠️ CRITICAL - Fix Versions Validation Rule (New)**:
  - **MANDATORY**: Check actual Fix Versions in Jira, NOT just based on release date in raw data
  - **Reason**: Tickets may have multiple release dates due to quarterly versions (e.g., ☀️ Q3Y25) but only belong to 1 specific release version
  - **Process**: Use Jira MCP to get Fix Versions of each ticket and only include tickets belonging to the exact requested release version
  - **Example**: STL-6521 has release date "2025-08-19,2025-07-22" but Fix Versions = ["☀️ Q3Y25", "SP24 Jul 22th"] → NOT part of "SP26 Aug 19th"
- **New Filtering Rules (Updated)**:
  - ✅ **Include**: Story, Bug Report, Technical improvement
  - ❌ **Exclude**: Internal Bug, Task (all Tasks, no exceptions)
- Classification based on Ticket Type, not dependent on emoji
- Links use moneyforward.atlassian.net domain
- Automatically remove duplicates and irrelevant tickets
- **Terminology Consistency**: **MANDATORY** use standard terminology from `terms.md` dictionary
- **⚠️ Fix Versions Priority**: **MANDATORY** check actual Fix Versions instead of just relying on release dates to avoid including tickets already released in other versions