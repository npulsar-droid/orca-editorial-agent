#!/bin/bash
# Deploy to Google Cloud Run

# APIキーを環境変数またはローカルファイルから取得
if [ -z "$ORCAROUTER_API_KEY" ]; then
    if [ -f "/Users/pulsar/Downloads/orcarouter-1.txt" ]; then
        ORCAROUTER_API_KEY=$(cat /Users/pulsar/Downloads/orcarouter-1.txt)
    fi
fi

if [ -z "$TAVILY_API_KEY" ]; then
    if [ -f "/Users/pulsar/Downloads/tavily.txt" ]; then
        TAVILY_API_KEY=$(cat /Users/pulsar/Downloads/tavily.txt)
    fi
fi

if [ -z "$ORCAROUTER_API_KEY" ]; then
    echo "エラー: ORCAROUTER_API_KEY が取得できませんでした。"
    exit 1
fi

echo "🚀 Cloud Run へデプロイを開始します..."

gcloud run deploy orca-editorial-agent \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars="ORCAROUTER_API_KEY=${ORCAROUTER_API_KEY},TAVILY_API_KEY=${TAVILY_API_KEY}"

echo "✅ デプロイコマンドが完了しました！"
