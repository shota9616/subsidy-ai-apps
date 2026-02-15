# AI経営管理 Streamlitアプリ

補助金申請書類生成・記事下書き・戦略分析のWebアプリケーション。

## 🚀 クイックスタート

```bash
# ローカル実行
streamlit run app.py

# デプロイ（Streamlit Cloud）
# GitHubにpush → 自動デプロイ
```

## 📁 プロジェクト構造

```
.
├── app.py                    # ホームページ（ポータル）
├── pages/
│   ├── 1_香川県補助金申請.py  # 🟢 稼働中 - メイン機能
│   ├── 2_記事下書き.py        # 🟡 開発中
│   └── 3_戦略分析.py          # 🟡 開発中
├── lib/
│   ├── auth.py               # 認証（パスワード保護）
│   ├── styles.py             # 共通スタイル・フッター
│   ├── anthropic_client.py   # Claude API クライアント
│   └── file_utils.py         # ファイル操作ユーティリティ
├── modules/
│   └── subsidy/kagawa_mirai/ # 香川県補助金モジュール
│       ├── hearing_reader.py      # ヒアリングシート読込
│       ├── ai_text_generator.py   # AI文章生成
│       ├── document_generator.py  # 書類生成
│       ├── calculate_plan.py      # 収支計画計算
│       ├── data_models.py         # データモデル
│       └── validator.py           # 要件検証
├── templates/kagawa_mirai/   # Word/Excelテンプレート
└── assets/kagawa_mirai/      # サンプルファイル
```

## 🎯 香川県補助金申請（メイン機能）

### ワークフロー
1. **ヒアリングシートアップロード** - 7シート構成のExcel
2. **データプレビュー** - 企業情報・財務・経費を表示
3. **AI文章生成** - Claude APIで事業計画書10セクションを自動生成
4. **文章編集** - 生成テキストの確認・修正
5. **書類生成** - Word/Excel4種を出力
6. **検証** - 付加価値・給与要件をチェック
7. **ZIPダウンロード**

### 生成書類
- 交付申請書（Excel）
- 事業計画書（Word）
- 収支計画書（Excel）
- 誓約書（Word）

### データモデル（data_models.py）
- `HearingData` - ヒアリングシート全体
- `CompanyInfo` - 企業基本情報
- `FinancialInfo` - 財務データ
- `ExpenseItem` - 経費項目
- `EffectInfo` - 効果（売上増・コスト削減）
- `WageInfo` - 賃上げ計画

## 🔧 開発ガイド

### 環境変数（secrets.toml）
```toml
password = "xxx"           # 認証パスワード
ANTHROPIC_API_KEY = "sk-xxx"  # Claude API
```

### コード修正時の注意
1. **テンプレート修正** → `templates/kagawa_mirai/` 内のWord/Excel
2. **AI生成文の調整** → `modules/subsidy/kagawa_mirai/ai_text_generator.py`
3. **収支計算ロジック** → `calculate_plan.py`
4. **UI/UXの変更** → `pages/1_香川県補助金申請.py`

### よく編集するファイル
| 目的 | ファイル |
|------|----------|
| プロンプト調整 | `ai_text_generator.py` |
| 書類フォーマット | `document_generator.py` |
| 計算ロジック | `calculate_plan.py` |
| バリデーション | `validator.py` |
| UI変更 | `pages/1_香川県補助金申請.py` |

## 🌐 デプロイ

**本番URL:** https://ks1997616-cbwzpjpam4hwg2rjgmfwdf.streamlit.app/

- Streamlit Cloudで自動デプロイ（mainブランチpush時）
- Secretsは Streamlit Cloud の設定画面で管理

## 📝 TODO / 開発メモ

<!-- ここに開発中のタスクや改善案を記録 -->

---

*このファイルを編集してプロジェクトの最新状態を反映してください*
