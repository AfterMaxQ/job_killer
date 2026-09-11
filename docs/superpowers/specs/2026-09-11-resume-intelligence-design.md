# Job Killer 智能简历生成设计规范

## 1. 目标

`build-resume` 的目标不是单纯把 JD 关键词改写进简历，而是建立一条可审查、可泛化、证据驱动的简历生成链路：

```text
候选人事实
    ↓
候选人证据
    ↓
岗位模型
    ↓
岗位要求 × 候选人证据
    ↓
候选人定位
    ↓
内容选择
    ↓
简历写作
    ↓
Claim Audit
    ↓
格式与渲染验证
    ↓
PDF
```

Agent 必须能够回答：

- 招聘方真正想找什么能力；
- 候选人的哪些事实能够证明这些能力；
- 哪些经历值得写、哪些应该弱化或删除；
- 哪些能力只是接触或学习，不能包装成实战能力；
- 这份简历希望招聘者最终记住候选人的什么特点。

所有候选人档案、证据、岗位分析和中间决策继续使用 Markdown 保存，确保人类可以直接阅读、编辑、审查和通过 Git 管理。

所有示例必须使用完全虚构的人物、学校、企业、项目和数据，不得包含真实用户或仓库维护者的个人信息。

---

## 2. Skill 设计原则

### 2.1 Markdown 是候选人数据的 Source of Truth

候选人的以下信息均使用普通 Markdown 保存：

- 基本信息；
- 教育背景；
- 工作经历；
- 项目经历；
- 比赛经历；
- 技能与能力；
- 求职方向；
- 能力证据。

Markdown 可以采用稳定标题结构以方便 Agent 解析，但不能退化成只有机器易读、人类难编辑的数据格式。

不使用 JSON、数据库或复杂 Schema 作为候选人档案的主要存储形式。

### 2.2 Skill 是稳定 SOP，领域与用户信息属于运行时数据

`SKILL.md`、`references/`、`scripts/` 描述的是 Agent 如何完成任务。

候选人的行业、目标岗位、个人经历和求职偏好属于运行时数据，不通过修改 Skill 文件完成领域适配。

`first-start` 只负责建立或更新 Markdown 求职画像，例如：

```text
个人信息/
└── 求职方向/
    └── 目标方向.md
```

Agent 每次生成简历时根据：

```text
候选人档案
+
求职方向
+
当前 JD
```

实时构建岗位模型，而不是依赖写死的岗位分类。

### 2.3 Progressive Disclosure

遵循 Anthropic Agent Skills 的渐进式披露设计：

```text
Frontmatter
    ↓
SKILL.md
    ↓
references / scripts / assets
```

职责约束：

- `description`：说明 Skill 做什么以及什么时候触发；
- `SKILL.md`：只保留核心 Workflow、Decision Rules、Constraints、Resource Routing、Validation、Failure Handling；
- `references/`：存放详细领域规则、写作规范、示例与长篇说明；
- `scripts/`：执行确定性验证、文件处理、编译和清理；
- `assets/`：保存模板和静态资源。

`SKILL.md` 不承载大段示例、固定岗位分类和大量 LaTeX 细节。

---

## 3. 目标目录结构

```text
skills/
└── build-resume/
    ├── SKILL.md
    │
    ├── references/
    │   ├── job-modeling.md
    │   ├── evidence-model.md
    │   ├── matching-positioning.md
    │   ├── writing-standards.md
    │   ├── skills-section.md
    │   ├── resume-examples.md
    │   ├── latex-reference.md
    │   └── validation-rules.md
    │
    ├── scripts/
    │   └── validate-resume.py
    │
    ├── shell/
    │   ├── build.sh
    │   ├── clean.sh
    │   └── install-packages.sh
    │
    └── template/
        ├── header.tex
        ├── education.tex
        ├── skills.tex
        ├── internship.tex
        ├── projects.tex
        ├── studentwork.tex
        ├── selfeval.tex
        ├── footer.tex
        ├── resume.cls
        ├── zh_CN-Adobefonts_external.sty
        └── linespacing_fix.sty
```

现有 `shell/` 与 `template/` 可以继续作为确定性执行和模板目录，不要求为了目录命名而进行无价值重构。

---

## 4. 候选人 Markdown 档案

建议使用以下结构：

```text
个人信息/
├── 基本信息.md
├── 教育背景.md
├── 技能能力.md
│
├── 求职方向/
│   └── 目标方向.md
│
├── 工作经历/
│   ├── 经历-A.md
│   └── 经历-B.md
│
├── 项目经历/
│   ├── 项目-A.md
│   └── 项目-B.md
│
├── 比赛经历/
│   └── 比赛-A.md
│
└── 证据索引.md
```

每段工作或项目经历既保存自然语言事实，也允许保存结构化的 Evidence Unit。

---

## 5. Evidence Unit

### 5.1 目的

经历本身回答：

> 做过什么？

Evidence Unit 回答：

> 这件事能够证明什么？

以及：

> 这件事不能证明什么？

### 5.2 推荐 Markdown 格式

```markdown
# 某项目

## 基本信息

- 时间：
- 角色：
- 类型：

## 项目背景

自然语言描述项目背景。

## 实际工作

- ...
- ...
- ...

## 实际成果

- ...
- ...

## 使用技术

- ...
- ...

# 能力证据

## E1｜某项能力

### 事实

真实发生了什么。

### 可以证明

- 能力 A
- 能力 B

### 证据强度

4 / 5

### 适合支持

- 某类岗位
- 某类职责

### 表达边界

不能从这段经历推导出的能力或成果。
```

### 5.3 Evidence Strength

采用 0–5 级简单语义：

| 等级 | 含义 |
|---|---|
| 0 | 没有证据 |
| 1 | 了解 / 接触 |
| 2 | 课程 / 学习 / 简单实验 |
| 3 | 项目中实际使用 |
| 4 | 独立或核心完成 |
| 5 | 真实业务 / 生产环境 / 有明确结果 |

证据强度只用于 Agent 决策，不直接映射成“精通”“熟练掌握”等简历措辞。

JD 对某项能力要求很高，也不能反向提升候选人的 Evidence Strength。

---

## 6. 证据索引

`个人信息/证据索引.md` 用于跨经历快速浏览，不作为唯一事实来源。

示例：

```markdown
# 能力证据索引

## 后端工程

- 项目 A / E2
- 工作经历 B / E1

## 数据分析

- 项目 C / E1
- 比赛 A / E3

## 自动化

- 工作经历 A / E4
```

具体项目和经历文件仍然是最终事实来源。

---

## 7. 每份 JD 的可审查中间文件

针对某个岗位生成简历时建立独立目录：

```text
temp_resume/
└── <公司>-<岗位>/
    ├── job-model.md
    ├── match-matrix.md
    ├── positioning.md
    ├── resume.md
    └── claim-audit.md
```

所有中间结果都使用 Markdown，方便用户检查 Agent 的关键决策。

---

## 8. Job Model

Agent 读取 JD 后不得立即开始写简历，必须先形成 `job-model.md`。

推荐结构：

```markdown
# 岗位模型

## 岗位基本信息

- 岗位：
- 团队：
- 职级：
- 主要领域：

## 招聘目标

一句话描述招聘方真正希望招到什么类型的人。

## 核心能力

### P0｜核心能力

- 能力：
- JD 证据：
- 重要度：

### P1｜重要能力

...

## 门槛条件

- 学历
- 工作年限
- 必备资格
- 地域
- 语言

## 强信号

出现这些经历会显著提升匹配度。

## 加分项

有最好，没有也不影响基本资格。

## 隐含需求

明确区分：

- JD 明确要求；
- Agent 合理推断。

## 岗位核心命题

招聘方实际上在购买什么能力？
```

### 8.1 Job Model 禁止行为

不得：

- 看见一个技术关键词就判断为岗位核心；
- 把所有 JD 要求赋予相同重要度；
- 根据职位名称套固定职业模板；
- 因为候选人擅长某项技术，反向高估该能力在 JD 中的重要性。

---

## 9. Requirement × Evidence Matrix

完成岗位模型后，读取候选人相关 Evidence，生成 `match-matrix.md`。

示例：

```markdown
# 岗位能力 × 候选人证据

| 能力 | JD重要度 | 最强证据 | 证据强度 | 策略 |
|---|---:|---|---:|---|
| API工程 | 5 | 项目A/E2 | 5 | 强调 |
| 数据库 | 4 | 工作B/E1 | 4 | 强调 |
| 云平台 | 4 | 项目C/E3 | 2 | 谨慎 |
| 高并发 | 3 | 无明确证据 | 0 | 不写 |
| 英语沟通 | 2 | 语言能力 | 4 | 简写 |
```

`策略` 可使用：

- 核心卖点；
- 强调；
- 正常展示；
- 弱化；
- 谨慎；
- 不写；
- 需要用户确认。

---

## 10. Candidate Positioning

真正选择简历内容之前生成 `positioning.md`。

推荐结构：

```markdown
# 本次简历定位

## Target Identity

希望招聘方在快速扫读后记住候选人是什么样的人。

## Top Signals

最值得展示的 3–4 个信号。

## Supporting Signals

辅助证明。

## Weaknesses

当前和岗位存在的真实差距。

## Strategy

如何发挥优势、减少无关内容、避免夸大短板。

## Resume Story

整份简历应该形成什么统一叙事。
```

任何候选内容都需要判断：

> 这条内容是否增强本次 Positioning？

即使经历本身很好，如果不能增强本次定位，也允许压缩或删除。

---

## 11. 内容选择模型

内容选择不再只做“相关 / 部分相关 / 不相关”三分类。

Agent 综合判断：

```text
岗位重要度
×
证据强度
×
差异化价值
×
篇幅成本
```

据此决定：

- 哪段实习保留；
- 哪个项目进入简历；
- 哪项技能突出；
- 哪段经历只保留一句；
- 哪些内容完全删除。

---

## 12. STAR 的定位

STAR 保留，但只作为 Agent 理解和整理经历的工具。

不得强制最终每条 Bullet 都机械包含完整的：

```text
Situation
Task
Action
Result
```

最终简历优先采用：

```text
Action
+
Technical / Professional Decision
+
Scope / Result
```

例如内部分析：

```text
S：原流程依赖人工整理资料
T：降低重复整理成本
A：设计自动化处理流程
R：完成端到端自动处理
```

最终可以压缩为：

> 设计自动化资料处理流程，打通采集、清洗与结构化输出链路，减少重复人工整理。

---

## 13. 量化原则

不要求每个项目必须出现数字。

成果表达优先级：

```text
1. 真实业务指标
2. benchmark / 测试指标
3. 用户 / 数据 / 请求规模
4. 完成工作规模
5. 明确交付状态
6. 定性技术成果
```

没有真实数字不构成失败。

为了满足“量化成果”规则而创造数字属于严重错误。

---

## 14. 专业技能模块

### 14.1 定位

专业技能区的目标不是展示候选人认识多少技术名词，而是快速表达：

> 候选人具备哪些能力，以及这些技术如何组合成实际能力。

同时保留 ATS 所需的关键技术词。

### 14.2 默认结构

优先采用：

```text
能力主题：关键词；证据信号
```

例如：

```text
后端工程：Java、Spring Boot、MySQL、Redis；能够独立完成 API、数据层与缓存链路设计

数据分析：Python、Pandas、SQL、可视化；完成数据清洗、分析建模与结果呈现闭环

工程实践：Linux、Docker、Git、CI/CD；具备开发、部署、调试和问题定位经验
```

结构语义：

```text
能力域
:
代表性技术 / 方法
;
能力或证据信号
```

### 14.3 三种技能区策略

#### Capability-first

默认策略。

适合：

- 实习生；
- 应届生；
- 能力结构清晰的候选人。

强调：

```text
能力 + 关键词 + 证据
```

#### Keyword-dense

适合：

- JD 有大量明确工具要求；
- ATS 匹配明显重要；
- 技术关键词本身就是筛选条件。

即使使用该策略也必须分类，不得退化成长串名词。

#### Minimal

适合：

- 工作经历已经非常强；
- 技术能力可以直接从经历读出；
- 页面空间紧张。

只保留最核心的 2–3 个能力簇。

### 14.4 动态能力簇

不得写死：

```text
后端
前端
算法
测试
```

Agent 根据：

```text
当前 JD
+
候选人最强 Evidence
```

动态形成 2–5 个能力簇。

可能出现：

- 云平台工程；
- 数据分析；
- 项目交付；
- 商业分析；
- 用户研究；
- 机器学习；
- 财务建模；
- 供应链分析；
- 自动化；
- 系统工程。

### 14.5 技能区约束

- 只保留真正能够形成招聘信号的技术或方法；
- 不要求固定技术数量；
- 避免同义或高度重合技术重复；
- 普通 API 调用不得自动视为技能；
- 证据弱的能力不得放在最显眼位置；
- 不使用“精通”“专家级”等无法证明的词；
- 技能描述必须与项目和工作经历中的事实一致。

---

## 15. Claim Audit

简历草稿完成后生成 `claim-audit.md`。

每个高价值 Claim 分类为：

```text
FACT
DERIVED
NEEDS_CONFIRMATION
UNSUPPORTED
```

### FACT

用户或档案明确提供。

### DERIVED

由已有事实合理总结，且不改变事实强度。

例如多个经历都显示候选人独立完成从开发到部署，可以合理总结为：

> 具备独立交付能力。

### NEEDS_CONFIRMATION

合理但现有证据不足。

细致模式可以询问用户。

全自动模式不得直接写入正式简历。

### UNSUPPORTED

缺乏足够事实支持。

必须删除。

示例：

```markdown
# Claim Audit

## C1

简历表述：

> 优化系统高并发性能。

证据：

没有性能测试、并发测试或性能优化记录。

判断：

UNSUPPORTED

处理：

删除。
```

---

## 16. Agent 工作流

`build-resume/SKILL.md` 的核心 Workflow 保持在以下层级：

```text
1. Detect Context
2. Gather Candidate Evidence
3. Model Job
4. Match Evidence
5. Define Positioning
6. Select Content
7. Write Resume
8. Audit Claims
9. Validate Structure
10. Build PDF
11. Verify PDF
12. Deliver
```

### Step 1：Detect Context

检测：

- 是否存在候选人档案；
- 是否已有当前岗位的中间文件；
- 是否已有 `resume.md`；
- 是否已有 PDF；
- LaTeX 环境是否可用。

### Step 2：Gather Candidate Evidence

读取当前任务需要的候选人 Markdown 档案。

先读取索引和概要，再按需要读取具体项目、工作和证据文件。

### Step 3：Model Job

读取 `references/job-modeling.md`。

形成 `job-model.md`。

### Step 4：Match Evidence

读取 `references/evidence-model.md`。

生成 `match-matrix.md`。

### Step 5：Define Positioning

读取 `references/matching-positioning.md`。

生成 `positioning.md`。

### Step 6：Select Content

根据岗位重要度、Evidence Strength、差异化和页面预算决定内容。

### Step 7：Write Resume

读取：

```text
references/writing-standards.md
```

如果启用技能 / 核心能力模块，再读取：

```text
references/skills-section.md
```

### Step 8：Audit Claims

生成 `claim-audit.md`。

所有 `UNSUPPORTED` 必须删除。

`NEEDS_CONFIRMATION` 在未经确认时不得进入正式简历。

### Step 9：Validate Structure

读取：

```text
references/validation-rules.md
```

并执行确定性验证脚本。

### Step 10：Build PDF

读取：

```text
references/latex-reference.md
```

使用现有构建脚本完成 LaTeX 编译。

### Step 11：Verify PDF

验证：

- PDF 成功生成；
- 页面没有明显溢出；
- 没有空模块；
- 没有异常换行；
- 页数符合当前排版目标。

### Step 12：Deliver

最终交付：

- `resume.md`；
- `resume.pdf`；
- 必要时告知用户中间分析文件所在目录。

---

## 17. 三种交互模式

保留：

```text
细致模式
宏观模式
全自动模式
```

但交互应围绕会改变简历决策的信息，而不是机械排版选项。

### 17.1 细致模式

主要确认：

- Job Model；
- Candidate Positioning；
- 关键事实缺口；
- `NEEDS_CONFIRMATION` Claim；
- 最终简历。

不逐模块反复询问：

- 要写两点还是三点；
- 日期放哪；
- 每个技能写几个词。

这些属于 Agent 可自主判断的执行细节。

### 17.2 宏观模式

只确认：

```text
Job Model + Positioning
```

之后由 Agent 自主完成内容选择、写作、验证和排版。

### 17.3 全自动模式

不主动提问。

缺少信息时：

- 使用现有真实证据；
- 弱化不确定内容；
- 删除证据不足的 Claim；
- 不通过猜测补齐事实。

---

## 18. Progressive Disclosure 资源路由

### Job Modeling

读取：

```text
references/job-modeling.md
```

### Evidence Modeling

读取：

```text
references/evidence-model.md
```

### Matching / Positioning

读取：

```text
references/matching-positioning.md
```

### Resume Writing

读取：

```text
references/writing-standards.md
```

### Skills Section

仅当简历包含技能 / 核心能力模块时读取：

```text
references/skills-section.md
```

### Examples

仅当需要参考表达方式时读取：

```text
references/resume-examples.md
```

### PDF

读取：

```text
references/latex-reference.md
```

### Final Validation

读取：

```text
references/validation-rules.md
```

避免每次生成简历都将所有长篇规则同时塞入上下文。

---

## 19. 确定性脚本

LLM 负责：

- 理解；
- 判断；
- 语义匹配；
- 定位；
- 内容选择；
- 写作；
- Claim 语义审计。

Script 负责：

- 文件存在性验证；
- Markdown 结构检查；
- 重复内容检查；
- 占位符检查；
- 机械格式检查；
- LaTeX 构建；
- PDF 页数检查；
- 临时文件清理。

新增：

```text
scripts/validate-resume.py
```

建议检查：

- `resume.md` 是否存在；
- 是否存在未替换占位符；
- 是否存在空模块；
- 是否存在明显重复 Bullet；
- Markdown 标题结构是否正常；
- 是否包含被明确禁止的熟练度表达；
- `claim-audit.md` 是否仍存在未处理的 `UNSUPPORTED`；
- 构建必需字段是否缺失；
- PDF 是否成功生成；
- PDF 页数；
- LaTeX 临时文件是否残留。

“某一句是否夸大候选人的能力”这类语义问题仍然由 Agent 判断，不能假装脚本可以完成。

---

## 20. Validation

最终输出之前必须同时通过三类验证：

```text
Evidence Validation
+
Content Validation
+
Rendering Validation
```

### 20.1 Evidence Validation

确认：

- 所有核心 Claim 都有证据来源；
- `UNSUPPORTED` Claim 已删除；
- `NEEDS_CONFIRMATION` 未经确认没有进入正式简历；
- 没有因为 JD 关键词而人为提高候选人能力等级。

### 20.2 Content Validation

确认：

- 简历形成明确 Positioning；
- 最强证据获得最多篇幅；
- 专业技能区不是单纯技术名词仓库；
- Bullet 没有机械复制同一种句式；
- 没有为了量化制造数字；
- 没有为了套 STAR 写冗余背景；
- 弱相关经历没有抢占核心篇幅。

### 20.3 Rendering Validation

确认：

- PDF 正常生成；
- 没有文本溢出；
- 没有明显异常换行；
- 没有空模块；
- 页数符合当前简历排版策略；
- 临时 LaTeX 文件已清理。

---

## 21. Failure Handling

### JD 信息不足

只使用能够确认的内容建立 Job Model，并标记低置信度推断。

不得自行补全公司或岗位要求。

### 候选人缺少关键证据

不得创造经历。

细致模式可以询问用户是否存在尚未录入的真实经历。

宏观和全自动模式直接弱化或删除该能力相关内容。

### PDF 编译失败

必须保留已经生成的有效 Markdown：

```text
job-model.md
match-matrix.md
positioning.md
resume.md
claim-audit.md
```

报告构建失败原因，不得因为 PDF 构建失败丢失有效内容。

---

## 22. 简历示例设计

`references/resume-examples.md` 不保存单一“标准答案”。

至少覆盖：

```text
Example A：技术实习 / 应届生
Example B：业务 / 分析类岗位
Example C：已有工作经验候选人
```

示例的作用是说明：

- 信息密度；
- Evidence 表达；
- 能力分组；
- 内容取舍；
- 不同岗位的表达差异。

不得把示例当作固定语言模板。

示例文件顶部必须明确：

```markdown
# Resume Examples

以下示例全部为虚构数据。

它们只用于说明：

- 信息密度
- 证据表达
- 能力分组
- 内容取舍
- 不同岗位的表达差异

不得：

- 将示例人物信息复制到真实简历
- 将示例数字当作用户数据
- 将示例技术栈自动添加到候选人档案
- 要求所有简历复制相同章节或句式
```

---

## 23. 技术岗位虚构简历示例

以下人物、学校、企业、项目和数据均为虚构内容。

# 林川

求职方向：软件工程 / AI 应用工程实习

电话：138-0000-0000  
邮箱：example@example.com  
GitHub：github.com/example

## 教育背景

**东岭大学｜计算机科学与技术｜本科**  
2023.09 - 2027.06

核心课程：数据结构、操作系统、计算机网络、数据库系统、软件工程、机器学习

## 专业能力

- **AI 应用工程**：Python、FastAPI、LangGraph、RAG；能够完成模型调用、工具编排、检索与服务接口的端到端实现
- **后端与数据**：Java、Spring Boot、MySQL、Redis；具备 REST API、数据模型、缓存与异步任务开发经验
- **工程实践**：Linux、Docker、Git、CI/CD；能够独立完成开发环境搭建、服务部署、日志排查与问题定位

## 实习经历

### 星河数据科技｜软件工程实习生

2026.05 - 2026.08

- 开发企业文档处理服务，将文件解析、文本清洗、信息抽取与结构化输出拆分为可复用处理节点
- 设计任务状态与异常重试机制，解决长任务执行失败后需要人工重新运行的问题
- 为内部服务补充接口测试与日志追踪流程，使开发人员能够快速定位失败步骤和异常输入

## 项目经历

### DocPilot 企业知识检索平台｜独立开发

技术栈：Python、FastAPI、PostgreSQL、Elasticsearch、Docker

面向内部文档检索场景构建知识查询系统，解决资料分散和关键词搜索难以定位完整答案的问题。

- 设计文档解析、切分、索引与检索链路，将不同格式文件统一转换为可检索数据结构
- 实现关键词与语义检索组合策略，并对查询结果进行重排，提高长文档场景下的结果相关性
- 封装 FastAPI 服务并使用 Docker 部署，完成从数据导入、检索到接口交付的完整工程闭环

### QueueLab 异步任务调度服务｜核心开发

技术栈：Java、Spring Boot、Redis、RabbitMQ、MySQL

针对批量任务同步执行导致接口等待时间过长的问题，实现独立异步任务调度服务。

- 基于消息队列拆分任务提交与任务执行流程，支持任务状态查询和失败重试
- 使用 Redis 保存高频任务状态，减少重复数据库查询
- 完成异常处理、任务日志和 Docker 部署，使服务能够独立运行和排查

### 示例说明

该示例刻意避免：

```text
AI：Python、PyTorch、LangGraph、RAG、FastAPI、Docker...
```

这样的纯技术堆砌。

专业能力采用：

```text
能力主题
+
关键技术
+
能做到什么
```

因此既保留 ATS 关键词，也能让招聘者快速理解候选人的能力结构，并自然关联到后续经历证据。

---

## 24. 非技术岗位技能表达示例

商业分析岗位可以采用：

```markdown
## 核心能力

- **市场与行业分析**：行业规模、竞争格局、用户研究；能够从公开数据和访谈信息形成结构化判断
- **数据分析**：Excel、SQL、Python；能够完成数据清洗、指标拆解与可视化分析
- **项目推进**：需求拆解、跨团队协作、结果汇报；能够独立推进从问题定义到交付的分析任务
```

Skill 不默认所有岗位都需要“技术栈”模块。

---

## 25. first-start 职责

`first-start` 只负责：

- 介绍工具链；
- 收集行业方向；
- 收集目标岗位；
- 收集候选人阶段；
- 收集求职偏好；
- 初始化或更新个人档案。

求职方向写入：

```text
个人信息/求职方向/目标方向.md
```

示例：

```markdown
# 求职方向

## 目标岗位

- 数据分析
- 商业分析

## 偏好行业

- 企业服务
- 消费互联网

## 当前阶段

应届生

## 求职重点

希望突出数据分析能力与业务理解。

## 其他偏好

暂无。
```

`first-start` 不直接修改其他 Skill 的流程、示例或分类体系。

---

## 26. init-personal-info 职责

`init-personal-info` 建立：

```text
人类可编辑
+
事实优先
+
证据友好
```

的 Markdown 候选人档案。

收集经历时应围绕以下问题获取高价值事实：

- 你具体负责什么；
- 为什么做这件事；
- 真正由你完成的部分是什么；
- 做了什么关键判断或方案选择；
- 有什么真实可验证结果；
- 有哪些容易被误解或夸大的边界。

用户不需要理解 Evidence Unit、Evidence Strength 等内部术语。

Agent 将自然语言整理成相应 Markdown。

---

## 27. build-resume/SKILL.md 建议骨架

```markdown
---
name: build-resume
description: Build evidence-grounded, job-targeted resumes from a candidate's Markdown profile and a job description. Use when the user wants to create, tailor, revise, or compile a resume/CV for a specific role, compare their experience against a job description, or generate a job-specific resume PDF.
---

# Build Resume

## Purpose

Generate a truthful, evidence-grounded and job-targeted resume.

## Inputs

- Candidate Markdown profile
- Target JD
- Existing resume, if present

## Core Rules

- Never fabricate candidate facts.
- Treat evidence strength separately from JD importance.
- Do not write unsupported claims.
- Quantify only when real numbers exist.
- Skills must communicate capability, not merely list tools.

## Workflow

1. Detect current state.
2. Read candidate profile.
3. Build Job Model.
4. Build Requirement × Evidence Matrix.
5. Define Candidate Positioning.
6. Select resume content.
7. Write resume.
8. Run Claim Audit.
9. Validate.
10. Build and verify PDF.

## Job Modeling

Read:

references/job-modeling.md

## Evidence Modeling

Read:

references/evidence-model.md

## Matching and Positioning

Read:

references/matching-positioning.md

## Resume Writing

Read:

references/writing-standards.md

If a skills/core-capabilities section is used, also read:

references/skills-section.md

## Examples

Read only when additional examples are useful:

references/resume-examples.md

## PDF

Read:

references/latex-reference.md

Run:

shell/build.sh

## Validation

Read:

references/validation-rules.md

Run:

scripts/validate-resume.py

Do not deliver the final resume if unsupported claims remain.

## Failure Handling

Never replace missing candidate evidence with invented experience.
Preserve valid Markdown artifacts if PDF generation fails.
```

---

## 28. 文件范围

设计涉及以下主要文件：

```text
skills/build-resume/SKILL.md
skills/build-resume/references/
skills/build-resume/scripts/
skills/build-resume/shell/
skills/build-resume/template/

skills/init-personal-info/SKILL.md
skills/first-start/SKILL.md
```

README、CLAUDE 和其他使用说明只描述当前实际结构和当前用法，不写版本演进、迁移历史或曾经行为。

---

## 29. 验收标准

### 29.1 岗位理解

面对陌生岗位，Agent 能根据 JD 动态生成能力模型，而不是依赖预设的“后端 / 前端 / 算法 / 测试”等有限分类。

### 29.2 候选人理解

Agent 能明确区分：

```text
事实
能力证据
证据强度
表达边界
```

### 29.3 内容选择

面对多个经历，Agent 能解释为什么选择某段经历，以及该经历支持什么岗位要求。

### 29.4 专业技能

专业技能区默认采用：

```text
能力主题 + 关键技术 / 方法 + 证据信号
```

不得默认退化为大量技术名词罗列。

### 29.5 真实性

任何强 Claim 都必须能够追溯到：

```text
候选人档案
或
用户明确确认
```

没有真实数字时不得制造数字。

### 29.6 泛化性

Skill 不依赖软件工程领域示例才能工作。

面对技术、金融、分析、运营、产品、设计、咨询等不同岗位时，都能够根据 JD 动态建立能力模型。

### 29.7 可审查性

用户能够直接打开：

```text
job-model.md
match-matrix.md
positioning.md
claim-audit.md
resume.md
```

理解 Agent 的关键判断。

### 29.8 Skill 结构

`SKILL.md` 保持核心 SOP 和资源路由职责。

详细规则、示例和排版知识通过 `references/` 按需加载。

确定性验证由脚本执行，语义判断仍由 Agent 负责。

---

## 30. 最终原则

系统的核心不是让 Agent 把简历写得更华丽，而是让 Agent 在写作之前先建立正确判断：

> 这个岗位在找什么人？

> 候选人真正有什么证据？

> 哪些证据值得展示？

> 哪些表达只是合理总结？

> 哪些内容没有证据，绝对不能写？

只有完成这些判断后，才进入最终写作和排版阶段。
