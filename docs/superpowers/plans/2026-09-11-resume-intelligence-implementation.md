# Resume Intelligence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `job_killer` 的简历链路改造成基于 Markdown 档案与证据、可审查、可泛化的 JD 定制简历系统，并让专业技能模块从技术名词罗列升级为能力信号表达。

**Architecture:** 保持候选人事实、证据与每份 JD 的中间决策均以 Markdown 为 Source of Truth；`build-resume/SKILL.md` 只承担核心 SOP 与资源路由，详细判断规则拆入 `references/`，确定性检查进入 `scripts/validate-resume.py`，现有 `shell/` 与 `template/` 保持不动。`first-start` 只维护运行时求职画像，`init-personal-info` 负责建立证据友好的 Markdown 档案，`build-resume` 依次生成 Job Model、匹配矩阵、Positioning、Resume 与 Claim Audit。

**Tech Stack:** Markdown Agent Skills、Python 3、现有 Bash/XeLaTeX 构建脚本、现有 LaTeX 模板。

**Spec:** `docs/superpowers/specs/2026-09-11-resume-intelligence-design.md`

## Global Constraints

- 候选人档案、证据、岗位分析和中间决策必须继续使用 Markdown，禁止改成 JSON/数据库主存储。
- Skill 文件描述稳定 SOP；行业、岗位、候选人信息属于运行时数据，不通过改写 Skill 文件完成领域适配。
- 所有示例必须为完全虚构数据，不得包含真实用户或仓库维护者个人信息。
- 不得编造经历、技能、指标、生产环境或成果；没有真实数字时允许定性表达。
- Evidence Strength 与 JD 重要度必须独立，JD 强需求不能反向提高候选人证据强度。
- STAR 只作为内部分析方法，不强制最终每条 Bullet 套完整 STAR。
- 专业技能模块默认表达“能力主题 + 关键词/方法 + 证据信号”，不得退化为长串技术名词。
- `UNSUPPORTED` Claim 必须删除；未经确认的 `NEEDS_CONFIRMATION` 不得进入正式简历。
- 保留现有 `skills/build-resume/shell/` 与 `template/` 目录，除非实现中发现明确阻塞，不做无价值目录重构。
- README、CLAUDE、SKILL 等说明文档只描述当前版本实际状态和当前用法，不写迁移史、旧行为或版本演进。

---

## File Map

### Core skills

- Modify: `skills/build-resume/SKILL.md` — 精简为入口、核心 SOP、Decision Rules、资源路由、验证与失败处理。
- Modify: `skills/init-personal-info/SKILL.md` — 改成证据友好的 Markdown 档案初始化与更新流程。
- Modify: `skills/first-start/SKILL.md` — 停止改写其他 Skill，改为建立/更新 `个人信息/求职方向/目标方向.md`。

### New references

- Create: `skills/build-resume/references/job-modeling.md` — Job Model 结构、重要度判断、显式要求与合理推断的边界。
- Create: `skills/build-resume/references/evidence-model.md` — Evidence Unit、Evidence Strength、证据索引、表达边界。
- Create: `skills/build-resume/references/matching-positioning.md` — Requirement × Evidence Matrix、内容选择、Candidate Positioning。
- Create: `skills/build-resume/references/skills-section.md` — Capability-first / Keyword-dense / Minimal 三种技能区策略。
- Create: `skills/build-resume/references/resume-examples.md` — 至少三类完全虚构示例及禁止复制说明。
- Create: `skills/build-resume/references/validation-rules.md` — Evidence / Content / Rendering 三层验证规则。

### Existing references to revise

- Modify: `skills/build-resume/references/writing-standards.md` — 删除强制量化、机械 STAR、固定岗位分类等过度规则；保留高信息密度、真实表达原则。
- Modify: `skills/build-resume/references/common-errors.md` — 将内容审计与新工作流保持一致，去除与新规则冲突的旧检查项。
- Keep/adjust only if required: `skills/build-resume/references/latex-reference.md` — 仅修正新 `temp_resume/<公司>-<岗位>/resume.md` 路径相关说明。
- Replace content: `skills/build-resume/references/good-resume-exemple.md` — 不再作为唯一标准答案；可删除或改成指向 `resume-examples.md` 的简短兼容说明，最终仓库不得保留真实个人信息示例。

### Deterministic validation

- Create: `skills/build-resume/scripts/validate-resume.py` — 检查文件、Markdown 结构、占位符、重复 Bullet、禁用熟练度词、Claim Audit 状态、PDF 页数与 LaTeX 临时文件。
- Create: `skills/build-resume/scripts/tests/test_validate_resume.py` — 使用临时目录和虚构 fixture 覆盖 validator 的关键行为。

### Documentation

- Modify: `README.md` — 描述当前工作流和 Markdown 档案结构。
- Modify: `CLAUDE.md` — 更新当前目录职责与行为指导，不写迁移历史。

---

### Task 1: 固化 Markdown 档案与 Evidence 规则

**Files:**
- Create: `skills/build-resume/references/evidence-model.md`
- Modify: `skills/init-personal-info/SKILL.md`

**Interfaces:**
- Consumes: 用户自然语言提供的基本信息、教育、经历、项目、比赛、技能和求职信息。
- Produces: 人类可编辑的 Markdown 档案约定；经历中的 `# 能力证据` / `E1｜...` 结构；Evidence Strength 0–5；`个人信息/证据索引.md`。

- [ ] **Step 1: 编写 `evidence-model.md` 的固定语义**

必须定义：Evidence Unit 的事实、可以证明、证据强度、适合支持、表达边界；0–5 级定义；“JD 重要度不得改变 Evidence Strength”；证据索引不是唯一事实来源。

- [ ] **Step 2: 用纯虚构示例验证 reference 可读性**

示例至少包含一段“项目中实际使用 = 3”和一段“真实业务且有明确结果 = 5”，并分别给出不能声称的边界。

- [ ] **Step 3: 重写 `init-personal-info/SKILL.md` 的目录与采集流程**

目标目录采用：

```text
个人信息/
├── 基本信息.md
├── 教育背景.md
├── 技能能力.md
├── 求职方向/目标方向.md
├── 工作经历/
├── 项目经历/
├── 比赛经历/
└── 证据索引.md
```

Agent 对用户保持自然问题，不要求用户理解 Evidence Unit 术语；整理时再写成规范 Markdown。

- [ ] **Step 4: 增加经历采集问题**

至少覆盖：具体负责什么、为什么做、本人完成部分、关键判断/方案、真实结果、容易夸大的边界。

- [ ] **Step 5: 人工检查**

确认整个 Skill 没有要求 JSON/YAML 主存储，没有自动制造证据强度，没有真实个人信息示例。

- [ ] **Step 6: Commit**

```bash
git add skills/build-resume/references/evidence-model.md skills/init-personal-info/SKILL.md
git commit -m "feat: add evidence-grounded candidate profile"
```

---

### Task 2: 将 first-start 改为运行时求职画像

**Files:**
- Modify: `skills/first-start/SKILL.md`

**Interfaces:**
- Consumes: 行业方向、目标岗位、当前阶段、求职重点、其他偏好。
- Produces: `个人信息/求职方向/目标方向.md`；不再修改任何其他 Skill 文件。

- [ ] **Step 1: 删除“改写 5 个 skill”作为领域适配机制的指令**

新流程只能读取和更新求职画像，不触碰 `build-resume`、`greeting-generator`、`hr-communicator`、`interview-question-generator` 的规则文件。

- [ ] **Step 2: 定义求职画像 Markdown**

```markdown
# 求职方向

## 目标岗位
- ...

## 偏好行业
- ...

## 当前阶段
...

## 求职重点
...

## 其他偏好
...
```

- [ ] **Step 3: 定义已有画像的更新行为**

存在 `目标方向.md` 时先读取当前内容，只更新用户明确要求的字段；不得无故覆盖其它偏好。

- [ ] **Step 4: 检查跨领域行为**

用“软件工程 → 商业分析”的虚构切换场景确认流程只改画像，不改 Skill。

- [ ] **Step 5: Commit**

```bash
git add skills/first-start/SKILL.md
git commit -m "refactor: make job targeting runtime profile data"
```

---

### Task 3: 建立 Job Model 与匹配/定位 references

**Files:**
- Create: `skills/build-resume/references/job-modeling.md`
- Create: `skills/build-resume/references/matching-positioning.md`

**Interfaces:**
- Consumes: 当前 JD、`目标方向.md`、候选人相关 Evidence。
- Produces: `job-model.md`、`match-matrix.md`、`positioning.md` 的稳定 Markdown 结构。

- [ ] **Step 1: 编写 Job Model 规则**

必须包含：岗位基本信息、招聘目标、P0/P1 能力、门槛条件、强信号、加分项、隐含需求、岗位核心命题。

- [ ] **Step 2: 明确推断边界**

显式要求与 Agent 推断必须分开；禁止“关键词出现一次 = 核心能力”、禁止所有 JD 条目同权重、禁止用候选人强项反向解释 JD。

- [ ] **Step 3: 编写 Requirement × Evidence Matrix 规则**

表格固定字段：`能力 | JD重要度 | 最强证据 | 证据强度 | 策略`；策略限定为核心卖点、强调、正常展示、弱化、谨慎、不写、需要用户确认。

- [ ] **Step 4: 编写 Candidate Positioning 规则**

固定包含 Target Identity、Top Signals、Supporting Signals、Weaknesses、Strategy、Resume Story。

- [ ] **Step 5: 定义内容选择模型**

明确使用：

```text
岗位重要度 × 证据强度 × 差异化价值 × 篇幅成本
```

它是语义决策框架，不要求脚本计算数学乘积。

- [ ] **Step 6: Commit**

```bash
git add skills/build-resume/references/job-modeling.md skills/build-resume/references/matching-positioning.md
git commit -m "feat: add job modeling and resume positioning rules"
```

---

### Task 4: 重构写作规则与专业技能模块

**Files:**
- Modify: `skills/build-resume/references/writing-standards.md`
- Create: `skills/build-resume/references/skills-section.md`
- Modify: `skills/build-resume/references/common-errors.md`

**Interfaces:**
- Consumes: 已完成的 Positioning、匹配矩阵、候选人事实与 Evidence。
- Produces: 简历正文写作规则和 2–5 个动态能力簇的技能区。

- [ ] **Step 1: 将 STAR 改为内部分析工具**

最终 Bullet 默认采用：`Action + Technical/Professional Decision + Scope/Result`，不再强制每条写完整 Situation/Task/Action/Result。

- [ ] **Step 2: 将“必须量化”改为“证据优先、真实量化优先”**

按顺序允许：真实业务指标 → benchmark → 规模 → 工作规模 → 交付状态 → 定性技术成果。禁止因缺数字而创造数字。

- [ ] **Step 3: 移除固定职业 ontology**

删除把“后端/前端/算法/测试”当成默认分类系统的规则；可保留为示例，但明确不能作为固定岗位类别。

- [ ] **Step 4: 编写 `skills-section.md`**

完整定义三种策略：Capability-first（默认）、Keyword-dense、Minimal；动态生成 2–5 个能力簇。

- [ ] **Step 5: 固定技能行语义**

默认：

```text
能力主题：关键技术 / 方法；证据信号
```

证据信号必须能回到候选人事实；普通 API 调用不能自动升级成技能。

- [ ] **Step 6: 更新 common-errors**

至少新增：纯名词堆砌、技能能力无证据、为了 ATS 提升熟练度、为了量化编数字、机械 STAR、弱证据抢核心位置。

- [ ] **Step 7: Commit**

```bash
git add skills/build-resume/references/writing-standards.md skills/build-resume/references/skills-section.md skills/build-resume/references/common-errors.md
git commit -m "refactor: make resume writing evidence and capability driven"
```

---

### Task 5: 替换唯一标准简历示例

**Files:**
- Create: `skills/build-resume/references/resume-examples.md`
- Modify or remove: `skills/build-resume/references/good-resume-exemple.md`

**Interfaces:**
- Consumes: 新写作规则与技能区规则。
- Produces: 至少三类完全虚构、风格不同的示例；不再存在可关联真实用户的样例。

- [ ] **Step 1: 在文件顶部写示例安全边界**

明确示例不得复制人物信息、数字、技术栈或固定句式到真实简历。

- [ ] **Step 2: 编写 Example A：技术实习 / 应届生**

专业能力使用“能力主题 + 关键词 + 证据信号”，项目 Bullet 不机械 STAR。

- [ ] **Step 3: 编写 Example B：商业/数据分析岗位**

使用“核心能力”而非技术栈，展示非技术领域泛化。

- [ ] **Step 4: 编写 Example C：已有工作经验候选人**

采用 Minimal 技能区，主要让工作成果承担证据。

- [ ] **Step 5: 处理旧示例文件**

如果保留 `good-resume-exemple.md`，其内容只写“示例见 `resume-examples.md`”，不保留旧人物和项目正文；若没有任何代码/文档依赖，可删除并同步引用。

- [ ] **Step 6: 仓库搜索个人信息残留**

搜索旧示例中的姓名、学校、真实项目名等标识，确保 build-resume 示例文件中无真实个人信息。

- [ ] **Step 7: Commit**

```bash
git add skills/build-resume/references/resume-examples.md skills/build-resume/references/good-resume-exemple.md
git commit -m "docs: replace resume example with fictional varied examples"
```

若旧文件被删除，则使用 `git add -A`。

---

### Task 6: 重写 build-resume 核心 SOP

**Files:**
- Modify: `skills/build-resume/SKILL.md`
- Modify only if required: `skills/build-resume/references/latex-reference.md`

**Interfaces:**
- Consumes: Task 1–5 的 references。
- Produces: 每个 JD 目录下 `job-model.md`、`match-matrix.md`、`positioning.md`、`resume.md`、`claim-audit.md`，随后构建 PDF。

- [ ] **Step 1: 重写 frontmatter description**

必须同时表达能力与触发条件，并覆盖创建、定制、修改、针对 JD 比对、生成 PDF 等意图。

- [ ] **Step 2: 将 SKILL.md 压缩为核心规则**

保留 Purpose、Inputs、Core Rules、Workflow、交互模式、资源路由、Validation、Failure Handling；删除大段写作知识和示例。

- [ ] **Step 3: 定义 12 步工作流**

```text
Detect Context
Gather Candidate Evidence
Model Job
Match Evidence
Define Positioning
Select Content
Write Resume
Audit Claims
Validate Structure
Build PDF
Verify PDF
Deliver
```

- [ ] **Step 4: 定义 JD 任务目录**

```text
temp_resume/<公司>-<岗位>/
├── job-model.md
├── match-matrix.md
├── positioning.md
├── resume.md
└── claim-audit.md
```

路径中的公司/岗位缺失时使用用户提供的可辨识名称，不得凭空补公司名。

- [ ] **Step 5: 调整三种交互模式**

细致模式只确认 Job Model、Positioning、关键事实缺口、NEEDS_CONFIRMATION 和最终简历；宏观模式只确认 Job Model + Positioning；全自动模式对不确定内容直接弱化/删除。

- [ ] **Step 6: 定义 Claim Audit**

分类固定为 `FACT / DERIVED / NEEDS_CONFIRMATION / UNSUPPORTED`，并明确最终交付前不得残留未处理 UNSUPPORTED。

- [ ] **Step 7: 对齐 LaTeX 路径**

现有 build 逻辑如假设 `temp_resume/*.md`，在 SKILL/latex reference 中改为读取当前任务目录的 `resume.md`；不要修改 `shell/build.sh`，除非实际执行证明脚本本身强依赖旧路径。

- [ ] **Step 8: Commit**

```bash
git add skills/build-resume/SKILL.md skills/build-resume/references/latex-reference.md
git commit -m "refactor: rebuild resume skill around evidence workflow"
```

---

### Task 7: 实现确定性 validator（TDD）

**Files:**
- Create: `skills/build-resume/scripts/validate-resume.py`
- Create: `skills/build-resume/scripts/tests/test_validate_resume.py`
- Create: `skills/build-resume/references/validation-rules.md`

**Interfaces:**
- CLI: `python skills/build-resume/scripts/validate-resume.py <task-dir> [--pdf resume.pdf]`
- Exit `0`: 所有确定性检查通过。
- Exit `1`: 至少一个 error；stdout/stderr 输出可理解的问题列表。

- [ ] **Step 1: 写 failing tests：最小合法任务目录通过**

Fixture 创建 `job-model.md`、`match-matrix.md`、`positioning.md`、`resume.md`、`claim-audit.md`，claim audit 不含未处理 UNSUPPORTED。

- [ ] **Step 2: 运行测试确认失败**

```bash
python -m unittest skills/build-resume/scripts/tests/test_validate_resume.py -v
```

Expected: FAIL，因为 validator 尚不存在。

- [ ] **Step 3: 实现文件存在和 Markdown 标题检查**

实现 `validate_task_dir(path: Path) -> list[str]`；缺少关键文件、`resume.md` 无一级标题或无内容时返回错误。

- [ ] **Step 4: 运行测试确认通过**

```bash
python -m unittest skills/build-resume/scripts/tests/test_validate_resume.py -v
```

- [ ] **Step 5: 写 failing tests：占位符、禁用措辞、重复 Bullet**

至少覆盖 `TODO`/`<placeholder>`、`精通`/`专家级`、完全相同的两条 `- ` Bullet。

- [ ] **Step 6: 实现文本机械检查**

只做可确定判断；不要尝试在脚本中判断“这项能力是否夸大”。

- [ ] **Step 7: 写 failing tests：Claim Audit 中未处理 UNSUPPORTED**

规定若 `claim-audit.md` 同一 Claim 块包含 `UNSUPPORTED` 且没有 `处理：删除` 或等价的明确删除状态，则 validator 报错。

- [ ] **Step 8: 实现 Claim Audit 检查**

解析以 `## C` 开头的块，检查判断和处理字段。

- [ ] **Step 9: 写 failing tests：PDF 与临时文件**

当传入 `--pdf` 时：文件不存在应失败；如环境可读 PDF 页数则检查页数，否则只检查文件存在且非空。检查任务/根目录中 `.aux/.log/.out` 等残留的逻辑保持保守，不删除文件。

- [ ] **Step 10: 实现 PDF/临时文件检查**

不要新增重量级依赖；优先使用标准库和当前环境已有命令。无法可靠判断页数时输出 warning 而不是假装成功验证页数。

- [ ] **Step 11: 编写 `validation-rules.md`**

明确 Evidence Validation 与 Content Validation 由 Agent 做；validator 只负责 Structure/Mechanical/Rendering 可确定部分。

- [ ] **Step 12: 全量运行 validator tests**

```bash
python -m unittest skills/build-resume/scripts/tests/test_validate_resume.py -v
```

Expected: PASS。

- [ ] **Step 13: Commit**

```bash
git add skills/build-resume/scripts skills/build-resume/references/validation-rules.md
git commit -m "feat: add deterministic resume validation"
```

---

### Task 8: 对齐 README 与 CLAUDE 当前用法

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: Task 1–7 已实现行为。
- Produces: 只描述当前系统如何使用的用户/Agent 文档。

- [ ] **Step 1: 更新 README 的 build-resume 描述**

写清：粘贴 JD → 岗位模型 → Evidence 匹配 → Positioning → Markdown Resume → Claim Audit → 验证 → PDF。

- [ ] **Step 2: 更新候选人档案目录说明**

明确档案与 Evidence 仍是可人工维护 Markdown，并描述 `求职方向/目标方向.md` 与 `证据索引.md` 的职责。

- [ ] **Step 3: 更新 CLAUDE 行为指导**

强调事实来源、运行时画像、动态能力簇、不得为量化造数、不得把 API 调用自动当技能。

- [ ] **Step 4: 删除历史叙事**

确保 README/CLAUDE 不出现“旧版、原来、本次改造、迁移、以前会”等版本演进表述。

- [ ] **Step 5: Commit**

```bash
git add README.md CLAUDE.md
git commit -m "docs: document evidence-driven resume workflow"
```

---

### Task 9: 端到端虚构场景验收

**Files:**
- No production file required unless fixes are found.
- Temporary fixtures must use fictional data and must not be committed unless intentionally added as tests/examples.

**Interfaces:**
- Consumes: 完整 Skill 链路。
- Produces: 对技术岗位与非技术岗位都能成立的验收结论。

- [ ] **Step 1: 技术岗位场景**

使用完全虚构候选人 + AI/软件工程 JD，检查是否形成 5 个中间 Markdown 文件；技能区应采用 Capability-first 或合理选择其它策略。

- [ ] **Step 2: 检查弱证据行为**

JD 加入候选人只“学习过”的技能，确认 match matrix 标低证据强度，简历不得写成“熟练/实战优化”。

- [ ] **Step 3: 非技术岗位场景**

使用完全虚构商业分析候选人 + JD，确认能力簇能动态变为市场分析、数据分析、项目推进等，不出现软件工程默认分类残留。

- [ ] **Step 4: Claim Audit 场景**

人为让草稿出现一个无证据强 Claim，确认其被标为 `UNSUPPORTED` 并在最终 resume 删除。

- [ ] **Step 5: 运行 validator**

```bash
python skills/build-resume/scripts/validate-resume.py <fixture-task-dir>
```

Expected: 最终版本 exit 0；含未处理 UNSUPPORTED 的中间版本 exit 1。

- [ ] **Step 6: 若本机有 XeLaTeX，做一次现有构建链路验证**

沿用仓库现有 `skills/build-resume/shell/build.sh`，不重写模板；确认 PDF 可生成且现有清理逻辑有效。没有 XeLaTeX 时记录该环境限制，不伪造通过结果。

- [ ] **Step 7: 运行仓库级敏感示例扫描**

确认 `skills/build-resume/references/` 的示例没有真实用户、真实学校/公司/项目个人组合信息。

- [ ] **Step 8: 最终文档一致性检查**

确认 `SKILL.md` 直接指向所有新 references，不形成 reference → reference → reference 的深层引用链。

- [ ] **Step 9: Commit fixes if needed**

```bash
git add -A
git commit -m "test: verify evidence-driven resume workflow"
```

若验收无需修改文件，则不创建空提交。

---

## Final Verification

- [ ] `skills/build-resume/SKILL.md` 已成为短而明确的 Router + Workflow，而非大而全 Prompt。
- [ ] `first-start` 不再改写其它 Skill。
- [ ] `init-personal-info` 的主存储全部为人类可编辑 Markdown。
- [ ] 每个目标 JD 可以形成 `job-model.md`、`match-matrix.md`、`positioning.md`、`resume.md`、`claim-audit.md`。
- [ ] 专业技能支持 Capability-first / Keyword-dense / Minimal，并由 JD + Evidence 动态生成能力簇。
- [ ] STAR 不再是最终 Bullet 的机械模板。
- [ ] 缺少数字时允许定性成果，任何数字都必须来自事实。
- [ ] `UNSUPPORTED` 不得进入最终简历。
- [ ] `validate-resume.py` 的单元测试全部通过。
- [ ] 技术与非技术两个虚构场景均通过端到端验收。
- [ ] build-resume 示例中没有真实用户个人信息。
- [ ] README、CLAUDE、SKILL 只描述当前状态与当前用法。
