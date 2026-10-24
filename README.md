# DSH Knowledge Base

把几本书读成 Agent Skill，再配上一套可复用的提示词模板和个人知识库。

这个仓库里的每个 `*-skill` 目录都是一个**可直接投喂给 AI Agent 的知识库**：遵循 `SKILL.md` + `references` 的渐进式披露结构，Agent 先读 `SKILL.md` 判断该不该加载，再按章节检索原文。

## 目录结构

```
.
├── agentic-ai-skill/        《一本书讲透Agentic AI》     13 章
├── chaoji-tishici-skill/    《超级提示词》(AFP 架构)      10 章
├── wanxiaozhuan-skill/      《玩转Skill》                12 章
├── zhinengshidai-skill/     《智能时代》                  7 章
├── 提示词模板库/             可复用提示词模板
└── 知识库/                  个人知识库（IT / AI / 英语 / UC / 历史）
```

## 四个书知识库

| Skill | 原书 | 作者 | 出版 | 章数 | 解决什么 |
|---|---|---|---|---|---|
| `agentic-ai-skill` | 一本书讲透 Agentic AI | 王吉伟 | 机械工业出版社 2026.1 | 13 | 项目该不该上 Agent、怎么设计 Agentic Workflow、成熟度与治理 |
| `chaoji-tishici-skill` | 超级提示词 | 郭泽德 | 机械工业出版社 2026.5 | 10 | AFP 架构；为什么提示词"写得很长却不好用"；怎么把一次性指令做成可复用系统 |
| `wanxiaozhuan-skill` | 玩转 Skill | 程希冀 | 机械工业出版社 2026.4 | 12 | 怎么把专家经验固化成 Skill；Skill 为什么不被触发或执行不稳 |
| `zhinengshidai-skill` | 智能时代 | 吴军 | 中信 2016 | 7 | 一项业务能否"变成数据问题"；大数据思维 vs 机械思维 |

## 单个 Skill 的内部结构

以 `agentic-ai-skill/` 为例，四个库都是同一套形态：

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 入口。含 `name` / `description` 元数据与使用说明，Agent 据此决定是否加载 |
| `chapters/chNN-*.md` | 逐章结构化提取：核心论点、框架、案例、可操作结论 |
| `cheatsheet.md` | 一页速查 |
| `patterns.md` | 可复用的设计模式 / 反模式 |
| `glossary.md` | 术语表 |

## 怎么用

**作为 Agent Skill 加载** —— 把某个 `*-skill` 目录放进 Agent 的 skills 目录即可，`SKILL.md` 的 `description` 就是触发条件。

**当普通笔记读** —— 直接读 `SKILL.md` 概览，再按需跳章节，不必线性通读。

**检索式提问** —— 每个 `chapters/` 文件名都带章节语义（如 `ch05-afp-architecture.md`），按主题定位比全文搜索快。

## 另外两个目录

- **`提示词模板库/`** —— 通用六段模板、语气模板，以及周工作日志 / 小红书热点 / 检索摘要 / 比价摘要等场景模板
- **`知识库/`** —— 分类整理的个人知识库，含索引、每日/月度速递脚本

## 说明

各 `SKILL.md` 头部标注了原书的作者、出版社、字数与生成日期，内容是**结构化提炼**而非原文复制，用于理解与检索；引用原文请以纸书或正版电子书为准。

---

生成时间：2026-10
