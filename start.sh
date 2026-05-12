#!/bin/bash

echo "🚀 正在拉取最新代码..."
git pull origin main

echo "📦 生成数据库迁移..."
python manage.py makemigrations

echo "🗄️ 执行数据库迁移..."
python manage.py migrate

echo "🛑 停止旧服务器（如果存在）..."
kill -9 $(lsof -ti:8000) 2>/dev/null || true

echo "✅ 启动 Django 服务器..."
python manage.py runserver
