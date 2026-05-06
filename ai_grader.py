import requests
import json
import re
from typing import Dict, List, Any, Optional
import time
from config import Config

class AIGrader:
    def __init__(self):
        """初始化AI批改器"""
        self.api_key = Config.DEEPSEEK_API_KEY
        self.api_url = Config.DEEPSEEK_API_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _call_deepseek_api(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> Optional[str]:
        """调用Deepseek API

        Args:
            messages: 消息列表
            max_tokens: 最大token数

        Returns:
            API响应内容
        """
        try:
            payload = {
                'model': 'deepseek-chat',
                'messages': messages,
                'max_tokens': max_tokens,
                'temperature': 0.1,  # 低温度确保一致性
                'stream': False
            }

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"API调用失败: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"API调用异常: {str(e)}")
            return None

    def _build_grading_prompt(self, question: str, student_answer: str, answer_type: str) -> List[Dict[str, str]]:
        """构建批改提示词

        Args:
            question: 题目内容
            student_answer: 学生答案
            answer_type: 答案类型

        Returns:
            提示词消息列表
        """
        system_prompt = """你是一位专业的数学老师，负责批改学生的数学试卷。你需要：
1. 仔细分析题目要求和学生的解答
2. 判断学生答案是否正确
3. 如果错误，指出具体的错误原因
4. 给出详细的评分理由

请严格按照以下JSON格式返回结果：
{
    "is_correct": true/false,
    "score": 分数（0-100）,
    "error_reason": "错误原因（如果正确则为空）",
    "detailed_analysis": "详细分析",
    "correct_answer": "标准答案（可选）"
}
"""

        user_prompt = f"""请批改以下数学题：

题目：{question}

学生答案：{student_answer}

答案类型：{answer_type}

请分析学生答案的正确性，给出评分和详细分析。"""

        return [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]

    def _parse_grading_result(self, api_response: str) -> Dict[str, Any]:
        """解析批改结果

        Args:
            api_response: API响应内容

        Returns:
            解析后的批改结果
        """
        try:
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', api_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                result = json.loads(json_str)
                return {
                    'success': True,
                    'data': result,
                    'raw_response': api_response
                }
            else:
                # 如果没有找到JSON，尝试手动解析
                return self._manual_parse_result(api_response)

        except json.JSONDecodeError:
            # JSON解析失败，尝试手动解析
            return self._manual_parse_result(api_response)
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"解析结果失败: {str(e)}",
                'raw_response': api_response
            }

    def _manual_parse_result(self, text: str) -> Dict[str, Any]:
        """手动解析结果（当JSON解析失败时）

        Args:
            text: 文本内容

        Returns:
            解析结果
        """
        # 简单的关键词匹配
        is_correct = None
        score = 0
        error_reason = ""

        # 判断正确性
        correct_keywords = ['正确', '对的', '正确无误', '完全正确']
        incorrect_keywords = ['错误', '不对', '不正确', '有误', '错误']

        text_lower = text.lower()

        if any(keyword in text_lower for keyword in correct_keywords):
            is_correct = True
            score = 100
        elif any(keyword in text_lower for keyword in incorrect_keywords):
            is_correct = False
            score = 0
            # 尝试提取错误原因
            error_patterns = [
                r'错误原因[：:](.*?)(?=\n|$)',
                r'因为(.*?)(?=\n|$)',
                r'问题在于(.*?)(?=\n|$)'
            ]
            for pattern in error_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    error_reason = match.group(1).strip()
                    break

        if is_correct is None:
            return {
                'success': False,
                'data': None,
                'error': '无法确定答案正确性',
                'raw_response': text
            }

        return {
            'success': True,
            'data': {
                'is_correct': is_correct,
                'score': score,
                'error_reason': error_reason,
                'detailed_analysis': text,
                'correct_answer': ''
            },
            'raw_response': text
        }

    def grade_single_answer(self, question: str, student_answer: str, answer_type: str = 'text') -> Dict[str, Any]:
        """批改单个答案

        Args:
            question: 题目内容
            student_answer: 学生答案
            answer_type: 答案类型

        Returns:
            批改结果
        """
        try:
            # 构建提示词
            messages = self._build_grading_prompt(question, student_answer, answer_type)

            # 调用API
            api_response = self._call_deepseek_api(messages)

            if api_response is None:
                return {
                    'success': False,
                    'data': None,
                    'error': 'API调用失败'
                }

            # 解析结果
            result = self._parse_grading_result(api_response)

            return result

        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"批改过程异常: {str(e)}"
            }

    def grade_paper(self, structured_content: Dict[str, Any]) -> Dict[str, Any]:
        """批改整张试卷

        Args:
            structured_content: 结构化的试卷内容

        Returns:
            批改结果
        """
        try:
            questions = structured_content.get('questions', [])
            answers = structured_content.get('answers', [])

            grading_results = []
            total_score = 0
            correct_count = 0

            # 创建题目编号到答案的映射
            answer_map = {ans['question_number']: ans for ans in answers}

            for question in questions:
                question_number = question['number']
                question_content = question['content']

                # 查找对应的学生答案
                student_answer = answer_map.get(question_number)
                if student_answer:
                    answer_content = student_answer['content']
                    answer_type = student_answer.get('type', 'text')

                    # 批改单个答案
                    result = self.grade_single_answer(question_content, answer_content, answer_type)

                    if result['success']:
                        grading_data = result['data']
                        is_correct = grading_data.get('is_correct', False)
                        score = grading_data.get('score', 0)

                        grading_result = {
                            'question_number': question_number,
                            'question_content': question_content,
                            'student_answer': answer_content,
                            'is_correct': is_correct,
                            'score': score,
                            'error_reason': grading_data.get('error_reason', ''),
                            'detailed_analysis': grading_data.get('detailed_analysis', ''),
                            'correct_answer': grading_data.get('correct_answer', ''),
                            'bbox': student_answer.get('bbox', {})
                        }

                        grading_results.append(grading_result)
                        total_score += score
                        if is_correct:
                            correct_count += 1

                        # 避免API调用过于频繁
                        time.sleep(1)
                    else:
                        # API调用失败，记录错误
                        grading_results.append({
                            'question_number': question_number,
                            'question_content': question_content,
                            'student_answer': answer_content,
                            'is_correct': False,
                            'score': 0,
                            'error_reason': '批改服务暂时不可用',
                            'detailed_analysis': '',
                            'correct_answer': '',
                            'bbox': student_answer.get('bbox', {})
                        })
                else:
                    # 没有找到对应答案
                    grading_results.append({
                        'question_number': question_number,
                        'question_content': question_content,
                        'student_answer': '',
                        'is_correct': False,
                        'score': 0,
                        'error_reason': '未找到学生答案',
                        'detailed_analysis': '',
                        'correct_answer': '',
                        'bbox': {}
                    })

            # 计算总体统计
            total_questions = len(questions)
            average_score = total_score / max(total_questions, 1)
            accuracy = (correct_count / max(total_questions, 1)) * 100

            return {
                'success': True,
                'data': {
                    'grading_results': grading_results,
                    'statistics': {
                        'total_questions': total_questions,
                        'correct_count': correct_count,
                        'total_score': total_score,
                        'average_score': round(average_score, 2),
                        'accuracy': round(accuracy, 2)
                    }
                },
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f"批改试卷异常: {str(e)}"
            }