import os
from pathlib import Path
import numpy as np
from google import genai
from dotenv import load_dotenv

# 1. 初始化環境與客戶端
load_dotenv()
client = genai.Client()

# 2. 自動掃描並讀取 data 資料夾中的所有 .md 檔案
data_dir = Path("data")
knowledge_base = []
file_sources = []

if data_dir.exists() and data_dir.is_dir():
    # 改為搜尋 .md 檔案
    for file_path in data_dir.glob("*.md"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                knowledge_base.append(content)
                file_sources.append(file_path.name)
else:
    print("❌ 找不到 data 資料夾，請確認是否已在專案根目錄建立！")
    exit()

if not knowledge_base:
    print("⚠️ data 資料夾中沒有找到任何有效的 .md 檔案內容！")
    exit()

print(f"✅ 成功從 data 資料夾載入 {len(knowledge_base)} 個 Markdown 檔案：{file_sources}\n")

# 3. 將知識庫文字轉換為向量 (Embedding)
print("正在將知識庫進行向量化...")
embed_response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=knowledge_base,
)
doc_embeddings = np.array([e.values for e in embed_response.embeddings])


# 4. 輔助函數：計算餘弦相似度 (Cosine Similarity)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 5. 使用者提問與檢索階段
user_query = "ERP 的核心價值是什麼？"
print(f"👤 使用者問題：{user_query}\n")

# 將使用者問題轉為向量
query_embed_response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=user_query,
)
query_vector = np.array(query_embed_response.embeddings[0].values)

# 計算相似度並找出最相關的檔案
similarities = [cosine_similarity(query_vector, doc_v) for doc_v in doc_embeddings]
best_match_idx = np.argmax(similarities)
retrieved_context = knowledge_base[best_match_idx]
retrieved_file = file_sources[best_match_idx]

print(f"📂 【最相關的來源檔案】: {retrieved_file}")
print(f"🔍 【檢索到的內部知識】:\n{retrieved_context}\n")

# 6. 生成階段：結合檢索內容與提問，呼叫 Gemini 進行回答
prompt = f"""
你是一個企業智慧小幫手。請根據以下提供給你的內部知識來回答使用者問題。如果知識中沒有答案，請誠實告知。

[內部知識]
{retrieved_context}

[使用者問題]
{user_query}
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
)

print(f"🤖 【Gemini 最終回答】:\n{response.text}")