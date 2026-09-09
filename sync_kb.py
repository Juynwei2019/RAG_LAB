import os
from pathlib import Path
import chromadb
from google import genai
from dotenv import load_dotenv
from utils.chunker import chunk_markdown

# 初始化環境與客戶端
load_dotenv()
client = genai.Client()

# 初始化 ChromaDB 本地持久化資料庫（會自動在專案下建立 chroma_db 資料夾）
db_client = chromadb.PersistentClient(path="./chroma_db")
collection = db_client.get_or_create_collection(name="company_knowledge")

data_dir = Path("data")
if not data_dir.exists() or not data_dir.is_dir():
    print("❌ 找不到 data 資料夾，請確認是否已建立！")
    exit()

total_new_chunks = 0

# 掃描所有 .md 檔案
for file_path in data_dir.glob("*.md"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        
        # 進行切塊
        chunks = chunk_markdown(text)
        print(f"📄 處理檔案: {file_path.name} (切出 {len(chunks)} 個片段)")
        
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{file_path.name}_chunk_{idx}"
            
            # 檢查 ChromaDB 中是否已存在該片段，避免重複計算 API 費用
            existing = collection.get(ids=[chunk_id])
            if not existing['ids']:
                print(f"  ⏳ 正在向量化新片段: {chunk_id}")
                
                # 呼叫 Gemini Embedding API
                resp = client.models.embed_content(
                    model="gemini-embedding-2",
                    contents=chunk
                )
                vector = resp.embeddings[0].values
                
                # 寫入 ChromaDB
                collection.add(
                    ids=[chunk_id],
                    embeddings=[vector],
                    documents=[chunk],
                    metadatas=[{"source": file_path.name}]
                )
                total_new_chunks += 1
            else:
                print(f"  ⏩ 已存在，略過: {chunk_id}")

print(f"\n✅ 知識庫同步完成！本次新增向量化片段數: {total_new_chunks}")