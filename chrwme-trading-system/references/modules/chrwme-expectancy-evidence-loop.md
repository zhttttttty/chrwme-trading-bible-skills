---
name: chrwme-expectancy-evidence-loop
description: >-
  当用户要用胜率、平均盈利、平均亏损和交易成本评估系统，比较固定 R:R 与真实 Expectancy，或决定回测后是否进入 Forward Testing、何时基于证据更新规则时使用。不适用于用少量交易立即改系统、把回测当未来保证，或在数据不足时宣称策略有 Edge。Triggers: expectancy, backtest, forward test, 期望值, 胜率, 策略复盘。
metadata:
  source_book: "《Chrwme Trading Bible》技术校订版，Chrwme"
  source_chapter: "第3、16、17章"
  tags: [trading, expectancy, backtesting, forward-testing, evidence]
  related_skills:
    - slug: chrwme-invalidation-risk-sizing
      relation: composes-with
---

# Expectancy 与证据更新循环

## R — 原文（Reading）

> “Expectancy =（Win Rate × Average Win）−（Loss Rate × Average Loss）− Trading Costs。历史回测不能保证未来结果，因此还需要 Forward Testing 与持续复盘。”
>
> — 第17章《风险管理》

## I — 方法论骨架（Interpretation）

单笔 R:R 只是系统分布中的一个输入。系统是否可能有 Edge，要同时看胜率、平均盈利、平均亏损、费用、滑点、回撤、连续亏损和市场状态敏感性。历史回测先形成基线，Forward Testing 检查样本外与真实执行，持续复盘只在预设证据门被触发时更新规则。持仓管理的临时变化也属于策略变更，必须重新进入证据循环。

## A1 — 书中的应用（Past Application）

第3、16章允许把 1:1 作为作者原始筛选门，但明确说策略有效性最终应由历史 Expectancy 验证。第17章给出期望值公式，并把回测、前测、回撤、连续亏损和状态敏感性纳入评估。资料没有提供作者模型的真实交易数据，因此不能据此宣称正期望。

## A2 — 触发场景（Future Trigger）

- 用户有交易日志，想计算或解释 Expectancy。
- 用户比较高 R:R 低胜率与低 R:R 高胜率系统。
- 用户经历少量连亏，想知道是否应立即修改规则。
- 用户完成回测，想设计前测和判停条件。

与 `chrwme-invalidation-risk-sizing` 的区别：风险 skill 约束单笔损失；本 skill 判断跨样本系统是否值得继续验证或更新。

## E — 可执行步骤（Execution）

1. **审计样本**：确认交易定义一致、样本区间、费用和滑点已计入；混合不同规则的样本先拆分。
2. **计算基线**：统计胜率、平均盈利、平均亏损、每笔成本、Expectancy、最大回撤和最长连亏；同时给出样本量限制。分批退出还要报告尾部收益集中度，不能只用提高后的“盈利交易比例”评价。
3. **分层检查**：按市场状态、品种、时段、数据类型或规则版本分组，寻找表现是否依赖少数环境。真实合约、连续合约、回溯调整连续序列和指数/CFD 代理必须分开报告，不得拼成同一业绩序列。
4. **前测设计**：冻结规则，设定独立样本、最大风险、观察指标和预先定义的停止/复核条件。
5. **证据更新**：只有执行偏差、成本变化、状态变化或样本外结果触发预设阈值时才修改；修改后建立新版本并重新回测/前测。

## B — 边界（Boundary）

- 回测不能保证未来，正历史 Expectancy 也不等于可交易或适合用户。
- 小样本和过度分组会制造虚假稳定性；必须报告不确定性而非只报点估计。
- 嵌套时间窗口不是独立验证；在近期样本上选出的参数扩展到更长历史，仍然保留选择偏差。
- 分批止盈会改变胜率、平均盈亏、持仓时间和右尾暴露；应与全仓退出版本同时比较收益、回撤、集中度和成本。
- 不能因少数输赢评价决策质量或频繁改规则。
- 本 skill 不替用户选择策略、风险承受度或资金投入，也不把作者框架当成已验证 Edge。

## 相关 skills

- composes-with: `chrwme-invalidation-risk-sizing` — 一致的单笔风险定义是可比较样本的前提。
- evidence standard: [`backtest-evidence-standard.md`](../backtest-evidence-standard.md) — 所有量化绩效请求先用它核对规则冻结、数据层级、样本独立性、指标和压力测试。
- case study: [`nasdaq-futures-pdl-case-study.md`](../nasdaq-futures-pdl-case-study.md) — 仅在 Nasdaq 期货、PDL 反转量化或分批退出研究请求中读取。

## 审计信息

- 三重验证：V1 / V2 / V3 全部通过，见 `../verified.md` 的 v11。
- 行为测试：见 `test-prompts.json` 与 `test-results.md`。
