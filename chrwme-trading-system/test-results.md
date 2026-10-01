# Router test results — chrwme-trading-system

- Test type: route-table and boundary audit
- Cases: 13
- Result: 13/13 passed

| Case | Selected route | Result |
|---|---|---|
| route-01 | top-down → working range → sweep → structure → reversal → risk | PASS |
| route-02 | PD Array quality only | PASS |
| route-03 | structure state only | PASS |
| route-04 | Wyckoff range → phase router | PASS |
| route-05 | invalidation/risk sizing only | PASS |
| route-06 | expectancy/evidence only | PASS |
| route-07 | top-down → structure | PASS |
| route-08 | five-stage cycle only | PASS |
| route-09 | expectancy/evidence + risk; Nasdaq futures case reference | PASS |
| reject-01 | reject; fundamental research | PASS |
| reject-02 | reject; live-price tool | PASS |
| edge-01 | risk module, then stop for missing inputs | PASS |
| edge-02 | top-down module, then stop for missing timeframe | PASS |

This audit verifies routing coverage, dependency order, and stop conditions. It
does not establish a statistical trading edge or guarantee identical wording.
