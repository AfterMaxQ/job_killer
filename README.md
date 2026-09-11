# Job Killer

求职技能工具链 —— 6 个 Claude Code Skills，覆盖从个人档案、JD 定制、HR 沟通到面试准备的完整流程。

## 技能总览

```text
first-start
    │
    ├─ 建立 / 更新求职方向画像
    │
    └─ init-personal-info
           │
           ├─ 人类可编辑 Markdown 候选人档案
           └─ Evidence 能力证据
                    │
      ┌─────────────┼──────────────────┐
      ▼             ▼                  ▼
greeting-generator build-resume interview-question-generator
      │             │
      ▼             ▼
hr-communicator   JD → Job Model → Evidence Match → Positioning
                              → Resume → Claim Audit → PDF
```

## 安装

### npm

在 Claude Code 项目目录运行：

```bash
npx @ethan_ray/job-killer
```

可用：

```bash
npx @ethan_ray/job-killer --force
npx @ethan_ray/job-killer --help
```

### 手动安装

将仓库 `skills/` 下的 6 个目录放入项目：

```text
.claude/skills/
├── first-start/
├── init-personal-info/
├── build-resume/
├── greeting-generator/
├── hr-communicator/
└── interview-question-generator/
```

## 候选人档案

候选人数据以 Markdown 为 Source of Truth，用户可以直接打开、修改和通过 Git 管理。

推荐结构：

```text
个人信息/
├── 基本信息.md
├── 教育背景.md
├── 技能能力.md
├── 求职方向/
│   └── 目标方向.md
├── 工作经历/
├── 项目经历/
├── 比赛经历/
└── 证据索引.md
```

### 求职方向

`个人信息/求职方向/目标方向.md` 保存当前：

- 目标岗位；
- 偏好行业；
- 当前阶段；
- 求职重点；
- 其它偏好。

这是运行时画像。不同岗位的 Skill 在执行时读取，不需要修改 Skill 文件来“适配行业”。

### Evidence

工作、项目和比赛经历可以增加 `# 能力证据`，用于说明：

- 真实发生了什么；
- 这件事能证明哪些能力；
- 证据强度；
- 适合支持什么岗位；
- 哪些更强 Claim 不能从该经历推出。

Evidence 仍然是普通 Markdown。原始事实始终是最终依据。

## Skills

### `first-start`

**用途**：介绍工具链、建立或更新求职方向画像，并按需进入个人档案初始化。

**触发**：`开始`、`怎么用`、`初始化系统`、`换求职方向` 等。

### `init-personal-info`

**用途**：建立事实优先、证据友好的人类可编辑 Markdown 档案。

**触发**：`初始化档案`、`整理我的资料`、`更新项目经历` 等。

### `build-resume`

**用途**：根据候选人事实、Evidence 和目标 JD 生成可审查的针对性简历，再编译为 PDF。

核心流程：

```text
JD
↓
job-model.md
↓
match-matrix.md
↓
positioning.md
↓
resume.md
↓
claim-audit.md
↓
validator
↓
LaTeX / PDF
```

每份 JD 使用独立目录：

```text
temp_resume/<公司>-<岗位>/
├── job-model.md
├── match-matrix.md
├── positioning.md
├── resume.md
└── claim-audit.md
```

专业技能 / 核心能力区会根据 JD + Evidence 动态生成能力簇。支持：

- **Capability-first**：默认，用能力主题 + 关键词/方法 + 证据信号表达；
- **Keyword-dense**：JD 工具要求密集、ATS 关键词重要时使用；
- **Minimal**：工作经历已经足够强或页面空间紧张时使用。

没有真实数字时允许使用规模、交付状态或定性成果，不为了量化制造数据。

### `greeting-generator`

**用途**：生成 Boss 直聘、猎聘等平台的首次触达消息。

### `hr-communicator`

**用途**：处理 HR 后续沟通，包括面试时间、薪资、材料、Offer 等场景。

### `interview-question-generator`

**用途**：结合 JD 和候选人项目/工作材料准备面试问题与口语化回答。

## build-resume 验证

确定性检查：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "temp_resume/<公司>-<岗位>"
```

PDF 生成后：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "temp_resume/<公司>-<岗位>" --pdf resume.pdf
```

Validator 检查文件结构、占位符、重复 Bullet、强熟练度措辞、未处理 Claim、PDF 基础状态和 LaTeX 临时文件。语义真实性仍由 Agent 根据 Evidence 做审计。

## PDF 依赖

`build-resume` 使用 XeLaTeX：

- MiKTeX 或 TeX Live；
- 模板位于 `.claude/skills/build-resume/template/`；
- 编译脚本：

```bash
bash .claude/skills/build-resume/shell/build.sh
```

可选照片：

```text
images/you.jpg
```

没有照片时直接跳过。

## 推荐工作流

1. 首次使用：`first-start` 建立求职方向；
2. `init-personal-info` 建立或维护 Markdown 档案；
3. 发现岗位：可用 `greeting-generator` 首次触达；
4. 投递简历：`build-resume` 读取 JD 与 Evidence，生成分析文件、简历和 PDF；
5. HR 回复：使用 `hr-communicator`；
6. 收到面试：使用 `interview-question-generator`。

## 核心约束

- 不编造候选人事实；
- JD 重要度不能提升 Candidate Evidence Strength；
- `UNSUPPORTED` Claim 不进入最终简历；
- 普通 API 调用不会自动被包装成高级技能；
- 技能区不是所有工具的库存清单；
- STAR 用于理解经历，不要求最终 Bullet 机械套模板；
- 所有示例只用于学习表达原则，不能复制为真实候选人数据。