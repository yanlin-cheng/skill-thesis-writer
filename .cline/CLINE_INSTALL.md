# Cline 技能安装指南

本文件说明如何将 thesis-writer 技能安装到 Cline 中。

## 安装方法

### 方法一：项目级安装（推荐）

将 `skill-thesis-writer` 文件夹复制到项目的 `.cline/skills/` 目录下：

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
│       └── skill-thesis-writer/    # ← 技能文件夹（名称必须与 SKILL.md 中的 name 一致）
│           ├── SKILL.md            # ← 必需的主文件
│           ├── references/         # 可选的参考文档
│           ├── scripts/            # 可选的工具脚本
│           └── assets/             # 可选的资源文件
└── ...其他项目文件
```

### 方法二：全局安装（所有项目可用）

将技能复制到用户主目录下的 `.cline/skills/` 文件夹：

**Windows:**
```powershell
mkdir -p $env:USERPROFILE\.cline\skills
Copy-Item -Recurse skill-thesis-writer $env:USERPROFILE\.cline\skills\
```

**macOS/Linux:**
```bash
mkdir -p ~/.cline/skills
cp -r skill-thesis-writer ~/.cline/skills/
```

## 验证安装

1. 打开 VS Code
2. 启动 Cline 扩展
3. 点击设置图标 → Skills
4. 查看是否显示 "skill-thesis-writer" 技能
5. 确认技能开关已启用

## 使用方法

安装成功后，当你在 Cline 中提出以下类型的问题时，该技能会自动激活：

✅ **论文撰写类请求：**
- "帮我写一篇关于XXX的论文"
- "设计一下论文框架"
- "优化这段学术文字"

✅ **格式规范类请求：**
- "参考文献格式化"
- "检查是否符合GB/T 7714-2015"
- "生成统计表格"

✅ **降AI痕迹类请求：**
- "降低AI味"
- "让文本更自然"
- "改成人类学者风格"

## 常见问题

### Q1: 安装后技能没有出现在列表中？
**A:** 请确认：
1. 文件夹名称是否为 `skill-thesis-writer`（与 SKILL.md 中 name 字段完全一致）
2. SKILL.md 是否在文件夹根目录
3. YAML frontmatter 格式是否正确（以 `---` 开头和结尾）

### Q2: 技能出现了但不自动触发？
**A:** 
- 确认技能开关已打开（启用状态）
- 检查 description 中的关键词是否匹配你的问题
- 尝试重启 Cline

### Q3: 如何更新技能？
**A:** 直接替换 `.cline/skills/skill-thesis-writer/SKILL.md` 文件即可，Cline 会自动重新加载。

---

**注意：** 当全局技能和项目级技能同名时，全局技能优先。建议团队协作时使用项目级安装。
