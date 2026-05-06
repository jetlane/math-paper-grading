@echo off
REM Windows安装脚本

echo 正在安装数学试卷批改系统...
echo.

REM 检查Python版本
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 创建虚拟环境
echo 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo 错误：创建虚拟环境失败
    pause
    exit /b 1
)

REM 激活虚拟环境并安装依赖
echo 安装依赖包...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误：安装依赖包失败
    pause
    exit /b 1
)

REM 复制环境变量文件
if not exist .env (
    echo 复制环境变量配置文件...
    copy .env.example .env
    echo 请编辑 .env 文件，填入您的Deepseek API配置
) else (
    echo 环境变量文件已存在，跳过复制
)

echo.
echo 安装完成！
echo 请按照以下步骤启动系统：
echo 1. 编辑 .env 文件，配置您的Deepseek API密钥
echo 2. 运行：venv\Scripts\activate
echo 3. 运行：python app.py

echo.
echo 按任意键退出...
pause >nul