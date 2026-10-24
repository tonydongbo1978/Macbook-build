# 第 4 章：如何使用 Skill

## 核心思想
Skill 的"安装"就是**把文件夹放到约定目录**，平台自动扫描、按需加载。理解各平台的路径与触发方式，比记住某个工具的界面更重要——因为标准统一，Skill 可以跨工具迁移。

## 本章框架

- **主流平台与路径（书中快照，版本变化快）**：
  | 平台 | 项目级 | 全局级 | 特点 |
  |---|---|---|---|
  | Claude Code | `.claude/skills/` | `~/.claude/skills/` | 生态核心，`/skill` 手动触发，有权限管理 |
  | TRAE（字节） | `.trae/skills/` | `~/.trae/skills/` | 可视化 Skill 管理面板 |
  | OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` | 开源，多模型后端，细粒度权限 |
  | Google Antigravity | `.agent/skills/` | `~/.gemini/antigravity/skills/` | Agent 优先，多智能体并行 |
  | Cursor | `.cursor/skills/`（也扫 `.claude/skills/`、`.agents/skills/`） | `~/.cursor/skills/` 等 | `/` 搜索调用；`/migrate-to-skills` 迁移旧规则 |
  | Codex（OpenAI） | `.agents/skills/`（向上逐级扫描到仓库根） | `~/.agents/skills/` | 内置 `$skill-creator`、`$skill-installer` |
- **触发方式三种**：自动（模型读 description 判断）、手动（`/skill` 或 `/` 搜索）、显式限定（`disable-model-invocation: true`）。
- **不用编程工具也能用**：网页版/桌面版智能体（如支持 Skill 的工作平台）同样可以加载；限制在于本地文件与命令权限。
- **获取他人 Skill**：官方仓库（Anthropic 的 docx/xlsx/pdf/skill-creator）、社区市场、GitHub；安装＝复制文件夹或解压 `.skill`。
- **来源优先级**：项目级 > 全局级 > 扩展/插件级（同名时）。

## 关键概念
- **项目级 / 全局级 / 组织级**：三层作用域；团队场景可加"组织级"统一分发。
- **自动触发**：依赖 description 的语义匹配。
- **显式调用**：避免误触发的手段。
- **跨平台兼容**：OpenSkills 标准带来的"一次编写，多处运行"。

## 心智模型
- **"路径即安装"**：没有安装程序，只有目录约定。
- **"先手动，再自动"**：新 Skill 先用 `/` 显式调用验证，稳定后再交给自动触发。
- **"平台是壳，Skill 是核"**：换工具不该重写能力。

## 反模式
- 把 Skill 放在错误层级（项目专用却放全局，污染所有会话）。
- 依赖某个平台的私有格式（迁移即失效）。
- 装了十几个功能重叠的 Skill（description 互相竞争，触发混乱）。

## 关键结论
1. 学会看目录约定，就能在任意支持 OpenSkills 的工具里用同一套 Skill。
2. 触发质量取决于 description，而不是平台。
3. 团队应统一"权威来源"目录，避免同名多版本。

## 连接
- **第 2 章**：目录结构与元数据规范。
- **第 12 章**：团队级的库管理与分发。
- **第 6 章**：description 与边界的设计方法。
