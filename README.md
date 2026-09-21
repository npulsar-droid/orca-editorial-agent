# Orca-Editorial Agent ✍️

<img src="https://github.com/user-attachments/assets/7dab2322-a740-4c19-bbb6-a9f977669d72" width="800" alt="UIイメージ">

**Orca-Editorial Agent** は、AIと人間が協業（Human-in-the-loop）して、高品質な記事を作成するための業務自動化エージェントです。
リサーチ、執筆、ファクトチェック・校正の3つのステップに分割し、工程ごとに最適なLLM（OrcaRouter経由）を自動で切り替えることで、**コストを劇的に抑えながらプロ品質のテキスト**を生み出します。

## 🎯 主な機能

1. **リサーチ (Research)**
   * 指定したテーマに基づいて、Tavily APIを用いて最新のWeb情報を検索・要約します。
   * 安価で高速なモデル（`orcarouter/free` 等）を活用し、推論コストを最小限に抑えます。
2. **構成・執筆 (Writing)**
   * リサーチノートを元に、Markdown形式の記事を下書きします。
3. **ファクトチェック・校正 (Fact Check & Proofreading)**
   * 最新のハイエンドモデル（`Claude 3.5 Sonnet` 等）を使用し、論理の飛躍（校閲）や誤字脱字（校正）を厳しくチェックします。
   * 外部で人間が書いた原稿の持ち込み・添削にも対応。

## 💡 アーキテクチャと技術スタック

* **Frontend**: HTML5, JavaScript, Tailwind CSS
* **Backend**: Python, FastAPI
* **AI Gateway**: OrcaRouter (OpenAI互換APIでのモデル動的ルーティング)
* **External API**: Tavily Search API
* **Infrastructure**: Google Cloud Run

## 🚀 ローカル環境での動かし方

1. リポジトリをクローンし、必要なライブラリをインストールします。
```bash
git clone https://github.com/yourusername/orca-editorial-agent.git
cd orca-editorial-agent
pip install -r requirements.txt
```

2. 環境変数を設定します。
```bash
export ORCAROUTER_API_KEY="your_orcarouter_api_key"
export TAVILY_API_KEY="your_tavily_api_key"
```

3. FastAPIサーバーを起動します。
```bash
uvicorn app.main:app --reload --port 8080
```
ブラウザで `http://localhost:8080` にアクセスしてください。

## ☁️ Cloud Run へのデプロイ

同梱されている `deploy.sh` を実行することで、Google Cloud Run へ簡単にデプロイできます。

```bash
./deploy.sh
```
※事前に `gcloud` CLI のインストールとログインが必要です。

---
*Developed for AI HACK 2026*
