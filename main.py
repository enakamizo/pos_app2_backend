from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ これを追加
import mysql.connector
import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数を取得
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}

app = FastAPI()

# ✅ CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/product/{code}")
def get_product(code: str):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, price FROM products WHERE code = %s", (code,))
    product = cursor.fetchone()
    conn.close()

    if product:
        return product
    else:
        return {"error": "商品が見つかりません"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
