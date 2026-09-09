# 🏢 企業內部智慧知識庫 (Gemini RAG System)

這是一套專為中小企業設計的輕量級 RAG（檢索增強生成）知識庫系統。透過 Google Gemini API、ChromaDB 與 Streamlit，讓企業能輕鬆將散落的 Markdown 文件（SOP、規章、說明書）轉化為具備高精準度的內部智慧問答助理。

---

## 📂 專案目錄結構

```text
company_rag_system/
├── data/                    # 存放企業內部各類 Markdown 知識庫文件
├── chroma_db/               # ChromaDB 本地持久化資料庫儲存目錄（執行同步後自動產生）
├── utils/
│   ├── __init__.py
│   └── chunker.py           # Markdown 語意切塊模組
├── sync_kb.py               # 知識庫同步腳本（負責檢測變更並寫入向量資料庫）
├── app.py                   # Streamlit 網頁互動介面主程式
├── requirements.txt         # 專案相依套件清單
└── .env                     # API 金鑰等環境變數
```

## ⚙️ 環境建置與安裝步驟

### 1. 建立並啟動虛擬環境
打開終端機，執行以下指令：

```bash
python -m venv venv
# Windows 啟動指令：
.\venv\Scripts\Activate
```

### 2. 安裝相依套件
```bash
pip install google-genai python-dotenv numpy chromadb streamlit
```

### 3. 設定 API 金鑰
在專案根目錄下建立一個 `.env` 檔案，並填入您的 Google AI Studio API 金鑰：

```env
GEMINI_API_KEY=您的_API_金鑰
```

---

## 🚀 系統使用與操作指南

### 步驟一：準備知識庫文件
將企業內部的 Markdown 文件（`.md`）放入 `data/` 資料夾中。

### 步驟二：同步知識庫
每次新增或修改內部文件後，執行同步腳本將文件進行語意切塊、向量化並寫入 ChromaDB：

```bash
python sync_kb.py
```

### 步驟三：啟動網頁聊天介面
執行 Streamlit 啟動本機網頁伺服器：

```bash
streamlit run app.py
```

瀏覽器將自動開啟網頁介面，即可開始進行智慧問答與文件來源檢視！

---

## 🛠️ 技術棧 (Tech Stack)

* **大語言模型**：`gemini-2.5-flash` / `gemini-1.5-pro`
* **向量化模型**：`gemini-embedding-2`
* **向量資料庫**：ChromaDB (Local Persistent)
* **介面框架**：Streamlit
* **官方 SDK**：`google-genai`
