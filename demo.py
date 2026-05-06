#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学试卷批改系统演示脚本
展示系统的主要功能和流程
"""

import os
import sys
import time

def print_header():
    """打印系统头部"""
    print("=" * 60)
    print("    数学试卷批改系统 - 演示版本")
    print("    Math Paper Grading System - Demo")
    print("=" * 60)
    print()

def print_system_overview():
    """打印系统概述"""
    print("📋 系统概述")
    print("-" * 40)
    print("这是一个基于Python和AI技术的智能数学试卷批改系统")
    print("主要功能：")
    print("  • 📝 智能OCR识别试卷内容")
    print("  • 🤖 AI智能批改答案")
    print("  • ❌ 在图片上标记错误位置")
    print("  • 📊 提供详细的批改统计")
    print()

def print_tech_stack():
    """打印技术栈"""
    print("🛠️  技术栈")
    print("-" * 40)
    print("后端框架: Flask 2.3.3")
    print("OCR引擎: PaddleOCR 2.7.0.3")
    print("AI接口: Deepseek API")
    print("图像处理: OpenCV + Pillow")
    print("前端技术: HTML5 + CSS3 + JavaScript")
    print()

def print_workflow():
    """打印工作流程"""
    print("🔄 工作流程")
    print("-" * 40)
    steps = [
        "1. 用户上传数学试卷截图",
        "2. OCR处理器识别文本内容",
        "3. AI批改器判断答案正确性",
        "4. 图像标记器在图片上标记错误",
        "5. 显示批改结果和统计信息"
    ]

    for step in steps:
        print(step)
        time.sleep(0.5)
    print()

def print_modules():
    """打印主要模块"""
    print("🧩 主要模块")
    print("-" * 40)

    modules = [
        {
            "name": "OCR处理器 (ocr_processor.py)",
            "desc": "使用PaddleOCR识别试卷中的文本内容，支持数学公式识别"
        },
        {
            "name": "AI批改器 (ai_grader.py)",
            "desc": "集成Deepseek API进行智能批改，支持多种题型"
        },
        {
            "name": "图像标记器 (image_marker.py)",
            "desc": "在原始图片上用红色标记错误位置，支持叉号和圆圈"
        },
        {
            "name": "Flask应用 (app.py)",
            "desc": "Web界面和API接口，提供用户友好的操作体验"
        },
        {
            "name": "配置文件 (config.py)",
            "desc": "系统配置管理，支持环境变量配置"
        }
    ]

    for module in modules:
        print(f"  📁 {module['name']}")
        print(f"     {module['desc']}")
        print()

def print_supported_features():
    """打印支持的功能"""
    print("✨ 支持的功能")
    print("-" * 40)
    features = [
        "✅ 选择题批改 (A, B, C, D选项)",
        "✅ 填空题批改 (数字、表达式答案)",
        "✅ 计算题批改 (包含计算过程)",
        "✅ 应用题批改 (文字解答)",
        "✅ 几何题批改 (图形相关)",
        "✅ 错误位置标记 (红色叉号和圆圈)",
        "✅ 详细批改报告",
        "✅ 统计信息展示",
        "✅ 响应式Web界面"
    ]

    for feature in features:
        print(f"  {feature}")
        time.sleep(0.2)
    print()

def print_file_structure():
    """打印文件结构"""
    print("📁 项目文件结构")
    print("-" * 40)
    structure = """
math-paper-grading/
├── app.py                    # Flask主应用
├── config.py                 # 配置文件
├── ocr_processor.py          # OCR处理模块
├── ai_grader.py             # AI批改模块
├── image_marker.py          # 图像标记模块
├── requirements.txt         # 依赖包列表
├── .env.example            # 环境变量示例
├── README.md               # 项目说明
├── static/
│   ├── uploads/            # 上传文件存储
│   └── results/            # 处理结果存储
└── templates/
    ├── upload.html         # 上传页面
    ├── result.html         # 结果页面
    ├── 404.html           # 404错误页面
    └── 500.html           # 500错误页面
"""
    print(structure)

def print_usage_instructions():
    """打印使用说明"""
    print("📖 快速开始")
    print("-" * 40)
    instructions = [
        "1. 安装依赖: pip install -r requirements.txt",
        "2. 配置环境变量: 复制 .env.example 为 .env 并填写配置",
        "3. 启动应用: python app.py",
        "4. 访问 http://localhost:5000",
        "5. 上传数学试卷截图",
        "6. 查看批改结果"
    ]

    for instruction in instructions:
        print(f"  {instruction}")
        time.sleep(0.3)
    print()

def print_requirements():
    """打印系统要求"""
    print("⚙️  系统要求")
    print("-" * 40)
    requirements = [
        "• Python 3.8+",
        "• 至少4GB内存 (推荐8GB以上)",
        "• 支持CUDA的GPU (可选，用于加速OCR处理)",
        "• Deepseek API密钥",
        "• 网络连接 (用于API调用)"
    ]

    for req in requirements:
        print(req)
    print()

def main():
    """主函数"""
    print_header()

    sections = [
        ("系统概述", print_system_overview),
        ("技术栈", print_tech_stack),
        ("工作流程", print_workflow),
        ("主要模块", print_modules),
        ("支持功能", print_supported_features),
        ("文件结构", print_file_structure),
        ("系统要求", print_requirements),
        ("使用说明", print_usage_instructions)
    ]

    for title, func in sections:
        input(f"按回车键查看: {title}...")
        print()
        func()
        print()

    print("🎉 演示结束！")
    print("这是一个完整的数学试卷批改系统，具备AI智能识别和批改功能。")
    print("要运行完整的系统，请按照使用说明进行安装和配置。")

if __name__ == '__main__':
    main()