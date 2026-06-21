---
name: interview-question-generator
description: 当用户需要生成面试题、进行模拟面试准备、或根据JD和项目代码定制技术面试Q&A时使用。触发条件：用户提到"面试题""面试准备""mock interview""interview prep""模拟面试""帮我做面试题""怎么准备这个岗位"、或粘贴JD要求生成针对性面试准备材料
---

# Interview Question Generator

## Overview

Generate mock interview Q&A that teaches the user how to **talk through** their project in a real interview — explaining architecture, design decisions, and tradeoffs in their own words. Not a code quiz.

**JD Integration:** If the user provides a job description (JD), the skill parses it to extract what the employer cares about, then maps those requirements to the project's actual code/design. Every question anchors to a specific JD concern — so the user knows exactly which part of the JD each answer targets. Without a JD, the skill falls back to pure codebase-driven Q&A.

## Core Principle

**In a real interview, nobody asks you to recite code.** They ask you to explain your thinking. The skill generates answers structured for oral delivery: clear narrative, logical reasoning, design rationale. Code references exist only as anchors for verbal explanation ("in our FileProcessReceiver, we handled retries by..."), never as the answer itself.

**With a JD, answers bridge two things:** what the employer is looking for, and what you actually built. The narrative becomes: "JD asks for X — in our project, we handled X by..."

## When to Use

- User asks for "interview questions," "mock interview," or "interview prep"
- User wants to practice explaining their project verbally
- User needs structured Q&A that tests understanding, not memorization
- User pastes a job description (JD) and asks for targeted interview prep
- User says "这个岗位怎么准备面试" or similar JD + prep combo

**Do NOT use for:** generic textbook Q&A, LeetCode-style problems, behavioral questions unrelated to the codebase.

## Core Process

### Phase 0: JD Check

Before anything else, check if the user provided a JD:

- If the user pasted a JD (job description with requirements/responsibilities): proceed to **Phase 1: Parse JD**
- If the user just said "面试题" or "interview prep" with no JD attached: ask once — "有 JD 的话贴一下，我可以针对性地出面试官最可能问的题。没有的话我就直接看代码出通用的。" Then skip to Phase 2 (skip Phase 1 & 3)

### Phase 1: Parse JD

**Only if a JD was provided.** Extract structured information from the JD. Parse directly — do not ask the user questions.

**Output — JD 解析摘要：**

| 维度 | 提取内容 |
|------|---------|
| 硬技能 | 语言/框架/中间件/DB/云平台等明确要求 |
| 业务领域 | 电商/金融/SaaS/数据平台/企业软件等 |
| 关键词 | "高并发""0到1""重构""带人""核心模块""性能优化"等 |
| 隐性信号 | JD 反复强调的词 → 面试必问方向（例如 JD 三次提到"性能"，意味着至少有 2 道题要围绕性能展开） |
| 职级信号 | 通过措辞判断——"参与"vs"负责"vs"主导"；"了解"vs"熟悉"vs"精通" |

**Output — 面试官最可能追问的 3-5 个方向：**
```
1. [方向] — 因为 JD 强调 [具体表述]
2. [方向] — 因为 JD 强调 [具体表述]
...
```

**Key rule:** Every JD phrase you extract must be traceable to a specific sentence in the JD. Don't invent requirements.

### Phase 2: Explore with JD Lens

Build a mental model of the project's technology and architecture:

1. Read `CLAUDE.md` (or equivalent) for tech stack and architecture overview
2. Scan key source files: security config, core services, message queue setup, cache layer, frontend state
3. Identify the project's **signature patterns** — the interesting design decisions an interviewer would want to hear about

**Checklist — confirm you understand:**
- [ ] Tech stack (every layer: framework, DB, cache, MQ, search, frontend)
- [ ] Module structure and dependency chain
- [ ] Auth flow end-to-end
- [ ] Core business pipeline (e.g., file upload → process → index)
- [ ] Resilience patterns (retry, degradation, caching)
- [ ] Frontend data flow (API → store → component)

**If a JD was provided, also confirm:**
- [ ] JD 要求的每个技术栈，项目中用到了吗？怎么用的？
- [ ] JD 的关键词（高并发/性能/重构等），项目中哪些设计决策能回应？
- [ ] JD 隐含的职级预期，项目中的复杂度能匹配吗？如果不能，哪些地方需要补充说明？

**JD 驱动扫描策略：**
- 不要在 JD 没提到的技术细节上花太多时间
- JD 强调的方向（如 "性能优化"），深挖相关代码和设计
- JD 提到的技术栈中，项目没用到的要标记——面试可能被问到"为什么不用 X"

### Phase 3: Map JD ↔ Project

**Only if a JD was provided.** Skip to Phase 4 if no JD.

Build a mapping table connecting each JD requirement to the project's actual implementation. This table is the blueprint for all subsequent question generation.

**Mapping table format:**

| JD 要求 | 项目对应点 | 出题方向 | 优先级 |
|---------|-----------|---------|--------|
| "高并发系统设计" | RabbitMQ 削峰 + Redis 缓存 | 怎么用文件处理流水线讲清楚并发设计 | 高 |
| "数据库设计能力" | MySQL 元数据 + ES 全文搜索 | 为什么双存储，不做单一库？ | 高 |
| "CI/CD 经验" | （项目未涉及） | — | 跳过 |

**Rules:**
- **JD 强调 + 项目能展示 → 高优先级，必出题**（多出 1-2 道追问）
- **JD 强调 + 项目薄弱 → 标记跳过或降权**（可出 1 道"诚实承认+讲思路"的题）
- **JD 未提 + 项目有亮点 → 低优先级**（最多 1 道，作为加分项）
- **JD 提到 + 项目完全没有 → 准备 1 道"诚实回答"型题**："我们项目没用 X，但我知道它的原理是..."

**保底验证：** 映射表完成后，对照 JD 逐条检查——每个 JD 核心要求至少有一条映射（出题或诚实回答）。

### Phase 4: Ask

Ask the user TWO required questions before generating. Do NOT proceed until both are answered.

#### Question 1: 题量

> 你想生成多少道面试题？（建议 5–15 道）

#### Question 2: 分类占比

> 你希望各类型题目的占比是怎样的？

**如果用户没有明确说占比**，给出推荐方案让用户选择：

根据项目实际技术栈，提供 2–3 个预设方案：

```
方案 A — 均衡覆盖：各类型按默认权重分配
  架构 15% | 后端 20% | 前端 15% | 数据/缓存 10%
  安全 10% | 异步/消息 10% | 搜索 5% | 存储 10% | 可靠性 5%

方案 B — 后端深度：聚焦服务端设计和数据流
  架构 20% | 后端 30% | 数据/缓存 15% | 安全 10%
  异步/消息 10% | 存储 10% | 前端 5%

方案 C — 全栈均衡：前后端各半
  后端 25% | 前端 25% | 架构 15% | 数据/缓存 10%
  安全 10% | 存储 10% | 异步/消息 5%
```

**如果用户提供了 JD：** 在三个预设方案外增加 **方案 D — JD 驱动**，作为推荐方案：

```
方案 D — JD 驱动（推荐）：按 JD 关注点自动分配权重
  [根据 JD 实际内容，列出各类别的建议题数和理由]
  例如 JD 偏后端 → 架构 20% | 后端 30% | 数据/缓存 15%...
```

方案 D 是针对这份 JD 定制的最佳分配。但保留用户选择 A/B/C 的权利。

**如果用户已经给了占比**，复述确认：

> 确认一下：你要的是 [N] 道题，[总结占比]。我按这个分配来生成？

得到用户确认后再继续。

#### 可选追问

- 目标难度？（初级 / 中级 / 高级，默认按项目实际深度）
- 特别想深挖的方向？（如"多问点缓存穿透那块"）

Wait for the user's response to BOTH required questions before proceeding.

### Phase 5: Categorize

根据用户确认的分类占比，把题目分配到具体类别。各类别覆盖内容如下（跳过项目未使用的类别）：

| Category | What it covers |
|----------|---------------|
| Architecture & Design | Module split, data flow, why this structure |
| Backend Core | Service design, API design, Spring patterns |
| Frontend | Component design, state management, real-time updates |
| Data & Caching | DB design, Redis strategy, cache penetration/avalanche |
| Security & Auth | Login flow, token design, access control |
| Async & Messaging | Message queues, scheduled tasks, event flow |
| Search & Indexing | ES design, indexing strategy, search API |
| Storage & Files | Upload pipeline, chunking, dedup, storage backend |
| Reliability | Fault tolerance, retry logic, graceful degradation, testing |

**分配规则：**
- 用户指定了百分比 → 严格按用户给的来
- 用户选了预设方案 → 按预设方案的权重计算具体题数
- 题数不能整除时，优先补到后端和架构类别

### Phase 6: Generate — Oral-First Answers

This is the critical phase. Every answer must read like something you'd **say out loud in an interview**.

### JD Anchor (per question, when JD provided)

Each question opens with a JD anchor line that tells the user WHY this question exists:

```
> 🎯 对应JD："[JD 中的原表述]"
```

When answering in an interview, the user mentally links back to this JD requirement — the answer serves the JD.

## Answer Structure (Oral-First)

Every answer follows this narrative structure:

```
Q: [Specific question tied to the project]
> 🎯 对应JD："[JD 中的原表述]"  ← 如有 JD

A:

**一句话概述** — 用一句话说清楚这是什么

**整体思路** (1-2 句)
先讲清楚面对什么问题，选择了什么方案，为什么。

**具体怎么做** (分点，口头叙述风格)
- 先做什么 → 为什么这一步在前
- 然后做什么 → 这里的关键考虑是什么
- 最后做什么 → 结果是什么

**为什么这样设计** (2-3 个关键决策)
- 选了 A 而不是 B，因为...
- 这里有个坑是 X，我们通过 Y 来规避...
- 如果直接做 Z 会有什么问题，所以我们...

**边界和取舍** (如适用)
- 这个方案在什么场景下不够用
- 如果用户量增长 10 倍，哪里需要改

**追问准备** (1-2 句，JD 核心关注方向时必填)
- 如果面试官继续追问"[更深或相关的追问]"，你可以说...
```

## Writing Rules for Answers

### ✅ DO — Oral style

- 用"我们"、"你" 这样的口语化表达
- 先讲"为什么"再讲"怎么做"
- 把技术决策讲成故事：遇到了什么问题 → 想了什么办法 → 为什么选了这个
- 代码只作为口头叙述的佐证，偶尔提及类名/方法名即可
- 多用对比："如果不用 X，就会出现 Y 问题"
- 如果提供了 JD，答案中自然融入 JD 语言："JD 要求高并发经验，我们在项目中..."

### ❌ DON'T — Written documentation style

- 不要大段粘贴代码
- 不要罗列配置项和参数
- 不要像 API 文档一样列举每个方法
- 不要用"第一步、第二步"这种书面化序号
- 不要让答案看起来像 README

### Comparison: Wrong vs Right

**❌ Wrong (written doc style):**
```
Q: 文件上传后的处理流程是怎样的？

FileProcessReceiver.handle() 方法接收 FileProcessMessage。
首先 switch message.getCurrentStage():
  case UPLOADED -> thumbnailGenerator.generate(file)
  case THUMBNAILED -> textExtractor.extract(file)
  case TEXT_EXTRACTED -> esIndexService.index(file)
异常时检查 retryCount < MAX_RETRY，计算 delay = 30000 * (1 << retryCount)
```

**✅ Right (oral style):**
```
Q: 文件上传完成后，后端怎么处理这个文件？

一句话概述：文件上传后进入一个四阶段的处理流水线，由 RabbitMQ 驱动，
每个阶段处理完再投递到下一阶段，失败自动重试。

整体思路：
用户文件上传完只是存到了 MinIO，后面还有缩略图、文本提取、搜索索引
这些事情比较耗时，不能堵在上传请求里同步做。所以我们用消息队列把这些
步骤串成一个异步流水线。

具体怎么做：
- 上传完成后，先发一条消息到 RabbitMQ，标记阶段为 UPLOADED
- 消费者拿到消息，第一步是生成缩略图。这里有个细节——先发下阶段消息
  再更新数据库状态。顺序反了的话，消息发失败了数据库却已经改了状态，
  这条文件就卡住了。先发消息，失败了抛异常，数据库没动，下次重试还从
  当前阶段开始
- 第二步是文本提取，PDF、Word、图片都在这步处理。图片我们还接了一个
  本地的 Ollama 模型做 OCR，但这个不是必需的，挂了也不影响主流程
- 第三步是建 ES 索引，让文件内容可以被全文搜索

为什么这样设计：
- 异步而不是同步：上传是用户操作，等太久体验很差。异步处理虽然用户
  看不到中间过程，但我们在前端用 SSE 实时推送状态变化，用户能看到
  "处理中→已完成"的转变
- 指数退避重试：失败后不是马上重试，而是 30s → 60s → 120s 递增。
  如果是基础设施抖动，等一等就好了；如果三次都失败，区分一下是
  Redis/ES 挂了（降级，文件还能用）还是数据库写失败（标记失败）
- 状态机而不是线性流程：每个阶段独立，即使某一步挂了，前面的工作
  不白做。而且后续如果要加新步骤（比如病毒扫描），插在中间就行

边界：
- 如果文件量很大，单条队列会有瓶颈，后续可以按用户分片
- Ollama OCR 是本地模型，处理大图会很慢，生产环境可能需要换云端 OCR
```

## Question Quality Checklist

For each generated question, verify:

- [ ] Question is project-specific (not "What is Redis?")
- [ ] Answer starts with one-sentence summary
- [ ] Answer explains WHY before HOW
- [ ] Answer uses oral/conversational language
- [ ] Answer mentions specific design tradeoffs
- [ ] No code blocks longer than 5 lines
- [ ] File/class references are narrative anchors, not the main content
- [ ] Answer includes at least one "如果不用 X，就会 Y" comparison

## Output Format

```markdown
# [项目名] 模拟面试 Q&A

> 技术栈：[简要列举]
> JD 解析：[如果提供了 JD，列出关键要求摘要；如果没有，此行省略]
> 题目数：N | 难度：[级别]

---

## JD 解析摘要（如有 JD）

| 硬技能 | 业务领域 | 关键词 | 高频追问方向 |
|--------|---------|--------|------------|
| [...] | [...] | [...] | [...] |

---

## 分类：[类别名]

### Q1: [问题]
> 🎯 对应JD："[JD中的具体表述]"  ← 如有 JD

[口语化回答]

> 💡 追问准备：[如适用，JD 核心方向必填]

### Q2: [问题]
> 🎯 对应JD："[JD中的具体表述]"  ← 如有 JD

[口语化回答]

> 💡 追问准备：[如适用]

---

(重复所有分类和题目)
```

## Complete JD-Driven Example

**Input JD (excerpt):**

```
高级后端开发工程师
要求：熟悉 Java/Spring Boot，有高并发系统设计经验，熟悉消息队列和缓存，
具备数据库设计能力，有系统性能优化经验优先
```

**Phase 1 Output — JD 解析：**

| 维度 | 提取 |
|------|------|
| 硬技能 | Java, Spring Boot, MQ, 缓存, DB |
| 业务领域 | 未明确 |
| 关键词 | "高并发""设计经验""性能优化" |
| 隐性信号 | "高级"+"设计"→ 面试会追问架构决策能力；"性能优化"单独标为"优先" |
| 职级信号 | "高级"+"设计经验"+"具备...能力" → P6/高级工程师 |

**面试官最可能追问的 3 个方向：**
1. 高并发设计 — JD 排第二 + "系统设计经验"
2. 性能优化 — 独立列为"优先"项
3. 数据库设计 — 写的是"设计能力"不是"使用经验"

**Phase 3 Output — 映射表：**

| JD 要求 | 项目对应点 | 出题方向 | 优先级 |
|---------|-----------|---------|--------|
| 高并发系统设计 | RabbitMQ 削峰 + Redis 缓存 + 异步流水线 | 文件处理流水线怎么扛并发 | 高 |
| 性能优化经验 | ES 索引优化 + 缓存命中率策略 | 搜索性能怎么一步步优化的 | 高 |
| 数据库设计能力 | MySQL 元数据 + ES 全文搜索双存储 | 为什么双存储，数据一致性怎么保证 | 高 |
| 熟悉消息队列 | RabbitMQ 四阶段文件处理 pipeline | 消息可靠性怎么保证，失败怎么处理 | 中 |

**Resulting Q (excerpt):**

### Q1: 你们系统的文件处理流程怎么保证高并发下的稳定性？

> 🎯 对应JD："有高并发系统设计经验"

一句话概述：文件上传后通过 RabbitMQ 驱动一个四阶段异步流水线，削峰填谷，保证上传接口不被耗时处理拖垮。

整体思路：用户上传是同步操作需要即时响应，但后续缩略图、文本提取、索引构建都很耗时——如果同步处理，上传一个文件要等好几秒，多用户时直接打满线程池。所以我们用消息队列把上传和处理解耦。

具体怎么做：
- 上传完成后，先发一条消息到 RabbitMQ，标记阶段为 UPLOADED。这里有个细节——先发消息再写数据库状态，顺序反了会出问题：消息发失败了但数据库已经改了状态，这条文件就卡住了
- 消费者拿到消息后，按 UPLOADED → THUMBNAILED → TEXT_EXTRACTED → INDEXED 四个阶段依次处理，每阶段完成发下一阶段消息。阶段独立的好处是某一步挂了前面的不白做
- Redis 缓存上传状态，前端通过 SSE 实时看到进度变化

为什么这样设计：
- 异步而不是同步：上传是用户操作，等太久体验差。异步后用 SSE 推状态，用户能看到"处理中→已完成"
- 指数退避重试：30s → 60s → 120s。瞬时抖动自愈，三次都失败再告警，区分是基础设施问题还是数据问题
- 阶段独立 + 状态机：后续加病毒扫描等步骤只需插在中间，不影响现有流程

边界：
- 单条队列有吞吐上限，QPS 再涨需要按用户哈希分片
- 当前重试策略对瞬时故障友好，持久故障需要人工介入

> 💡 追问准备：如果面试官问"并发再涨 10 倍怎么办"，可以说——瓶颈在 RabbitMQ 单队列吞吐，可以做 consumer 水平扩展 + 按用户哈希分片；如果消息量到百万级可以换 Kafka 做分区并行消费。

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 答案像技术文档 | 想象你在会议室对着白板讲，不是写 README |
| 大段粘贴代码 | 代码最多 5 行，只用于口头叙述的佐证 |
| 先讲怎么做再讲为什么 | 永远先讲"为什么"，建立 context 再展开细节 |
| 只讲 happy path | 一定要讲异常场景和边界条件 |
| 不对比方案 | 每个设计决策都要提到被放弃的替代方案 |
| 生成前不问数量和分类 | Phase 4 (Ask) 是强制步骤 |
| 全是后端题 | 前端、架构、可靠性各占合理比例 |
| 生成了 JD 提到但项目中没用到的技术的题 | 标记跳过，或改成"诚实回答"型题（"我们没用 X，但我知道..."） |
| JD 关键词没有在答案中呼应 | 每道 JD 锚定的题，答案中至少呼应一次 JD 原表述 |
| JD 提供了但不调整分类权重 | 启动方案 D，JD 强调的方向多出题 |
