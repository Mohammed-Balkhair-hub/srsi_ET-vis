"""CNN pipeline — pure 2D left→right layout; dims row below steps (no overlap)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from manim import *
from branding import (
    ACCENT, BLUE_D, GOLD_D, GREEN_D, INK, MUTED, ORANGE_D, PURPLE_D, RED_D, TEAL_D,
    BrandScene, dims_badge,
)

STEP_DIM = MUTED
STEP_ACTIVE = "#D4A017"


class CNNPipeline(BrandScene):
    chapter_title = "5 · CNN Architecture"

    def construct(self):
        self.setup_branding()
        # Clear default dims position — we use a dedicated mid-row badge
        if self.dims is not None:
            self.remove(self.dims)
        self.dims = None
        self._dims_visible = False

        self.say("Follow left → right. The yellow step is the one running now.", wait=1.6)

        # ---- Step strip (top) ----
        step_names = ["Conv", "BN", "ReLU", "Pool", "Flatten", "FC", "Softmax"]
        pieces, step_mobs = [], []
        for i, name in enumerate(step_names):
            t = Text(name, font="Sans", weight=BOLD, color=STEP_DIM).scale(0.36)
            pieces.append(t)
            step_mobs.append(t)
            if i < len(step_names) - 1:
                pieces.append(Text("→", font="Sans", color=MUTED).scale(0.32)
                              )
        row = VGroup(*pieces).arrange(RIGHT, buff=0.26)
        row.next_to(self.title_mob, DOWN, buff=0.35).set_x(0)
        # Keep clear of logo on the right
        row.shift(LEFT * 0.35)
        self.add(row)
        self.play(FadeIn(row), run_time=1.1)

        def light_step(idx: int):
            self.play(*[
                step_mobs[i].animate.set_color(STEP_ACTIVE if i == idx else STEP_DIM)
                for i in range(len(step_mobs))
            ], run_time=0.6)

        def show_dims(text: str, wait: float = 0.7):
            """Dims badge sits on its own row UNDER the step strip — never overlaps Conv/BN…"""
            new_d = dims_badge(text, scale=0.30)
            new_d.next_to(row, DOWN, buff=0.28).align_to(row, LEFT)
            if self.dims is not None:
                self.play(FadeOut(self.dims), run_time=0.25)
                self.remove(self.dims)
            self.dims = new_d
            self.add(self.dims)
            self._dims_visible = True
            self.play(FadeIn(self.dims), run_time=0.4)
            if wait:
                self.wait(wait)

        def block_stack(n: int, side: float, color, x: float, y: float = -0.85):
            """2D faux-stack: slight down-right offsets (left→right pipeline)."""
            g = VGroup()
            for i in range(n):
                sq = Square(side_length=side, fill_opacity=0.32, stroke_width=2.0, color=color)
                sq.shift(RIGHT * i * 0.12 + DOWN * i * 0.12)
                g.add(sq)
            g.move_to([x, y, 0])
            return g

        # ---- Feature extraction, left → right ----
        s_in = block_stack(3, 1.7, BLUE_D, -4.5)
        in_tag = Text("input", font="Sans", color=BLUE_D).scale(0.26).next_to(s_in, DOWN, buff=0.2)
        self.play(FadeIn(s_in), FadeIn(in_tag), run_time=1.0)
        show_dims("[B, 3, 32, 32]  input image")
        self.say("Start: RGB image batch on the left.", wait=1.3)

        light_step(0)
        self.say("Conv: more channels (kernels). Spatial size kept with padding.", wait=1.4)
        s_conv = block_stack(5, 1.55, RED_D, -2.2)
        a1 = Arrow(s_in.get_right(), s_conv.get_left(), buff=0.12, color=GOLD_D, stroke_width=3)
        self.play(GrowArrow(a1), FadeIn(s_conv), run_time=1.2)
        show_dims("[B, 16, 32, 32]  after Conv")
        self.wait(1.2)

        light_step(1)
        self.say("BN: renormalize — shape does not change.", wait=1.3)
        self.play(s_conv.animate.set_color(ORANGE_D), run_time=0.9)
        show_dims("[B, 16, 32, 32]  after BN (same)")
        self.wait(1.1)

        light_step(2)
        self.say("ReLU: zero negatives — shape still unchanged.", wait=1.3)
        self.play(s_conv.animate.set_color(GREEN_D), run_time=0.9)
        show_dims("[B, 16, 32, 32]  after ReLU (same)")
        self.wait(1.1)

        light_step(3)
        self.say("Pool: halves height & width; channels stay.", wait=1.4)
        s_pool = block_stack(5, 1.05, TEAL_D, 0.4)
        a2 = Arrow(s_conv.get_right(), s_pool.get_left(), buff=0.12, color=GOLD_D, stroke_width=3)
        self.play(GrowArrow(a2), FadeIn(s_pool), run_time=1.2)
        show_dims("[B, 16, 16, 16]  after Pool (H,W ÷ 2)")
        self.wait(1.2)

        self.say("Repeat Conv→BN→ReLU→Pool once more…", wait=1.3)
        s_deep = block_stack(7, 0.75, PURPLE_D, 2.7)
        a3 = Arrow(s_pool.get_right(), s_deep.get_left(), buff=0.1, color=GOLD_D, stroke_width=3)
        for i in range(4):
            light_step(i)
            self.wait(0.55)
        self.play(GrowArrow(a3), FadeIn(s_deep), run_time=1.2)
        show_dims("[B, 32, 8, 8]  after 2nd block")
        self.wait(1.3)

        self.say("Now the classifier head — still left → right.", wait=1.3)
        self.play(
            FadeOut(VGroup(s_in, in_tag, s_conv, s_pool, s_deep, a1, a2, a3)),
            run_time=0.9,
        )

        # ---- Classifier: flatten | hidden | outputs  (left → right, flat) ----
        light_step(4)
        flat = VGroup(*[
            Dot(radius=0.1, color=GOLD_D).shift(UP * (1.4 - i * 0.38))
            for i in range(8)
        ]).shift(LEFT * 4.2 + DOWN * 0.5)
        flat_l = Text("Flatten", font="Sans", color=GOLD_D).scale(0.3).next_to(flat, UP, buff=0.25)
        self.play(FadeIn(flat), FadeIn(flat_l), run_time=1.0)
        show_dims("[B, 2048]  Flatten (32×8×8)")
        self.say("Flatten turns the volume into one long vector.", wait=1.4)

        light_step(5)
        hidden = VGroup(*[
            Circle(0.24, color=TEAL_D, fill_opacity=0.35, stroke_width=2.5).shift(UP * (1.0 - i * 0.55))
            for i in range(5)
        ]).shift(ORIGIN + DOWN * 0.5)
        hid_l = Text("Dense / FC", font="Sans", color=TEAL_D).scale(0.3).next_to(hidden, UP, buff=0.25)

        outs = VGroup(*[
            Circle(0.3, color=c, fill_opacity=0.3, stroke_width=2.5).shift(UP * (0.75 - i * 0.85))
            for i, c in enumerate([ORANGE_D, BLUE_D, GREEN_D])
        ]).shift(RIGHT * 3.5 + DOWN * 0.5)
        names = ["Cat", "Dog", "Bird"]
        name_lbls = VGroup(*[
            Text(names[i], font="Sans", color=outs[i].get_color()).scale(0.32).next_to(outs[i], RIGHT, buff=0.22)
            for i in range(3)
        ])

        e1 = VGroup(*[
            Line(a.get_right(), b.get_left(), stroke_width=1.1, stroke_opacity=0.35, color=MUTED)
            for a in flat for b in hidden
        ])
        e2 = VGroup(*[
            Line(a.get_right(), b.get_left(), stroke_width=1.3, stroke_opacity=0.4, color=MUTED)
            for a in hidden for b in outs
        ])

        self.play(Create(e1), FadeIn(hidden), FadeIn(hid_l), run_time=1.1)
        self.wait(0.5)
        self.play(Create(e2), FadeIn(outs), FadeIn(name_lbls), run_time=1.1)
        show_dims("[B, num_classes]  after FC (logits)")
        self.say("FC layers mix features into one score per class.", wait=1.4)

        light_step(6)
        probs = np.array([0.12, 0.81, 0.07])
        self.say("Softmax turns scores into probabilities that sum to 1.", wait=1.4)
        readout = VGroup(*[
            Text(f"{names[i]}  {probs[i]*100:.0f}%", font="Sans", color=outs[i].get_color()).scale(0.34)
            for i in range(3)
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.5)

        anims = [
            outs[i].animate.set_fill(outs[i].get_color(), opacity=0.25 + 0.55 * float(probs[i]))
            for i in range(3)
        ]
        ring = Circle(radius=0.44, color=GOLD_D, stroke_width=4).move_to(outs[1])
        self.play(*anims, Create(ring), FadeIn(readout), run_time=1.4)
        show_dims("probabilities sum to 1")
        self.say("Prediction: Dog (81%)", wait=2.0)
