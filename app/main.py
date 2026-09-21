import os
import json
import urllib.request
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Orca-Editorial Agent")

templates = Jinja2Templates(directory="app/templates")

client = OpenAI(
    base_url="https://api.orcarouter.ai/v1",
    api_key=os.getenv("ORCAROUTER_API_KEY", "dummy_key")
)

TAVILY_KEY_PATH = "/Users/pulsar/Downloads/tavily.txt"
TAVILY_API_KEY = ""
if os.path.exists(TAVILY_KEY_PATH):
    with open(TAVILY_KEY_PATH, "r") as f:
        TAVILY_API_KEY = f.read().strip()

class GenerateRequest(BaseModel):
    theme: str
    step: str = "writing"
    article: str = ""

def perform_web_search(query: str):
    if not TAVILY_API_KEY:
        return [{"title": "設定エラー", "body": "Tavily APIキーが読み込めませんでした。"}]
    try:
        url = "https://api.tavily.com/search"
        data = json.dumps({
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 3
        }).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
        formatted_results = []
        for r in result.get("results", []):
            formatted_results.append({"title": r.get("title", "No Title"), "body": r.get("content", "No Content")})
        if not formatted_results:
            return [{"title": "検索結果なし", "body": "関連する情報が見つかりませんでした。"}]
        return formatted_results
    except Exception as e:
        return [{"title": "検索エラー", "body": str(e)}]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/generate")
async def generate_step(req: GenerateRequest):
    model_map = {
        "research": "orcarouter/free",
        "writing": "orcarouter/auto",
        "fact_check": "orcarouter/auto"
    }
    model_name = model_map.get(req.step, "orcarouter/auto")

    async def event_generator():
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
                agent_name = "リサーチエージェント"
            elif req.step == "writing":
                system_prompt = "あなたはプロのWebライターです。提供されたWebリサーチ結果（最新情報）を必ず踏まえて、読者を惹きつけるマークダウン形式の記事を執筆してください。"
                agent_name = "執筆エージェント"
            else:
                system_prompt = "あなたは厳格なファクトチェッカーです。記事の内容が論理的かつ事実に基づいているか検証し、必要に応じて修正案を提示してください。"
                agent_name = "ファクトチェックエージェント"
                yield json.dumps({"type": "status", "message": "🧐 ファクトチェックエージェント起動（記事の検証中...）", "progress": 30}) + "\n"

            if req.step == "fact_check":
                prompt = f"テーマ: {req.theme}\n\n【検証対象の記事本文】\n{req.article}\n\n上記の記事の内容が論理的かつ事実に基づいているか検証し、修正箇所があれば指摘し、完成版の記事を出力してください。"
            else:
                prompt = f"テーマ: {req.theme}\n\n{search_context}\n\n上記の情報を踏まえ、タスクを実行してください。"

            yield json.dumps({"type": "status", "message": f"🤖 {agent_name}がテキストをストリーミング生成中...", "progress": 70}) + "\n"

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
                timeout=120.0  # 2分応答がなければタイムアウト
            )
            
            actual_model = model_name
            full_text = ""
            for chunk in response:
                if hasattr(chunk, 'model') and chunk.model:
                    actual_model = chunk.model
                    
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_text += delta
                        yield json.dumps({"type": "chunk", "content": delta}) + "\n"
                        
            yield json.dumps({"type": "status", "message": "✨ すべての処理が完了しました！", "progress": 100}) + "\n"
            
            # ストリーミング時はトークン数がAPIから返らない事が多いので文字数から概算
            estimated_tokens = len(full_text)
            cost = round(estimated_tokens * 0.01, 2)
            
            yield json.dumps({
                "type": "done",
                "actual_model": actual_model,
                "tokens": estimated_tokens,
                "cost_estimate_jpy": cost
            }) + "\n"

        except Exception as e:
            yield json.dumps({"type": "error", "message": str(e)}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
