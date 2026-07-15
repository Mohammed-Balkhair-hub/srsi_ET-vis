"""Unroll the same scalar RNN over three time steps."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import ACCENT, BLUE_D, GOLD_D, INK, MUTED, ORANGE_D, TEAL_D, BrandScene

WX = 0.5
WH = 0.8
B = 0.0
XS = [1.0, 0.0, 1.0]


def step(h_prev: float, x: float) -> tuple[float, float]:
    a = WX * x + WH * h_prev + B
    return a, math.tanh(a)


class UnrollSequence(BrandScene):
    chapter_title = "3 · Unroll Over Time"

    def construct(self):
        self.setup_branding()
        self.say("Same weights every step — only h and x change.", wait=1.5)

        rule = Text(
            f"h_t = tanh( {WX} · x_t  +  {WH} · h_{{t-1}}  +  {B:g} )",
            font="Sans",
            color=ACCENT,
        ).scale(0.36)
        rule.to_edge(UP, buff=1.05)
        self.play(Write(rule), run_time=1.3)
        self.set_dims("scalar demo · T = 3 · h_0 = 0")

        shared = Text("W_x, W_h, b  shared for all t", font="Sans", color=TEAL_D).scale(0.32)
        shared.next_to(rule, DOWN, buff=0.25)
        self.play(FadeIn(shared), run_time=0.8)
        self.wait(1.0)

        # Build unroll boxes
        cells = VGroup()
        x_boxes = VGroup()
        h_boxes = VGroup()
        for t in range(3):
            cell = RoundedRectangle(
                width=1.55, height=1.15, corner_radius=0.1,
                stroke_width=2.5, color=TEAL_D, fill_opacity=0.12,
            )
            cell_l = Text(f"t = {t+1}", font="Sans", color=INK).scale(0.32).move_to(cell)
            cell_g = VGroup(cell, cell_l).shift(RIGHT * (t - 1) * 3.1)
            cells.add(cell_g)

            xb = RoundedRectangle(width=1.1, height=0.55, corner_radius=0.08, color=BLUE_D, fill_opacity=0.15, stroke_width=2)
            xl = Text(f"x={XS[t]:g}", font="Sans", color=INK).scale(0.28).move_to(xb)
            xg = VGroup(xb, xl).next_to(cell_g, UP, buff=0.35)
            x_boxes.add(xg)

        h0 = RoundedRectangle(width=1.2, height=0.55, corner_radius=0.08, color=ORANGE_D, fill_opacity=0.15, stroke_width=2)
        h0_l = Text("h_0 = 0", font="Sans", color=INK).scale(0.28).move_to(h0)
        h0_g = VGroup(h0, h0_l).next_to(cells[0], LEFT, buff=0.55)

        self.say("Unroll left → right. Current step lights yellow until it finishes.", wait=1.6)
        self.play(FadeIn(cells), FadeIn(x_boxes), FadeIn(h0_g), run_time=1.4)

        hs = [0.0]
        as_ = []
        for t, x in enumerate(XS):
            a, h = step(hs[-1], x)
            as_.append(a)
            hs.append(h)

        # Place h outputs under / right of cells
        h_out_mobs = VGroup()
        for t in range(3):
            hb = RoundedRectangle(width=1.35, height=0.55, corner_radius=0.08, color=ORANGE_D, fill_opacity=0.15, stroke_width=2)
            hl = Text(f"h_{t+1}≈{hs[t+1]:.3f}", font="Sans", color=INK).scale(0.26).move_to(hb)
            hg = VGroup(hb, hl).next_to(cells[t], DOWN, buff=0.4)
            h_out_mobs.add(hg)

        badge = Text("", font="Sans", color=ORANGE_D).scale(0.34).to_edge(DOWN, buff=1.15)

        for t in range(3):
            # Highlight active cell
            active = SurroundingRectangle(cells[t], color=GOLD_D, buff=0.06, stroke_width=4)
            self.say(f"Step t = {t+1}: multiply, sum, then tanh.", wait=1.2)
            self.play(Create(active), run_time=0.6)

            h_prev = hs[t]
            x = XS[t]
            a = as_[t]
            detail = Text(
                f"{WX}×{x:g} + {WH}×{h_prev:.3f} = {a:.3f}  →  tanh → {hs[t+1]:.3f}",
                font="Sans",
                color=INK,
            ).scale(0.30)
            detail.move_to(DOWN * 2.35)
            self.play(Write(detail), run_time=1.4)
            self.wait(1.2)

            self.play(FadeIn(h_out_mobs[t]), run_time=0.8)
            dims_txt = f"h_{t+1} ≈ {hs[t+1]:.3f}"
            self.set_dims(dims_txt, wait=0.8)

            if t < 2:
                ar = Arrow(
                    h_out_mobs[t].get_right(),
                    cells[t + 1].get_left() + DOWN * 0.15,
                    buff=0.12,
                    color=ORANGE_D,
                    stroke_width=3,
                )
                tip = Text("to next step", font="Sans", color=ORANGE_D).scale(0.24).next_to(ar, DOWN, buff=0.05)
                self.play(GrowArrow(ar), FadeIn(tip), run_time=0.9)
                self.wait(0.6)
                self.play(FadeOut(tip), run_time=0.3)

            self.play(FadeOut(active), FadeOut(detail), run_time=0.5)

        # Punchline
        self.say("At t=2, x=0 — yet h_2 still remembers x_1 through h_1.", wait=1.7)
        punch = Text(
            "Memory travels through h — that is recurrence.",
            font="Sans",
            weight=BOLD,
            color=ACCENT,
        ).scale(0.38)
        punch.move_to(DOWN * 2.35)
        # highlight t=2 path
        ring = SurroundingRectangle(VGroup(x_boxes[1], cells[1], h_out_mobs[1]), color=GOLD_D, buff=0.08, stroke_width=3)
        self.play(Create(ring), Write(punch), run_time=1.3)
        self.wait(2.2)
