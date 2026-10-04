"""LoRA from scratch: freeze W, learn a rank-r correction B·A."""
import torch
import torch.nn as nn


class LoRALinear(nn.Module):
    """Wraps a frozen nn.Linear and adds a trainable low-rank update."""

    def __init__(self, base: nn.Linear, r=8, alpha=16):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad = False                       # the wall stays painted
        self.A = nn.Parameter(torch.randn(r, base.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(base.out_features, r))   # B = 0 => ΔW = 0
        self.scale = alpha / r

    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.scale


def apply_lora(model, r=8, alpha=16, targets=("q_lin", "v_lin")):
    """Freeze everything, wrap the target projections, unfreeze the head."""
    for p in model.parameters():
        p.requires_grad = False
    for layer in model.distilbert.transformer.layer:
        for name in targets:
            setattr(layer.attention, name,
                    LoRALinear(getattr(layer.attention, name), r, alpha))
    for p in model.pre_classifier.parameters():
        p.requires_grad = True
    for p in model.classifier.parameters():
        p.requires_grad = True
    return model

