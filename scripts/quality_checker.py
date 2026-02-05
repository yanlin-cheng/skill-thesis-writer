#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文质量检查工具
功能：检查论文的逻辑一致性、格式规范、引用质量等
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class QualityIssue:
    """质量问题数据类"""
    category: str  # 问题类别
    severity: str  # 严重程度：error/warning/info
    message: str  # 问题描述
    location: Optional[str] = None  # 位置信息
    suggestion: Optional[str] = None  # 改进建议


@dataclass
class QualityReport:
    """质量报告"""
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    issues: List[QualityIssue] = field(default_factory=list)
    summary: str = ""
    score: float = 0.0  # 质量评分（0-100）


class QualityChecker:
    """论文质量检查器"""
    
    def __init__(self, discipline: str = "general"):
        self.discipline = discipline
        self.checklist = self._load_checklist()
    
    def _load_checklist(self) -> Dict:
        """加载检查清单"""
        return {
            "structure": [
                "标题是否准确概括研究内容",
                "摘要是否包含目的、方法、结果、结论",
                "关键词是否准确（3-5个）",
                "章节结构是否完整",
                "结论是否回应研究问题"
            ],
            "logic": [
                "研究问题→方法→结论 是否形成闭环",
                "变量操作性定义是否明确",
                "假设是否在讨论中验证",
                "文献综述是否支持研究缺口论证"
            ],
            "citation": [
                "引用格式是否统一",
                "是否有过度自引",
                "近5年文献占比是否达标"
            ],
            "writing": [
                "是否存在口语化表达",
                "标点符号使用是否规范",
                "是否存在连续长句"
            ]
        }
    
    def check_all(self, text: str, title: str = "", abstract: str = "") -> QualityReport:
        """
        执行全面质量检查
        
        Args:
            text: 论文正文
            title: 论文标题
            abstract: 摘要
            
        Returns:
            QualityReport: 质量报告
        """
        report = QualityReport()
        
        # 执行各项检查
        structure_issues = self.check_structure(text, title, abstract)
        logic_issues = self.check_logic(text)
        citation_issues = self.check_citations(text)
        writing_issues = self.check_writing_style(text)
        format_issues = self.check_format(text)
        
        # 合并所有问题
        all_issues = (structure_issues + logic_issues + citation_issues + 
                     writing_issues + format_issues)
        
        report.issues = all_issues
        report.total_issues = len(all_issues)
        report.errors = sum(1 for i in all_issues if i.severity == "error")
        report.warnings = sum(1 for i in all_issues if i.severity == "warning")
        report.infos = sum(1 for i in all_issues if i.severity == "info")
        
        # 计算评分
        report.score = self._calculate_score(report)
        
        # 生成摘要
        report.summary = self._generate_summary(report)
        
        return report
    
    def check_structure(self, text: str, title: str, abstract: str) -> List[QualityIssue]:
        """检查结构完整性"""
        issues = []
        
        # 检查标题长度
        if title:
            title_len = len(title.replace(" ", ""))
            if title_len > 30:
                issues.append(QualityIssue(
                    category="结构",
                    severity="warning",
                    message=f"标题过长（{title_len}字），建议控制在20字以内",
                    suggestion="精简标题，突出核心概念"
                ))
            elif title_len < 10:
                issues.append(QualityIssue(
                    category="结构",
                    severity="warning",
                    message=f"标题过短（{title_len}字），可能未能准确概括研究内容",
                    suggestion="补充关键变量或研究对象信息"
                ))
        
        # 检查摘要要素
        if abstract:
            abstract_lower = abstract.lower()
            required_elements = {
                "目的": ["旨在", "目的", "探讨", "研究", "考察"],
                "方法": ["采用", "方法", "设计", "选取"],
                "结果": ["结果", "发现", "表明", "显示"],
                "结论": ["结论", "表明", "说明", " suggests"]
            }
            
            for element, keywords in required_elements.items():
                if not any(kw in abstract for kw in keywords):
                    issues.append(QualityIssue(
                        category="结构",
                        severity="warning",
                        message=f"摘要可能缺少{element}要素",
                        suggestion=f"在摘要中明确说明研究的{element}"
                    ))
            
            # 检查摘要长度
            abstract_len = len(abstract.replace(" ", ""))
            if abstract_len < 200:
                issues.append(QualityIssue(
                    category="结构",
                    severity="warning",
                    message=f"摘要过短（{abstract_len}字），可能信息不完整",
                    suggestion="硕士论文摘要建议300-500字，博士论文500-800字"
                ))
        
        # 检查章节结构
        required_sections = ["引言", "方法", "结果", "讨论", "结论"]
        for section in required_sections:
            if section not in text:
                issues.append(QualityIssue(
                    category="结构",
                    severity="error",
                    message=f"缺少{section}部分",
                    suggestion=f"补充{section}章节"
                ))
        
        return issues
    
    def check_logic(self, text: str) -> List[QualityIssue]:
        """检查逻辑一致性"""
        issues = []
        
        # 检查假设验证闭环
        hypotheses = re.findall(r'[Hh]\d+[：:]\s*(.+?)[。\n]', text)
        if hypotheses:
            for h in hypotheses:
                h_text = h[1] if isinstance(h, tuple) else h
                # 检查是否在讨论中回应
                discussion_match = re.search(r'讨论.*' + re.escape(h_text[:10]), text, re.DOTALL)
                if not discussion_match:
                    issues.append(QualityIssue(
                        category="逻辑",
                        severity="warning",
                        message=f"假设'{h_text[:20]}...'可能未在讨论中充分回应",
                        suggestion="在讨论部分明确说明每个假设的验证结果"
                    ))
        
        # 检查变量定义一致性
        variable_definitions = re.findall(r'([\w\u4e00-\u9fa5]+).*?(?:操作性定义|定义为|是指)[：:](.+?)[。\n]', text)
        defined_vars = set(v[0] for v in variable_definitions)
        
        # 检查是否所有变量都有定义
        # 这是一个简化检查，实际应用中需要更复杂的NLP
        
        return issues
    
    def check_citations(self, text: str) -> List[QualityIssue]:
        """检查引用质量"""
        issues = []
        
        # 提取引用
        citations = re.findall(r'\[(\d+)\]', text)
        citation_nums = [int(c) for c in citations]
        
        if not citation_nums:
            issues.append(QualityIssue(
                category="引用",
                severity="error",
                message="正文中未发现引用标记",
                suggestion="使用[序号]格式添加文献引用"
            ))
            return issues
        
        # 检查引用连续性
        unique_citations = sorted(set(citation_nums))
        if len(unique_citations) < 10:
            issues.append(QualityIssue(
                category="引用",
                severity="warning",
                message=f"引用数量较少（{len(unique_citations)}篇）",
                suggestion="建议硕士论文引用不少于50篇，博士论文不少于100篇"
            ))
        
        # 检查是否有连续13字重复（简单检测）
        sentences = re.findall(r'[^。！？]+[。！？]', text)
        for i, sent in enumerate(sentences):
            for j in range(i+1, min(i+10, len(sentences))):
                if self._calculate_similarity(sent, sentences[j]) > 0.85:
                    issues.append(QualityIssue(
                        category="引用",
                        severity="warning",
                        message=f"发现疑似重复表述",
                        location=f"第{i+1}句与第{j+1}句",
                        suggestion="改写重复内容或直接引用并标注"
                    ))
                    break
        
        return issues
    
    def check_writing_style(self, text: str) -> List[QualityIssue]:
        """检查写作风格"""
        issues = []
        
        # 口语化表达检测
        colloquial_words = ["很", "非常", "挺", "挺", "蛮", "蛮", "蛮"]
        for word in colloquial_words:
            matches = re.findall(word + r'[\u4e00-\u9fa5]', text)
            if len(matches) > 3:
                issues.append(QualityIssue(
                    category="写作",
                    severity="info",
                    message=f"发现口语化用词'{word}'（{len(matches)}次）",
                    suggestion="替换为更正式的学术表达"
                ))
                break
        
        # 绝对化表述检测
        absolute_words = ["证明了", "绝对的", "完全的", "彻底"]
        for word in absolute_words:
            if word in text:
                issues.append(QualityIssue(
                    category="写作",
                    severity="warning",
                    message=f"发现绝对化表述'{word}'",
                    suggestion="使用'支持了'、'表明'等谨慎表述替代"
                ))
        
        # 长句检测
        sentences = re.findall(r'[^。！？]+[。！？]', text)
        long_sentences = [s for s in sentences if len(s) > 100]
        if len(long_sentences) > len(sentences) * 0.3:
            issues.append(QualityIssue(
                category="写作",
                severity="info",
                message=f"长句比例过高（{len(long_sentences)/len(sentences):.1%}）",
                suggestion="适当拆分长句，提高可读性"
            ))
        
        return issues
    
    def check_format(self, text: str) -> List[QualityIssue]:
        """检查格式规范"""
        issues = []
        
        # 检查中英文标点混用
        cn_punctuation = '，。！？；：""''（）【】'
        en_punctuation = ',.!?;:""''()[]'
        
        # 简单检查：中文内容后使用英文标点
        # 这是一个简化版本，实际需要更复杂的检测
        
        # 检查图表引用
        figures = re.findall(r'图\s*(\d+)', text)
        tables = re.findall(r'表\s*(\d+)', text)
        
        if figures:
            figure_nums = [int(f) for f in figures]
            if max(figure_nums) > 0 and not all(i in figure_nums for i in range(1, max(figure_nums)+1)):
                issues.append(QualityIssue(
                    category="格式",
                    severity="warning",
                    message="图编号可能不连续",
                    suggestion="检查图编号是否连续（图1、图2、图3...）"
                ))
        
        return issues
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        # 简单的字符级相似度
        set1 = set(text1)
        set2 = set(text2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def _calculate_score(self, report: QualityReport) -> float:
        """计算质量评分"""
        base_score = 100
        base_score -= report.errors * 10
        base_score -= report.warnings * 5
        base_score -= report.infos * 1
        return max(0, min(100, base_score))
    
    def _generate_summary(self, report: QualityReport) -> str:
        """生成检查摘要"""
        if report.score >= 90:
            level = "优秀"
        elif report.score >= 80:
            level = "良好"
        elif report.score >= 60:
            level = "合格"
        else:
            level = "需改进"
        
        return (f"质量评分：{report.score:.1f}/100（{level}）\n"
                f"发现问题：{report.total_issues}个 "
                f"（错误：{report.errors}，警告：{report.warnings}，提示：{report.infos}）")
    
    def generate_report(self, report: QualityReport, output_format: str = "markdown") -> str:
        """
        生成格式化的检查报告
        
        Args:
            report: 质量报告
            output_format: 输出格式（markdown/json）
            
        Returns:
            str: 格式化报告
        """
        if output_format == "json":
            return json.dumps({
                "score": report.score,
                "summary": report.summary,
                "total_issues": report.total_issues,
                "errors": report.errors,
                "warnings": report.warnings,
                "infos": report.infos,
                "issues": [
                    {
                        "category": i.category,
                        "severity": i.severity,
                        "message": i.message,
                        "location": i.location,
                        "suggestion": i.suggestion
                    }
                    for i in report.issues
                ]
            }, ensure_ascii=False, indent=2)
        
        # Markdown格式
        lines = []
        lines.append("# 论文质量检查报告")
        lines.append("")
        lines.append(f"**检查时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**学科领域**：{self.discipline}")
        lines.append("")
        lines.append("## 总体评价")
        lines.append("")
        lines.append(f"{report.summary}")
        lines.append("")
        
        if report.issues:
            lines.append("## 详细问题列表")
            lines.append("")
            
            # 按严重程度排序
            severity_order = {"error": 0, "warning": 1, "info": 2}
            sorted_issues = sorted(report.issues, 
                                 key=lambda x: severity_order.get(x.severity, 3))
            
            for i, issue in enumerate(sorted_issues, 1):
                severity_icon = {"error": "🔴", "warning": "🟡", "info": "🔵"}.get(issue.severity, "⚪")
                lines.append(f"### {i}. {severity_icon} [{issue.severity.upper()}] {issue.category}")
                lines.append("")
                lines.append(f"**问题**：{issue.message}")
                if issue.location:
                    lines.append(f"**位置**：{issue.location}")
                if issue.suggestion:
                    lines.append(f"**建议**：{issue.suggestion}")
                lines.append("")
        else:
            lines.append("## 检查结果")
            lines.append("")
            lines.append("✅ 未发现明显问题，论文质量良好！")
        
        return "\n".join(lines)


def main():
    """主函数：示例"""
    # 示例论文文本
    sample_text = """
# 示例论文

## 摘要

本研究旨在探讨XXX对YYY的影响。采用问卷调查法，选取了500名大学生作为被试。
结果表明，XXX与YYY呈显著正相关。结论：XXX对YYY有重要影响。

## 引言

XXX是一个重要的研究领域。很重要的是，以往研究存在不足。

## 方法

采用问卷调查法。

## 结果

结果发现，XXX对YYY有显著影响（p < .05）。

## 讨论

本研究证明了XXX对YYY的影响。

## 结论

综上所述，XXX对YYY有重要影响。
    """
    
    checker = QualityChecker(discipline="心理学")
    report = checker.check_all(
        text=sample_text,
        title="XXX对YYY的影响研究",
        abstract="本研究旨在探讨XXX对YYY的影响。采用问卷调查法，选取了500名大学生作为被试。结果表明，XXX与YYY呈显著正相关。结论：XXX对YYY有重要影响。"
    )
    
    print(checker.generate_report(report))
    print("\n" + "=" * 60)
    print("JSON格式报告：")
    print(checker.generate_report(report, output_format="json"))


if __name__ == "__main__":
    main()
