# Chrwme Trading Bible — 可执行精华

> 本文不是交易信号，也不是对原资料的逐章摘要。它把通过三重验证的 11 个方法组织成一条可执行、可否定、可复盘的分析链。原资料中的图表属于教学示例，不能当作真实交易记录或统计优势证明。

## 1. 核心思想：先建立情景，再寻找执行

这套资料最有价值的地方，不是某个独立术语，而是它要求把市场分析拆成不同层级。高时间周期负责背景与方向，中时间周期负责结构和位置，低时间周期只负责确认与执行。这样可以避免从一根低周期蜡烛直接推导宏观方向，也避免先决定多空，再到图上寻找支持自己的证据。

完整流程可以概括为：

1. 用高时间周期识别趋势、盘整、关键流动性与主要价格区间。
2. 用中时间周期判断价格当前处于区间何处，结构是否真的发生变化。
3. 把流动性扫取视为一个需要后续证据的事件，而不是自动反转信号。
4. 检查位移、结构确认和 PD Array 是否共同支持同一情景。
5. 只有在失效点、入场距离、仓位上限和退出逻辑都可定义时，才进入执行评估。
6. 用样本外前测、费用后的结果和版本化记录更新系统证据。

对应模块：[`chrwme-top-down-analysis-funnel`](../chrwme-trading-system/references/modules/chrwme-top-down-analysis-funnel.md)、[`chrwme-structure-state-classifier`](../chrwme-trading-system/references/modules/chrwme-structure-state-classifier.md)。

## 2. 结构语言：CHoCH、MSS、BOS 不是同义词

结构判断的重点不在于给每个拐点贴标签，而在于区分“警报”“确认”和“延续”。

- **CHoCH**：当前行为与此前节奏不一致，是潜在变化的早期警报，但通常不足以独立确认反转。
- **MSS**：在流动性事件、位移和关键结构破坏等证据配合下，市场状态发生了更有意义的转移。
- **BOS**：沿已确认方向突破结构，主要用于确认延续，而不是自动定义反转。
- **未确认突破**：只有影线越界、缺乏位移、快速收回或没有关键收盘确认时，应保留为未定状态。

任何结构标签都应同时记录：被突破的具体摆动点、突破方式、收盘位置、位移质量、前置流动性事件，以及什么新证据会推翻当前分类。若这些字段缺失，最诚实的输出是“证据不足”，而不是补全故事。

对应模块：[`chrwme-structure-state-classifier`](../chrwme-trading-system/references/modules/chrwme-structure-state-classifier.md)。

## 3. 流动性扫取：事件之后必须分流

等高、等低、前高、前低等位置可能聚集订单，但从图表本身不能证明具体机构意图。价格刺穿流动性后至少有三种合理路径：

- 快速拒绝并出现反向位移，成为反转候选；
- 在边界附近接受并继续推进，成为延续候选；
- 缺乏清晰位移或结构确认，继续等待。

因此，Sweep 的正确用途是启动路由，而不是直接下单。需要观察刺穿后是否收回、是否出现明确位移、是否破坏有意义的结构，以及回撤位置是否存在合格的价格数组。仅有影线或仅有“扫了前高/前低”的叙述，都不足以判定反转。

对应模块：[`chrwme-liquidity-sweep-router`](../chrwme-trading-system/references/modules/chrwme-liquidity-sweep-router.md)。

## 4. PD Array：定义正确不等于可以交易

Order Block、Fair Value Gap 和 Breaker 容易被当作静态矩形，但资料更适合被理解为上下文过滤器：

- **Order Block** 需要与后续位移、结构变化及位置相关，不能把任意反向蜡烛都命名为 OB。
- **FVG** 描述三蜡烛结构中的不平衡，但不保证必然回补，也不保证触及后反转。
- **Breaker** 需要先有原结构被明确失效，再讨论角色转换；不能只因价格穿过一个区块就命名。

质量过滤至少包括定义是否成立、形成原因、所在区间位置、与当前结构方向是否一致、是否已经被反复消耗，以及失效条件。PD Array 是安排回撤和风险位置的候选区域，不是独立信号。

对应模块：[`chrwme-pd-array-quality-filter`](../chrwme-trading-system/references/modules/chrwme-pd-array-quality-filter.md)。

## 5. 五阶段模型：用缺失条件约束叙事

作者的多空模型可以整理为五段：流动性事件、位移、结构确认、回撤至合格区域、向下一目标扩展。它适合用于检查情景完整度，而不是把所有走势强行塞进固定模板。

执行时应逐项标注“已出现、未出现、无法判断”，并明确缺失的关键条件。例如，已经扫低但没有向上位移，只能说第一阶段可能出现；已经位移但没有破坏关键结构，也不能跳到回撤执行。阶段标签必须能够被后续价格行为推翻。

对应模块：[`chrwme-five-stage-market-cycle`](../chrwme-trading-system/references/modules/chrwme-five-stage-market-cycle.md)。

## 6. PDH/PDL：动态工作区间，不是永久支撑阻力

前日高点和前日低点可以定义一个日内工作区间，用来观察溢价、折价、边界扫取、接受与迁移。但这个区间是动态的：

- 短暂刺穿后快速收回，可能保留原区间，但仍需结构证据；
- 在边界外持续接受，原区间的解释力下降；
- 新的信息形成后，应更新工作区间，而不是永远围绕昨日边界叙事。

前日边界反转需要条件链：价格到达有意义的边界或流动性位置，发生扫取或测试，随后出现反向位移和结构确认，再等待合格回撤区域。缺少任一关键环节时，都应输出等待或失效，而不是“靠近边界就反向”。目标也不能机械地设为区间另一端；应结合途中结构、流动性和风险收益约束。

对应模块：[`chrwme-dynamic-working-range`](../chrwme-trading-system/references/modules/chrwme-dynamic-working-range.md)、[`chrwme-pdh-pdl-reversal-executor`](../chrwme-trading-system/references/modules/chrwme-pdh-pdl-reversal-executor.md)。

## 7. Wyckoff：事件链优先于图形相似

吸筹和派发不是看到横盘后凭位置猜测。更稳健的做法是观察供需事件链：初步支撑或供应、高潮、自动反应、二次测试、假突破或弹簧、强弱信号，以及测试后的接受情况。若事件不完整或互相矛盾，应分类为未定。

初始区间的后半程与趋势中的再积累、再派发也应分开。判断重点包括此前是否已有明确趋势、当前区间在更大结构中的位置、突破方向和回测表现。Wyckoff 分类描述的是供需演化假说，不等同于作者五阶段执行模型；二者可以互相提供背景，但不能互相替代。

对应模块：[`chrwme-wyckoff-range-classifier`](../chrwme-trading-system/references/modules/chrwme-wyckoff-range-classifier.md)、[`chrwme-wyckoff-phase-router`](../chrwme-trading-system/references/modules/chrwme-wyckoff-phase-router.md)。

## 8. 风险：从失效点反推仓位

风险管理的次序应是：先定义情景何时错误，再测量入场到失效点的距离，最后依据允许风险和合约规格计算仓位。不能先选择想要的仓位，再把止损塞进一个方便的位置。

基础关系为：

`仓位上限 = 单笔允许亏损金额 /（止损距离 × 每点价值 + 预计费用与滑点）`

如果缺少账户规模、风险上限、点值、合约乘数、手续费或滑点数据，skill 应指出缺失字段，而不是编造精确仓位。结构止损也不保证成交价格等于计划价格；跳空、流动性和市场冲击仍需单独考虑。

对应模块：[`chrwme-invalidation-risk-sizing`](../chrwme-trading-system/references/modules/chrwme-invalidation-risk-sizing.md)。

## 9. 证据：从漂亮案例走向可更新系统

教学图只能解释概念，不能证明策略有优势。系统评价需要至少记录胜率、平均盈利、平均亏损、交易费用和样本数量，并计算：

`Expectancy = 胜率 × 平均盈利 − 败率 × 平均亏损`

更重要的是建立证据循环：冻结规则版本，使用一致的数据和费用假设回测，保留样本外区间，再进行前向测试，记录偏差与执行错误，最后只在有证据时修改规则。小样本的正期望、只展示成功案例或在同一数据上反复调参，都不能证明稳定优势。

对应模块：[`chrwme-expectancy-evidence-loop`](../chrwme-trading-system/references/modules/chrwme-expectancy-evidence-loop.md)。

## 10. 一次完整分析应该怎样输出

假设用户只给出一张局部图，并问“这里能不能做多”。这套方法不应立刻给出肯定或否定答案，而应把输出分成五层：

1. **已知事实**：列出图中能够直接观察的时间周期、摆动高低点、PDH/PDL、是否越界、收盘位置和明显位移。不要把“机构吸筹”写成事实。
2. **当前分类**：说明高周期背景是否可见，结构处于 CHoCH 警报、MSS 确认、BOS 延续还是未确认；Sweep 属于反转候选、延续候选还是等待。
3. **缺失信息**：若看不到更高周期、交易日时区、合约点值、费用或关键蜡烛收盘，应明确要求补充。截图之外的信息不能凭经验补齐。
4. **条件分支**：例如“若价格收回 PDL 后出现向上位移并破坏相关摆动高点，再等待合格回撤；若在 PDL 下方持续接受，则撤销反转候选并重估工作区间”。两个分支都应有可观察条件。
5. **风险与证据**：只有失效位可定义且账户与合约数据齐全时才计算仓位；即使当前 setup 通过，也应说明它是否属于经过回测的固定规则版本。

一个合格的简化输出可以采用以下模板：

- 背景：可见 / 不可见；当前 Bias 及证据。
- 结构：标签、被突破摆动点、位移与收盘质量。
- 流动性：被测试的池、Sweep 后路径分类。
- 区域：候选 OB/FVG/Breaker 的定义核对与失效条件。
- 决策：等待 / 条件性候选 / 规则不适用；不要用“必涨”“必跌”。
- 风险：失效距离、缺失的仓位参数、最大允许风险由用户规则决定。
- 更新条件：什么后续行为会确认、降级或推翻当前结论。

这类输出的价值不是预测得更像，而是让用户能在下一根 K 线出现后检查此前判断是否仍成立。可否定性越清楚，复盘时越不容易用事后叙事保护原结论。

## 11. 常见陷阱

1. 把 Sweep 直接翻译为反转。
2. 把任意反向蜡烛、缺口或被穿越区域分别命名为 OB、FVG、Breaker。
3. 用低周期噪声决定高周期方向。
4. 看到一个 CHoCH 就宣告趋势彻底反转。
5. 把 PDH/PDL 当作永不变化的支撑阻力。
6. 用图形相似度替代 Wyckoff 事件链。
7. 先定仓位，再寻找止损位置。
8. 把教学案例、回测片段或少量胜单当作稳定统计优势。
9. 用“机构一定在……”解释无法从价格数据直接验证的意图。
10. 在关键输入缺失时输出伪精确的入场、止损、目标或仓位。

## 12. 推荐调用顺序

对于一张待分析图表，可按以下顺序调用：

1. [`chrwme-top-down-analysis-funnel`](../chrwme-trading-system/references/modules/chrwme-top-down-analysis-funnel.md)
2. [`chrwme-structure-state-classifier`](../chrwme-trading-system/references/modules/chrwme-structure-state-classifier.md)
3. [`chrwme-liquidity-sweep-router`](../chrwme-trading-system/references/modules/chrwme-liquidity-sweep-router.md)
4. [`chrwme-pd-array-quality-filter`](../chrwme-trading-system/references/modules/chrwme-pd-array-quality-filter.md)
5. 根据场景选择五阶段、PDH/PDL 或 Wyckoff 分支
6. [`chrwme-invalidation-risk-sizing`](../chrwme-trading-system/references/modules/chrwme-invalidation-risk-sizing.md)
7. [`chrwme-expectancy-evidence-loop`](../chrwme-trading-system/references/modules/chrwme-expectancy-evidence-loop.md)

这 11 个 skills 的共同约束是：把事实、推断和未知分开；给每个结论提供失效条件；在缺少必要输入时停止补全；把风险控制和证据质量放在术语叙事之前。
