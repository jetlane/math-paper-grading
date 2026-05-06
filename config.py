import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # Deepseek API配置
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions')

    # 文件上传配置
    UPLOAD_FOLDER = 'static/uploads'
    RESULT_FOLDER = 'static/results'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # OCR配置
    OCR_LANGUAGE = 'ch'  # 中文

    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'math_grading_secret_key')
    DEBUG = True

# 确保目录存在
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.RESULT_FOLDER, exist_ok=True)