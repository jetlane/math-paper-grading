import cv2
import numpy as np
from paddleocr import PaddleOCR
import json
import re
from typing import Dict, List, Tuple, Any

class OCRProcessor:
    def __init__(self, use_angle_cls=True, lang='ch'):
        """初始化OCR处理器

        Args:
            use_angle_cls: 是否使用角度分类
            lang: 语言类型，默认中文
        """
        self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang, show_log=False)

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """图像预处理

        Args:
            image_path: 图像路径

        Returns:
            预处理后的图像
        """
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图像: {image_path}")

        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 二值化处理
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 降噪处理
        kernel = np.ones((2, 2), np.uint8)
        denoised = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        return denoised

    def extract_text_regions(self, image_path: str) -> List[Dict[str, Any]]:
        """提取文本区域

        Args:
            image_path: 图像路径

        Returns:
            文本区域列表，包含文本内容和位置信息
        """
        # 预处理图像
        processed_image = self.preprocess_image(image_path)

        # OCR识别
        result = self.ocr.ocr(processed_image, cls=True)

        text_regions = []
        if result is not None:
            for line in result:
                for box in line:
                    # box[0] 是边界框坐标，box[1] 是文本和置信度
                    bbox = box[0]
                    text, confidence = box[1]

                    # 过滤低置信度的结果
                    if confidence > 0.5:
                        region = {
                            'text': text.strip(),
                            'confidence': float(confidence),
                            'bbox': {
                                'x_min': int(min(point[0] for point in bbox)),
                                'y_min': int(min(point[1] for point in bbox)),
                                'x_max': int(max(point[0] for point in bbox)),
                                'y_max': int(max(point[1] for point in bbox))
                            }
                        }
                        text_regions.append(region)

        return text_regions

    def parse_math_content(self, text_regions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """解析数学内容，识别题目和答案

        Args:
            text_regions: 文本区域列表

        Returns:
            结构化的数学内容
        """
        math_content = {
            'questions': [],
            'answers': [],
            'metadata': {
                'total_regions': len(text_regions),
                'processing_time': None
            }
        }

        # 按y坐标排序，从上到下
        sorted_regions = sorted(text_regions, key=lambda x: x['bbox']['y_min'])

        current_question = None
        question_number = 0

        for region in sorted_regions:
            text = region['text']

            # 识别题目编号模式
            question_patterns = [
                r'^(\d+)[\.．、]',  # 1. 或 1．或 1、
                r'^第(\d+)题',      # 第1题
                r'^(\d+)[\s\.．、]',  # 1 或 1. 或 1．或 1、
            ]

            is_question = False
            for pattern in question_patterns:
                if re.match(pattern, text):
                    question_number += 1
                    current_question = {
                        'number': question_number,
                        'content': text,
                        'bbox': region['bbox'],
                        'confidence': region['confidence']
                    }
                    math_content['questions'].append(current_question)
                    is_question = True
                    break

            # 如果不是题目，且当前有题目，则可能是答案
            if not is_question and current_question is not None:
                # 检查是否包含数学答案特征
                answer_indicators = ['=', '解', '答', '原式', '得']
                has_answer_indicator = any(indicator in text for indicator in answer_indicators)

                if has_answer_indicator or self._is_math_expression(text):
                    answer = {
                        'question_number': question_number,
                        'content': text,
                        'bbox': region['bbox'],
                        'confidence': region['confidence'],
                        'type': self._classify_answer_type(text)
                    }
                    math_content['answers'].append(answer)

        return math_content

    def _is_math_expression(self, text: str) -> bool:
        """判断是否为数学表达式

        Args:
            text: 文本内容

        Returns:
            是否为数学表达式
        """
        math_symbols = ['+', '-', '×', '÷', '*', '/', '=', '(', ')', '[', ']', '{', '}']
        math_functions = ['sin', 'cos', 'tan', 'log', 'ln', '√', '∑', '∫']

        # 检查是否包含数学符号
        has_math_symbol = any(symbol in text for symbol in math_symbols)

        # 检查是否包含数学函数
        has_math_function = any(func in text for func in math_functions)

        # 检查是否包含数字
        has_number = bool(re.search(r'\d', text))

        return has_math_symbol or has_math_function or (has_number and len(text) < 50)

    def _classify_answer_type(self, text: str) -> str:
        """分类答案类型

        Args:
            text: 答案文本

        Returns:
            答案类型
        """
        if re.match(r'^[A-Da-d]$', text.strip()):
            return 'choice'  # 选择题
        elif '=' in text and len(text) < 20:
            return 'calculation'  # 计算题
        elif any(word in text for word in ['解', '答', '证明']):
            return 'solution'  # 解答题
        elif re.match(r'^\d+$', text.strip()):
            return 'number'  # 纯数字答案
        else:
            return 'text'  # 文本答案

    def get_structured_content(self, image_path: str) -> Dict[str, Any]:
        """获取结构化的试卷内容

        Args:
            image_path: 图像路径

        Returns:
            结构化的试卷内容
        """
        try:
            # 提取文本区域
            text_regions = self.extract_text_regions(image_path)

            # 解析数学内容
            math_content = self.parse_math_content(text_regions)

            return {
                'success': True,
                'data': math_content,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }