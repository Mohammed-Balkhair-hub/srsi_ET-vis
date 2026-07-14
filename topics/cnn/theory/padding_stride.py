"""Padding, stride, and the output-size formula."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import ACCENT, BLUE_D, GOLD_D, GREEN_D, INK, MUTED, ORANGE_D, RED_D, TEAL_D, BrandScene, highlight_window, number_grid


class PaddingAndStride(BrandScene):
    chapter_title = "3 · Padding and Stride"

    def construct(self):
        self.setup_branding()
        self.say("Without padding, each convolution shrinks the map.", wait=1.6)

        core = number_grid([[1] * 4 for _ in range(4)], cell=0.5, color=BLUE_D)
        core.shift(LEFT * 3.2)
        core_lbl = Text("Input 4×4", font="Sans", color=INK).scale(0.3).next_to(core, UP, buff=0.15)
        self.play(FadeIn(core), Write(core_lbl), run_time=1.1)

        self.say("Valid padding (P=0): output is smaller than input.", wait=1.4)
        small = number_grid([[0] * 2 for _ in range(2)], cell=0.5, color=ORANGE_D)
        small.shift(LEFT * 0.5)
        small_lbl = Text("Valid → 2×2", font="Sans", color=ORANGE_D).scale(0.3).next_to(small, UP, buff=0.15)
        a1 = Arrow(core.get_right(), small.get_left(), buff=0.12, color=MUTED, stroke_width=3)
        self.play(GrowArrow(a1), FadeIn(small), Write(small_lbl), run_time=1.2)
        self.wait(1.2)

        self.say("Same padding: add a border of zeros so size stays the same.", wait=1.4)
        padded_vals = [
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
        ]
        padded = number_grid(padded_vals, cell=0.42, color=TEAL_D, font_scale=0.22)
        padded.shift(RIGHT * 3.0)
        for i in range(6):
            for j in range(6):
                if i in (0, 5) or j in (0, 5):
                    padded[i * 6 + j][0].set_fill(MUTED, opacity=0.2)
                    padded[i * 6 + j][1].set_color(MUTED)
        pad_lbl = Text("Same P=1 → keep size", font="Sans", color=TEAL_D).scale(0.28).next_to(padded, UP, buff=0.12)
        a2 = Arrow(small.get_right(), padded.get_left(), buff=0.12, color=TEAL_D, stroke_width=3)
        self.play(GrowArrow(a2), FadeIn(padded), Write(pad_lbl), run_time=1.4)
        note = Text("For 3×3 kernel, P = ⌊K/2⌋ = 1 preserves spatial size", font="Sans", color=INK).scale(0.3)
        note.to_edge(DOWN, buff=1.15)
        self.play(Write(note), run_time=0.9)
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(core, core_lbl, small, small_lbl, a1, a2, padded, pad_lbl, note)),
            run_time=0.8,
        )

        self.say("Stride = how far the kernel jumps each step.", wait=1.5)
        left_title = Text("Stride = 1", font="Sans", color=GREEN_D).scale(0.4).shift(LEFT * 3.2 + UP * 2.2)
        right_title = Text("Stride = 2", font="Sans", color=RED_D).scale(0.4).shift(RIGHT * 3.2 + UP * 2.2)
        self.play(Write(left_title), Write(right_title), run_time=0.9)

        base_l = number_grid([[i + j for j in range(5)] for i in range(5)], cell=0.48, color=BLUE_D, font_scale=0.22)
        base_l.shift(LEFT * 3.2 + DOWN * 0.2)
        base_r = number_grid([[i + j for j in range(5)] for i in range(5)], cell=0.48, color=BLUE_D, font_scale=0.22)
        base_r.shift(RIGHT * 3.2 + DOWN * 0.2)
        self.play(FadeIn(base_l), FadeIn(base_r), run_time=1.1)

        self.say("S=1: move one pixel at a time (dense coverage).", wait=1.3)
        for c0 in range(3):
            w = highlight_window(base_l, 5, 5, 0, c0, 3, color=GREEN_D)
            self.play(Create(w), run_time=0.7)
            self.wait(0.8)
            self.play(FadeOut(w), run_time=0.5)

        self.say("S=2: jump two pixels → roughly half the spatial size.", wait=1.3)
        for c0 in (0, 2):
            w = highlight_window(base_r, 5, 5, 0, c0, 3, color=RED_D)
            self.play(Create(w), run_time=0.8)
            self.wait(0.9)
            self.play(FadeOut(w), run_time=0.5)
        self.wait(1.2)

        self.play(FadeOut(VGroup(left_title, right_title, base_l, base_r)), run_time=0.7)

        self.say("Output size formula (from the slides):", wait=1.4)
        formula = Text("W_out = floor( (W − K + 2P) / S ) + 1", font="Sans", weight=BOLD, color=ACCENT).scale(0.42)
        formula.move_to(UP * 1.5)
        self.play(Write(formula), run_time=1.0)
        self.set_dims("W=32, K=3")

        examples = VGroup(
            Text("P=1, S=1 → ⌊(32−3+2)/1⌋+1 = 32  (same)", font="Sans", color=INK).scale(0.34),
            Text("P=0, S=1 → ⌊(32−3+0)/1⌋+1 = 30  (shrinks)", font="Sans", color=INK).scale(0.34),
            Text("P=1, S=2 → ⌊(32−3+2)/2⌋+1 = 16  (halved)", font="Sans", color=INK).scale(0.34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.5)

        for ex in examples:
            self.play(FadeIn(ex, shift=RIGHT * 0.15), run_time=0.9)
            self.wait(1.2)
        self.wait(1.8)
