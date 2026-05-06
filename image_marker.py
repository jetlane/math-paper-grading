import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from typing import Dict, List, Any, Tuple

class ImageMarker:
    def __init__(self):
        """初始化图像标记器"""
        self.error_color = (255, 0, 0)  # 红色 BGR格式
        self.cross_color = (0, 0, 255)  # 红色 RGB格式 (PIL使用)
        self.circle_color = (255, 0, 0)  # 红色

    def _load_image(self, image_path: str) -> Tuple[np.ndarray, Image.Image]:
        """加载图像，返回OpenCV和PIL格式

        Args:
            image_path: 图像路径

        Returns:
            (cv2_image, pil_image) 元组
        """
        # 使用OpenCV加载
        cv2_image = cv2.imread(image_path)
        if cv2_image is None:
            raise ValueError(f"无法加载图像: {image_path}")

        # 转换为PIL格式
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)

        return cv2_image, pil_image

    def _draw_cross(self, draw: ImageDraw.ImageDraw, center: Tuple[int, int], size: int = 30) -> None:
        """绘制叉号

        Args:
            draw: PIL绘图对象
            center: 中心点坐标 (x, y)
            size: 叉号大小
        """
        x, y = center
        half_size = size // 2

        # 绘制两条交叉线
        draw.line(
            [(x - half_size, y - half_size), (x + half_size, y + half_size)],
            fill=self.cross_color,
            width=4
        )
        draw.line(
            [(x + half_size, y - half_size), (x - half_size, y + half_size)],
            fill=self.cross_color,
            width=4
        )

    def _draw_circle(self, draw: ImageDraw.ImageDraw, bbox: Dict[str, int], thickness: int = 3) -> None:
        """绘制圆圈

        Args:
            draw: PIL绘图对象
            bbox: 边界框 {'x_min', 'y_min', 'x_max', 'y_max'}
            thickness: 线条粗细
        """
        x_min, y_min, x_max, y_max = bbox['x_min'], bbox['y_min'], bbox['x_max'], bbox['y_max']

        # 绘制矩形框
        draw.rectangle(
            [(x_min, y_min), (x_max, y_max)],
            outline=self.circle_color,
            width=thickness
        )

    def _draw_error_marker(self, draw: ImageDraw.ImageDraw, bbox: Dict[str, int], marker_type: str = 'both') -> None:
        """绘制错误标记

        Args:
            draw: PIL绘图对象
            bbox: 边界框
            marker_type: 标记类型 ('cross', 'circle', 'both')
        """
        x_min, y_min, x_max, y_max = bbox['x_min'], bbox['y_min'], bbox['x_max'], bbox['y_max']

        # 计算中心点
        center_x = (x_min + x_max) // 2
        center_y = (y_min + y_max) // 2
        center = (center_x, center_y)

        if marker_type in ['cross', 'both']:
            self._draw_cross(draw, center, size=min(x_max - x_min, y_max - y_min) // 2)

        if marker_type in ['circle', 'both']:
            self._draw_circle(draw, bbox, thickness=3)

    def _add_error_label(self, draw: ImageDraw.ImageDraw, bbox: Dict[str, int], question_number: int, error_text: str = "") -> None:
        """添加错误标签

        Args:
            draw: PIL绘图对象
            bbox: 边界框
            question_number: 题目编号
            error_text: 错误文本
        """
        try:
            # 尝试使用中文字体
            font_paths = [
                '/System/Library/Fonts/STHeiti Light.ttc',  # macOS
                '/System/Library/Fonts/STHeiti Medium.ttc',
                'C:/Windows/Fonts/simhei.ttf',  # Windows
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # Linux
            ]

            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, 20)
                        break
                    except:
                        continue

            if font is None:
                font = ImageFont.load_default()

        except:
            font = ImageFont.load_default()

        # 标签位置（在边界框上方）
        label_x = bbox['x_min']
        label_y = max(0, bbox['y_min'] - 40)

        # 绘制标签背景
        label_text = f"第{question_number}题错误"
        text_bbox = draw.textbbox((label_x, label_y), label_text, font=font)
        draw.rectangle(text_bbox, fill=(255, 0, 0))

        # 绘制标签文本
        draw.text((label_x, label_y), label_text, fill=(255, 255, 255), font=font)

    def mark_errors_on_image(self, original_image_path: str, grading_results: List[Dict[str, Any]],
                           output_path: str, marker_type: str = 'both') -> Dict[str, Any]:
        """在图像上标记错误

        Args:
            original_image_path: 原始图像路径
            grading_results: 批改结果列表
            output_path: 输出图像路径
            marker_type: 标记类型 ('cross', 'circle', 'both')

        Returns:
            处理结果
        """
        try:
            # 加载图像
            cv2_image, pil_image = self._load_image(original_image_path)

            # 创建绘图对象
            draw = ImageDraw.Draw(pil_image)

            # 处理每个批改结果
            marked_count = 0
            for result in grading_results:
                # 只标记错误的答案
                if not result.get('is_correct', True):
                    bbox = result.get('bbox', {})

                    # 检查边界框是否有效
                    if bbox and all(key in bbox for key in ['x_min', 'y_min', 'x_max', 'y_max']):
                        question_number = result.get('question_number', 0)

                        # 绘制错误标记
                        self._draw_error_marker(draw, bbox, marker_type)

                        # 添加错误标签
                        error_reason = result.get('error_reason', '')
                        self._add_error_label(draw, bbox, question_number, error_reason)

                        marked_count += 1

            # 保存标记后的图像
            pil_image.save(output_path, 'JPEG', quality=95)

            return {
                'success': True,
                'marked_count': marked_count,
                'output_path': output_path,
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'marked_count': 0,
                'output_path': '',
                'error': str(e)
            }

    def create_summary_overlay(self, original_image_path: str, grading_statistics: Dict[str, Any],
                             output_path: str) -> Dict[str, Any]:
        """创建批改统计覆盖层

        Args:
            original_image_path: 原始图像路径
            grading_statistics: 批改统计信息
            output_path: 输出图像路径

        Returns:
            处理结果
        """
        try:
            # 加载图像
            cv2_image, pil_image = self._load_image(original_image_path)

            # 创建绘图对象
            draw = ImageDraw.Draw(pil_image)

            # 获取图像尺寸
            width, height = pil_image.size

            # 创建统计信息面板
            stats = grading_statistics
            panel_height = 120
            panel_y = height - panel_height

            # 绘制半透明背景
            overlay = Image.new('RGBA', (width, panel_height), (0, 0, 0, 128))
            pil_image.paste(overlay, (0, panel_y), overlay)

            # 重新创建绘图对象（因为图像已被修改）
            draw = ImageDraw.Draw(pil_image)

            # 添加统计文本
            try:
                font = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 18)
            except:
                font = ImageFont.load_default()

            # 统计信息
            total_questions = stats.get('total_questions', 0)
            correct_count = stats.get('correct_count', 0)
            average_score = stats.get('average_score', 0)
            accuracy = stats.get('accuracy', 0)

            text_lines = [
                f"总题数: {total_questions}  正确: {correct_count}  错误: {total_questions - correct_count}",
                f"平均分: {average_score:.1f}  正确率: {accuracy:.1f}%"
            ]

            # 绘制文本
            text_y = panel_y + 10
            for line in text_lines:
                draw.text((20, text_y), line, fill=(255, 255, 255), font=font)
                text_y += 30

            # 保存结果
            pil_image.save(output_path, 'JPEG', quality=95)

            return {
                'success': True,
                'output_path': output_path,
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'output_path': '',
                'error': str(e)
            }

    def process_grading_result(self, original_image_path: str, grading_result: Dict[str, Any],
                             output_dir: str, marker_type: str = 'both') -> Dict[str, Any]:
        """处理完整的批改结果

        Args:
            original_image_path: 原始图像路径
            grading_result: 批改结果
            output_dir: 输出目录
            marker_type: 标记类型

        Returns:
            处理结果
        """
        try:
            # 生成输出文件名
            base_name = os.path.basename(original_image_path)
            name, ext = os.path.splitext(base_name)

            # 标记错误的图像
            marked_image_path = os.path.join(output_dir, f"{name}_marked{ext}")
            marking_result = self.mark_errors_on_image(
                original_image_path,
                grading_result.get('grading_results', []),
                marked_image_path,
                marker_type
            )

            if not marking_result['success']:
                return marking_result

            # 添加统计信息的图像
            summary_image_path = os.path.join(output_dir, f"{name}_summary{ext}")
            summary_result = self.create_summary_overlay(
                marked_image_path,
                grading_result.get('statistics', {}),
                summary_image_path
            )

            return {
                'success': True,
                'marked_image_path': marked_image_path,
                'summary_image_path': summary_image_path if summary_result['success'] else '',
                'marked_count': marking_result['marked_count'],
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'marked_image_path': '',
                'summary_image_path': '',
                'marked_count': 0,
                'error': str(e)
            }