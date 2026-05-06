from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import os
import uuid
from datetime import datetime
from config import Config
from ocr_processor import OCRProcessor
from ai_grader import AIGrader
from image_marker import ImageMarker

app = Flask(__name__)
app.config.from_object(Config)

# 初始化各模块
ocr_processor = OCRProcessor()
ai_grader = AIGrader()
image_marker = ImageMarker()

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """保存上传的文件"""
    if file and allowed_file(file.filename):
        # 生成唯一文件名
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filename, filepath
    return None, None

@app.route('/')
def index():
    """主页 - 上传页面"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有选择文件'
            })

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '没有选择文件'
            })

        # 保存文件
        filename, filepath = save_uploaded_file(file)
        if not filename:
            return jsonify({
                'success': False,
                'error': '文件格式不支持'
            })

        # 处理试卷
        result = process_exam_paper(filepath, filename)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'处理失败: {str(e)}'
        })

def process_exam_paper(image_path, filename):
    """处理试卷的主要流程"""
    try:
        # 步骤1: OCR识别
        print("开始OCR识别...")
        ocr_result = ocr_processor.get_structured_content(image_path)
        if not ocr_result['success']:
            return {
                'success': False,
                'error': f'OCR识别失败: {ocr_result["error"]}'
            }

        structured_content = ocr_result['data']
        print(f"识别到 {len(structured_content.get('questions', []))} 道题目")

        # 步骤2: AI批改
        print("开始AI批改...")
        grading_result = ai_grader.grade_paper(structured_content)
        if not grading_result['success']:
            return {
                'success': False,
                'error': f'AI批改失败: {grading_result["error"]}'
        }

        # 步骤3: 图像标记
        print("开始图像标记...")
        marker_result = image_marker.process_grading_result(
            image_path,
            grading_result['data'],
            Config.RESULT_FOLDER,
            marker_type='both'  # 同时使用叉号和圆圈
        )

        if not marker_result['success']:
            return {
                'success': False,
                'error': f'图像标记失败: {marker_result["error"]}'
        }

        # 准备返回结果
        result_data = {
            'success': True,
            'filename': filename,
            'original_image': f"/static/uploads/{filename}",
            'marked_image': f"/static/results/{os.path.basename(marker_result['marked_image_path'])}",
            'summary_image': f"/static/results/{os.path.basename(marker_result['summary_image_path'])}",
            'statistics': grading_result['data']['statistics'],
            'grading_results': grading_result['data']['grading_results'],
            'marked_count': marker_result['marked_count']
        }

        return result_data

    except Exception as e:
        return {
            'success': False,
            'error': f'处理过程异常: {str(e)}'
        }

@app.route('/result')
def result():
    """结果显示页面"""
    return render_template('result.html')

@app.route('/api/result/<result_id>')
def get_result(result_id):
    """获取处理结果数据"""
    # 这里可以实现结果缓存和检索逻辑
    # 为了简化，直接从session或临时存储中获取
    return jsonify({'error': '结果获取功能待实现'})

@app.route('/static/<path:filename>')
def serve_static(filename):
    """提供静态文件服务"""
    return send_from_directory('static', filename)

@app.route('/demo')
def demo():
    """演示页面"""
    return render_template('demo.html')

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("启动数学试卷批改系统...")
    print(f"上传目录: {Config.UPLOAD_FOLDER}")
    print(f"结果目录: {Config.RESULT_FOLDER}")
    print("请访问 http://localhost:5000")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)