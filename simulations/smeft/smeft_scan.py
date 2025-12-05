#!/usr/bin/env python3
import math
import csv
import argparse
from dataclasses import dataclass
from typing import List, Tuple

# Simple SMEFT collider-reach scan for contact operators
# This is a toy estimator: sigma ~ (C/Λ^2)^2 * S, with channel-dependent S.

CHANNELS = {
    "dilepton": {"S": 1.0, "limit_TeV": 25.0},
    "dijet": {"S": 1.0, "limit_TeV": 30.0},
}

@dataclass
class Point:
    channel: str
    Lambda_TeV: float
    C: float

    @property
    def C_over_L2(self) -> float:
        return self.C / (self.Lambda_TeV**2)

    def allowed(self) -> bool:
        lim = CHANNELS[self.channel]["limit_TeV"]
        # Require |C|/Λ^2 <= 1/lim^2 (units TeV^-2)
        return abs(self.C_over_L2) <= 1.0/(lim**2)


def scan(channel: str, Lambda_grid: List[float], C_grid: List[float]) -> List[Point]:
    out: List[Point] = []
    for L in Lambda_grid:
        for C in C_grid:
            out.append(Point(channel=channel, Lambda_TeV=L, C=C))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-prefix", default="/workspace/outputs/smeft_scan")
    args = p.parse_args()

    Lambda_grid = [10, 12, 15, 20, 25, 30]
    C_grid = [0.01, 0.03, 0.1, 0.3, 1.0]

    rows = [("channel","Lambda_TeV","C","C_over_L2_TeV^-2","allowed")]
    for ch in CHANNELS.keys():
        pts = scan(ch, Lambda_grid, C_grid)
        for pt in pts:
            rows.append((ch, pt.Lambda_TeV, pt.C, pt.C_over_L2, pt.allowed()))

    csv_path = f"{args.out_prefix}.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerows(rows)

    print("Saved:", csv_path)

if __name__ == "__main__":
    main()
