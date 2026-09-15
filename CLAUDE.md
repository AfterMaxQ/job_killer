## 文件夹结构

| 目录 | 职责 |
|---|---|
| `个人信息/` | 候选人 Markdown 档案 Source of Truth：基本信息、教育、技能、求职方向、工作/项目/比赛经历、Evidence |
| `个人信息/求职方向/目标方向.md` | 当前目标岗位、行业、阶段、求职重点和偏好；运行时读取，不修改 Skill 做领域适配 |
| `个人信息/证据索引.md` | 跨经历 Evidence 导航；具体经历文件仍是最终事实来源 |
| `temp_resume/<公司>-<岗位>/` | 每份 JD 的可审查分析目录：Job Model、匹配矩阵、Positioning、Resume、Claim Audit |
| `简历pdfs/` | 最终 PDF 简历归档（如项目使用该目录） |
| `简历pptx/` | PPTX 简历归档（如项目使用该目录） |
| `简历图片/` | 简历图片素材（如项目使用该目录） |
| `images/` | 简历照片等本地素材，例如 `you.jpg` |
| `build/` | LaTeX 编译临时输出 |
| `.claude/skills/` | Claude Code Skills |

## 工作流

| 场景 | 命令/技能 | 当前行为 |
|---|---|---|
| 首次使用 | `/first-start` | 介绍工具链，建立/更新求职方向画像，按需进入档案初始化 |
| 初始化档案 | `/init-personal-info` | 建立人类可编辑的 Markdown 候选人档案与可选 Evidence |
| 生成简历 | `/build-resume` | JD → Job Model → Evidence Match → Positioning → Resume → Claim Audit → Validation → PDF |
| 面试准备 | `/interview-question-generator` | 结合 JD 和候选人项目/工作材料生成面试 Q&A |
| 招聘招呼语 | `/greeting-generator` | 根据岗位和候选人档案生成首次触达消息 |
| HR 沟通 | `/hr-communicator` | 根据 HR 消息和候选人事实生成沟通方案 |
| 清理 | `bash .claude/skills/build-resume/shell/clean.sh` | 清理 LaTeX 临时文件 |

## build-resume 中间文件

每份 JD 使用独立目录：

```text
temp_resume/<公司>-<岗位>/
├── job-model.md
├── match-matrix.md
├── positioning.md
├── resume.md
└── claim-audit.md
```

职责：

- `job-model.md`：招聘方真正需要什么能力，区分明确要求与 Agent 推断；
- `match-matrix.md`：`能力 | JD重要度 | 最强证据 | 证据强度 | 策略`；
- `positioning.md`：Target Identity、Top Signals、Weaknesses、Strategy、Resume Story；
- `resume.md`：当前 JD 的最终 Markdown 简历；
- `claim-audit.md`：FACT / DERIVED / NEEDS_CONFIRMATION / UNSUPPORTED 审计。

## 行为指导

- **事实优先**：所有候选人 Claim 必须来自 Markdown 档案或用户明确确认。
- **Evidence 与 JD 分离**：JD 很需要某能力，不代表候选人的 Evidence Strength 可以提高。
- **运行时画像**：岗位、行业和求职方向写入 `目标方向.md`，不要通过改 Skill 文件做领域适配。
- **动态能力簇**：专业技能 / 核心能力由当前 JD + Evidence 生成，不固定套“后端/前端/算法/测试”。
- **技能不是名词仓库**：默认表达“能力主题：关键词/方法；证据信号”。
- **不为量化造数**：没有真实数字时使用规模、交付状态或定性结果。
- **API 调用不自动算技能**：只有能证明真实任务、方案组合和工程处理能力时才提升为能力信号。
- **STAR 用于分析**：最终 Bullet 优先 Action + Decision + Scope/Result，不机械套完整 STAR。
- **Claim Audit 必须闭环**：`UNSUPPORTED` 删除；`NEEDS_CONFIRMATION` 未确认不得进入正式简历。
- **修改范围最小**：只修改当前任务相关文件，不无故改模板、脚本或其它 Skill。
- **文档写当前状态**：README、CLAUDE、SKILL 和说明文件只描述当前可用结构与当前用法。

## 验证

生成 Markdown 后运行：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "temp_resume/<公司>-<岗位>"
```

PDF 构建后运行：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "temp_resume/<公司>-<岗位>" --pdf resume.pdf
```

Validator 只做确定性机械检查；语义真实性、Positioning 和 Evidence 强度仍由 Agent 负责。