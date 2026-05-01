#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据处理模块
实现数据导入、清洗、分析、导出功能
"""

import csv
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class DataProcessor:
    """数据处理类"""
    
    def __init__(self):
        self.data = []
        self.metadata = {}
    
    def load_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """从CSV文件加载数据"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
        return self.data
    
    def load_json(self, file_path: str) -> Dict[str, Any]:
        """从JSON文件加载数据"""
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return self.data
    
    def clean_data(self, remove_nulls: bool = True) -> List[Dict]:
        """清洗数据"""
        cleaned = []
        for row in self.data:
            if remove_nulls:
                cleaned_row = {k: v for k, v in row.items() if v is not None and v != ''}
            else:
                cleaned_row = row.copy()
            cleaned.append(cleaned_row)
        self.data = cleaned
        return self.data
    
    def filter_data(self, field: str, value: Any) -> List[Dict]:
        """过滤数据"""
        return [row for row in self.data if row.get(field) == value]
    
    def aggregate_data(self, field: str, operation: str = 'sum') -> Dict:
        """聚合数据"""
        result = {}
        for row in self.data:
            key = row.get(field, 'unknown')
            if key not in result:
                result[key] = []
            result[key].append(row)
        
        if operation == 'count':
            return {k: len(v) for k, v in result.items()}
        return result
    
    def export_csv(self, file_path: str) -> bool:
        """导出为CSV"""
        if not self.data:
            return False
        
        fieldnames = self.data[0].keys()
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
        return True
    
    def export_json(self, file_path: str) -> bool:
        """导出为JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        return True


class ReportGenerator:
    """报表生成器"""
    
    def __init__(self):
        self.reports = []
    
    def generate_summary(self, data: List[Dict]) -> Dict:
        """生成数据摘要"""
        total_records = len(data)
        return {
            'total_records': total_records,
            'generated_at': datetime.now().isoformat(),
            'status': 'success'
        }
    
    def generate_performance_report(self, user_data: Dict) -> Dict:
        """生成用户绩效报表"""
        return {
            'user_id': user_data.get('id'),
            'score': user_data.get('score', 0),
            'grade': self._calculate_grade(user_data.get('score', 0)),
            'generated_at': datetime.now().isoformat()
        }
    
    def _calculate_grade(self, score: float) -> str:
        """计算等级"""
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


if __name__ == "__main__":
    processor = DataProcessor()
    
    processor.data = [
        {"name": "张三", "score": 92, "department": "技术部"},
        {"name": "李四", "score": 88, "department": "技术部"},
        {"name": "王五", "score": 96, "department": "产品部"}
    ]
    
    filtered = processor.filter_data("department", "技术部")
    print(f"Filtered data: {filtered}")
    
    report_gen = ReportGenerator()
    summary = report_gen.generate_summary(processor.data)
    print(f"Summary: {summary}")
    
    perf_report = report_gen.generate_performance_report({"id": 1, "score": 92})
    print(f"Performance report: {perf_report}")
