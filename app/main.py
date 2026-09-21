import os
import json
import urllib.request
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# OrcaRouter APIキーの読み込み（Cloud Run環境変数 優先）
ORCAROUTER_API_KEY = os.getenv("ORCAROUTER_API_KEY", "")
if not ORCAROUTER_API_KEY:
    ORCA_KEY_PATH = "/Users/pulsar/Downloads/orcarouter-1.txt"
    if os.path.exists(ORCA_KEY_PATH):
        with open(ORCA_KEY_PATH, "r") as f:
            ORCAROUTER_API_KEY = f.read().strip()

client = OpenAI(
    base_url="https://api.orcarouter.ai/v1",
    api_key=ORCAROUTER_API_KEY
)

# APIキーの設定
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
if not TAVILY_API_KEY:
    TAVILY_KEY_PATH = "/Users/pulsar/Downloads/tavily.txt"
    if os.path.exists(TAVILY_KEY_PATH):
        with open(TAVILY_KEY_PATH, "r") as f:
            TAVILY_API_KEY = f.read().strip()

class GenerateRequest(BaseModel):
    theme: str
    step: str
    article: str = ""
    model: str = "orcarouter/auto"

def perform_web_search(query: str):
    if not TAVILY_API_KEY:
        return [{"title": "エラー", "body": "Tavily APIキーが設定されていません。"}]
    
    try:
        url = "https://api.tavily.com/search"
        data = json.dumps({
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": 5
        }).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        
        results = []
        for r in result.get("results", []):
            results.append({"title": r.get("title"), "body": r.get("content")})
        return results
    except Exception as e:
        return [{"title": "エラー", "body": f"検索中にエラーが発生しました: {str(e)}"}]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/generate")
async def generate_content(req: GenerateRequest):
    async def generate_stream():
        try:
            search_context = ""
            if req.step in ["research", "writing"]:
                if req.article.strip():
                    yield json.dumps({"type": "status", "message": "📄 事前知識（ファイル）を読み込んでいます...", "progress": 40}) + "\n"
                    search_context = f"【提供された事前リサーチ結果・コンテキスト】\n{req.article}\n\n"
                else:
                    yield json.dumps({"type": "status", "message": "🔍 リサーチエージェント起動（Tavily検索中...）", "progress": 20}) + "\n"
                    search_results = perform_web_search(req.theme)
                    search_context = "【Webリサーチ結果（最新情報）】\n"
                    for r in search_results:
                        search_context += f"- タイトル: {r.get('title')}\n  内容: {r.get('body')}\n\n"
                    yield json.dumps({"type": "status", "message": "✅ リサーチ完了。最新情報を取得しました。", "progress": 40}) + "\n"

            if req.step == "research":
                system_prompt = "あなたは優秀なリサーチャーです。提供されたWeb検索結果を元に、テーマに関する最新情報をわかりやすく要約してレポートを作成してください。"
                prompt = f"テーマ: {req.theme}\n\n{search_context}"
            elif req.step == "writing":
                system_prompt = "あなたはプロのWebライターです。提供されたリサーチ結果を元に、読者を惹きつける魅力的なブログ記事をMarkdown形式で執筆してください。"
                prompt = f"テーマ: {req.theme}\n\n{search_context}\n\n【指示】見出し、箇条書き、太字などを効果的に使い、Markdownで出力してください。"
            elif req.step == "fact_check":
                system_prompt = "あなたは厳格なファクトチェッカー兼プロの編集者です。記事本文に事実誤認や飛躍がないかをチェックし、修正箇所をリストアップした上で、修正を反映したリライト後の記事全文を作成してください。"
                prompt = f"テーマ: {req.theme}\n\n【検証対象の記事本文】\n{req.article}\n\n【指示】\n1. 修正が必要な箇所・理由・修正案を、以下のMarkdown Table形式で厳密に出力してください。（Markdownとして正しく認識されるよう、必ず表の直前に空行を1行入れてください）\n\n| 該当箇所 | 理由 | 修正案 |\n|---|---|---|\n| (該当箇所) | (理由) | (修正案) |\n\n※修正がない場合は「修正なし」と記載してください。\n2. テーブルの下に、「## リライト後の記事本文」という見出しをつけ、上記の修正案を全て反映した完成版の記事全文を出力してください。"
            else:
                raise ValueError("Invalid step")
                
            model_name = req.model

            yield json.dumps({"type": "status", "message": "🤖 エージェントがテキストをストリーミング生成中...", "progress": 70}) + "\n"
            
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
                timeout=300.0  # 推論モデル（o1やR1）の思考時間を考慮して5分に変更
            )
            
            actual_model = model_name
            full_text = ""
            
            for chunk in response:
                if getattr(chunk, "model", None):
                    actual_model = chunk.model
                
                content = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta.content else ""
                if content:
                    full_text += content
                    yield json.dumps({"type": "chunk", "content": content}) + "\n"
            
            tokens = len(full_text)
            cost = tokens * 0.0003
            yield json.dumps({"type": "done", "actual_model": actual_model, "tokens": tokens, "cost_estimate_jpy": round(cost, 2)}) + "\n"

        except Exception as e:
            yield json.dumps({"type": "error", "message": str(e)}) + "\n"

    return StreamingResponse(generate_stream(), media_type="application/x-ndjson")
