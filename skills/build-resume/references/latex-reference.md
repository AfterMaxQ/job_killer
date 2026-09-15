# LaTeX 格式与排版参考

本文件只负责把当前任务目录中的 `resume.md` 转换为现有 LaTeX 模板能够编译的 `resume.tex`。内容选择和事实判断在此之前已经完成，不在 LaTeX 阶段重新改写候选人事实。

## 输入

当前任务目录：

```text
temp_resume/<公司>-<岗位>/
└── resume.md
```

只使用该 `resume.md` 作为本次简历正文来源，不从其它旧 Markdown 自动拼接内容。

## 模板顺序

根据 `resume.md` 实际存在的模块，按合理顺序组装现有模板：

```text
header
education
skills
internship
projects
studentwork
selfeval
footer
```

模块不存在时跳过对应模板，不保留空标题。

模块顺序可以根据 Positioning 调整；上面只是模板可用列表，不是内容策略的固定顺序。

## 模板目录

安装后的默认路径：

```text
.claude/skills/build-resume/template/
```

仓库源码中对应：

```text
skills/build-resume/template/
```

现有 `shell/build.sh` 仍负责 XeLaTeX 编译和模板 `.cls/.sty` 的临时复制/清理。

## 个人信息

没有的字段直接删除，不输出空行。

虚构示例：

```latex
\SimpleEntry{\makebox[11em][l]{\prefix{电话：}138-0000-0000}\prefix{邮箱：}candidate@example.com}
\SimpleEntry{\makebox[11em][l]{\prefix{所在地：}杭州}\prefix{作品集：}\href{https://portfolio.example.com/demo}{portfolio.example.com/demo}}
```

示例中的姓名、电话、邮箱、地址和链接均为虚构，仅用于说明格式，绝不能复制到真实简历。

## 日期与标题

日期默认可使用：

```latex
\datedsubsection{项目名称｜角色}{2026.03--2026.06}
```

如果当前模板支持其它日期布局，可以根据页面需要调整，但不要在排版阶段改变真实时间。

## Content Bullet

最终 Bullet 来自 `resume.md`，不要求固定 2 条或 3 条。

根据实际条数选择模板现有宏，或按模板允许的方式连续输出：

```latex
\Content{...}{...}{...}
```

如果项目只需要两条，不要为了填满宏而制造第三条内容；应使用现有两条布局能力或合理组装。

## 技能 / 核心能力

技能区应忠实保留 `resume.md` 中已经确定的动态能力簇，例如：

```text
数据分析：SQL、Python、Excel；完成过从数据清洗到业务汇报的完整任务
```

不要在 LaTeX 阶段重新改回固定“后端 / 前端 / 数据库 / DevOps”分类。

分类前缀可继续使用：

```latex
\prefix{数据分析：}
```

正文不要因为排版需要改变 Evidence 强度。

## 常用格式规则

- 模块标题、项目名可以使用模板既有的强调样式；
- 分类前缀统一使用 `\prefix{}`；
- 普通正文避免过度 `\textbf{}`；
- 连续独立文本块之间按模板需要使用 `\par`，避免连行；
- 对 LaTeX 特殊字符做必要转义：`& % $ # _ { } ~ ^ \\`；
- URL 使用 `\href{}`，显示文本保持简短；
- 技术名词过长导致断行时可使用模板现有处理方式，但不要通过删除真实关键信息解决排版问题。

## 照片

只有 `images/you.jpg` 存在且用户当前简历策略允许照片时才启用照片宏。

照片尺寸属于排版决策，不要求固定在 0.12 / 0.14 / 0.16 三个值中；优先保证版面平衡。

## 页面策略

学生 / 实习简历可以以单页为默认目标。

超页时按内容优先级处理：

1. 删除弱相关内容；
2. 合并重复表达；
3. 缩短次要项目；
4. 使用 Minimal 技能区；
5. 最后才调整行距或其它版式参数。

不得为了单页删除 Job Model 的核心 Evidence。

不足一页时不要为了填满页面增加无关经历或空泛自评。

## 组装与构建

1. 读取当前任务目录 `resume.md`；
2. 读取需要的模板文件；
3. 用真实内容替换模板占位符；
4. 写根目录 `resume.tex`；
5. 运行：

```bash
bash .claude/skills/build-resume/shell/build.sh
```

6. 构建成功后运行 validator：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "<task-dir>" --pdf resume.pdf
```

## Failure Handling

- LaTeX 编译失败：保留 `resume.md` 和全部分析文件，展示编译错误，不声称完成；
- 特殊字符导致失败：只修正转义，不改候选人事实；
- 内容超页：返回内容选择阶段压缩弱相关信息，不擅自删核心 Evidence；
- 模板无法表达某模块：优先用现有模板的通用布局，不为了模板限制改变模块语义。

## Validation

- [ ] `resume.tex` 内容来自当前任务目录的 `resume.md`；
- [ ] 没有空模块；
- [ ] 没有真实个人信息示例残留在 reference；
- [ ] 技能区保留动态能力簇；
- [ ] 日期、数字、岗位、公司等事实没有被排版阶段修改；
- [ ] PDF 构建状态与实际一致；
- [ ] `.aux/.log/.out` 等临时文件按现有清理流程处理。