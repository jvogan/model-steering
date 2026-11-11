"""ATEM token masks and request-local steering schedules."""
from __future__ import annotations

import json
import math
import re
from typing import Any

import torch

POSITIONS = ("all", "prompt", "decode", "reasoning", "final")
CHANNELS = {"none": 0, "header": 1, "reasoning": 2, "final": 3, "other": 4}
PHRASE_WINDOW = 64


def gate(positions: str, seq_len: int) -> bool:
    """Phase test from the forward's length. A prefill forward carries the whole prompt
    (seq_len > 1); a cached decode forward carries one token. reasoning and final are decode positions."""
    if positions == "all":
        return True
    if positions == "prompt":
        return seq_len > 1
    if positions in ("decode", "reasoning", "final"):
        return seq_len == 1
    raise ValueError(f"positions must be one of {POSITIONS}")


def normalize_schedule(schedule: dict[str, Any] | None) -> dict[str, Any]:
    """constant; cosine {period, floor, ramp, anchor: final_header|decode_start}; until_phrase {phrase, then}."""
    schedule = schedule or {"type": "constant"}
    kind = schedule.get("type")
    if kind == "constant":
        return {"type": "constant"}
    if kind == "cosine":
        out = {"type": "cosine", "period": float(schedule.get("period", 24)), "floor": float(schedule.get("floor", 0.25)),
               "ramp": float(schedule.get("ramp", 1)), "anchor": schedule.get("anchor", "final_header")}
        if not (out["period"] > 0 and out["ramp"] > 0 and math.isfinite(out["floor"])) \
                or out["anchor"] not in ("final_header", "decode_start"):
            raise ValueError("cosine schedule needs period > 0, ramp > 0, finite floor, anchor final_header|decode_start")
        return out
    if kind == "until_phrase":
        phrase, then = schedule.get("phrase"), schedule.get("then", "off")
        if not isinstance(phrase, str) or not phrase.strip():
            raise ValueError("until_phrase schedule needs a nonempty phrase")
        after = 0.0 if then == "off" else float(then)
        return {"type": "until_phrase", "phrase": phrase.lower(), "then": then, "after": after}
    raise ValueError("schedule type must be constant, cosine or until_phrase")


def schedule_multiplier(schedule: dict[str, Any], decode_k: int, final_k: int | None, seen: set[str]) -> float:
    """Write multiplier for one row at one decode step. k counts decode tokens from the anchor;
    before a final_header anchor appears the cosine multiplier is 0."""
    if schedule["type"] == "constant":
        return 1.0
    if schedule["type"] == "until_phrase":
        return schedule["after"] if schedule["phrase"] in seen else 1.0
    k = final_k if schedule["anchor"] == "final_header" else decode_k
    if k is None or k < 0:
        return 0.0
    wave = schedule["floor"] + (1 - schedule["floor"]) * (1 + math.cos(2 * math.pi * k / schedule["period"])) / 2
    return min(1.0, (k + 1) / schedule["ramp"]) * wave


class TokenTracker:
    """Follows the ATEM channel of every position from the token ids each forward embeds.

    A message opens at <|start|>; its header runs to <|message|> ("assistant to=self" is
    reasoning, "assistant" or "to=user" is final, any other recipient is "other"), and its
    body ends at <|eom|> or <|eot|>. ``skip`` marks header positions, special-token positions,
    the position after a special token, and ``skip_after`` further positions. Each row also
    counts decode steps, tokens after the latest final-channel header, and watched phrases.
    """

    def __init__(self, special_ids, tags: dict[str, int], decode, attention_mask=None, skip_after: int = 0):
        self.special, self.tags, self.decode = set(special_ids) | set(tags.values()), tags, decode
        self.attention_mask, self.skip_after = attention_mask, skip_after
        self.rows: list[dict[str, Any]] | None = None
        self.seq_len, self.forwards = 0, 0
        self.skip = self.channel = self.valid = None
        self.phrases: set[str] = set()
        self._cache: dict[Any, Any] = {}

    def watch(self, phrase: str) -> None:
        self.phrases.add(phrase.lower())

    def observe(self, ids: torch.Tensor) -> None:
        values = ids.tolist()
        seq_len = len(values[0])
        if self.rows is None:
            self.rows = [{"state": "none", "channel": 0, "header": [], "left": 0, "decode_k": -1,
                          "final_k": None, "generated": [], "seen": set()} for _ in values]
        mask = None
        if seq_len > 1 and self.attention_mask is not None and self.attention_mask.shape[-1] == seq_len:
            mask = self.attention_mask.bool().tolist()
        skip, channel, decoding = [], [], seq_len == 1
        for row_ids, state, row_mask in zip(values, self.rows, mask or [None] * len(values)):
            if decoding:
                state["decode_k"] += 1
                state["generated"].append(row_ids[0])
                if state["final_k"] is not None:
                    state["final_k"] += 1
            row_skip, row_channel = [], []
            for position, token in enumerate(row_ids):
                if row_mask is not None and not row_mask[position]:
                    row_skip.append(True)
                    row_channel.append(0)
                    continue
                special = token in self.special
                header = state["state"] == "header" and not special
                row_skip.append(special or header or state["left"] > 0)
                row_channel.append(CHANNELS["header"] if header
                                   else state["channel"] if state["state"] == "body" and not special else 0)
                state["left"] = 1 + self.skip_after if special else max(0, state["left"] - 1)
                if token == self.tags["start"]:
                    state.update(state="header", header=[], channel=0)
                elif token == self.tags["message"] and state["state"] == "header":
                    found = re.search(r"to=(\S+)", self.decode(state["header"]))
                    recipient = found.group(1) if found else "user"
                    state.update(state="body", channel=CHANNELS["reasoning"] if recipient == "self"
                                 else CHANNELS["final"] if recipient == "user" else CHANNELS["other"])
                    if decoding and state["channel"] == CHANNELS["final"]:
                        state["final_k"] = -1  # the next token is body token k = 0
                elif token in (self.tags["eom"], self.tags["eot"]):
                    state.update(state="none", channel=0)
                elif header:
                    state["header"].append(token)
            skip.append(row_skip)
            channel.append(row_channel)
            if decoding and self.phrases:
                text = self.decode(state["generated"][-PHRASE_WINDOW:]).lower()
                state["seen"].update(phrase for phrase in self.phrases if phrase in text)
        self.seq_len, self.forwards, self._cache = seq_len, self.forwards + 1, {}
        self.skip = torch.tensor(skip, dtype=torch.bool, device=ids.device)
        self.channel = torch.tensor(channel, dtype=torch.int8, device=ids.device)
        self.valid = None if mask is None else torch.tensor(mask, dtype=torch.bool, device=ids.device)

    def mask(self, positions: str, skip_special: bool):
        """[B, T] write mask for the current forward, or False when no position qualifies."""
        key = (positions, skip_special)
        if key not in self._cache:
            if not gate(positions, self.seq_len):
                value = False
            else:
                value = torch.ones_like(self.skip) if self.valid is None else self.valid.clone()
                if positions in ("reasoning", "final"):
                    value &= self.channel == CHANNELS[positions]
                if skip_special:
                    value &= ~self.skip
            self._cache[key] = value
        return self._cache[key]

    def weight(self, positions: str, skip_special: bool, schedule: dict[str, Any]):
        """mask() times the schedule multiplier per row; schedules apply at decode steps only."""
        mask = self.mask(positions, skip_special)
        if mask is False or schedule["type"] == "constant" or self.seq_len > 1:
            return mask
        key = (positions, skip_special, json.dumps(schedule, sort_keys=True))
        if key not in self._cache:
            factors = [schedule_multiplier(schedule, row["decode_k"], row["final_k"], row["seen"]) for row in self.rows]
            self._cache[key] = mask.float() * torch.tensor(factors, device=mask.device)[:, None]
        return self._cache[key]


class LineTracker(TokenTracker):
    """TokenTracker with an optional per-row line rule: lines[i] = N also skips each newline token on row i and the
    N positions after it; lines[i] = None leaves row i exactly as TokenTracker marks it.

    Each row keeps its own newline countdown, separate from the special-token one, so neither shortens or lengthens
    the other. The rule applies to specs with skip_special enabled."""

    def __init__(self, *args, lines: list[int | None] | None = None, newlines: frozenset[int] = frozenset(), **kwargs):
        super().__init__(*args, **kwargs)
        self.lines, self.newlines = lines, newlines
        self.line_left = [0] * len(lines) if lines else []

    def observe(self, ids: torch.Tensor) -> None:
        super().observe(ids)
        if not self.lines or all(after is None for after in self.lines):
            return
        values = ids.tolist()
        if len(values) != len(self.lines):
            raise ValueError(f"{len(self.lines)} line rules for a batch of {len(values)} rows")
        valid = [None] * len(values) if self.valid is None else self.valid.tolist()
        extra = []
        for row, (row_ids, row_valid, after) in enumerate(zip(values, valid, self.lines)):
            if after is None:
                extra.append([False] * len(row_ids))
                continue
            left, flags = self.line_left[row], []
            for position, token in enumerate(row_ids):
                if row_valid is not None and not row_valid[position]:
                    flags.append(False)  # padding: the parent already skips it
                    continue
                newline = token in self.newlines
                flags.append(newline or left > 0)
                left = after if newline else max(0, left - 1)
            self.line_left[row] = left
            extra.append(flags)
        self.skip = self.skip | torch.tensor(extra, dtype=torch.bool, device=self.skip.device)
