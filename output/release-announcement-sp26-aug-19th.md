### 2025年8月19日 リリースノート - SP26

**メイン機能**
*   **【React移行 - 契約種別管理】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [SFM-437](https://moneyforward.atlassian.net/browse/SFM-437) [FE] 契約種別 - 各契約種別（電子契約・紙契約）で最大100個のカスタム項目を追加できない問題
    *   [SFM-413](https://moneyforward.atlassian.net/browse/SFM-413) ユーザーとして、エラー数を含むトップメッセージを確認できます
    *   [SFM-290](https://moneyforward.atlassian.net/browse/SFM-290) ユーザーとして、契約種別リストでドラッグ＆ドロップができます（ワークフローリストコンポーネント再利用）
    *   [SFM-189](https://moneyforward.atlassian.net/browse/SFM-189) ユーザーとして、契約種別を削除できます
    *   [SFM-407](https://moneyforward.atlassian.net/browse/SFM-407) ユーザー編集モーダルでユーザーグループドロップダウンの検索機能を有効化

*   **【通貨対応】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6947](https://moneyforward.atlassian.net/browse/STL-6947) (テスト中) ユーザーとして、通貨を含む契約をマネーフォワード クラウドBoxに送信できます
    *   [STL-6746](https://moneyforward.atlassian.net/browse/STL-6746) [FE] ユーザーとして、React版の契約種別でデフォルト通貨単位を設定できます
    *   [STL-6309](https://moneyforward.atlassian.net/browse/STL-6309) [一括送信フロー] ユーザーとして、通貨を含む契約金額で契約を申請できます
    *   [STL-6308](https://moneyforward.atlassian.net/browse/STL-6308) [一括送信フロー] 全権限/システム管理者/書類管理者として、一括送信テンプレートに通貨フィールドを設定できます
    *   [STL-6873](https://moneyforward.atlassian.net/browse/STL-6873) ステージング環境のフィーチャーフラグを削除し、全ステージング事業者で締結済み契約のデータ移行2を実施

*   **【Slack通知（法務案件）】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6749](https://moneyforward.atlassian.net/browse/STL-6749) [Email][BE] 法務担当者として、Slack通知と一致した案件完了通知メールを確認できます
    *   [STL-6592](https://moneyforward.atlassian.net/browse/STL-6592) 法務担当者として、法務案件のメール通知をオフにできます

*   **【カスタム項目拡張】**
    *   [STL-6508](https://moneyforward.atlassian.net/browse/STL-6508) フラグなし事業者のユーザーとして、最大100個のカスタム項目で契約種別と契約申請を正常に使用できます（回帰テスト）

**改善**
*   [STL-7016](https://moneyforward.atlassian.net/browse/STL-7016) [FE] MultiSelect.vueのJSON.stringify問題を修正

**不具合**
*   [STL-7082](https://moneyforward.atlassian.net/browse/STL-7082) [BE] タイムアウトが承認リクエストをキャンセルし、マルチステップワークフローで「認証なし」エラーを引き起こす
*   [STL-7037](https://moneyforward.atlassian.net/browse/STL-7037) [BE] 締結済み画面リストで「文書承認番号」ソートヘッダークリックで順序が変更されない
*   [SFM-437](https://moneyforward.atlassian.net/browse/SFM-437) [FE] 契約種別 - 各契約種別（電子契約・紙契約）で最大100個のカスタム項目を追加できない

**注意事項**
- 通貨対応機能は段階的リリースのため、現在は制限付きの事業者のみで利用可能です
- React移行（契約種別管理）は段階的移行中です。ステージング環境の3つのVueJS事業者は継続して旧システムを使用します
- 一部の機能はまだQAテスト中またはリリース準備中です
- カスタム項目の上限が100個に拡張されました
- SFM プロジェクトの一部機能（回帰テスト、バグバッシュフィードバック処理など）は次回リリースで完了予定です

**リリース統計**

**STL (Cloud Contract - Stampless):**
- 総チケット数: 22
- 完了: 12 (55%)
- 進行中: 9
- 未開始: 1

**SFM (Stampless Frontend Migration):**
- 総チケット数: 9
- 完了: 4 (44%)
- 進行中: 3
- 未開始: 2

**合計:**
- 総チケット数: 31
- 完了: 16 (52%)
- 進行中: 12
- 未開始: 3

---
*本リリースは、Cloud Contract（Stampless）プロダクトの継続的な改善とReact移行による新機能追加を目的としています。*