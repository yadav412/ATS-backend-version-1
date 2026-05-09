"""Resume vs job skill matching (public + internal HM skills only; no company keyword table)."""

from __future__ import annotations

import json
import re


def json_skill_array(raw: object) -> list:
    """Normalize job.skills / internal_required_skills from Text JSON or already-parsed list."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            val = json.loads(raw)
            return val if isinstance(val, list) else []
        except Exception:
            return []
    return []


def job_posting_skill_phrases_for_match(job) -> list[str]:
    """Phrases for match %: public Required Skills + internal_required_skills, deduped (case-insensitive)."""
    seen: set[str] = set()
    ordered: list[str] = []

    def _add_list(raw_list: list) -> None:
        for s in raw_list:
            t = (s if isinstance(s, str) else str(s)).strip()
            if not t:
                continue
            k = t.lower()
            if k not in seen:
                seen.add(k)
                ordered.append(t)

    _add_list(json_skill_array(getattr(job, "skills", None)))
    _add_list(json_skill_array(getattr(job, "internal_required_skills", None)))

    return ordered


def resume_skill_match_percent(resume_lower: str, phrases: list[str]) -> tuple[float, int, int]:
    clean = [p.strip() for p in phrases if (p or "").strip()]
    if not clean:
        return (0.0, 0, 0)
    if not resume_lower or not resume_lower.strip():
        return (0.0, 0, len(clean))
    matched = sum(1 for ph in clean if ph.lower() in resume_lower or re.search(re.escape(ph.lower()), resume_lower))
    pct = min(100.0, round(100.0 * matched / len(clean), 1))
    return (pct, matched, len(clean))
