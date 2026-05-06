#!/bin/bash
# Linux/Mac安装脚本

echo "正在安装数学试卷批改系统..."
echo

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python 3，请先安装Python 3.8+"
    exit 1
fi

# 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "错误：创建虚拟环境失败"
    exit 1
fi

# 激活虚拟环境并安装依赖
echo "安装依赖包..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误：安装依赖包失败"
    exit 1
fi

# 复制环境变量文件
if [ ! -f .env ]; then
    echo "复制环境变量配置文件..."
    cp .env.example .env
    echo "请编辑 .env 文件，填入您的Deepseek API配置"
else
    echo "环境变量文件已存在，跳过复制"
fi

echo
echo "安装完成！"
echo "请按照以下步骤启动系统："
echo "1. 编辑 .env 文件，配置您的Deepseek API密钥"
echo "2. 运行：source venv/bin/activate"
echo "3. 运行：python app.py"
echo
echo "安装脚本执行完毕！"