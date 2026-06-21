# LaTeX 格式与排版参考

> 供 build-resume SKILL.md 阶段五/七引用。Agent 在组装 LaTeX 前 Read 此文件。

## 排版配置 → LaTeX 映射表

| 配置项 | 值 | LaTeX 实现 |
|--------|-----|-----------|
| 个人信息布局 | 单列纵排 | 每字段独立 `\SimpleEntry{...}` |
| 个人信息布局 | 两列横排 | `\SimpleEntry` 配合宽度调整 |
| STAR 要点数 | 3 | `\Content{}{}{}` |
| STAR 要点数 | 2 | `\Contenttwo{}{}` |
| 日期位置 | 右侧对齐 | `\datedsubsection{}{日期}`（默认） |
| 技能分段 | 按类别 | `{后端：xxx}` `{前端：xxx}` 每类一行 |
| 自我评价点数 | N | N 个 `{N.xxx}` |
| 照片 | 有+宽度 | `\yourphoto{0.xx}` |
| 照片 | 无 | 注释掉 `\yourphoto` 行 |

---

## LaTeX 格式参考

### \SimpleEntry（个人信息行）

```latex
\SimpleEntry{\makebox[11em][l]{\prefix{电话：}13533942043}\prefix{邮箱：}1455726631@qq.com}
\SimpleEntry{\makebox[11em][l]{\prefix{所在地：}广州}\prefix{GitHub：}\href{https://github.com/AfterMaxQ}{github.com/AfterMaxQ}}
```

用户没有的字段直接删除对应行，不保留空行。

### \datedsubsection + \Content（项目经历，3 点）

标准项目结构：项目名称 | 角色 | 时间 + 技术栈 + 项目内容 + 核心工作（3点）+ 项目成果

```latex
\datedsubsection{\textbf{项目名称}，角色（独立开发/核心开发）}{时间}
{\prefix{技术栈：}核心框架 + 中间件 + 数据库（精准关键词，不堆砌）}
\par
{\prefix{项目内容：}1句话讲清项目定位与核心问题（不超过2行）}
\Content
{ 动作 + 技术 + 场景 + 结果 第一点，字+字符不超过60 ；}
{ 动作 + 技术 + 场景 + 结果 第二点，字+字符不超过60 ;}
{ 动作 + 技术 + 场景 + 结果 第三点，字+字符不超过60 。}
{\prefix{项目成果：}量化产出、优化效果或落地情况}
```

### \datedsubsection + \Contenttwo（项目经历，2 点）

```latex
\datedsubsection{\textbf{项目名称}，角色}{时间}
{\prefix{技术栈：}...}
\par
{\prefix{项目内容：}...}
\Contenttwo
{ 动作 + 技术 + 场景 + 结果 第一点，字+字符不超过60 ；}
{ 动作 + 技术 + 场景 + 结果 第二点，字+字符不超过60 。}
{\prefix{项目成果：}...}
```

### 多项目分隔

项目之间使用 `\projectsep`（浅灰虚线），定义在 `resume.cls`：

```latex
{\prefix{项目成果：}...}
\projectsep
% --- 项目N ---
\datedsubsection{\textbf{项目名称}，角色}{时间}
```

### 教育背景

标准结构（单段学历）：

```latex
\section{教育背景}
\datedsubsection{\textbf{学校名称}，专业全称，\textit{学历}}{入学时间 - 毕业时间}
{GPA x.x/4.0（专业前xx\%）}  % 有优势则写，标注满分
\par
{\prefix{核心课程：}课程1、课程2、...（8-10门，与岗位高度匹配）}
\par
{\textbf{学业荣誉：}xxx}  % 可选，按含金量排序
```

- GPA 低于 3.0 或无突出排名则不写
- 核心课程只列专业核心课/方向选修课，不放公共课（马原、大学英语、体育等）
- 课程按 JD 相关度排序，高分课程可标注分数如「数据库系统原理（94分）」

### 学生工作

```latex
\datedsubsection{部门，岗位，\textit{负责xxx工作}}{开始 - 结束}
```

### 个人评价

```latex
\section{个人评价}
{1.xxx}

{2.xxx}

{3.xxx}
```

每点 30-45 字。

### 专业技能

```latex
\section{专业技能}
{\prefix{后端：}Spring Boot、MyBatis、Spring Security...}

{\textbf{前端：}Vue 3、HTML5、JavaScript}

{\textbf{数据库：}MySQL、Redis、Elasticsearch...}
```

按技能类别分段，每段一行，按 JD 相关度排序。技能名称不加括号注解（版本号、配置细节等留给面试展开）。

**技能精选原则**：
- 每行不超过 5 个技术名词，只列最核心、最匹配 JD 的技术
- 重合度高的技术合并（如 `MySQL、Redis、Elasticsearch` 不额外加 `SQLite、ChromaDB`）
- 优先列 JD 明确要求的技术栈，其次列与岗位强相关的，其余果断删掉
- 宁可少列被问到再展开，不要堆砌让人质疑深度
- 禁止将基础调用方式列为专业技能
- **熟练度**：默认不加，如果用户选择则询问是否加熟练度。用户要求时加「熟练」或「掌握」，禁止「精通」。格式：`后端（熟练）`

---

## 排版规范

填充 LaTeX 模板时，必须遵守以下排版规则：

### 1. 行宽控制 — 杜绝溢出

- 每条 `\Content` 要点 `{ ... }` 内字符总数（含标点、空格）不超过 **60 字**
- 技术术语不得在行尾断开换行，必要时用 `\mbox{Spring Boot}` 包裹

### 2. 间距统一 — 拒绝参差

- `\section{}` 之间的垂直间距由模板 `\vspace{}` 统一控制
- `\Content` / `\Contenttwo` bullet 项间距由 `resume.cls` 的 `parsep=1.2ex` 统一控制，不在 resume.tex 中手动 `\setlist`
- 技能行、自评行等段落间距由 `resume.cls` 的 `\parskip=0.6ex` 统一控制
- 个人信息区域 `\SimpleEntry{}` 行间距均匀，相邻行基线对齐
- 不额外插入 `\\` 或 `\vspace` 破坏模板预设间距
- **LaTeX 换行规则**：连续 `{...}` 组不会自动换行，渲染为同一段落连续文字。多个 `{...}` 组之间必须用 `\par` 显式换行（如技术栈与项目内容之间、GPA 与核心课程之间）

### 3. 日期对齐 — 右边界齐平

- 所有 `\datedsubsection{}{}` 第二个花括号右对齐
- 日期格式统一为 `YYYY.M - YYYY.M` 或 `YYYY.M`

### 4. 页面平衡 — 避免虎头蛇尾

- 内容均匀填充整页
- 最后只剩 1-2 行跨到第二页 → 压缩；内容只占半页 → 适当增加间距

### 5. 孤行控制 — 不落单

- `\subsection{}` 标题不得单独留在页底
- 最后一条 STAR 要点不得孤零零出现在下一页开头

### 6. 字体规范

| 用途 | 中文 | 英文 | 字号 |
|------|------|------|------|
| 板块大标题 | 黑体 | Times New Roman | 14pt |
| 二级标题 | 宋体 | Times New Roman | 12pt |
| 正文描述 | 宋体 | Times New Roman | 10.5pt |
| 右侧辅助信息 | 宋体 | Times New Roman | 10pt |

**字重**：仅板块标题和项目/竞赛名称可加粗，正文描述、bullet 点、技术术语一律不加粗。

### 7. 编译后复核

编译成功后必须提醒用户打开 PDF 检查：
- 是否有文字跑出右边距？
- 各模块间距是否均匀？
- 日期列是否对齐？
- 加粗是否仅限板块标题（正文不得出现 `\textbf{}`）？
