# Chrwme Trading Bible Skills for Codex

一套从 **Chrwme Trading Bible Technical Revision** 提炼出的 11 个原子化 Codex skills，用于把 SMC、市场结构、流动性、PDH/PDL、Wyckoff、风险管理和策略验证组织成可执行、可否定、可复盘的分析流程。

这不是简单的书籍摘要。每个 skill 都有清晰的触发边界、执行步骤、失效条件、反例和测试用例，重点避免以下常见误用：

- 把 Liquidity Sweep 自动解释为反转；
- 把任意蜡烛或缺口命名为 OB、FVG、Breaker；
- 只看低时间周期就决定宏观方向；
- 把 PDH/PDL 当成价格必须遵守的固定边界；
- 在账户、合约或费用参数缺失时编造仓位；
- 把教学图或少量回测结果当作已证明的交易优势。

## 一体化版本（推荐）

[`chrwme-trading-system`](chrwme-trading-system/SKILL.md) 是一个可单独安装的总 skill。它把下面 11 个能力放在自己的 `references/modules/` 中，并根据用户问题自动选择最小模块集合：

- 简单问题通常只读取 1 个模块；
- PDH/PDL 反转等复合问题会按“背景 → 结构 → Sweep → 场景 → 风险”的依赖顺序组合模块；
- 输入不足时在当前关卡停止，不让后续模块编造入场、仓位或统计结论；
- 最终只输出一份合并后的分析，不把 11 份回答直接堆给用户。

因此，普通用户只安装 `chrwme-trading-system` 即可。仓库中的 11 个独立 skill 继续保留，供开发、调试或希望手动调用单一能力的用户使用。

## Skills

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

这些 skills 采用组合式设计。单个 skill 只负责一个明确判断，复杂问题可以依次调用多个 skill，减少一个大型提示词同时承担方向、入场、仓位和统计验证所产生的冲突。

## 安装

### 安装一体化版本（推荐）

```powershell
Copy-Item -LiteralPath '.\chrwme-trading-system' `
  -Destination (Join-Path $env:USERPROFILE '.codex\skills') `
  -Recurse
```

### 安装全部独立 skills

克隆仓库后，在 PowerShell 中运行：

```powershell
$target = Join-Path $env:USERPROFILE '.codex\skills'
Get-ChildItem -Directory -Filter 'chrwme-*' |
  Copy-Item -Destination $target -Recurse
```

### 安装单个 skill

```powershell
Copy-Item -LiteralPath '.\chrwme-liquidity-sweep-router' `
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

该问题通常先触发 `chrwme-liquidity-sweep-router`；若随后出现完整的 PDL Reversal 条件，再交给 `chrwme-pdh-pdl-reversal-executor`。涉及仓位时，继续调用 `chrwme-invalidation-risk-sizing`，而不是让前两个 skill 猜测风险比例或合约点值。

## 结构

一体化版本：

```text
chrwme-trading-system/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── composition-patterns.md
│   └── modules/
│       └── 11 个内部模块
├── test-prompts.json
└── test-results.md
```

独立版本：

每个 skill 目录包含：

```text
chrwme-*/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── test-prompts.json
└── test-results.md
```

- `SKILL.md`：触发范围、方法、执行步骤、边界和相邻 skill 路由。
- `agents/openai.yaml`：Codex 展示与调用元数据。
- `test-prompts.json`：3 个应触发、2 个不应触发、1 个边界用例。
- `test-results.md`：对应盲测结果。

## 测试与审计

- 11 个 skill 均通过 Codex `quick_validate.py`。
- 每个 skill 包含 6 条测试，共 66 条。
- 测试由三组独立子代理进行盲测，最终 66/66 通过。
- 其中包含 22 条相邻 skill 混淆用例，用于验证拒绝和路由能力。
- 一体化 `chrwme-trading-system` 也通过 `quick_validate.py`，包含 12 条组合路由、拒绝和缺失输入测试。

这些测试验证的是 skill 的触发、拒绝和执行边界，不证明交易方法本身具有统计优势。

## 文档

- [资料整体理解](docs/BOOK_OVERVIEW.md)
- [可执行精华](docs/DIGEST.md)
- [术语表](docs/GLOSSARY.md)

## 风险声明

本项目用于方法研究和交易流程分析，不构成投资建议、交易信号或盈利保证。原资料没有提供足以证明稳定优势的完整统计记录。任何实盘规则都应经过包含费用与滑点的回测、样本外验证和前向测试；仓位计算必须使用用户自行批准的风险上限及真实合约参数。

## 生成方式

本项目使用 `cangjie-skill` 的长内容蒸馏流程提取候选方法，经过独立性验证、原子化拆分、相邻 skill 路由设计和盲测，再按照 Codex skill 规范整理。
