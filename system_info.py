#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学试卷批改系统信息展示
"""

import os
import sys

def show_system_info():
    print("=" * 60)
    print("    数学试卷批改系统")
    print("=" * 60)

    print("\n系统功能:")
    print("  - 智能OCR识别试卷内容")
    print("  - AI智能批改答案")
    print("  - 在图片上标记错误位置")
    print("  - 提供详细的批改统计")

    print("\n技术栈:")
    print("  - Flask + PaddleOCR + Deepseek API")
    print("  - OpenCV + Pillow + HTML/CSS/JS")

    print("\n工作流程:")
    steps = [
        "用户上传数学试卷截图",
        "OCR处理器识别文本内容",
        "AI批改器判断答案正确性",
        "图像标记器在图片上标记错误",
        "显示批改结果和统计信息"
    ]

    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")

    print("\n支持题型:")
    print("  - 选择题、填空题、计算题")
    print("  - 应用题、几何题")

    print("\n主要文件:")
    files = [
        "app.py - Flask主应用",
        "ocr_processor.py - OCR处理模块",
        "ai_grader.py - AI批改模块",
        "image_marker.py - 图像标记模块",
        "templates/ - Web界面模板",
        "static/ - 静态文件存储"
    ]

    for file_info in files:
        print(f"  - {file_info}")

    print("\n启动方式:")
    print("  1. 安装依赖: pip install -r requirements.txt")
    print("  2. 配置API密钥: 编辑 .env 文件")
    print("  3. 启动服务: python app.py")
    print("  4. 访问: http://localhost:5000")

    print("\n" + "=" * 60)
    print("系统信息展示完成！")

if __name__ == '__main__':
    show_system_info()