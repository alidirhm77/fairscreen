"""
Tamper-evident audit trail.

Every decision (AI ranking, human override, twin test) is appended as a record whose
hash includes the previous record's hash — a hash chain. Editing any past record
breaks the chain, and verify() shows exactly where. Exportable as CSV / JSON.
"""
import hashlib
import json
from datetime import datetime, timezone


class AuditLog:
    def __init__(self):
        self.records: list[dict] = []

    def add(self, event: str, actor: str, candidate: str = "", detail: dict | None = None) -> dict:
        prev = self.records[-1]["hash"] if self.records else "GENESIS"
        rec = {
            "seq": len(self.records) + 1,
            "time_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "event": event,
            "actor": actor,
            "candidate": candidate,
            "detail": json.dumps(detail or {}, ensure_ascii=False, sort_keys=True),
            "prev_hash": prev,
        }
        rec["hash"] = self._hash(rec)
        self.records.append(rec)
        return rec

    @staticmethod
    def _hash(rec: dict) -> str:
        body = {k: rec[k] for k in ("seq", "time_utc", "event", "actor", "candidate", "detail", "prev_hash")}
        return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    def verify(self) -> tuple[bool, int | None]:
        prev = "GENESIS"
        for r in self.records:
            if r["prev_hash"] != prev or self._hash(r) != r["hash"]:
                return False, r["seq"]
            prev = r["hash"]
        return True, None
