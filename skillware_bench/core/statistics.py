# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Statistical variance engine, Pass@k estimators, and confidence intervals for benchmark runs."""

import math
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased estimator for Pass@k (HumanEval/Chen et al. formulation).

    Args:
        n: Total number of samples evaluated per problem.
        c: Number of correct/passing samples (c <= n).
        k: Threshold k (k <= n).
    """
    if n - c < k:
        return 1.0
    if c == 0:
        return 0.0

    # 1.0 - comb(n - c, k) / comb(n, k)
    return 1.0 - float(math.comb(n - c, k)) / float(math.comb(n, k))


@dataclass
class MetricDistribution:
    """Summary statistics for a continuous benchmark metric across N repetitions."""

    mean: float
    std_dev: float
    min: float
    max: float
    confidence_interval_95: List[float] = field(default_factory=list)

    @classmethod
    def from_samples(cls, samples: List[float]) -> "MetricDistribution":
        if not samples:
            return cls(mean=0.0, std_dev=0.0, min=0.0, max=0.0, confidence_interval_95=[0.0, 0.0])

        n = len(samples)
        mean_val = sum(samples) / float(n)
        variance = sum((x - mean_val) ** 2 for x in samples) / float(max(1, n - 1))
        std_val = math.sqrt(variance) if n > 1 else 0.0

        # Normal/t 95% margin of error (z=1.96 approximation for n >= 5)
        margin = 1.96 * (std_val / math.sqrt(n)) if n > 1 else 0.0
        ci = [round(max(0.0, mean_val - margin), 2), round(mean_val + margin, 2)]

        return cls(
            mean=round(mean_val, 2),
            std_dev=round(std_val, 2),
            min=round(min(samples), 2),
            max=round(max(samples), 2),
            confidence_interval_95=ci,
        )


@dataclass
class MultiRunStatistics:
    """Comprehensive multi-run statistical evaluation for a model on a scenario."""

    scenario_id: str
    model: str
    repetitions: int
    pass_at_1: float
    pass_at_k: float
    k_evaluated: int
    scores: MetricDistribution
    latencies: MetricDistribution
    tokens: MetricDistribution

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "model": self.model,
            "repetitions": self.repetitions,
            "pass_at_1": self.pass_at_1,
            "pass_at_k": self.pass_at_k,
            "k_evaluated": self.k_evaluated,
            "scores": asdict(self.scores),
            "latencies": asdict(self.latencies),
            "tokens": asdict(self.tokens),
        }


class StatisticalEvaluator:
    """Aggregates repeated crucible runs to calculate Pass@k and statistical variance."""

    @classmethod
    def aggregate_runs(
        cls,
        scenario_id: str,
        model: str,
        run_scores: List[float],
        run_latencies: List[float],
        run_tokens: List[int],
        pass_threshold: float = 70.0,
        k: int = 5,
    ) -> MultiRunStatistics:
        n = len(run_scores)
        if n == 0:
            raise ValueError("Cannot aggregate empty run results")

        passing_count = sum(1 for s in run_scores if s >= pass_threshold)
        pass_1 = round(passing_count / float(n), 4)

        eval_k = min(k, n)
        pass_k_val = round(pass_at_k(n=n, c=passing_count, k=eval_k), 4)

        return MultiRunStatistics(
            scenario_id=scenario_id,
            model=model,
            repetitions=n,
            pass_at_1=pass_1,
            pass_at_k=pass_k_val,
            k_evaluated=eval_k,
            scores=MetricDistribution.from_samples(run_scores),
            latencies=MetricDistribution.from_samples(run_latencies),
            tokens=MetricDistribution.from_samples([float(t) for t in run_tokens]),
        )
