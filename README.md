# 数学试卷批改系统

一个基于Python和AI技术的智能数学试卷批改系统，支持上传试卷截图，自动识别学生答案并进行批改，在原始图片上标记错误位置。

## ✨ 功能特点

- 📝 **智能OCR识别**：使用PaddleOCR技术精准识别试卷中的文本内容
- 🤖 **AI智能批改**：集成Deepseek API进行答案判断和评分
- ❌ **错误标记**：在原始图片上用红色叉号和圆圈标记错误位置
- 📊 **详细统计**：提供全面的批改结果统计分析
- 🎨 **美观界面**：现代化的Web界面，操作简单直观
- 📱 **响应式设计**：支持桌面和移动设备访问

## 🛠️ 技术栈

- **后端框架**: Flask 2.3.3
- **OCR引擎**: PaddleOCR 2.7.0.3
- **AI接口**: Deepseek API
- **图像处理**: OpenCV + Pillow
- **前端技术**: HTML5 + CSS3 + JavaScript

## 📋 系统要求

- Python 3.8+
- 至少4GB内存（推荐8GB以上）
- 支持CUDA的GPU（可选，用于加速OCR处理）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <项目地址>
cd math-paper-grading
```

### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖包
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量示例文件并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的配置：

```env
# Deepseek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

# Flask配置
SECRET_KEY=your_secret_key_here
```

### 4. 启动应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 📖 使用说明

### 1. 访问系统

打开浏览器，访问 `http://localhost:5000`

### 2. 上传试卷

- 点击"选择文件"按钮或直接拖拽试卷图片到上传区域
- 支持PNG、JPG、JPEG、BMP格式的图片
- 文件大小不超过16MB

### 3. 等待处理

系统会自动进行以下处理步骤：
1. **OCR识别**：提取试卷中的文本内容
2. **AI批改**：调用Deepseek API判断答案正确性
3. **错误标记**：在图片上标记错误位置

### 4. 查看结果

处理完成后，您可以看到：
- 📊 **统计概览**：总题数、正确率、平均分等
- 📋 **原始试卷**：上传的原始图片
- ❌ **标记结果**：带有错误标记的图片
- 📝 **详细分析**：每道题的批改详情

## 🔧 配置说明

### Deepseek API配置

1. 注册Deepseek账号并获取API密钥
2. 在`.env`文件中配置API密钥和URL
3. 确保网络能够访问Deepseek API

### OCR配置

系统使用PaddleOCR进行文本识别，支持：
- 中文文本识别
- 数学公式识别
- 角度校正

### 图像处理配置

- 错误标记颜色：红色
- 标记类型：叉号 + 圆圈
- 输出图片质量：95%

## 📁 项目结构

```
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
```

## 🐛 常见问题

### Q: OCR识别不准确怎么办？
A: 确保上传的图片清晰，文字对比度足够高。可以尝试调整图片的亮度和对比度。

### Q: API调用失败怎么办？
A: 检查网络连接，确认Deepseek API密钥配置正确，查看服务器日志了解具体错误。

### Q: 如何处理复杂的数学公式？
A: 系统支持基础的数学符号识别，对于复杂的公式建议使用清晰的印刷体。

### Q: 能否批量处理多张试卷？
A: 当前版本支持单张试卷处理，批量处理功能将在后续版本中添加。

## 🚀 性能优化

### 1. GPU加速

如果拥有NVIDIA GPU，可以安装CUDA版本的PaddlePaddle：

```bash
pip install paddlepaddle-gpu
```

### 2. 内存优化

- 调整上传文件大小限制
- 定期清理临时文件
- 使用图片压缩

### 3. API优化

- 增加API调用间隔避免限流
- 实现结果缓存
- 错误重试机制

## 🔒 安全说明

- 上传的图片仅用于本地处理，不会上传到第三方服务器
- API密钥等敏感信息使用环境变量存储
- 建议在生产环境中使用HTTPS

## 📈 后续计划

- [ ] 支持批量试卷处理
- [ ] 添加更多AI模型选项
- [ ] 支持导出批改报告
- [ ] 添加用户管理系统
- [ ] 支持更多题型识别
- [ ] 移动端应用开发

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

## 📄 许可证

本项目采用 MIT 许可证。

## 📞 联系方式

如有问题或建议，请通过以下方式联系我们：
- 邮箱：80921970@qq.com
- GitHub：https://github.com/jetlane/math-paper-grading

---

**让AI技术助力教育，让批改工作更加高效！** 📚✨