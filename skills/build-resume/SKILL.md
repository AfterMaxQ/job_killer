---
name: build-resume
description: Build truthful, evidence-grounded, job-targeted resumes from a candidate's Markdown profile and a job description, then compile them to PDF. Use when the user wants to create, tailor, revise, compare, or compile a resume/CV for a specific role, provides a JD for resume matching, or asks to turn their candidate profile into a job-specific resume.
---

# Build Resume

## Purpose

生成**真实、可追溯、针对当前 JD** 的简历。Agent 先理解岗位和候选人 Evidence，再决定内容与表达；Markdown 是候选人档案和每份 JD 中间决策的 Source of Truth，LaTeX/PDF 是最终呈现层。

## Inputs

- `个人信息/` 中的人类可编辑 Markdown 档案；
- 当前 JD；
- 可选：`个人信息/求职方向/目标方向.md`；
- 可选：当前岗位已有 `temp_resume/<任务目录>/`；
- 可选：`images/you.jpg`。

如果 `个人信息/` 不存在或缺少完成任务所需事实，按需使用 `init-personal-info` 补充真实信息。

## Core Rules

1. **Never fabricate candidate facts.** 经历、技能、指标、环境、角色和成果必须来自候选人档案或用户明确确认。
2. **Evidence Strength 与 JD 重要度分离。** 岗位越需要某能力，不代表候选人证据越强。
3. **不写 unsupported claims。** `UNSUPPORTED` 必须删除；`NEEDS_CONFIRMATION` 未确认不得进入正式简历。
4. **真实量化优先，不强制量化。** 没有真实数字时允许使用规模、交付状态或定性成果。
5. **Skills communicate capability.** 技能区默认表达能力主题、关键词/方法和证据信号，不做技术名词仓库。
6. **STAR 只做分析。** 最终 Bullet 不机械套完整 STAR。
7. **运行时建模。** 不依赖固定“后端/前端/算法/测试”等岗位分类；根据当前 JD + Evidence 动态生成能力维度。
8. **保留可审查中间文件。** Job Model、匹配、Positioning 和 Claim Audit 不只存在于临时推理中。

## Task Directory

每个目标 JD 建立独立目录：

```text
temp_resume/<公司>-<岗位>/
├── job-model.md
├── match-matrix.md
├── positioning.md
├── resume.md
└── claim-audit.md
```

命名规则：

- 公司和岗位都已知：`<公司>-<岗位>`；
- 公司未知：使用用户提供的可辨识岗位名称；
- 岗位未知：使用用户提供的可辨识任务名称；
- 不得为了目录好看凭空补公司名、团队名或岗位名。

已有任务目录时优先读取并延续，不无故重建。

## Interaction Modes

### ① 细致模式

适合首次投递或需要精细打磨。

只在会改变简历决策的节点确认：

- Job Model；
- Candidate Positioning；
- 关键事实缺口；
- `NEEDS_CONFIRMATION` Claim；
- 最终 `resume.md`。

不要逐模块反复询问“写 2 条还是 3 条”“日期放哪”“技能几个词”等可由 Agent 自主决定的排版细节。

### ② 宏观模式

确认：

```text
Job Model + Positioning
```

之后 Agent 自主完成匹配、内容选择、写作、审计和排版；最终展示简历。

### ③ 全自动模式

不主动提问。

- 信息不足：使用当前可确认事实；
- 弱 Evidence：按真实强度表达；
- `NEEDS_CONFIRMATION`：弱化或删除；
- `UNSUPPORTED`：删除；
- PDF 构建失败：保留全部 Markdown 中间结果并报告失败原因。

## Workflow

按顺序执行。

### 1. Detect Context

检查：

- `个人信息/`；
- `个人信息/求职方向/目标方向.md`；
- 当前任务目录；
- 当前任务是否已有 `resume.md` / `claim-audit.md`；
- `images/you.jpg`；
- `xelatex --version`。

如果用户只是修改已生成简历，不必重做与修改无关的分析；但任何新增 Claim 仍需 Evidence 和 Claim Audit。

### 2. Gather Candidate Evidence

读取候选人当前任务需要的 Markdown。

先读概要与索引，再按 Job Model 需要读取具体经历，避免把全部档案无差别塞进上下文。

Evidence 规则：

```text
Read references/evidence-model.md
```

### 3. Model Job

在写任何简历正文前：

```text
Read references/job-modeling.md
```

生成：

```text
<task-dir>/job-model.md
```

必须区分 JD 明确要求和 Agent 推断。

### 4. Match Evidence

读取：

```text
references/matching-positioning.md
```

生成：

```text
<task-dir>/match-matrix.md
```

固定字段：

```text
能力 | JD重要度 | 最强证据 | 证据强度 | 策略
```

### 5. Define Positioning

继续按 `references/matching-positioning.md` 生成：

```text
<task-dir>/positioning.md
```

至少包含：Target Identity、Top Signals、Supporting Signals、Weaknesses、Strategy、Resume Story。

### 6. Select Content

以以下语义框架选择内容：

```text
岗位重要度 × 证据强度 × 差异化价值 × 篇幅成本
```

不是数学乘法；用于决定：

- 哪段工作 / 项目进入简历；
- 哪些只保留一句；
- 哪些删除；
- 模块顺序；
- 技能区使用哪种策略。

### 7. Write Resume

读取：

```text
references/writing-standards.md
```

如果简历包含“专业技能 / 核心能力”模块，再读取：

```text
references/skills-section.md
```

需要更多表达参考时才读取：

```text
references/resume-examples.md
```

生成：

```text
<task-dir>/resume.md
```

示例只能学习原则，不能复制示例人物、数字、技术栈或固定句式。

### 8. Audit Claims

生成：

```text
<task-dir>/claim-audit.md
```

对高价值 Claim 使用四类：

```text
FACT
DERIVED
NEEDS_CONFIRMATION
UNSUPPORTED
```

#### FACT

候选人档案或用户明确提供的事实。

#### DERIVED

由多个真实事实合理总结，且没有提高事实强度。

#### NEEDS_CONFIRMATION

有合理线索，但现有证据不足以安全写入正式简历。

#### UNSUPPORTED

没有足够证据支持。

每个高风险 Claim 推荐记录：

```markdown
## C1

### 简历表述

...

### 证据

...

### 判断

FACT / DERIVED / NEEDS_CONFIRMATION / UNSUPPORTED

### 处理

保留 / 弱化 / 已确认 / 删除
```

最终交付前：

- 不得残留未处理 `UNSUPPORTED`；
- `NEEDS_CONFIRMATION` 未确认不得进入正式简历。

### 9. Validate Structure

读取：

```text
references/validation-rules.md
```

运行：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "<task-dir>"
```

仓库直接执行 Skill 源文件时，使用相应实际安装路径。

Validator 只负责确定性机械检查；语义真实性仍由 Agent 的 Evidence / Content Validation 负责。

### 10. Build PDF

读取：

```text
references/latex-reference.md
```

以当前任务目录的：

```text
resume.md
```

作为唯一简历内容来源，按启用模块组装根目录 `resume.tex`。

模板仍使用现有：

```text
template/
```

然后运行：

```bash
bash .claude/skills/build-resume/shell/build.sh
```

不要为了新工作流重写现有 LaTeX 构建脚本，除非脚本本身实际失败且原因与路径强耦合。

### 11. Verify PDF

再次运行 validator：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "<task-dir>" --pdf resume.pdf
```

并人工 / Agent 检查：

- PDF 可打开；
- 没有明显文本溢出；
- 没有空模块；
- 没有异常换行；
- 页面策略合理；
- 根目录没有不应残留的 LaTeX 临时文件。

### 12. Deliver

至少交付：

- `<task-dir>/resume.md`；
- `resume.pdf`（构建成功时）。

同时保留：

- `job-model.md`；
- `match-matrix.md`；
- `positioning.md`；
- `claim-audit.md`。

用户询问“为什么这样写”时，直接基于这些可审查文件解释。

## Resource Routing

| 阶段 | 读取 |
|---|---|
| Evidence | `references/evidence-model.md` |
| Job Modeling | `references/job-modeling.md` |
| Matching / Positioning | `references/matching-positioning.md` |
| Writing | `references/writing-standards.md` |
| Skills/Core Capabilities | `references/skills-section.md`，仅使用技能区时 |
| Examples | `references/resume-examples.md`，仅需要参考时 |
| LaTeX | `references/latex-reference.md` |
| Validation | `references/validation-rules.md` |
| 常见错误 | `references/common-errors.md`，需要排查时 |

所有 reference 由 `SKILL.md` 直接指向，避免形成深层 reference → reference 链。

## Decision Rules

### 技能区

默认优先 Capability-first；ATS 工具要求密集时可 Keyword-dense；工作经历已经足够强时可 Minimal。不得固定套一个分类。

### 数字

有真实数字就用；没有就使用规模、交付状态或定性成果。不得估算“看起来合理”的数字。

### 页面

学生 / 实习简历默认尽量单页，但不以删除核心 Evidence 或增加无价值内容为代价。

### 缺失能力

Evidence = 0：不写。Evidence 较弱：只按真实强度写，不因 JD 需要而升级。

## Failure Handling

### JD 信息不足

只建立能确认的 Job Model；低置信度内容标 `[推断]`。不伪造公司要求。

### 候选人证据不足

细致模式可以询问真实经历；宏观 / 全自动模式弱化或删除对应能力。

### Validator 失败

逐项修复错误后重跑，不跳过失败继续交付。

### PDF 编译失败

保留任务目录全部 Markdown，报告构建错误；不要删除有效分析成果，也不要声称 PDF 已成功。

## Validation

交付前必须同时通过：

1. **Evidence Validation**：Claim 可追溯、Evidence Strength 未被夸大；
2. **Content Validation**：Positioning 清晰、最强证据获得主要篇幅、技能区不是名词仓库；
3. **Mechanical / Rendering Validation**：运行 validator 并检查 PDF。

任何一层失败，都不能把当前结果标记为最终完成。