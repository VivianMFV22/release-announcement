### 2025年8月19日 リリースノート

**メイン機能**
*   **【複数通貨】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6308](https://moneyforward.atlassian.net/browse/STL-6308) [一括送信フロー] 全権限/システム管理者/書類管理者として、一括送信契約テンプレートに通貨フィールドを設定できる
    *   [STL-6309](https://moneyforward.atlassian.net/browse/STL-6309) [一括送信フロー] ユーザーとして、通貨を含む契約金額で契約を申請できる
    *   [STL-6746](https://moneyforward.atlassian.net/browse/STL-6746) [FE] ユーザーとして、React版の契約種別でデフォルト通貨単位を設定できる
    *   [STL-6873](https://moneyforward.atlassian.net/browse/STL-6873) ステージング環境のフィーチャーフラグを削除し、全ステージング事業者で締結済み契約のデータ移行2を実施
    *   [STL-6947](https://moneyforward.atlassian.net/browse/STL-6947) (テスト中) ユーザーとして、通貨を含む契約をBoxに送信できる

*   **【Slack通知（法務チェック）】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6522](https://moneyforward.atlassian.net/browse/STL-6522) [FE] (React移行) Cloud Contractユーザーとして、新しい通知設定ページを見ることができる
    *   [STL-6591](https://moneyforward.atlassian.net/browse/STL-6591) 法務チェックユーザーとして、個人設定ページで法務チェックのSlack通知をオン/オフできる
    *   [STL-6759](https://moneyforward.atlassian.net/browse/STL-6759) Slack通知ユーザーとして、Cloud ContractとのSlackアカウントのリンクを解除できる

**改善**
*   [STL-6521](https://moneyforward.atlassian.net/browse/STL-6521) [BE] LightPDFの使用にフィーチャーフラグを使用
*   [STL-6712](https://moneyforward.atlassian.net/browse/STL-6712) [改善][BE][書類種別、印章種類、カスタム項目] ユーザーはリストの上部から最新の項目を見ることができる
*   [STL-7016](https://moneyforward.atlassian.net/browse/STL-7016) [FE] MultiSelect.vueのJSON.stringify問題を修正

**不具合**
*   [STL-7037](https://moneyforward.atlassian.net/browse/STL-7037) [BE] 締結済み画面リストで「書類承認番号」ソートヘッダーをクリックしても順序が変更されない