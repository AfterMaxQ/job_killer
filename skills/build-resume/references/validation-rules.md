# Validation Rules

`build-resume` 的最终完成条件分成三层：Evidence Validation、Content Validation、Mechanical / Rendering Validation。

不要把所有验证都交给脚本。LLM 适合语义判断，脚本只负责确定性检查。

## 1. Evidence Validation — Agent 负责

确认：

- 所有核心 Claim 都能回到候选人事实或用户明确确认；
- Evidence Strength 与 JD 重要度保持独立；
- 团队成果没有全部归为个人成果；
- 课程、自学、项目、真实业务和生产环境没有混淆；
- 所有数字、规模、时间、角色和技术使用范围有真实来源；
- `UNSUPPORTED` 已删除；
- `NEEDS_CONFIRMATION` 未经确认没有进入最终简历。

脚本不能可靠判断“某句话是否夸大事实”，因此这些检查不能假装自动化。

## 2. Content Validation — Agent 负责

确认：

- `positioning.md` 有清晰 Target Identity；
- Top Signals 能在最终经历中得到证明；
- 最强 Evidence 获得主要篇幅；
- 弱相关经历没有抢占核心空间；
- 技能 / 核心能力区不是名词仓库；
- 能力簇来自当前 JD + Evidence，不是固定职业分类；
- 没有机械套完整 STAR；
- 没有为了量化制造数字；
- 没有为了填满页面增加无价值内容；
- ATS 关键词的表达强度没有超过 Evidence。

## 3. Mechanical Validation — Script 负责

运行：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "<task-dir>"
```

Validator 检查：

- 必须存在：`job-model.md`、`match-matrix.md`、`positioning.md`、`resume.md`、`claim-audit.md`；
- 必须文件非空且包含一级标题；
- 不残留 `TODO`、`TBD`、`<placeholder>`、模板 `⟨...⟩`；
- `resume.md` 不出现明确禁用的强熟练度词：`精通`、`专家级`、`熟练掌握`；
- 不出现完全相同的重复 Bullet；
- `claim-audit.md` 中未处理的 `UNSUPPORTED` 会失败；
- 未处理的 `NEEDS_CONFIRMATION` 会失败；
- 当前任务目录和执行时当前目录不应残留 `.aux/.log/.out/.toc/.synctex.gz` 等 LaTeX 临时文件。

这些都是确定性检查，不代表语义审计已经通过。

## 4. Rendering Validation

PDF 构建后运行：

```bash
python .claude/skills/build-resume/scripts/validate-resume.py "<task-dir>" --pdf resume.pdf
```

Validator 检查：

- PDF 文件存在；
- 文件非空；
- 具有 `%PDF-` 文件头；
- 环境存在 `pdfinfo` 时尝试读取页数；
- 无法读取页数时给 warning，不伪造“已验证页数”。

Agent 仍需检查：

- 文本是否溢出；
- 是否有异常换行；
- 是否有空模块；
- 页面空间是否合理；
- 动态技能簇是否被 LaTeX 模板错误改回固定分类。

## 5. Validator Exit Code

```text
0 = 所有确定性 error 检查通过
1 = 至少一个 error
```

Warning 不改变 exit code，但 Agent 必须如实报告未完成的验证，例如：

```text
pdfinfo 不可用，因此只验证了 PDF 文件存在、非空和文件头，没有验证页数。
```

## 6. Failure Handling

### validator exit 1

不得继续把当前结果标记为最终完成。逐项修复后重跑。

### Evidence / Content Validation 失败

不要尝试通过改措辞掩盖事实问题。返回候选人档案或匹配阶段，修正 Claim、Evidence 或内容选择。

### PDF 构建失败

保留：

```text
job-model.md
match-matrix.md
positioning.md
resume.md
claim-audit.md
```

报告实际构建错误，不删除有效 Markdown。

## 7. 最终完成条件

只有以下三项都成立才可以声明简历完成：

```text
Evidence Validation: PASS
Content Validation: PASS
Mechanical / Rendering Validation: PASS（或明确披露非关键 warning）
```

如果没有 XeLaTeX 或无法运行 PDF 构建，只能声明 Markdown 简历与分析完成，不能声称 PDF 已验证。