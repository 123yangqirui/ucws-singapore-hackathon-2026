#!/usr/bin/env python3
"""
创业助手AI - FastAPI服务启动脚本
"""
import uvicorn
import sys
from pathlib import Path


if __name__ == "__main__":
    print("=" * 50)
    print("  创业助手AI - FastAPI服务")
    print("=" * 50)
    print("\n服务启动中...")
    print("API文档地址: http://localhost:8000/docs")
    print("健康检查: http://localhost:8000/health")
    print("\n按 Ctrl+C 停止服务\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
