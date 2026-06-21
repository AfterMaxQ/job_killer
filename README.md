# Job Killer

求职技能工具链 —— 6 个 Claude Code 技能，覆盖从 JD 触达到面试准备的完整流程。

## 技能总览

```
first-start（新手引导）
    │
    └─ 领域适配 → init-personal-info（建档案）
                            │
        greeting-generator ── hr-communicator ── build-resume ── interview-question-generator
           (首次触达HR)        (HR回复后沟通)      (定制简历)         (面试模拟)
```

## 安装

将所有 skill 文件夹复制到你的 Claude Code 项目的 `.claude/skills/` 目录下：

```
.claude/skills/
├── first-start/
├── init-personal-info/
├── build-resume/
├── greeting-generator/
├── hr-communicator/
└── interview-question-generator/
```

## 技能详情

### `first-start` — 首次使用引导

**用途**：新手村。介绍工具链 + 将系统适配到你的求职领域。

**触发**：说 "开始"、"帮我"、"引导"

### `init-personal-info` — 个人信息初始化

**用途**：建立结构化个人信息档案，后续所有 skill 的数据源。

**触发**：说 "初始化"、"建立档案"

### `build-resume` — 简历生成

**用途**：粘贴 JD → Markdown 定制 → LaTeX 编译 → 专业排版 PDF。

**触发**：说 "生成简历"、粘贴 JD

### `greeting-generator` — 招呼语生成

**用途**：Boss直聘/猎聘主动触达 HR 的第一条消息。前 18 字决定 HR 点不点开。

**触发**：说 "招呼语"、"怎么跟HR说"

### `hr-communicator` — HR 沟通话术

**用途**：HR 回复后生成自然有策略的回复话术。覆盖 8 类场景（约面试/问薪资/问离职/问空窗期/要材料/面试确认/Offer沟通/婉拒）。3 版本输出 + 策略说明。

**触发**：粘贴 HR 消息、说 "怎么回HR"

### `interview-question-generator` — 面试 Q&A 生成

**用途**：根据 JD + 项目生成口语化面试 Q&A，教你讲出设计思路。

**触发**：说 "面试题"、"面试准备"

## 配置

### 头像照片

在项目根目录下放入 `images/you.jpg`，`build-resume` 会自动检测并在简历 PDF 中生成头像。

```
项目根目录/
├── images/
│   └── you.jpg          ← 你的照片（.jpg 格式）
├── .claude/
│   └── skills/
└── 个人信息/
```

- 支持格式：`.jpg`
- 推荐尺寸：证件照/半身照，任意分辨率均可（LaTeX 会自动缩放）
- 无照片：不创建 `images/you.jpg` 即可，`build-resume` 会自动跳过

生成简历时可在交互环节选择照片宽度（0.12 / 0.14 / 0.16 倍页宽）。

## 依赖

- **build-resume**：XeLaTeX（MiKTeX 或 TeX Live）
- 其余技能：无外部依赖

## 工作流

1. 首次使用 → `first-start` → 选择 B（领域适配）→ 自动进入 `init-personal-info`
2. 看到心仪岗位 → `greeting-generator`（发第一条消息）
3. HR 回复了 → `hr-communicator`（持续沟通）
4. 要投简历 → `build-resume`（粘贴 JD，生成定制 PDF）
5. 收到面试 → `interview-question-generator`（准备面试 Q&A）
