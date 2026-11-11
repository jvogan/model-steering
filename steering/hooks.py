"""Request-scoped neuron writes at the MLP down-projection input."""
from __future__ import annotations

import math

import torch

from .tracking import gate, normalize_schedule


def normalize_specs(raw, layers, scale=1.0):
    if not isinstance(raw, list) or not math.isfinite(scale):
        raise ValueError("interventions must be a list and scale must be finite")
    specs = []
    for spec in raw:
        if spec.get("type") != "neuron_add":
            raise ValueError("only neuron_add interventions are supported")
        layer = spec.get("layer")
        if isinstance(layer, bool) or not isinstance(layer, int) or not 0 <= layer < len(layers):
            raise ValueError("layer is outside the decoder")
        weight = layers[layer].mlp.down_proj.weight
        width = weight.shape[1]
        neurons = spec.get("neurons")
        if not isinstance(neurons, list) or not neurons or len(set(neurons)) != len(neurons) or any(
            isinstance(n, bool) or not isinstance(n, int) or not 0 <= n < width for n in neurons
        ):
            raise ValueError(f"neurons must be distinct integers in [0, {width - 1}]")
        values = spec.get("values", 1.0)
        values = [float(values)] * len(neurons) if isinstance(values, (int, float)) else [float(v) for v in values]
        if len(values) != len(neurons) or not all(math.isfinite(v) and math.isfinite(v * scale) for v in values):
            raise ValueError("values must contain one finite value per neuron")
        positions = spec.get("positions", "all")
        gate(positions, 1)
        schedule = normalize_schedule(spec.get("schedule"))
        if any(isinstance(v, (int, float)) and not math.isfinite(v) for v in schedule.values()):
            raise ValueError("schedule numbers must be finite")
        tensor_values = torch.tensor(values, dtype=torch.float32, device=weight.device) * scale
        if not bool(torch.isfinite(tensor_values).all()):
            raise ValueError("scaled values exceed float32 range")
        specs.append({"layer": layer, "positions": positions, "skip_special": bool(spec.get("skip_special", True)),
                      "schedule": schedule, "idx": torch.tensor(neurons, dtype=torch.long, device=weight.device),
                      "values": tensor_values})
    return specs


class NeuronSteering:
    """Apply specs in order and remove every hook when the request exits."""

    def __init__(self, layers, specs, tracker, embed):
        self.layers, self.tracker, self.embed = layers, tracker, embed
        self.specs = [s for s in specs if bool(torch.any(s["values"] != 0))]
        self.handles = []

    def __enter__(self):
        try:
            if self.specs:
                self.handles.append(self.embed.register_forward_pre_hook(lambda _module, args: self.tracker.observe(args[0])))
            grouped = {}
            for spec in self.specs:
                grouped.setdefault(spec["layer"], []).append(spec)
                if spec["schedule"]["type"] == "until_phrase":
                    self.tracker.watch(spec["schedule"]["phrase"])
            for layer, specs in grouped.items():
                self.handles.append(self.layers[layer].mlp.down_proj.register_forward_pre_hook(self._writer(specs)))
            return self
        except Exception:
            self.close()
            raise

    def _writer(self, specs):
        def write(_module, args):
            if not self.tracker.forwards:
                raise RuntimeError("token tracker must observe input IDs before neuron writes")
            x = args[0]
            if self.tracker.seq_len != x.shape[-2]:
                raise RuntimeError("token tracker and MLP sequence lengths differ")
            active = [(s, m) for s in specs if (m := self.tracker.weight(
                s["positions"], s["skip_special"], s["schedule"])) is not False]
            if not active:
                return None
            x = x.clone()
            for spec, mask in active:
                current = x[..., spec["idx"]].float()
                new = current + spec["values"] * mask.float()[..., None]
                x[..., spec["idx"]] = new.to(x.dtype)
            return (x, *args[1:])
        return write

    def close(self):
        for handle in self.handles:
            handle.remove()
        self.handles.clear()

    def __exit__(self, *_exc):
        self.close()
