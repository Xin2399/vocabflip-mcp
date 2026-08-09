FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY mcp_server.py app.py quiz_data.py reading_data.py ./
COPY templates/ ./templates/

# 创建数据目录
RUN mkdir -p /data

# 环境变量
ENV DB_PATH=/data/vocab.db
ENV PORT=8771

# 暴露 MCP SSE 端口
EXPOSE 8771

# 启动 MCP 服务
CMD ["python", "mcp_server.py"]
