"""Small CNN for 64x64 single-channel single-cell images + Grad-CAM."""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def _block(cin: int, cout: int) -> nn.Sequential:
    return nn.Sequential(nn.Conv2d(cin, cout, 3, padding=1), nn.BatchNorm2d(cout), nn.ReLU(inplace=True),
                         nn.Conv2d(cout, cout, 3, padding=1), nn.BatchNorm2d(cout), nn.ReLU(inplace=True))


class SmallCNN(nn.Module):
    """4 conv stages (16-32-64-128) -> global average pooling -> linear head."""

    def __init__(self, n_classes: int, in_ch: int = 1):
        super().__init__()
        self.stage1, self.stage2 = _block(in_ch, 16), _block(16, 32)
        self.stage3, self.stage4 = _block(32, 64), _block(64, 128)
        self.dropout = nn.Dropout(0.3)
        self.head = nn.Linear(128, n_classes)

    def features(self, x: torch.Tensor) -> torch.Tensor:
        x = F.max_pool2d(self.stage1(x), 2)   # 32
        x = F.max_pool2d(self.stage2(x), 2)   # 16
        x = F.max_pool2d(self.stage3(x), 2)   # 8
        return self.stage4(x)                 # 8x8, last conv -> Grad-CAM target

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        f = self.features(x)
        return self.head(self.dropout(f.mean(dim=(2, 3))))

    def replace_head(self, n_classes: int) -> None:
        self.head = nn.Linear(self.head.in_features, n_classes)


def grad_cam(model: SmallCNN, x: torch.Tensor, target_class: int) -> np.ndarray:
    """Grad-CAM heatmaps (N, 64, 64) in [0, 1] for `target_class`, from the last conv stage."""
    model.eval()
    feats = model.features(x)
    feats.retain_grad()
    logits = model.head(feats.mean(dim=(2, 3)))
    model.zero_grad()
    logits[:, target_class].sum().backward()
    weights = feats.grad.mean(dim=(2, 3), keepdim=True)            # (N, C, 1, 1)
    cam = F.relu((weights * feats).sum(dim=1, keepdim=True))        # (N, 1, 8, 8)
    cam = F.interpolate(cam, size=x.shape[-2:], mode="bilinear", align_corners=False)[:, 0]
    cam = cam.detach().numpy()
    mx = cam.reshape(len(cam), -1).max(axis=1)[:, None, None]
    return cam / np.maximum(mx, 1e-8)
