### 2025年8月19日 リリースノート

**メイン機能**
*   **【共通アドレス帳】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-7019](https://moneyforward.atlassian.net/browse/STL-7019) ユーザーとして、設定ページから共通アドレス帳にアクセスできます
    *   [STL-6753](https://moneyforward.atlassian.net/browse/STL-6753) ユーザーとして、相手方レコードをソートとページネーション機能付きのリストで確認できます

*   **【通貨対応】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6746](https://moneyforward.atlassian.net/browse/STL-6746) 全権限/システム管理者/書類管理者として、Reactバージョンの契約種別でデフォルト通貨単位を設定できます
    *   [STL-6309](https://moneyforward.atlassian.net/browse/STL-6309) ユーザーとして、一括送信フローで通貨を含む契約金額で契約を申請できます
    *   [STL-6308](https://moneyforward.atlassian.net/browse/STL-6308) 全権限/システム管理者/書類管理者として、一括送信テンプレートで通貨フィールドを設定できます
    *   [STL-6947](https://moneyforward.atlassian.net/browse/STL-6947) ユーザーとして、通貨を含む契約をマネーフォワード クラウドBoxに送信できます
    *   [STL-6873](https://moneyforward.atlassian.net/browse/STL-6873) ステージング環境のフィーチャーフラグを削除し、全ステージング事業者の締結済み契約データ移行を実行

*   **【法務案件用Slack通知】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Stampless with Biz - 事業者番号：8297-0083　
    > - PROD: Stampless 6789 事業者番号：6033-6255

    *   [STL-6749](https://moneyforward.atlassian.net/browse/STL-6749) 法務案件ユーザーとして、Slack通知と一貫性のある案件完了通知メールを確認できます
    *   [STL-6592](https://moneyforward.atlassian.net/browse/STL-6592) 法務案件ユーザーとして、個人設定ページで法務案件のメール通知をオン/オフできます

*   **【React 移行】（一般公開する予定日：未定）**
    > 一般公開まで以下の事業者で制限
    > - STG: Migration R Co.Ltd (Middle plan) - 事業者番号：2966-8562
    > - PROD: ReactJS migration (Middle) - 事業者番号：8769-0293

    *   [SFM-413](https://moneyforward.atlassian.net/browse/SFM-413) ユーザーとして、エラー数を含むトップメッセージを確認できます
    *   [SFM-290](https://moneyforward.atlassian.net/browse/SFM-290) ユーザーとして、リスト内で契約種別をドラッグ&ドロップできます
    *   [SFM-189](https://moneyforward.atlassian.net/browse/SFM-189) ユーザーとして、契約種別を削除できます

**改善**
*   [STL-7016](https://moneyforward.atlassian.net/browse/STL-7016) MultiSelect.vueのJSON.stringify問題を修正
*   [STL-6508](https://moneyforward.atlassian.net/browse/STL-6508) フラグなし事業者のユーザーとして、最大100個のカスタム項目で契約種別と契約申請を正常に使用できます（回帰テスト）

**不具合**
*   [STL-7082](https://moneyforward.atlassian.net/browse/STL-7082) タイムアウトが承認依頼をキャンセルし、複数ステップワークフローで「認証なし」エラーを引き起こす問題を修正
*   [STL-7037](https://moneyforward.atlassian.net/browse/STL-7037) 締結完了画面リストで「承認稟議番号」ソートヘッダーをクリックしても順序が変わらない問題を修正
