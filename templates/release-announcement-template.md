

### 2025年7月22日 リリースノート

**メイン機能**
*   **React移行：ワークフロー設定**
    *   [STL-6728](https://moneyforward.atlassian.net/browse/STL-6728) [React移行] リストと詳細でのドラッグ＆ドロップ機能の実装
*   **複数通貨**
    *   [STL-6363](https://moneyforward.atlassian.net/browse/STL-6363) ユーザーとして、締結済み契約リストで通貨による並べ替えが可能
    *   [STL-6266](https://moneyforward.atlassian.net/browse/STL-6266) [通常フロー] 申請者として、通貨を含む契約を申請できます
    *   [STL-6394](https://moneyforward.atlassian.net/browse/STL-6394) [通常フロー] 申請者として、内部・取引先承認保留中/差戻し/却下された契約で通貨値を確認できます
*   **Slack通知（法務チェック）**
    *   [STL-6522](https://moneyforward.atlassian.net/browse/STL-6522) [FE] (React移行) Cloud Contractユーザーとして、新しい通知設定ページを見ることができます
    *   [STL-6759](https://moneyforward.atlassian.net/browse/STL-6759) Slack通知ユーザーとして、Cloud ContractとのSlackアカウントのリンクを解除できます
    *   [STL-6591](https://moneyforward.atlassian.net/browse/STL-6591) 法務チェックユーザーとして、個人設定ページで法務チェックのSlack通知をオン/オフできます
*   **Open APIによるテンプレートからの契約送信**
    *   [STL-6886](https://moneyforward.atlassian.net/browse/STL-6886) ユーザーが意図的に連携済みの取引先項目を入力した場合、システムはそれらの値をスキップして保存しません。
    *   [STL-6699](https://moneyforward.atlassian.net/browse/STL-6699) ユーザーは、契約テンプレートのリストを見るための新しいAPIを呼び出すことができます
    *   [STL-6700](https://moneyforward.atlassian.net/browse/STL-6700) ユーザーは、既存のAPIを呼び出してワークフローテンプレートを取得できます
    *   [STL-6701](https://moneyforward.atlassian.net/browse/STL-6701) ユーザーは、テンプレートを選択して契約を作成するための新しいAPIを呼び出すことができます
    *   [STL-6702](https://moneyforward.atlassian.net/browse/STL-6702) テンプレートで作成された契約の場合、ユーザーは契約ファイルを更新できません
    *   [STL-6703](https://moneyforward.atlassian.net/browse/STL-6703) ユーザーは、テンプレートで作成された契約に取引先を設定できます
    *   [STL-6704](https://moneyforward.atlassian.net/browse/STL-6704) ユーザーは、承認リクエストのために契約を送信できます（テスト）

**改善**
*   [STL-6521](https://moneyforward.atlassian.net/browse/STL-6521) [BE] LightPDFの使用にフィーチャーフラグを使用
*   [STL-6712](https://moneyforward.atlassian.net/browse/STL-6712) [Improvement][BE][DocumentType,StampType,CustomFields] ユーザーはリストの上部から最新の項目を見ることができます

**不具合**
*   [STL-6863](https://moneyforward.atlassian.net/browse/STL-6863) 締結証明書PDFで簡体字中国語のフォントが表示されます
*   **債務支払マスター参照（第2リリース）**
    *   [STL-6900](https://moneyforward.atlassian.net/browse/STL-6900) [BE]ユーザーグループに基づいて権限が設定されている場合、支払側は契約を表示できません
