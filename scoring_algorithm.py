#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
绩效评估算法模块
实现多维度评分、权重计算、等级转换等功能
"""

from typing import Dict, List
from datetime import datetime


class PerformanceScorer:
    """绩效评分计算类"""
    
    WEIGHT_CONFIG = {
        'task_completion': 0.40,
        'code_quality': 0.25,
        'work_quantity': 0.15,
        'collaboration': 0.10,
        'innovation': 0.10
    }
    
    def __init__(self):
        self.assessments = []
    
    def calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """计算综合得分"""
        total = 0
        for dimension, weight in self.WEIGHT_CONFIG.items():
            score = scores.get(dimension, 0)
            total += score * weight
        return round(total, 2)
    
    def calculate_task_completion_score(
        self,
        total_tasks: int,
        completed_tasks: int,
        quality_avg: float
    ) -> float:
        """计算任务完成度得分"""
        if total_tasks == 0:
            return 0
        
        completion_rate = (completed_tasks / total_tasks) * 100
        quality_bonus = (quality_avg - 50) * 0.2
        return min(100, max(0, completion_rate + quality_bonus))
    
    def calculate_code_quality_score(
        self,
        review_score: float,
        bug_rate: float,
        test_coverage: float
    ) -> float:
        """计算代码质量得分"""
        score = (
            review_score * 0.4 +
            (100 - bug_rate * 10) * 0.3 +
            test_coverage * 0.3
        )
        return min(100, max(0, score))
    
    def convert_to_grade(self, score: float) -> str:
        """分数转等级"""
        if score >= 95:
            return 'S'
        elif score >= 85:
            return 'A'
        elif score >= 75:
            return 'B'
        elif score >= 60:
            return 'C'
        else:
            return 'D'
    
    def generate_assessment_report(
        self,
        user_id: int,
        username: str,
        period: str,
        scores: Dict[str, float]
    ) -> Dict:
        """生成评估报告"""
        overall_score = self.calculate_overall_score(scores)
        grade = self.convert_to_grade(overall_score)
        
        report = {
            'user_id': user_id,
            'username': username,
            'period': period,
            'overall_score': overall_score,
            'grade': grade,
            'dimension_scores': scores,
            'generated_at': datetime.now().isoformat()
        }
        
        self.assessments.append(report)
        return report


class AITaskEvaluator:
    """AI任务评估器"""
    
    def __init__(self):
        self.evaluation_history = []
    
    def evaluate_task_completion(
        self,
        task_title: str,
        commits: List[Dict],
        expected_output: str
    ) -> Dict:
        """评估任务完成情况"""
        commit_count = len(commits)
        total_lines = sum(c.get('lines_changed', 0) for c in commits)
        
        completion_rate = min(100, (commit_count * 15) + (total_lines / 10))
        
        return {
            'task_title': task_title,
            'completion_rate': round(completion_rate, 2),
            'commit_count': commit_count,
            'total_lines_changed': total_lines,
            'assessment': self._get_assessment(completion_rate)
        }
    
    def evaluate_code_quality(self, diff_content: str) -> Dict:
        """评估代码质量"""
        lines = diff_content.split('\n')
        
        comment_ratio = sum(1 for line in lines if line.strip().startswith('#')) / max(len(lines), 1)
        has_error_handling = any('try' in line or 'except' in line for line in lines)
        has_type_hints = any(':' in line and '->' in line for line in lines)
        
        quality_score = (
            min(comment_ratio * 100, 30) +
            (20 if has_error_handling else 0) +
            (20 if has_type_hints else 0) +
            30
        )
        
        return {
            'quality_score': round(min(100, quality_score), 2),
            'comment_ratio': round(comment_ratio, 2),
            'has_error_handling': has_error_handling,
            'has_type_hints': has_type_hints
        }
    
    def _get_assessment(self, rate: float) -> str:
        """获取评估结论"""
        if rate >= 90:
            return '优秀 - 任务完全完成,质量很高'
        elif rate >= 75:
            return '良好 - 任务基本完成,质量较好'
        elif rate >= 60:
            return '合格 - 任务部分完成,需要改进'
        else:
            return '不合格 - 任务未完成,需要重点关注'


if __name__ == "__main__":
    scorer = PerformanceScorer()
    
    scores = {
        'task_completion': 85,
        'code_quality': 90,
        'work_quantity': 80,
        'collaboration': 88,
        'innovation': 75
    }
    
    overall = scorer.calculate_overall_score(scores)
    grade = scorer.convert_to_grade(overall)
    print(f"Overall score: {overall}, Grade: {grade}")
    
    evaluator = AITaskEvaluator()
    commits = [
        {'message': 'feat: add user auth', 'lines_changed': 150},
        {'message': 'fix: login bug', 'lines_changed': 30}
    ]
    
    result = evaluator.evaluate_task_completion(
        "用户认证功能",
        commits,
        "实现完整的用户认证流程"
    )
    print(f"Task evaluation: {result}")
    
    sample_code = """
# User authentication module
def authenticate(username: str, password: str) -> bool:
    '''Authenticate user credentials'''
    try:
        user = get_user(username)
        return verify_password(password, user.hash)
    except Exception as e:
        log_error(e)
        return False
"""
    
    quality = evaluator.evaluate_code_quality(sample_code)
    print(f"Code quality: {quality}")
