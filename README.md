# Ambiguity Budget

## Gauge card

```text
DECISION POINTS  fixed before review
ROUND 1          statuses + cited source lines
REVISION         no dimension may regress
CLEAR            total weighted ambiguity is within budget
```

A specification can be grammatically complete and still leave several materially different implementations valid. This contract makes that uncertainty countable. The owner names two to eight decision points and a maximum budget. Validators fetch the whole specification and label each point `RESOLVED`, `MULTIPLE`, or `MISSING`, with exact line indexes and a digest of the bytes they read.

Contract code assigns weights 0, 2, and 3. A designated reviewer may submit a new public revision only while the review needs work. Every dimension must stay equal or improve, and the total must fall strictly. A single new ambiguity rejects the entire revision instead of being hidden by improvements elsewhere.

## Demonstrated rounds

The controlled draft fixture leaves launch timing and the closed launch-region set with multiple answers, while final approval is missing. The revision fixes a UTC launch time, a closed region set, an exclusive approval role, and rollback ownership. Live evidence records both finalizations and a rejected post-clear replay. The fixtures are operator-controlled review material, not third-party attestations.

## Check locally

```powershell
genvm-lint contracts\contract.py
pytest -q tests
```
