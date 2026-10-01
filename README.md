# Chrwme Trading Bible Skills for Codex

一个从 **Chrwme Trading Bible Technical Revision** 提炼出的 Codex skill，内含 11 个按需加载的分析模块，用于把 SMC、市场结构、流动性、PDH/PDL、Wyckoff、风险管理和策略验证组织成可执行、可否定、可复盘的分析流程。

这不是简单的书籍摘要。每个 skill 都有清晰的触发边界、执行步骤、失效条件、反例和测试用例，重点避免以下常见误用：

- 把 Liquidity Sweep 自动解释为反转；
- 把任意蜡烛或缺口命名为 OB、FVG、Breaker；
- 只看低时间周期就决定宏观方向；
- 把 PDH/PDL 当成价格必须遵守的固定边界；
- 在账户、合约或费用参数缺失时编造仓位；
- 把教学图或少量回测结果当作已证明的交易优势。

仓库还包含一个独立的
[`Nasdaq Futures PDL Reversal Research Case`](chrwme-trading-system/references/nasdaq-futures-pdl-case-study.md)，
示范如何把周线背景、PDL Sweep、两小时位移、结构止损和分批退出写成可复现规则，并把真实期货、连续合约与代理数据的证据边界分开。它是研究案例，不是第 12 个理论模块，也不是默认参数或交易建议。

## 一体化版本（推荐）

[`chrwme-trading-system`](chrwme-trading-system/SKILL.md) 是一个可单独安装的总 skill。它把下面 11 个能力放在自己的 `references/modules/` 中，并根据用户问题自动选择最小模块集合：

- 简单问题通常只读取 1 个模块；
- PDH/PDL 反转等复合问题会按“背景 → 结构 → Sweep → 场景 → 风险”的依赖顺序组合模块；
- 输入不足时在当前关卡停止，不让后续模块编造入场、仓位或统计结论；
- 最终只输出一份合并后的分析，不把 11 份回答直接堆给用户。

仓库只发布 `chrwme-trading-system` 这一个入口；11 个能力作为内部模块随总 skill 一起安装，不会在 Codex 中显示为 11 个独立入口。

## 内部模块

| Skill | 用途 |
|---|---|
| `chrwme-top-down-analysis-funnel` | 分配高、中、低时间周期的分析职责，形成从背景到执行的漏斗。 |
| `chrwme-structure-state-classifier` | 区分 CHoCH、MSS、BOS 和未确认突破。 |
| `chrwme-liquidity-sweep-router` | 将 Sweep 路由为等待、反转候选或延续候选。 |
| `chrwme-pd-array-quality-filter` | 核对 OB、FVG、Breaker 的机械定义与上下文质量。 |
| `chrwme-five-stage-market-cycle` | 映射 Chrwme 多空五阶段模型，并指出缺失条件。 |
| `chrwme-dynamic-working-range` | 管理 PDH/PDL 工作区间的保留、失效和迁移。 |
| `chrwme-pdh-pdl-reversal-executor` | 核对前日高低点反转模型的完整条件链。 |
| `chrwme-wyckoff-range-classifier` | 根据供需事件链区分吸筹、派发和未定区间。 |
| `chrwme-wyckoff-phase-router` | 区分初始区间后半程与再积累、再派发。 |
| `chrwme-invalidation-risk-sizing` | 从结构失效点反推止损距离和仓位输入。 |
| `chrwme-expectancy-evidence-loop` | 用 Expectancy、回测、前测和版本化复盘更新策略证据。 |

## 推荐调用顺序

```text
Top-down 背景
  → 结构状态
  → 流动性 Sweep 路由
  → PD Array 质量过滤
  → 五阶段 / PDH-PDL / Wyckoff 场景分支
  → 失效点与仓位
  → Expectancy 与证据更新
```

这些模块采用组合式设计。每个模块只负责一个明确判断，总入口根据问题依次加载所需模块，减少一个大型提示词同时承担方向、入场、仓位和统计验证所产生的冲突。

## 安装

```powershell
Copy-Item -LiteralPath '.\chrwme-trading-system' `
  -Destination (Join-Path $env:USERPROFILE '.codex\skills') `
  -Recurse
```

安装后新建一个 Codex 任务，确认对应 skill 出现在可用 skills 列表中。

## 使用示例

```text
价格扫过 PDL 后重新站回，但还没有明显 MSS。
请判断这是反转候选、延续候选还是应该继续等待，
并列出什么证据会确认或推翻当前判断。
```

总入口通常先加载 `liquidity-sweep-router`；若随后出现完整的 PDL Reversal 条件，再加载 `pdh-pdl-reversal-executor`。涉及仓位时继续加载 `invalidation-risk-sizing`，而不是让前两个模块猜测风险比例或合约点值。

## 结构

```text
chrwme-trading-system/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── composition-patterns.md
│   ├── nasdaq-futures-pdl-case-study.md
│   └── modules/
│       └── 11 个内部模块
├── test-prompts.json
└── test-results.md
```

- `SKILL.md`：总入口、自动路由、依赖顺序和停止条件。
- `agents/openai.yaml`：Codex 展示与调用元数据。
- `references/modules/`：11 个内部分析模块。
- `references/nasdaq-futures-pdl-case-study.md`：量化规则、分批退出与数据源边界的实证案例。
- `test-prompts.json`：组合路由、拒绝和缺失输入用例。
- `test-results.md`：总入口路由审计结果。

## 测试与审计

- 打包前，11 个模块来源均通过 Codex `quick_validate.py`。
- 原子模块阶段共完成 66 条独立盲测，最终 66/66 通过，其中包含 22 条相邻模块混淆用例。
- 当前发布的一体化 `chrwme-trading-system` 通过 `quick_validate.py`，并包含 13 条组合路由、拒绝和缺失输入测试。

这些测试验证的是 skill 的触发、拒绝和执行边界，不证明交易方法本身具有统计优势。

## 文档

- [资料整体理解](docs/BOOK_OVERVIEW.md)
- [可执行精华](docs/DIGEST.md)
- [术语表](docs/GLOSSARY.md)

## 风险声明

本项目用于方法研究和交易流程分析，不构成投资建议、交易信号或盈利保证。原资料没有提供足以证明稳定优势的完整统计记录。任何实盘规则都应经过包含费用与滑点的回测、样本外验证和前向测试；仓位计算必须使用用户自行批准的风险上限及真实合约参数。

## 生成方式

本项目使用 `cangjie-skill` 的长内容蒸馏流程提取候选方法，经过独立性验证、原子化拆分、相邻 skill 路由设计和盲测，再按照 Codex skill 规范整理。
