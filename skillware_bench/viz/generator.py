# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Standalone SVG and graphic visualization generator for Skillware-Bench figures."""

import math
from pathlib import Path
from typing import Dict, List, Optional, Union

from skillware_bench.core.models import ComparativeDeltaReport


class VisualGenerator:
    """Generates zero-dependency SVG figures for benchmark publications and reports."""

    @classmethod
    def generate_radar_chart(
        cls,
        pillar_scores: Dict[str, float],
        title: str = "Skillware-Bench 10-Pillar Evaluation Profile",
        output_path: Optional[Union[str, Path]] = None,
        width: int = 700,
        height: int = 600,
    ) -> str:
        """Generate a standalone SVG 10-pillar spider/radar plot."""
        cx = width / 2.0
        cy = (height / 2.0) + 20.0
        radius = min(width, height) * 0.35

        pillars = list(pillar_scores.keys())
        n = len(pillars)
        if n < 3:
            raise ValueError("Radar chart requires at least 3 dimensions")

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0f172a; font-family: sans-serif;">',
            f'<text x="{cx}" y="45" font-size="20" font-weight="bold" fill="#f8fafc" '
            f'text-anchor="middle">{title}</text>',
        ]

        # Draw concentric guide rings (20%, 40%, 60%, 80%, 100%)
        for ring in [0.2, 0.4, 0.6, 0.8, 1.0]:
            r = radius * ring
            svg_parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#334155" '
                f'stroke-dasharray="3,3" stroke-width="1"/>'
            )
            svg_parts.append(
                f'<text x="{cx + 5}" y="{cy - r + 12}" font-size="10" fill="#64748b">'
                f"{int(ring * 100)}%</text>"
            )

        # Draw axis spokes and labels
        angles = [2.0 * math.pi * i / n - (math.pi / 2.0) for i in range(n)]
        data_points = []

        for i, (name, angle) in enumerate(zip(pillars, angles)):
            ax = cx + radius * math.cos(angle)
            ay = cy + radius * math.sin(angle)
            svg_parts.append(
                f'<line x1="{cx}" y1="{cy}" x2="{ax}" y2="{ay}" stroke="#475569" stroke-width="1.2"/>'
            )

            # Calculate label anchor point
            lx = cx + (radius + 28) * math.cos(angle)
            ly = cy + (radius + 28) * math.sin(angle)
            anchor = (
                "middle"
                if abs(math.cos(angle)) < 0.2
                else ("start" if math.cos(angle) > 0 else "end")
            )
            svg_parts.append(
                f'<text x="{lx}" y="{ly}" font-size="11" font-weight="500" fill="#cbd5e1" '
                f'text-anchor="{anchor}" dominant-baseline="central">{name}</text>'
            )

            # Data point
            score = max(0.0, min(100.0, pillar_scores[name]))
            norm_r = radius * (score / 100.0)
            px = cx + norm_r * math.cos(angle)
            py = cy + norm_r * math.sin(angle)
            data_points.append((px, py))

        # Draw radar polygon
        points_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in data_points)
        svg_parts.append(
            f'<polygon points="{points_str}" fill="rgba(56, 189, 248, 0.35)" '
            f'stroke="#38bdf8" stroke-width="2.5"/>'
        )

        for px, py in data_points:
            svg_parts.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#38bdf8" stroke="#0f172a" stroke-width="1.5"/>'
            )

        svg_parts.append("</svg>")
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(svg_content, encoding="utf-8")

        return svg_content

    @classmethod
    def generate_delta_lift_chart(
        cls,
        deltas: List[ComparativeDeltaReport],
        output_path: Optional[Union[str, Path]] = None,
        width: int = 800,
        height: int = 450,
    ) -> str:
        """Generate an SVG comparative lift bar chart showing token and latency compression."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0f172a; font-family: sans-serif;">',
            f'<text x="{width / 2.0}" y="40" font-size="20" font-weight="bold" fill="#f8fafc" '
            f'text-anchor="middle">Empirical Delta (Δ) Optimization Across Crucibles</text>',
            '<line x1="80" y1="360" x2="740" y2="360" stroke="#475569" stroke-width="2"/>',
        ]

        n = len(deltas)
        bar_group_width = (740 - 80) / max(1, n)
        bar_width = min(36.0, bar_group_width * 0.35)

        for i, d in enumerate(deltas):
            gx = 80 + i * bar_group_width + (bar_group_width / 2.0)

            # Token compression bar
            tok_pct = max(0.0, min(100.0, d.token_reduction_pct))
            tok_h = (tok_pct / 100.0) * 260.0
            svg_parts.append(
                f'<rect x="{gx - bar_width - 2}" y="{360 - tok_h}" width="{bar_width}" '
                f'height="{tok_h}" fill="#38bdf8" rx="4"/>'
            )
            svg_parts.append(
                f'<text x="{gx - (bar_width / 2.0) - 2}" y="{360 - tok_h - 8}" '
                f'font-size="11" fill="#7dd3fc" text-anchor="middle">-{tok_pct:.0f}%</text>'
            )

            # Latency compression bar
            lat_pct = max(0.0, min(100.0, d.latency_reduction_pct))
            lat_h = (lat_pct / 100.0) * 260.0
            svg_parts.append(
                f'<rect x="{gx + 2}" y="{360 - lat_h}" width="{bar_width}" '
                f'height="{lat_h}" fill="#4ade80" rx="4"/>'
            )
            svg_parts.append(
                f'<text x="{gx + (bar_width / 2.0) + 2}" y="{360 - lat_h - 8}" '
                f'font-size="11" fill="#86efac" text-anchor="middle">-{lat_pct:.0f}%</text>'
            )

            # Label below
            short_id = (
                d.scenario_id.replace("_01", "").replace("finance_", "").replace("office_", "")
            )
            svg_parts.append(
                f'<text x="{gx}" y="385" font-size="11" fill="#94a3b8" text-anchor="middle">{short_id}</text>'
            )

        # Legend
        svg_parts.append(
            '<rect x="260" y="415" width="14" height="14" fill="#38bdf8" rx="2"/>'
            '<text x="282" y="427" font-size="12" fill="#cbd5e1">Token Compression %</text>'
            '<rect x="440" y="415" width="14" height="14" fill="#4ade80" rx="2"/>'
            '<text x="462" y="427" font-size="12" fill="#cbd5e1">Latency Reduction %</text>'
        )

        svg_parts.append("</svg>")
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(svg_content, encoding="utf-8")

        return svg_content
