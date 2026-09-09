import streamlit as st
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

# 連結本地 ChromaDB
db_client = chromadb.PersistentClient(path="./chroma_db")
collection = db_client.get_or_create_collection(name="company_knowledge")

st.set_page_config(page_title="企業內部智慧小幫手", page_icon="🏢")
st.title("🏢 企業內部智慧知識庫 (RAG)")
st.markdown("請在下方輸入您的問題，系統將自動檢索內部 Markdown 檔案並為您解答。")

user_query = st.text_input("💬 請輸入問題：")

if user_query:
    with st.spinner("⏳ 正在檢索內部知識與生成回答..."):
        # 1. 取得使用者問題的 Embedding
        q_resp = client.models.embed_content(
            model="gemini-embedding-2",
            contents=user_query
        )
        q_vector = q_resp.embeddings[0].values
        
        # 2. 從 ChromaDB 檢索最相關的前 3 個片段
        results = collection.query(
            query_embeddings=[q_vector],
            n_results=3
        )
        
        retrieved_docs = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        
        if not retrieved_docs:
            st.warning("⚠️ 找不到相關的內部知識，請確認知識庫是否有同步資料。")
        else:
            # 3. 組合上下文
            context = "\n\n---\n\n".join(retrieved_docs)
            
            # 4. 呼叫 Gemini 3.6 Flash 生成回答
            prompt = f"""
你是一個專業的企業智慧小幫手。請嚴格根據以下提供的內部知識來回答使用者問題。如果內部知識中完全沒有答案，請誠實告知「根據現有內部知識無法回答」。絕對不要自行瞎編。

[內部知識片段]
{context}

[使用者問題]
{user_query}
"""
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            
            st.subheader("💡 智慧回答")
            st.write(response.text)
            
            # 5. 顯示參考來源
            with st.expander("🔍 檢視引用的內部知識與來源檔案"):
                for idx, (doc, meta) in enumerate(zip(retrieved_docs, metadatas)):
                    st.markdown(f"**來源檔案：** `{meta.get('source', '未知')}`")
                    st.markdown(f"**內文片段：**\n> {doc}")
                    st.markdown("---")