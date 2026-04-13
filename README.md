# 跨学科AI论文写作助手 SKILL

> **跨学科AI论文写作助手，专为本科生/研究生论文写作提供全方位支持**。支持工科、心理学、教育学、管理学等多学科领域，提供符合中国学术规范（GB/T 7714-2015）的论文写作、数据分析、参考文献管理一体化解决方案。当用户需要撰写论文内容、设计论文框架、优化论文章节、处理参考文献格式、进行统计分析、或降低AI生成文本痕迹时使用此技能。

## 核心特性

- 🎯 **学科智能识别**：自动识别学科领域，匹配相应写作规范
- 🇨🇳 **国标合规保障**：严格遵循GB/T 7714-2015参考文献格式
- 🧠 **深度降AI味**：通过"思维过程模拟"等技术，让文本呈现人类学者风格
- 📊 **统计工具集成**：自动生成符合学术规范的统计结果表格
- ✅ **智能质量检查**：多维度检查论文的逻辑、格式、引用质量
- 🔌 **多编辑器兼容**：完美支持 Cline、CodeBuddy、Claude Desktop 等 6+ 主流 AI 编辑器

---

## ⚡ 快速上手（3 步即可使用）

> ✨ 已完美适配主流 AI 编辑器！无论你使用 Cline、CodeBuddy 还是 Claude Desktop，都能即装即用。

### 📦 安装方法

#### 方法一：Cline 用户（推荐）

```bash
# 1️⃣ 克隆或下载本仓库
git clone https://github.com/yanlin-cheng/skill-thesis-writer.git

# 2️⃣ 复制到你的论文项目目录
mkdir -p .cline/skills
cp -r skill-thesis-writer .cline/skills/skill-thesis-writer

# 3️⃣ 重启 Cline，在 Skills 列表中查看是否出现 "skill-thesis-writer"
```

#### 方法二：其他 AI 编辑器用户

| 编辑器 | 安装路径 | 详细说明 |
|-------|---------|---------|
| **Cline** (VS Code) | `.cline/skills/` | 👉 [查看完整指南](.cline/CLINE_INSTALL.md) |
| **CodeBuddy** | `~/.codebuddy/skills/` | UI 导入或手动复制文件夹 |
| **Claude Desktop/Code** | `.claude/skills/` | 复制后重启 Claude |
| **Cursor / Windsurf** | `.cursor/skills/` 或 `.windsurf/skills/` | 同样支持标准格式 |

> 💡 **通用步骤：** 将 `skill-thesis-writer` 文件夹复制到对应编辑器的 `skills` 目录下，重启编辑器即可识别。

---

### 🆘 遇到问题？AI 帮你搞定！

如果按照上述步骤仍然无法导入，别担心！试试这个方法：

1. **将整个 `skill-thesis-writer` 文件夹放到你的项目工作目录中**
2. **打开你的 AI 助手（Cline/CodeBuddy/Claude），输入以下指令：**

```
我有一个论文写作技能文件夹叫 "skill-thesis-writer"，请你：
1. 读取它的 SKILL.md 文件
2. 检查并修复格式问题（如果有的话）
3. 帮我配置为当前可用的 Skill
```

3. **AI 会自动完成所有配置和修复工作！**

> 🤖 这就是 AI 技能的魔力——即使遇到问题，也能用 AI 来解决 AI 的配置问题！

---

## 适用学科

| 学科 | 核心支持 | 特殊规范 |
|------|---------|---------|
| **工科**（计算机/自动化） | 实验设计、消融实验、技术路线图 | 算法伪代码规范、三线表、被动语态≥60% |
| **心理学** | 量表信效度、中介/调节效应、伦理声明 | Cronbach's α报告、Bootstrap检验 |
| **教育学** | 准实验设计、行动研究、问卷设计 | 教育伦理、霍桑效应提示、三角验证 |
| **管理学** | 理论模型、假设验证链、共同方法偏差检验 | CMB检验、SEM分析、简单斜率图 |

## 📂 项目结构（2025-04-13 更新）

> **重要变更**：v1.1 版本已将所有 Python 脚本转换为 **MD 指南文档**，由 AI 智能执行而非机械运行，效果更可靠、更安全。

```
skill-thesis-writer/
├── SKILL.md                          # 核心技能指令（必读）
├── README.md                         # 本文件
├── .cline/                           # Cline 安装指南
│   └── CLINE_INSTALL.md              # Cline 详细安装说明
│
├── references/guides/                # ✨ 核心：AI 指南文档（2025 新增）
│   ├── ai_humanizer_guide.md         # 🔧 AI痕迹消除指南
│   ├── references_formatting_guide.md # 📚 参考文献格式化指南
│   ├── stat_tables_guide.md          # 📊 统计表格生成指南
│   └── quality_checklist_guide.md    # ✅ 论文质量检查清单
│
├── references/                       # 学科写作指南
│   ├── writing_standards.md          # 通用写作规范
│   ├── engineering_guide.md          # 工科写作指南
│   ├── psychology_guide.md           # 心理学写作指南
│   ├── education_guide.md            # 教育学写作指南
│   ├── management_guide.md           # 管理学写作指南
│   └── gbt7714_spec.md               # GB/T 7714格式详解
│
├── scripts/                          # ⚠️ 已弃用（保留供参考，建议使用 guides/ 中的文档）
│   ├── ai_humanizer.py               # （已弃用）→ 请用 ai_humanizer_guide.md
│   ├── format_references.py          # （已弃用）→ 请用 references_formatting_guide.md
│   ├── generate_stat_table.py        # （已弃用）→ 请用 stat_tables_guide.md
│   └── quality_checker.py            # （已弃用）→ 请用 quality_checklist_guide.md
│
└── assets/                           # 模板资源
    └── templates/                    # 论文模板
        ├── engineering_thesis.md     # 工科论文模板
        └── social_science_thesis.md  # 社科论文模板
```

### 🆕 v1.1 更新：从脚本到智能文档

| 变更前 (v1.0) | 变更后 (v1.1) | 为什么更好？ |
|---------------|--------------|-------------|
| Python 脚本机械替换文字 | AI 理解上下文后灵活调整 | 避免语病和机械感 |
| 正则表达式解析参考文献 | AI 逐条检查+智能修正 | 更准确、更安全 |
| 固定模板生成表格 | AI 根据数据定制格式 | 符合具体期刊要求 |
| 自动评分系统 | 分维度详细报告 + 建议 | 建设性反馈 |

**如何使用新的指南文档？**

直接告诉你的 AI 助手：
```
请按照 references/guides/ 中的指南帮助我：
- 降低这段文字的 AI 痕迹 → 用 ai_humanizer_guide.md
- 格式化我的参考文献列表 → 用 references_formatting_guide.md
- 生成统计结果表格 → 用 stat_tables_guide.md
- 全面检查我的论文质量 → 用 quality_checklist_guide.md
```
AI 会自动读取对应指南并按步骤执行！

### 2. 在主流 AI 编辑器中使用

本 SKILL 已按照标准格式设计，支持以下 AI 编辑器：

---

#### 🎯 Cline（VS Code 扩展）

**Cline 是目前最流行的 VS Code AI 助手之一，完美支持 Skills 系统。**

##### 安装方法

**方法 A：项目级安装（推荐用于团队项目）**

```bash
# 在你的项目根目录执行
mkdir -p .cline/skills
cp -r skill-thesis-writer .cline/skills/skill-thesis-writer
```

**目录结构应为：**
```
your-project/
├── .cline/
│   └── skills/
│       └── skill-thesis-writer/    ← 技能文件夹
│           ├── SKILL.md            ← 必需的主文件
│           ├── references/
│           ├── scripts/
│           └── assets/
└── ...其他项目文件
```

**方法 B：全局安装（所有项目可用）**

**Windows (PowerShell):**
```powershell
mkdir $env:USERPROFILE\.cline\skills -Force
Copy-Item -Recurse skill-thesis-writer $env:USERPROFILE\.cline\skills\
```

**macOS/Linux:**
```bash
mkdir -p ~/.cline/skills
cp -r skill-thesis-writer ~/.cline/skills/
```

##### 验证安装

1. 打开 VS Code
2. 启动 Cline 扩展（侧边栏或快捷键）
3. 点击 **⚙️ 设置图标 → Skills**
4. 查看是否显示 "skill-thesis-writer" 技能卡片
5. ✅ 确认技能开关已启用（蓝色状态）

##### 使用方式

安装成功后，当你在 Cline 对话框中输入以下类型的问题时，技能会**自动激活**：

| 触发场景 | 示例问题 |
|---------|---------|
| 📝 **论文撰写** | "帮我写一篇关于深度学习的论文开题报告" |
| 🔧 **框架设计** | "设计一下心理学实验的论文框架" |
| ✍️ **文本优化** | "优化这段学术文字，降低AI痕迹" |
| 📚 **参考文献** | "把这些文献按 GB/T 7714 格式化" |
| 📊 **统计分析** | "生成一个回归分析结果表格" |
| 🔍 **质量检查** | "检查这篇论文有没有逻辑问题" |

**详细说明请查看 [`.cline/CLINE_INSTALL.md`](.cline/CLINE_INSTALL.md)**

---

#### 💻 CodeBuddy（IDE 插件）

CodeBuddy 原生支持 SKILL 格式。

##### 安装方法

**全局安装（推荐）：**
```bash
# 将整个项目复制到 CodeBuddy 的 skills 目录
# 路径通常为 ~/.codebuddy/skills/ 或通过 CodeBuddy 设置界面导入
cp -r skill-thesis-writer ~/.codebuddy/skills/
```

**或通过 CodeBuddy UI 导入：**
1. 打开 CodeBuddy 设置面板
2. 选择 "Skills" 或 "自定义技能"
3. 点击 "添加技能"
4. 选择 `skill-thesis-writer` 文件夹
5. 确认导入

##### 使用方式

- 技能会自动根据 description 字段触发
- 也可以在对话中手动提及："使用 thesis-writer 技能"

---

#### 🤖 Claude Desktop / Claude Code

Claude 支持标准 SKILL.md 格式。

##### 安装方法

**项目级安装：**
```bash
mkdir -p .claude/skills
ln -s ../skill-thesis-writer .claude/skills/skill-thesis-writer
# Windows: mklink /D .claude\skills\skill-thesis-writer skill-thesis-writer
```

**或全局安装（macOS/Linux）：**
```bash
mkdir -p ~/.claude/skills
cp -r skill-thesis-writer ~/.claude/skills/
```

##### 配置 Claude Desktop

在 `~/.claude/config.json` 或项目的 `.claude/settings.json` 中添加：

```json
{
  "skills": [
    ".claude/skills/skill-thesis-writer"
  ]
}
```

---

#### 📋 其他兼容编辑器

以下编辑器也支持标准 SKILL 格式：

| 编辑器 | 安装路径 | 说明 |
|-------|---------|------|
| **Cursor** | `.cursor/skills/` | 与 Cline 类似的结构 |
| **Windsurf** | `.windsurf/skills/` | 支持 YAML frontmatter |
| **Continue** | `.continue/skills/` | 开源 AI 编程助手 |
| **Aider** | `.aider/skills/` | 终端 AI 助手 |

通用安装命令：
```bash
mkdir -p .<editor-name>/skills
cp -r skill-thesis-writer .<editor-name>/skills/skill-thesis-writer
```

---

### 3. 使用指南文档

> ⚠️ **注意**：原 Python 脚本已弃用，请改用 MD 指南文档。让 AI 助手读取对应指南并智能执行即可。

| 任务 | 使用文档 | 示例指令 |
|------|---------|---------|
| 降低AI痕迹 | `guides/ai_humanizer_guide.md` | "请按 ai_humanizer_guide.md 帮我优化这段文字" |
| 格式化参考文献 | `guides/references_formatting_guide.md` | "请按 GB/T 7714 规范格式化我的参考文献列表" |
| 生成统计表格 | `guides/stat_tables_guide.md` | "帮我生成一个描述性统计表（M±SD格式）" |
| 全面质量检查 | `guides/quality_checklist_guide.md` | "请按清单逐项检查我的论文质量" |

只需将上述示例指令发给你的 AI 助手，它会自动读取对应指南并按步骤执行！

## 核心功能详解

### 1. 降AI味技术

**检测指标**：
- 句子长度变异系数（CV < 0.3提示风险）
- 连接词密度（> 5%提示过度使用）
- 被动语态比例（学科特定阈值）

**处理策略**：
1. **连接词替换**："此外"→"无独有偶"、"值得注意的是"等
2. **句式节奏调整**：长短句交错，避免均匀句式
3. **限定词添加**："一定程度上"、"初步看来"等谨慎表述
4. **批判性注入**：添加研究局限、反向论证
5. **学科适配**：工科被动语态≥60%，社科适度使用"笔者认为"

**使用示例**：
```python
from scripts.ai_humanizer import AIHumanizer

humanizer = AIHumanizer(discipline="心理学")
result = humanizer.detect(text)  # 检测AI痕迹
optimized = humanizer.humanize(text, aggressive=True)  # 降AI味处理
```

### 2. 参考文献管理

**功能**：
- 自动格式化为GB/T 7714-2015格式
- 去重检测（相似度>85%触发警告）
- 年代分析（工科近5年≥40%，社科≥30%）
- 学科合规性检查

**支持文献类型**：
- 期刊论文[J]
- 专著[M]
- 学位论文[D]
- 会议论文[C]
- 电子文献[EB/OL]

### 3. 统计表格生成

**支持表格类型**：
- 描述性统计表（M±SD、偏度、峰度）
- 相关分析矩阵（Pearson/Spearman，**标注显著性）
- 回归分析表（多层模型、ΔR²）
- 方差分析表（F值、偏η²）
- 中介效应表（Bootstrap检验、效应占比）

### 4. 质量检查

**检查维度**：
- **结构完整性**：标题、摘要、章节、结论闭环
- **逻辑一致性**：假设-方法-结果对应关系
- **引用质量**：格式统一性、重复检测
- **写作风格**：口语化、绝对化、长句检测
- **格式规范**：图表编号、标点符号

## 学科写作指南速查

### 工科类要点

```yaml
必备章节:
  - 绪论（研究背景、问题提出、创新点）
  - 相关工作（技术路线对比）
  - 方法论（算法原理、伪代码）
  - 实验设计（数据集、评价指标、消融实验）
  - 结果分析（定量+定性）
  - 结论与展望

图表规范:
  - 流程图: 遵循ANSI标准
  - 架构图: 输入→处理→输出清晰标注
  - 表格: 三线表

常见陷阱:
  - ⚠️ 仅用准确率评价模型（需补充F1、AUC等）
  - ⚠️ 缺乏消融实验
  - ⚠️ 未提供代码/数据可复现性说明
```

### 心理学类要点

```yaml
必备章节:
  - 引言（理论背景、研究假设）
  - 文献综述（理论演进脉络）
  - 研究方法（被试、材料、程序）
  - 结果（预注册分析计划优先）
  - 讨论（理论贡献与实践意义）

特殊要求:
  - 伦理声明: 知情同意、伦理审查编号
  - 量表报告: Cronbach's α ≥ 0.70
  - 效应量: 必须报告Cohen's d或η²

常见陷阱:
  - ⚠️ 量表来源未标注
  - ⚠️ 信效度检验缺失
  - ⚠️ 忽视霍桑效应
```

### 管理学类要点

```yaml
必备章节:
  - 引言（管理实践问题）
  - 理论模型（概念模型图）
  - 研究假设（H1a、H1b...清晰标注）
  - 方法论（问卷设计、抽样策略）
  - 数据分析（CMB检验→假设验证）

特殊要求:
  - 共同方法偏差: Harman单因子检验/ULMC
  - 中介/调节: Bootstrap法、简单斜率图
  - 控制变量: 年龄、性别、行业等

常见陷阱:
  - ⚠️ 共同方法偏差未检验
  - ⚠️ 量表来源混乱
  - ⚠️ 理论贡献提炼不足
```

## 写作流程建议

### 阶段一：框架构建（Interaction Phase）

1. **深度需求探询**：回答AI提出的3-5个细化问题
2. **学科匹配**：自动匹配对应学科指南
3. **大纲生成**：获取结构化论文大纲

### 阶段二：内容生成（Generation Phase）

1. **分章生成**：按大纲逐章生成内容
2. **批判性注入**：自动添加对比分析、研究缺口
3. **学科适配**：应用学科特异性表达

### 阶段三：质量优化（Quality Phase）

1. **降AI味处理**：应用ai_humanizer优化文本
2. **质量检查**：运行quality_checker检测问题
3. **格式规范化**：使用format_references格式化引用

### 阶段四：最终完善（Finalization Phase）

1. **统计表格生成**：使用generate_stat_table生成表格
2. **全文审阅**：人工审核关键论点
3. **查重检测**：使用专业查重工具

## 示例演示

### 示例1：工科论文实验设计

**输入**：我正在写一篇关于CNN图像识别的论文，需要设计实验部分

**AI响应**：
```
📚 学科识别：计算机/人工智能（工科）

🔍 为了设计符合规范的实验章节，请回答：
1. 您使用的具体CNN架构？（ResNet/YOLO/自定义）
2. 数据集来源与规模？（如ImageNet子集，共多少张图）
3. 评价指标？（准确率/精确率/召回率/F1/mAP）
4. 是否有对比算法？（传统方法/SOTA方法）
5. 是否做消融实验？（验证各模块贡献）

[用户回答后生成结构化的实验设计章节]
```

### 示例2：心理学量表信效度报告

**输入**：我的问卷有15个题项，Cronbach α=0.82，这样写可以吗？

**AI响应**：
```
📚 学科识别：心理学/问卷研究

✅ 信度良好（α=0.82 > 0.70阈值）

⚠️ 但规范报告应包含：
1. 量表来源：改编自XXX（年份）编制的XXX量表
2. 信度细节：各维度的α值（如适用）
3. 效度检验：探索性/验证性因子分析结果
4. 题项示例：至少展示2-3个代表性题项

建议表述模板：
"本研究采用XXX量表测量XXX，该量表由XXX（年份）编制，
共X个题项，采用Likert X点计分。经检验，量表Cronbach's 
α系数为0.82，表明信度良好。验证性因子分析结果显示，
模型拟合指标为：χ²/df=X.XX，CFI=X.XX，RMSEA=X.XX，
表明量表结构效度可接受。"
```

### 示例3：管理学共同方法偏差检验

**输入**：我的调节效应分析做完了，需要加共同方法偏差检验吗？

**AI响应**：
```
📚 学科识别：管理学/组织行为

✅ 必须添加！单一来源问卷调查的常见要求

🔧 检验流程：
1. Harman单因子检验（探索性因子分析）
   - 未旋转因子分析，第一因子解释率<40%
   
2. 或：ULMC（未测单一方法潜变量）
   - 比较含/不含方法因子的模型拟合差异

3. 在正文中明确报告：
   "由于本研究数据均来自被试自我报告，可能存在共同方法偏差。
   采用Harman单因子检验，结果显示第一因子解释率为XX%(<40%)，
   表明共同方法偏差问题不严重。"
```

## 更新日志

### v1.1 (2026-04-13) — 重构：从脚本到智能文档
- ✅ 将所有 Python 脚本转换为 **MD 指南文档**（`references/guides/`）
- 📝 新增 4 份完整指南：AI 痕迹消除 / 参考文献格式化 / 统计表格 / 质量检查
- 🔧 标记 `scripts/` 为已弃用，由 AI 智能执行替代机械运行
- 🐛 修复 Cline 兼容性问题，优化 YAML frontmatter
- 📖 完善多编辑器安装说明（Cline/CodeBuddy/Claude/Cursor/Windsurf）

### v1.0 (2025-02-04)
- 初始版本发布
- 支持工科、心理学、教育学、管理学四个学科
- 实现AI痕迹检测与消除核心功能
- 集成GB/T 7714-2015参考文献格式化
- 提供统计表格自动生成
- 实现多维度论文质量检查

## 贡献与反馈

欢迎提出改进建议！您可以通过以下方式参与：
- 报告问题：描述具体的错误或不足
- 功能建议：提出新的功能需求
- 学科扩展：提供其他学科的写作规范

## 许可

本SKILL仅供学术研究与学习使用。

---

**作者**：AI论文写作助手团队
**版本**：v1.1
**更新日期**：2026年4月13日
