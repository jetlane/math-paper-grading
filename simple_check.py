#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单依赖检查脚本
"""

import sys
import os

def main():
    print("数学试卷批改系统依赖检查")
    print("=" * 50)

    # 检查Python版本
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"Python版本过低: {python_version.major}.{python_version.minor}")
        print("需要Python 3.8或更高版本")
        return False
    else:
        print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")

    # 检查依赖包
    try:
        import flask
        print("Flask: 已安装")
    except ImportError:
        print("Flask: 未安装")
        return False

    try:
        import paddleocr
        print("PaddleOCR: 已安装")
    except ImportError:
        print("PaddleOCR: 未安装")
        return False

    try:
        import cv2
        print("OpenCV: 已安装")
    except ImportError:
        print("OpenCV: 未安装")
        return False

    try:
        import PIL
        print("Pillow: 已安装")
    except ImportError:
        print("Pillow: 未安装")
        return False

    try:
        import requests
        print("Requests: 已安装")
    except ImportError:
        print("Requests: 未安装")
        return False

    try:
        import numpy
        print("NumPy: 已安装")
    except ImportError:
        print("NumPy: 未安装")
        return False

    # 检查配置文件
    if os.path.exists('.env'):
        print("配置文件: 已存在")
    else:
        print("配置文件: 不存在，请复制 .env.example 为 .env")
        return False

    print("\n所有依赖检查通过！")
    print("启动命令: python app.py")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)