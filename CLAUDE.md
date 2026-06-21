
## 文件夹结构

| 目录                                  | 职责                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| `个人信息/`                           | 个人档案数据源（手工维护）：基本信息、项目经历、专业技能、比赛经历、工作经历、自我评价 |
| `个人信息/个人项目经历/项目技术文档/` | 项目深度技术文档（架构、API、数据模型、技术难点），供 interview-question-generator 读取 |
| `temp_resume/`                        | 针对具体 JD 的定制简历（由 build-resume 生成）               |
| `简历pdfs/`                           | 最终 PDF 简历归档                                            |
| `简历pptx/`                           | PPTX 简历归档                                                |
| `简历图片/`                           | 简历图片素材                                                 |
| `images/`                             | 简历照片（you.jpg）                                          |
| `build/`                              | LaTeX 编译临时文件（自动管理）                               |
| `.claude/skills/`                     | Claude Code 技能定义                                         |

## 工作流

| 场景       | 命令/技能                                         | 说明                                                         |
| ---------- | ------------------------------------------------- | ------------------------------------------------------------ |
| 首次使用   | `/first-start`                                    | 引导式初始化，选项 A 功能介绍 + 选项 B 档案初始化            |
| 初始化档案 | `/init-personal-info`                             | 交互式填充 `个人信息/` 各子目录                              |
| 生成简历   | `/build-resume`                                   | 粘贴 JD → 全流程交互 → Markdown → LaTeX → PDF                |
| 面试准备   | `/interview-question-generator`                   | 粘贴 JD → 解析 → 读项目技术文档 → 出题 → 口语化 Q&A          |
| 招聘招呼语 | `/greeting-generator`                             | 粘贴 JD → 生成 Boss 直聘/猎聘等平台招呼语                    |
| HR 沟通    | `/hr-communicator`                                | 粘贴 HR 消息 → 生成回复话术（薪资谈判/离职原因/offer 沟通等） |
| 清理       | `bash .claude/skills/build-resume/shell/clean.sh` | 清理 LaTeX 编译临时文件                                      |

## 技能

- `first-start` — 首次使用引导（功能介绍 + 档案初始化）
- `init-personal-info` — 初始化个人信息文件夹
- `build-resume` — JD → Markdown → LaTeX PDF 全流程简历生成
- `interview-question-generator` — JD + 项目技术文档 → 模拟面试 Q&A
- `greeting-generator` — JD → 招聘平台招呼语
- `hr-communicator` — HR 消息 → 回复话术

## 行为指导

- 简洁优先，大道至简
- 用户让你加东西 → 加上，不是替换
- 不要堆砌无逻辑修饰词显得硬凑
- 修改只碰相关文件，不改无关代码和配置
