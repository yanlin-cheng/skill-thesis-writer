#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GB/T 7714-2015 参考文献格式化工具
支持自动格式化、去重检测、年代分析
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reference:
    """参考文献数据类"""
    ref_type: str  # 文献类型：journal/monograph/thesis/conference/web
    authors: List[str]
    title: str
    year: int
    journal: Optional[str] = None  # 期刊名
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None  # 出版社
    place: Optional[str] = None  # 出版地
    editors: Optional[List[str]] = None  # 编者
    book_title: Optional[str] = None  # 论文集中的书名
    url: Optional[str] = None  # 网址
    access_date: Optional[str] = None  # 访问日期
    doi: Optional[str] = None
    
    def __hash__(self):
        return hash((self.title.lower(), self.year))
    
    def __eq__(self, other):
        return self.title.lower() == other.title.lower() and self.year == other.year


class ReferenceFormatter:
    """参考文献格式化器"""
    
    # 文献类型标识
    TYPE_CODES = {
        'journal': 'J',
        'monograph': 'M',
        'thesis': 'D',
        'conference': 'C',
        'report': 'R',
        'standard': 'S',
        'patent': 'P',
        'newspaper': 'N',
        'web': 'EB/OL'
    }
    
    def __init__(self):
        self.references: List[Reference] = []
        
    def parse_from_text(self, text: str) -> List[Reference]:
        """
        从文本解析参考文献
        
        Args:
            text: 包含参考文献信息的文本
            
        Returns:
            List[Reference]: 解析后的参考文献列表
        """
        refs = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            ref = self._parse_single_reference(line)
            if ref:
                refs.append(ref)
        
        self.references = refs
        return refs
    
    def _parse_single_reference(self, line: str) -> Optional[Reference]:
        """解析单条参考文献"""
        # 尝试匹配常见格式
        
        # 格式1: 作者. 标题[J]. 期刊, 年, 卷(期): 页码.
        journal_pattern = r'^(.+?)\.\s*(.+?)\s*\[J\]\.\s*(.+?),\s*(\d{4})\s*,\s*(\d+)\s*\((\d+)\)\s*:\s*(.+?)\.$'
        match = re.match(journal_pattern, line)
        if match:
            authors_str, title, journal, year, volume, issue, pages = match.groups()
            return Reference(
                ref_type='journal',
                authors=[a.strip() for a in authors_str.split(',')],
                title=title.strip(),
                year=int(year),
                journal=journal.strip(),
                volume=volume,
                issue=issue,
                pages=pages.strip()
            )
        
        # 格式2: 作者. 书名[M]. 出版地: 出版社, 年.
        book_pattern = r'^(.+?)\.\s*(.+?)\s*\[M\]\.\s*(.+?)\s*:\s*(.+?),\s*(\d{4})\.$'
        match = re.match(book_pattern, line)
        if match:
            authors_str, title, place, publisher, year = match.groups()
            return Reference(
                ref_type='monograph',
                authors=[a.strip() for a in authors_str.split(',')],
                title=title.strip(),
                year=int(year),
                place=place.strip(),
                publisher=publisher.strip()
            )
        
        # 格式3: 作者. 标题[D]. 保存地: 保存单位, 年.
        thesis_pattern = r'^(.+?)\.\s*(.+?)\s*\[D\]\.\s*(.+?)\s*:\s*(.+?),\s*(\d{4})\.$'
        match = re.match(thesis_pattern, line)
        if match:
            authors_str, title, place, school, year = match.groups()
            return Reference(
                ref_type='thesis',
                authors=[a.strip() for a in authors_str.split(',')],
                title=title.strip(),
                year=int(year),
                place=place.strip(),
                publisher=school.strip()
            )
        
        return None
    
    def format_gbt7714(self, refs: Optional[List[Reference]] = None) -> List[str]:
        """
        格式化为GB/T 7714-2015格式
        
        Args:
            refs: 参考文献列表，默认使用已解析的列表
            
        Returns:
            List[str]: 格式化后的参考文献字符串列表
        """
        if refs is None:
            refs = self.references
        
        formatted = []
        for i, ref in enumerate(refs, 1):
            formatted_ref = self._format_single_reference(ref, i)
            formatted.append(formatted_ref)
        
        return formatted
    
    def _format_single_reference(self, ref: Reference, index: int) -> str:
        """格式化单条参考文献"""
        type_code = self.TYPE_CODES.get(ref.ref_type, 'M')
        
        # 格式化作者
        authors_str = self._format_authors(ref.authors)
        
        if ref.ref_type == 'journal':
            # 期刊：[序号] 作者. 题名[J]. 刊名, 年, 卷(期): 页码.
            return f"[{index}] {authors_str}. {ref.title}[{type_code}]. {ref.journal}, {ref.year}, {ref.volume}({ref.issue}): {ref.pages}."
        
        elif ref.ref_type == 'monograph':
            # 专著：[序号] 作者. 题名[M]. 出版地: 出版者, 年.
            return f"[{index}] {authors_str}. {ref.title}[{type_code}]. {ref.place}: {ref.publisher}, {ref.year}."
        
        elif ref.ref_type == 'thesis':
            # 学位论文：[序号] 作者. 题名[D]. 保存地: 保存单位, 年.
            return f"[{index}] {authors_str}. {ref.title}[{type_code}]. {ref.place}: {ref.publisher}, {ref.year}."
        
        elif ref.ref_type == 'conference':
            # 会议论文：[序号] 作者. 题名[C]//编者. 文集名. 出版地: 出版者, 年: 页码.
            editors_str = self._format_authors(ref.editors) if ref.editors else ""
            if editors_str:
                return f"[{index}] {authors_str}. {ref.title}[{type_code}]//{editors_str}. {ref.book_title}. {ref.place}: {ref.publisher}, {ref.year}: {ref.pages}."
            else:
                return f"[{index}] {authors_str}. {ref.title}[{type_code}]. {ref.place}: {ref.publisher}, {ref.year}."
        
        elif ref.ref_type == 'web':
            # 电子文献：[序号] 作者. 题名[EB/OL]. (更新日期)[引用日期]. URL.
            access_date = ref.access_date or datetime.now().strftime('%Y-%m-%d')
            return f"[{index}] {authors_str}. {ref.title}[{type_code}]. [{access_date}]. {ref.url}."
        
        else:
            return f"[{index}] {authors_str}. {ref.title}[{type_code}]. {ref.year}."
    
    def _format_authors(self, authors: List[str]) -> str:
        """格式化作者列表"""
        if not authors:
            return ""
        
        # 处理中英文作者
        formatted = []
        for author in authors:
            author = author.strip()
            # 如果是英文作者（包含字母）
            if re.search(r'[a-zA-Z]', author):
                formatted.append(author)
            else:
                # 中文作者
                formatted.append(author)
        
        # 如果超过3个作者，使用"等"或"et al"
        if len(formatted) > 3:
            # 检测是中文还是英文
            if re.search(r'[\u4e00-\u9fff]', formatted[0]):
                return ", ".join(formatted[:3]) + ", 等"
            else:
                return ", ".join(formatted[:3]) + ", et al"
        else:
            return ", ".join(formatted)
    
    def detect_duplicates(self, refs: Optional[List[Reference]] = None, 
                         similarity_threshold: float = 0.85) -> List[Tuple[Reference, Reference, float]]:
        """
        检测重复文献
        
        Args:
            refs: 参考文献列表
            similarity_threshold: 相似度阈值
            
        Returns:
            List[Tuple]: 重复文献对及相似度
        """
        if refs is None:
            refs = self.references
        
        duplicates = []
        for i, ref1 in enumerate(refs):
            for ref2 in refs[i+1:]:
                similarity = self._calculate_similarity(ref1, ref2)
                if similarity >= similarity_threshold:
                    duplicates.append((ref1, ref2, similarity))
        
        return duplicates
    
    def _calculate_similarity(self, ref1: Reference, ref2: Reference) -> float:
        """计算两条参考文献的相似度"""
        # 如果标题完全匹配（忽略大小写和空格）
        title1 = re.sub(r'\s+', '', ref1.title.lower())
        title2 = re.sub(r'\s+', '', ref2.title.lower())
        
        if title1 == title2:
            return 1.0
        
        # 计算标题相似度（简单的字符匹配）
        common = set(title1) & set(title2)
        union = set(title1) | set(title2)
        
        return len(common) / len(union) if union else 0.0
    
    def analyze_timeliness(self, refs: Optional[List[Reference]] = None, 
                          years_back: int = 5) -> Dict:
        """
        分析文献时效性
        
        Args:
            refs: 参考文献列表
            years_back: 近X年定义
            
        Returns:
            Dict: 时效性分析报告
        """
        if refs is None:
            refs = self.references
        
        current_year = datetime.now().year
        cutoff_year = current_year - years_back
        
        recent_count = sum(1 for r in refs if r.year >= cutoff_year)
        total_count = len(refs)
        
        recent_ratio = recent_count / total_count if total_count > 0 else 0
        
        # 按年份分布
        year_dist = {}
        for ref in refs:
            year_dist[ref.year] = year_dist.get(ref.year, 0) + 1
        
        return {
            'total': total_count,
            'recent_count': recent_count,
            'recent_ratio': recent_ratio,
            'years_back': years_back,
            'year_distribution': year_dist,
            'oldest_year': min((r.year for r in refs), default=None),
            'newest_year': max((r.year for r in refs), default=None)
        }
    
    def check_compliance(self, discipline: str = "general") -> Dict:
        """
        检查文献是否符合学科要求
        
        Args:
            discipline: 学科领域（工科/社科）
            
        Returns:
            Dict: 合规性检查结果
        """
        timeliness = self.analyze_timeliness()
        
        # 学科要求
        requirements = {
            '工科': {'recent_ratio': 0.40, 'years_back': 5},
            '社科': {'recent_ratio': 0.30, 'years_back': 5},
            'general': {'recent_ratio': 0.35, 'years_back': 5}
        }
        
        req = requirements.get(discipline, requirements['general'])
        
        issues = []
        if timeliness['recent_ratio'] < req['recent_ratio']:
            issues.append(
                f"近{req['years_back']}年文献占比{timeliness['recent_ratio']:.1%}，"
                f"低于{discipline}要求({req['recent_ratio']:.0%})"
            )
        
        return {
            'discipline': discipline,
            'requirement': req,
            'actual': timeliness,
            'is_compliant': len(issues) == 0,
            'issues': issues
        }
    
    def sort_references(self, refs: Optional[List[Reference]] = None, 
                       method: str = "author_year") -> List[Reference]:
        """
        排序参考文献
        
        Args:
            refs: 参考文献列表
            method: 排序方法（author_year/year_author/citation_order）
            
        Returns:
            List[Reference]: 排序后的列表
        """
        if refs is None:
            refs = self.references
        
        if method == "author_year":
            return sorted(refs, key=lambda r: (r.authors[0] if r.authors else "", r.year))
        elif method == "year_author":
            return sorted(refs, key=lambda r: (r.year, r.authors[0] if r.authors else ""))
        else:
            return refs


def main():
    """主函数：命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GB/T 7714参考文献格式化工具')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--discipline', '-d', default='general',
                       choices=['工科', '社科', 'general'],
                       help='学科领域')
    parser.add_argument('--check-duplicates', '-c', action='store_true',
                       help='检测重复文献')
    parser.add_argument('--analyze-timeliness', '-a', action='store_true',
                       help='分析文献时效性')
    
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 初始化格式化器
    formatter = ReferenceFormatter()
    refs = formatter.parse_from_text(text)
    
    print(f"共解析 {len(refs)} 条参考文献")
    print("=" * 50)
    
    # 格式化输出
    formatted = formatter.format_gbt7714(refs)
    print("\n格式化结果：")
    for ref_str in formatted[:5]:  # 显示前5条
        print(ref_str)
    if len(formatted) > 5:
        print(f"... 共 {len(formatted)} 条")
    
    # 检测重复
    if args.check_duplicates:
        print("\n" + "=" * 50)
        print("重复文献检测：")
        duplicates = formatter.detect_duplicates(refs)
        if duplicates:
            for ref1, ref2, sim in duplicates:
                print(f"相似度 {sim:.2%}: {ref1.title} | {ref2.title}")
        else:
            print("未发现重复文献")
    
    # 时效性分析
    if args.analyze_timeliness:
        print("\n" + "=" * 50)
        print("文献时效性分析：")
        timeliness = formatter.analyze_timeliness(refs)
        print(f"文献总数: {timeliness['total']}")
        print(f"近5年文献: {timeliness['recent_count']} ({timeliness['recent_ratio']:.1%})")
        print(f"年份范围: {timeliness['oldest_year']} - {timeliness['newest_year']}")
        
        # 合规性检查
        compliance = formatter.check_compliance(args.discipline)
        print(f"\n学科合规性({args.discipline})：")
        print(f"要求近5年占比 ≥ {compliance['requirement']['recent_ratio']:.0%}")
        print(f"实际: {compliance['actual']['recent_ratio']:.1%}")
        print(f"状态: {'通过' if compliance['is_compliant'] else '未通过'}")
        if compliance['issues']:
            for issue in compliance['issues']:
                print(f"  ⚠️ {issue}")
    
    # 保存输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for ref_str in formatted:
                f.write(ref_str + '\n')
        print(f"\n结果已保存至: {args.output}")


if __name__ == "__main__":
    main()
