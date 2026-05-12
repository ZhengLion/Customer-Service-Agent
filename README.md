# Customer Service Agent

## 環境
- Python 3.11
- MySQL 8.0
- Ollama + qwen2.5:7b

## 步驟

### 建立conda環境
```bash
conda create -n cs-agent python=3.11 -y
conda activate cs-agent
pip install langgraph langchain langchain-ollama pymysql sqlalchemy python-dotenv
```

### 設定.env
DB_HOST=localhost
DB_PORT=3306
DB_USER=agent_user
DB_PASSWORD=your_password
DB_NAME=cs_agent
LLM_MODEL=qwen2.5:7b

### 初始化db
```bash
python db/init_db.py
python db/seed.py
```

### 測試
```bash
python test_agent.py
```

## 系統架構
- Planner Node：意圖、實體
- Tool Node：MySQL 工具
- Memory Node：STM + LTM
- Verifier Node：驗證輸出
- Responder Node：自然語言回覆生成
