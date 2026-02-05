#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI痕迹消除模块
功能：检测并消除学术文本中的AI生成特征，使其更接近人类学者写作风格
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import Counter


@dataclass
class DetectionResult:
    """检测结果数据类"""
    cv_score: float  # 句子长度变异系数
    connective_density: float  # 连接词密度
    passive_ratio: float  # 被动语态比例
    risk_level: str  # 风险等级：low/medium/high
    suggestions: List[str]  # 改进建议


class AIHumanizer:
    """AI痕迹消除器"""
    
    # 高频连接词及其替换选项
    CONNECTIVE_ALTERNATIVES = {
        "此外": ["无独有偶", "与此同时", "进一步而言", "从另一维度来看", "补充说明", "值得注意的是"],
        "而且": ["更有甚者", "尤为重要的是", "值得强调的是", "更重要的是", "不仅如此"],
        "另外": ["除此之外", "另一方面", "此外值得注意的是"],
        "但是": ["然而", "尽管如此", "不可否认的是", "反观之", "与之形成对比的是", "但需要指出的是"],
        "不过": ["诚然", "虽说如此", "但值得注意的是"],
        "因此": ["由此可见", "推而广之", "综合上述分析", "基于此", "据此推断", "有鉴于此"],
        "所以": ["这意味着", "这一结果表明", "据此可推断", "有鉴于此", "综上所述"],
        "例如": ["以...为例", "具体而言", "一个典型的例子是", "不妨以...为例"],
        "比如": ["如", "举例来说", "一个恰当的例子是", "具体来看"],
        "总之": ["综上所述", "总而言之", "归纳起来", "总的来看", "一言以蔽之"],
        "首先": ["第一", "首要的是", "从第一点来看"],
        "其次": ["第二", "进而", "除此之外"],
        "最后": ["最终", "综上所述", "归根结底"]
    }
    
    # 学科特异性表达
    DISCIPLINE_EXPRESSIONS = {
        "工科": {
            "practice": ["从工程实现角度来看", "在实际部署环境中", "考虑到计算资源的限制", "针对实际应用场景"],
            "technical": ["该模块的输入维度为{}", "在GPU环境下，单次推理耗时约{}", "模型参数量为{}M，计算量为{}GFlops"],
            "evaluation": ["从准确率来看，模型达到了{}%", "消融实验表明，移除{}后，{}下降了{}%", "与基线模型相比，本文方法在{}上提升了{}个百分点"]
        },
        "心理学": {
            "observation": ["本研究发现", "数据分析结果显示", "我们观察到", "一个值得注意的模式是"],
            "caution": ["这一模式可能暗示", "据此我们推测", "一种可能的解释是", "这提示我们"],
            "theory": ["这一发现与{}的预测相符", "从{}的视角来看", "这一结果支持了{}的观点"]
        },
        "教育学": {
            "practice": ["从教学实践的角度来看", "这一发现对教育实践的启示在于", "课堂观察发现", "教师反馈显示"],
            "suggestion": ["基于上述发现，建议教师在{}加以关注", "课程设计可考虑融入{}", "教育管理者或许需要重新审视{}"]
        },
        "管理学": {
            "perspective": ["从组织行为学的视角来看", "基于{}的逻辑", "这一发现对{}提供了实证支持"],
            "implication": ["对管理实践的启示是", "组织在{}或许需要考虑", "这一结果提示管理者"]
        }
    }
    
    # 限定词与谨慎表述
    HEDGING_WORDS = [
        "一定程度上", "一般而言", "从现有数据来看", "在本文研究范围内",
        "初步看来", "可能暗示", "似乎表明", "或许", "大概",
        "倾向于", "一定程度上可以认为", "据现有证据推测"
    ]
    
    # 批判性表达模板
    CRITICAL_TEMPLATES = {
        "literature": [
            "尽管{}（{}）的研究在{}方面取得了显著进展，但其研究设计存在{}，这可能影响了{}的可靠性。",
            "需要指出的是，现有研究在{}尚未达成一致，{}（{}）认为{}，而{}（{}）则提出{}，这种分歧暗示了{}的复杂性。",
            "从现有文献来看，{}的研究多集中于{}，而对{}的关注相对不足，这一空白为本研究提供了切入点。"
        ],
        "methodology": [
            "本研究采用{}，虽然该方法在{}方面具有优势，但我们也意识到其可能存在的局限，如{}。",
            "为了尽可能控制{}，本研究采取了{}，尽管如此，{}仍可能对结果产生一定影响。",
            "受限于{}，本研究的样本主要来源于{}，这在一定程度上限制了结论向{}的推广。"
        ],
        "results": [
            "这一发现与{}的预测一致，然而，考虑到{}，我们倾向于以更为谨慎的态度解读这一结果。",
            "值得注意的是，{}仅在{}下显著，这暗示了{}与{}之间的关系可能受到{}的影响。",
            "虽然本研究未能发现{}的支持证据，但这一\"零结果\"本身也具有启示意义——它提示我们可能需要重新审视{}。"
        ]
    }
    
    def __init__(self, discipline: str = "general"):
        """
        初始化
        
        Args:
            discipline: 学科领域，可选：general/工科/心理学/教育学/管理学
        """
        self.discipline = discipline
        
    def detect(self, text: str) -> DetectionResult:
        """
        检测文本中的AI痕迹
        
        Args:
            text: 待检测文本
            
        Returns:
            DetectionResult: 检测结果
        """
        # 分句
        sentences = self._split_sentences(text)
        
        # 计算句子长度变异系数
        cv_score = self._calculate_cv(sentences)
        
        # 计算连接词密度
        connective_density = self._calculate_connective_density(text)
        
        # 计算被动语态比例
        passive_ratio = self._calculate_passive_ratio(sentences)
        
        # 评估风险等级
        risk_level = self._assess_risk(cv_score, connective_density, passive_ratio)
        
        # 生成建议
        suggestions = self._generate_suggestions(cv_score, connective_density, passive_ratio)
        
        return DetectionResult(
            cv_score=cv_score,
            connective_density=connective_density,
            passive_ratio=passive_ratio,
            risk_level=risk_level,
            suggestions=suggestions
        )
    
    def humanize(self, text: str, aggressive: bool = False) -> str:
        """
        消除AI痕迹
        
        Args:
            text: 待处理文本
            aggressive: 是否采用激进模式（更多改写）
            
        Returns:
            str: 优化后的文本
        """
        result = text
        
        # 1. 替换高频连接词
        result = self._replace_connectives(result)
        
        # 2. 添加限定词（适度）
        if aggressive:
            result = self._add_hedging(result)
        
        # 3. 学科特异性增强
        if self.discipline in self.DISCIPLINE_EXPRESSIONS:
            result = self._enhance_discipline_style(result)
        
        # 4. 句式节奏调整
        result = self._adjust_rhythm(result)
        
        return result
    
    def _split_sentences(self, text: str) -> List[str]:
        """分句"""
        # 中文分句
        pattern = r'[^。！？；]+[。！？；]'
        sentences = re.findall(pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _calculate_cv(self, sentences: List[str]) -> float:
        """计算句子长度变异系数"""
        if len(sentences) < 2:
            return 0.0
        
        lengths = [len(s) for s in sentences]
        mean = sum(lengths) / len(lengths)
        variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
        std = variance ** 0.5
        
        return std / mean if mean > 0 else 0.0
    
    def _calculate_connective_density(self, text: str) -> float:
        """计算连接词密度"""
        connectives = list(self.CONNECTIVE_ALTERNATIVES.keys())
        connective_count = sum(text.count(c) for c in connectives)
        total_chars = len(text)
        
        return (connective_count * len(connectives[0])) / total_chars if total_chars > 0 else 0.0
    
    def _calculate_passive_ratio(self, sentences: List[str]) -> float:
        """计算被动语态比例"""
        if not sentences:
            return 0.0
        
        # 中文被动标记
        passive_markers = ["被", "由", "受到", "得到", "得以", "为...所"]
        passive_count = 0
        
        for sentence in sentences:
            if any(marker in sentence for marker in passive_markers):
                passive_count += 1
        
        return passive_count / len(sentences)
    
    def _assess_risk(self, cv: float, density: float, passive: float) -> str:
        """评估风险等级"""
        risk_score = 0
        
        # CV过低（句式过于均匀）
        if cv < 0.2:
            risk_score += 2
        elif cv < 0.3:
            risk_score += 1
        
        # 连接词密度过高
        if density > 0.08:
            risk_score += 2
        elif density > 0.05:
            risk_score += 1
        
        # 根据学科评估被动语态
        if self.discipline == "工科" and passive < 0.5:
            risk_score += 1
        elif self.discipline in ["心理学", "教育学", "管理学"] and passive > 0.6:
            risk_score += 1
        
        if risk_score >= 4:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"
    
    def _generate_suggestions(self, cv: float, density: float, passive: float) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if cv < 0.3:
            suggestions.append("句子长度过于均匀，建议混合使用长短句（CV目标：>0.35）")
        
        if density > 0.05:
            suggestions.append("连接词使用过于频繁，建议替换为多样化表达或隐性连接")
        
        if self.discipline == "工科":
            if passive < 0.5:
                suggestions.append("被动语态比例偏低，建议增加被动表述（工科建议≥60%）")
        else:
            if passive > 0.6:
                suggestions.append("被动语态比例偏高，建议增加主动表述")
        
        return suggestions
    
    def _replace_connectives(self, text: str) -> str:
        """替换连接词"""
        result = text
        for word, alternatives in self.CONNECTIVE_ALTERNATIVES.items():
            # 使用计数器确保替换的多样性
            count = result.count(word)
            for i in range(count):
                # 轮询使用不同的替换词
                replacement = alternatives[i % len(alternatives)]
                result = result.replace(word, replacement, 1)
        return result
    
    def _add_hedging(self, text: str) -> str:
        """添加限定词"""
        # 在绝对化表述前添加限定词
        absolute_patterns = [
            (r"证明了", "一定程度上证明了"),
            (r"表明了", "初步表明了"),
            (r"说明了", "似乎说明了"),
        ]
        
        result = text
        for pattern, replacement in absolute_patterns:
            result = re.sub(pattern, replacement, result)
        
        return result
    
    def _enhance_discipline_style(self, text: str) -> str:
        """增强学科特异性表达"""
        expressions = self.DISCIPLINE_EXPRESSIONS.get(self.discipline, {})
        
        # 这里可以添加更复杂的学科特异性改写逻辑
        # 目前保持原文，留给后续扩展
        return text
    
    def _adjust_rhythm(self, text: str) -> str:
        """调整句式节奏"""
        sentences = self._split_sentences(text)
        
        # 简单的节奏调整：将过长的句子拆分为短句
        adjusted_sentences = []
        for sentence in sentences:
            if len(sentence) > 50:
                # 尝试在逗号处拆分
                parts = sentence.split('，')
                if len(parts) > 2:
                    # 合并前两个部分，其余单独成句
                    adjusted_sentences.append('，'.join(parts[:2]) + '。')
                    for part in parts[2:]:
                        if part.strip():
                            adjusted_sentences.append(part.strip() + '。')
                else:
                    adjusted_sentences.append(sentence)
            else:
                adjusted_sentences.append(sentence)
        
        return ''.join(adjusted_sentences)
    
    def generate_critical_insertion(self, section_type: str, **kwargs) -> str:
        """
        生成批判性表达插入语
        
        Args:
            section_type: 章节类型（literature/methodology/results）
            **kwargs: 模板填充参数
            
        Returns:
            str: 批判性表达语句
        """
        templates = self.CRITICAL_TEMPLATES.get(section_type, [])
        if not templates:
            return ""
        
        import random
        template = random.choice(templates)
        
        try:
            return template.format(**kwargs)
        except KeyError:
            return template


def main():
    """主函数：命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI痕迹消除工具')
    parser.add_argument('input', help='输入文本或文件路径')
    parser.add_argument('--discipline', '-d', default='general', 
                       choices=['general', '工科', '心理学', '教育学', '管理学'],
                       help='学科领域')
    parser.add_argument('--detect-only', '-t', action='store_true',
                       help='仅检测不处理')
    parser.add_argument('--aggressive', '-a', action='store_true',
                       help='激进模式（更多改写）')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 读取输入
    if args.input.endswith('.txt'):
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.input
    
    # 初始化处理器
    humanizer = AIHumanizer(discipline=args.discipline)
    
    # 检测
    result = humanizer.detect(text)
    
    print("=" * 50)
    print("AI痕迹检测报告")
    print("=" * 50)
    print(f"句子长度变异系数(CV): {result.cv_score:.3f}")
    print(f"连接词密度: {result.connective_density:.3f}")
    print(f"被动语态比例: {result.passive_ratio:.2%}")
    print(f"风险等级: {result.risk_level.upper()}")
    print("\n改进建议:")
    for i, suggestion in enumerate(result.suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    if not args.detect_only:
        print("\n" + "=" * 50)
        print("降AI味处理结果")
        print("=" * 50)
        
        optimized = humanizer.humanize(text, aggressive=args.aggressive)
        print(optimized)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(optimized)
            print(f"\n结果已保存至: {args.output}")


if __name__ == "__main__":
    main()
