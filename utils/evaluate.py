

from collections.abc import Mapping, Sequence
from typing import Any

from metric.metric import Metric    
from metric.types import RelevanceJudgments


DELTA_REPORT_TOLERANCE = 1e-9


class Evaluator:

    @staticmethod
    def evaluate(qrels : Mapping[str, RelevanceJudgments], 
                 runs : Mapping[str, Sequence[str]], 
                 metric: Metric) -> dict[str, Any]:
        per_query = {}
        for query_id, relevance in qrels.items():
            retrieved_ids = runs.get(query_id, [])
            per_query[query_id] = metric.score(relevance, retrieved_ids)

        scores = list(per_query.values())
        mean_value = metric.mean(scores)
        excluded = sum(score is None for score in scores)

        return {
            "metric": metric.__class__.__name__,
            "k": metric.k,
            "per_query": per_query,
            "mean_score": mean_value,
            "num_evaluated_queries": len(scores) - excluded,
            "num_excluded_queries": excluded
        }

    @staticmethod
    def compare_reports(baseline: dict, candidate: dict) -> dict:
        improved = []
        regressed = []
        unchanged = []
        excluded = []
        per_query_delta = {}
        if baseline['metric'] != candidate['metric']:
            raise ValueError("Baseline and candidate metrics must be the same")
        if baseline['k'] != candidate['k']:
            raise ValueError("Baseline and candidate k must be the same")
        if baseline['per_query'].keys() != candidate['per_query'].keys():
            raise ValueError("Baseline and candidate must have the same set of queries")
        for query_id, query_score in baseline['per_query'].items():
            candidate_score = candidate['per_query'].get(query_id)
            if query_score is None and candidate_score is None:
                excluded.append(query_id)
                continue
            if query_score is None or candidate_score is None:
                raise ValueError(f"Inconsistent evaluation coverage for {query_id}")
            delta = candidate_score - query_score 
            if delta > DELTA_REPORT_TOLERANCE :
                improved.append(query_id)
            elif delta < -DELTA_REPORT_TOLERANCE :
                regressed.append(query_id)
            else:
                unchanged.append(query_id)

            per_query_delta[query_id] = delta

        mean_delta = sum(per_query_delta.values()) / len(per_query_delta) if per_query_delta else None

        return {
            "metric": candidate['metric'],
            "k": candidate['k'],
            "mean_delta": mean_delta,
            "per_query_delta": per_query_delta,
            "improved": improved,
            "regressed": regressed,
            "unchanged": unchanged,
            "excluded": excluded,
        }

    @staticmethod
    def check_regression(
        comparison: dict,
        max_mean_drop: float,
        max_query_drop: float,
    ) -> dict:
        # reject negative threshold values
        if max_mean_drop < 0:
            raise ValueError("max_mean_drop must be non-negative")
        if max_query_drop < 0:
            raise ValueError("max_query_drop must be non-negative")
        
        # if no query is evaluated return inconsistent
        if not comparison["per_query_delta"]:
            return {
                "status": "INCONCLUSIVE",
                "reasons": ["no queries evaluated"],
            }
        
        reasons = []

        #fail if the mean delta < -max_mean_drop
        if comparison["mean_delta"] is not None and comparison["mean_delta"] < -max_mean_drop - DELTA_REPORT_TOLERANCE:
            reasons.append("mean delta below threshold")
        
        # fail if query delta < -max_query_drop
        for query_id, delta in comparison["per_query_delta"].items():
            if delta < -max_query_drop - DELTA_REPORT_TOLERANCE:
                    reasons.append(f"query {query_id} dropped by {abs(delta)}, max allowed drop is {max_query_drop}")
        return {
            "status": "FAIL" if reasons else "PASS",
            "reasons": reasons,
        }

