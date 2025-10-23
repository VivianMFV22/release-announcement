# AI Processing Prompt for Release Announcement (Japanese Format)

## Context
You are an AI assistant specialized in processing Jira data to create Japanese-format release announcements. Your tasks are:
1. **Data Processing**: Convert ticket data into structured release notes 
2. **Translation**: Translate completely to Japanese using standard terminology from `terms.md`
3. **Formatting**: Follow the template structure from `templates/release-announcement-template.md`

## Required Files Reference
- **`instructions/terms.md`**: MANDATORY dictionary for Japanese translations
- **`templates/release-announcement-template.md`**: Exact format structure to follow

## Data Retrieval and Processing

### Step 1: Get Release Version Data
**Single project support**: Process STL project only

1. **List project versions**: 
   ```
   mcp_jira-cloud_listProjectVersions
   - projectKey: "STL"
   - includeArchived: false
   ```

2. **Search tickets**: 
   ```
   mcp_jira-cloud_searchIssues
   - projectKey: "STL"
   - jql: "fixVersion = \"[ACTUAL_VERSION_NAME_FROM_STEP_1]\""
   - maxResults: 100
   - includeHierarchy: true
   - includeProgress: true
   ```
   
   **⚠️ IMPORTANT**: Use the actual version name found in Step 1, not a sample
   - Example: `"fixVersion = \"SP28 Sep 16th\""` (sample only)
   - Always use the exact version name from the project versions list

3. **⚠️ CRITICAL**: Always include `parent` field to get Epic information


### Step 2: Apply Filtering Rules
**⚠️ IMPORTANT**: Include ALL tickets tagged with the fix version, **regardless of status** (Done, In Development, To Do, etc.)

**Include:**
- ✅ Story, Bug Report, Technical improvement
- ✅ All status types: Done, In Development, In Review, To Do, Ready For Release, etc.

**Exclude:**
- ❌ Internal Bug, Task (all Tasks, no exceptions), Subtask, Spike

### Step 3: Categorize Tickets
**メイン機能** (Main Features):
- Stories with Epic (parent.fields.issuetype.name == "Epic")
- Group by Epic name: `parent.fields.summary`
- Format: **【Epic Name in Japanese】（一般公開する予定日：未定）**
- **Environment restrictions**:
  - **STL features (default)**: 
    - STG: Stampless with Biz - 事業者番号：8297-0083
    - PROD: Stampless 6789 事業者番号：6033-6255
  - **React migration features**: 
    - STG: Migration R Co.Ltd (Middle plan) - 事業者番号：2966-8562
    - PROD: ReactJS migration (Middle) 事業者番号：8769-0293

**改善** (Improvements):
- Technical improvement tickets
- Stories without Epic

**不具合** (Bug Fixes):
- Bug Report tickets only

### Step 4: Translation and Output ⚠️ CRITICAL - DO NOT SKIP
1. **🚨 TRANSLATE ALL CONTENT TO JAPANESE**: Use `instructions/terms.md` dictionary MANDATORY
   - **ALL ticket summaries MUST be translated to Japanese**
   - **ALL technical terms MUST use terms.md dictionary**
   - **NO English content should remain in final output**
2. **Epic Name Translation**: Translate Epic names to Japanese using `terms.md` dictionary
   - Example: "Multiple currencies" → "通貨対応"
   - Example: "React migration phase 3" → "React移行フェーズ3"
   - Example: "Choose multiple authorizers" → "複数承認者選択"
3. **Ticket Summary Translation Examples**:
   - "SuperAdmin/System Admin/ Doc Manager can receive..." → "全権限/システム管理者/書類管理者が...受信できます"
   - "Internal users (Admin/Operator) can see..." → "社内ユーザー（管理者/オペレーター）が...確認できます"
4. **Format**: Follow `templates/release-announcement-template.md` structure exactly
5. **Output**: Save to `output/release-announcement-YYYY-MM-DD-japanese.md`

### ⚠️ TRANSLATION CHECKLIST - VERIFY BEFORE COMPLETION:
- [ ] All Epic names translated using terms.md
- [ ] All ticket summaries translated to Japanese
- [ ] All role names translated (SuperAdmin → 全権限, System Admin → システム管理者, etc.)
- [ ] No English content remains except ticket keys (STL-XXXX)
- [ ] Links use moneyforward.atlassian.net domain

## ⚠️ CRITICAL - API Requirements

### Epic Field Requirements - CRITICAL
**⚠️ MANDATORY: Always include `parent` field when fetching Epic information**

**Problem**: Epic relationships are stored in `parent` field, NOT in Epic Link field
- **Epic Link** (`customfield_10014`): Often null for Stories
- **Parent** (`parent`): Contains actual Epic information

**Epic Data Structure:**
```json
{
  "key": "STL-XXXX",
  "parent": {    // THIS contains Epic information
    "key": "STL-6231",
    "fields": {
      "summary": "⭐️Multiple currencies",
      "issuetype": {"name": "Epic"}
    }
  }
}
```

**Impact**: Without parent field → All tickets go to 改善 section (WRONG)
**Solution**: With parent field → Proper Epic grouping in メイン機能 section (CORRECT)

### Data Processing Workflow
1. **Use MCP Jira tools**: All data retrieval through MCP tools
2. **Include all required fields**: Especially `parent` for Epic information
3. **Extract Epic relationships**: From parent field data structure
4. **Follow categorization rules**: Apply filtering and grouping logic

## Validation Checklist
- ✅ **Single project**: STL project processed
- ✅ **Fix Versions validated**: Check actual Fix Versions in Jira (not just release dates)
- ✅ **Epic information**: Retrieved via `parent` field
- ✅ **Filtering rules**: Applied correctly (exclude Internal Bug, Task)
- ✅ **🚨 CRITICAL - Japanese translation**: Using `terms.md` dictionary
- ✅ **🚨 CRITICAL - Epic name translation**: Epic names translated to Japanese using `terms.md`
- ✅ **🚨 CRITICAL - Ticket summaries translation**: ALL ticket summaries translated to Japanese
- ✅ **🚨 CRITICAL - Role names translation**: SuperAdmin → 全権限, System Admin → システム管理者, etc.
- ✅ **🚨 CRITICAL - No English content**: Except ticket keys (STL-XXXX) and URLs
- ✅ **Template format**: Followed exactly with environment restrictions
- ✅ **Links**: All use moneyforward.atlassian.net domain
- ✅ **Epic grouping**: NO individual listing in メイン機能, must group by Epic
- ✅ **STL tickets without Epic**: Move to 改善 section

### 🔥 FINAL VERIFICATION - BEFORE COMPLETING TASK:
**Read the entire output file and confirm:**
1. **Zero English ticket summaries remain** (except STL-XXXX keys)
2. **All role names use Japanese terms from terms.md**
3. **All Epic names are in Japanese**
4. **File name ends with -japanese.md**