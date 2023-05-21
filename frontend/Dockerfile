# ベースとなるイメージの指定
FROM node:16

# ワーキングディレクトリの指定
WORKDIR /app

# 依存関係ファイルをコピー
COPY package*.json ./

# 依存関係のインストール
RUN npm install

# アプリケーションのコピー
COPY .. .

# ポートのエクスポート
EXPOSE 5173

# 実行コマンド
CMD ["npm", "run", "dev", "--",  "--host"]
