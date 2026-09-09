def chunk_markdown(text: str) -> list[str]:
    """根據 Markdown 標題（# 和 ##）進行智慧語意切塊"""
    # 以第一層標題 (#) 切分
    primary_chunks = [c.strip() for c in text.split("# ") if c.strip()]
    final_chunks = []
    
    for p_chunk in primary_chunks:
        # 如果區塊內還有第二層標題 (##)，進一步細分
        sub_chunks = [sc.strip() for sc in p_chunk.split("## ") if sc.strip()]
        for sc in sub_chunks:
            if sc:
                # 為了保留標題語意，可以把標題補回去或直接保留內文
                final_chunks.append(sc)
                
    # 如果檔案內完全沒有寫標題，就退回到以完整文字作為一個 chunk
    if not final_chunks and text.strip():
        final_chunks.append(text.strip())
        
    return final_chunks
