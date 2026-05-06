#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学试卷批改系统测试脚本
用于测试系统各模块的功能
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch
import tempfile
from PIL import Image
import numpy as np

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ocr_processor import OCRProcessor
from ai_grader import AIGrader
from image_marker import ImageMarker
from config import Config

class TestOCRProcessor(unittest.TestCase):
    """OCR处理器测试"""

    def setUp(self):
        """测试前准备"""
        self.ocr = OCRProcessor()

    def test_preprocess_image(self):
        """测试图像预处理"""
        # 创建一个测试图像
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        Image.fromarray(test_image).save(temp_file.name)

        try:
            # 测试预处理
            processed = self.ocr.preprocess_image(temp_file.name)
            self.assertIsNotNone(processed)
            self.assertEqual(processed.shape[:2], (100, 100))
        finally:
            os.unlink(temp_file.name)

    def test_parse_math_content(self):
        """测试数学内容解析"""
        # 模拟OCR结果
        mock_regions = [
            {
                'text': '1. 计算：2 + 3 = ?',
                'confidence': 0.95,
                'bbox': {'x_min': 10, 'y_min': 10, 'x_max': 100, 'y_max': 30}
            },
            {
                'text': '5',
                'confidence': 0.90,
                'bbox': {'x_min': 50, 'y_min': 40, 'x_max': 70, 'y_max': 60}
            }
        ]

        result = self.ocr.parse_math_content(mock_regions)

        self.assertIn('questions', result)
        self.assertIn('answers', result)
        self.assertEqual(len(result['questions']), 1)

    def test_is_math_expression(self):
        """测试数学表达式识别"""
        # 测试数学表达式
        self.assertTrue(self.ocr._is_math_expression('2 + 3 = 5'))
        self.assertTrue(self.ocr._is_math_expression('x + y = 10'))
        self.assertTrue(self.ocr._is_math_expression('sin(x) + cos(y)'))

        # 测试非数学表达式
        self.assertFalse(self.ocr._is_math_expression('这是一个测试句子'))

    def test_classify_answer_type(self):
        """测试答案类型分类"""
        self.assertEqual(self.ocr._classify_answer_type('A'), 'choice')
        self.assertEqual(self.ocr._classify_answer_type('5'), 'number')
        self.assertEqual(self.ocr._classify_answer_type('2 + 3 = 5'), 'calculation')
        self.assertEqual(self.ocr._classify_answer_type('解：...'), 'solution')

class TestAIGrader(unittest.TestCase):
    """AI批改器测试"""

    def setUp(self):
        """测试前准备"""
        self.grader = AIGrader()

    @patch('ai_grader.AIGrader._call_deepseek_api')
    def test_grade_single_answer(self, mock_api_call):
        """测试单个答案批改"""
        # 模拟API响应
        mock_api_call.return_value = '''{
            "is_correct": true,
            "score": 100,
            "error_reason": "",
            "detailed_analysis": "答案正确",
            "correct_answer": "5"
        }'''

        result = self.grader.grade_single_answer(
            "计算：2 + 3 = ?",
            "5",
            "calculation"
        )

        self.assertTrue(result['success'])
        self.assertTrue(result['data']['is_correct'])
        self.assertEqual(result['data']['score'], 100)

    def test_build_grading_prompt(self):
        """测试批改提示词构建"""
        messages = self.grader._build_grading_prompt(
            "计算：2 + 3 = ?",
            "5",
            "calculation"
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[1]['role'], 'user')

    def test_parse_grading_result_valid_json(self):
        """测试有效的JSON结果解析"""
        json_response = '''{
            "is_correct": false,
            "score": 0,
            "error_reason": "计算错误",
            "detailed_analysis": "应该是 2 + 3 = 5",
            "correct_answer": "5"
        }'''

        result = self.grader._parse_grading_result(json_response)

        self.assertTrue(result['success'])
        self.assertFalse(result['data']['is_correct'])
        self.assertEqual(result['data']['error_reason'], '计算错误')

    def test_parse_grading_result_invalid_json(self):
        """测试无效JSON结果解析"""
        text_response = "答案错误，因为学生计算不正确，正确答案应该是 5"

        result = self.grader._parse_grading_result(text_response)

        self.assertTrue(result['success'])
        self.assertFalse(result['data']['is_correct'])

class TestImageMarker(unittest.TestCase):
    """图像标记器测试"""

    def setUp(self):
        """测试前准备"""
        self.marker = ImageMarker()

    def test_load_image(self):
        """测试图像加载"""
        # 创建测试图像
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        Image.fromarray(test_image).save(temp_file.name)

        try:
            cv2_image, pil_image = self.marker._load_image(temp_file.name)

            self.assertIsNotNone(cv2_image)
            self.assertIsNotNone(pil_image)
            self.assertEqual(pil_image.size, (100, 100))
        finally:
            os.unlink(temp_file.name)

    def test_draw_cross(self):
        """测试叉号绘制"""
        # 创建空白图像
        image = Image.new('RGB', (100, 100), 'white')
        draw = ImageDraw.Draw(image)

        # 绘制叉号
        self.marker._draw_cross(draw, (50, 50), 20)

        # 验证图像已修改（简单的像素检查）
        # 中心点应该是红色
        center_pixel = image.getpixel((50, 50))
        self.assertEqual(center_pixel, (255, 0, 0))

    def test_draw_circle(self):
        """测试圆圈绘制"""
        # 创建空白图像
        image = Image.new('RGB', (100, 100), 'white')
        draw = ImageDraw.Draw(image)

        # 绘制圆圈
        bbox = {'x_min': 25, 'y_min': 25, 'x_max': 75, 'y_max': 75}
        self.marker._draw_circle(draw, bbox, 3)

        # 验证图像已修改
        # 边界点应该是红色
        border_pixel = image.getpixel((25, 25))
        self.assertEqual(border_pixel, (255, 0, 0))

    def test_mark_errors_on_image(self):
        """测试错误标记功能"""
        # 创建测试图像
        test_image = np.ones((200, 200, 3), dtype=np.uint8) * 255  # 白色背景
        temp_input = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        Image.fromarray(test_image).save(temp_input.name)

        # 创建测试结果
        grading_results = [
            {
                'is_correct': False,
                'question_number': 1,
                'bbox': {'x_min': 50, 'y_min': 50, 'x_max': 100, 'y_max': 100}
            }
        ]

        temp_output = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)

        try:
            result = self.marker.mark_errors_on_image(
                temp_input.name,
                grading_results,
                temp_output.name,
                'both'
            )

            self.assertTrue(result['success'])
            self.assertEqual(result['marked_count'], 1)
            self.assertTrue(os.path.exists(temp_output.name))
        finally:
            os.unlink(temp_input.name)
            if os.path.exists(temp_output.name):
                os.unlink(temp_output.name)

class TestSystemIntegration(unittest.TestCase):
    """系统集成测试"""

    def test_config_loading(self):
        """测试配置加载"""
        self.assertIsNotNone(Config.DEEPSEEK_API_URL)
        self.assertIsNotNone(Config.UPLOAD_FOLDER)
        self.assertIsNotNone(Config.RESULT_FOLDER)

    def test_directory_creation(self):
        """测试目录创建"""
        self.assertTrue(os.path.exists(Config.UPLOAD_FOLDER))
        self.assertTrue(os.path.exists(Config.RESULT_FOLDER))

def run_tests():
    """运行所有测试"""
    print("🧪 开始运行数学试卷批改系统测试...")
    print("=" * 50)

    # 创建测试套件
    test_suite = unittest.TestSuite()

    # 添加测试类
    test_suite.addTest(unittest.makeSuite(TestOCRProcessor))
    test_suite.addTest(unittest.makeSuite(TestAIGrader))
    test_suite.addTest(unittest.makeSuite(TestImageMarker))
    test_suite.addTest(unittest.makeSuite(TestSystemIntegration))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    print("=" * 50)
    if result.wasSuccessful():
        print("✅ 所有测试通过！")
        print(f"✅ 共运行 {result.testsRun} 个测试")
    else:
        print("❌ 部分测试失败")
        print(f"❌ 失败测试数: {len(result.failures)}")
        print(f"❌ 错误测试数: {len(result.errors)}")

    return result.wasSuccessful()

if __name__ == '__main__':
    # 检查依赖
    try:
        import cv2
        import PIL
        import numpy
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请先运行: pip install -r requirements.txt")
        sys.exit(1)

    # 运行测试
    success = run_tests()
    sys.exit(0 if success else 1)