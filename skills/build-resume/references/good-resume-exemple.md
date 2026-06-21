# 雷穗辉 — SDE 实习 @ Amazon Devices Asia

## 基本信息

- 姓名：雷穗辉
- 电话：13533942043
- 邮箱：1455726631@qq.com
- 所在地：广州
- GitHub：github.com/AfterMaxQ

## 教育背景

广东外语外贸大学，软件工程（主修）+ 国际贸易（辅修），本科 | 2023.09 - 2027.06

核心课程：数据结构与算法、计算机网络、操作系统、数据库系统原理、Java 程序设计、软件工程、机器学习、深度学习

竞赛获奖：APMCM 亚太数学建模二等奖、全国大学生统计建模大赛省级三等奖

## 专业技能

后端：Java、Spring Boot 3.5、MyBatis、Spring Security、JWT、Maven 多模块架构
数据库与中间件：MySQL、Redis、RabbitMQ、Elasticsearch、MinIO、ChromaDB
AI 与数据：机器学习、PyTorch、Scikit-learn、XGBoost、FinBERT、Ollama、RAG、LLM Agent 开发
DevOps 与工程化：Docker Compose、Nginx、Cloudflare Tunnel、Git、Streamlit、Linux

## 项目经历

### AllahPan 家庭共享云盘系统 | 独立开发 | 2026.04

技术栈：Spring Boot 3.5 + MyBatis + MySQL + Redis + RabbitMQ + Elasticsearch + MinIO + Vue 3

项目内容：面向家庭场景的私有云盘，解决公有云盘隐私泄露与大文件传输受限痛点

- 设计多模块 Maven 架构，模块职责解耦、搜索服务独立部署；基于 JWT 实现无状态认证与令牌自动刷新；
- 实现分片上传与 MD5 秒传去重，Redis 管理上传会话，MinIO 双 bucket 隔离存储与软删除；
- 基于 RabbitMQ 构建异步文件处理流水线，死信队列 + 指数退避重试；Elasticsearch 多字段加权全文搜索。

项目成果：独立完成架构到部署全流程，已部署家庭服务器并通过 Cloudflare Tunnel 公网访问，GitHub 开源。

### FinanceAgent 金融量化挖掘智能体 | 独立开发 | 2025.12

技术栈：PyTorch + Transformers + DeepSeek API + FinBERT + Pandas + Streamlit + Plotly

项目内容：LLM + 深度学习混合金融决策系统，解决 LLM 金融计算"幻觉"与传统量化分析交互性差的痛点

- 设计 Function Calling 驱动的双脑协同架构，LLM 推理与量化计算解耦，工具注册表插件化扩展；
- 研发 LSTM+Transformer 双头预测模型，交叉注意力融合量价与 FinBERT 情感特征，T+1 准确率 82%；
- 实现 7 套量化工具，Agent 自主规划分析路径并生成结构化投资报告。

项目成果：方向准确率 82%（基准 50%），SEC 财报评估从数小时压缩至秒级，一站式宏观到个股全链路分析。

### 信用风险预测与评分系统 | 独立开发 | 2025.08

技术栈：Python + Pandas + Scikit-learn + XGBoost + Optuna + Streamlit + Joblib

项目内容：为金融机构构建自动化信用风险评估系统，替代人工审批效率低、标准不统一的痛点

- 整合 3 个数据源构建 30+ 特征宽表，VIF+IV/WOE 筛选 10 个核心特征，降低过拟合；
- 针对 9% 违约样本不平衡，SMOTETomek 组合采样平衡训练集，Optuna 超参数自动调优；
- 测试集 AUC 0.98、KS 86%，Streamlit 开发 Web 应用实时输出违约概率与信用评分。

项目成果：数据清洗到 Web 部署完整 ML 链路（GitHub 开源），模型区分能力符合金融风控业务标准。

## 个人评价

1. 软件工程 + 经济学复合背景，对 AI 技术保持高度热情，执行能力强、主动闭环任务，可快速适应新环境
2. 自主学习能力突出，系统掌握 Java 后端与机器学习技术体系，热衷探索 AI 在业务场景中的创新应用

<!--排版配置
个人信息布局: 两列横排
STAR要点数: 3
日期位置: 右侧对齐
技能分段: 按类别分段
自我评价点数: 2
照片: 0.14
-->