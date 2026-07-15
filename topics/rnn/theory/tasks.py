"""RNN task shapes + vanishing-gradient intuition."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import ACCENT, BLUE_D, GOLD_D, INK, MUTED, ORANGE_D, RED_D, TEAL_D, BrandScene


class RNNTasks(BrandScene):
    chapter_title = "4 · Tasks & Limits"

    def construct(self):
        self.setup_branding()
        self.say("Same cell — different ways to map inputs to outputs.", wait=1.5)

        # Many-to-one
        def seq_boxes(n: int, color=BLUE_D, label_prefix="x") -> VGroup:
            g = VGroup()
            for i in range(n):
                b = RoundedRectangle(width=0.7, height=0.5, corner_radius=0.06, color=color, fill_opacity=0.15, stroke_width=2)
                t = Text(f"{label_prefix}{i+1}", font="Sans", color=INK).scale(0.22).move_to(b)
                g.add(VGroup(b, t))
            return g.arrange(RIGHT, buff=0.12)

        self.say("Many-to-one: whole sequence → one label (e.g. sentiment).", wait=1.5)
        xs = seq_boxes(4)
        ys = RoundedRectangle(width=0.9, height=0.55, corner_radius=0.08, color=ORANGE_D, fill_opacity=0.18, stroke_width=2.5)
        yl = Text("y", font="Sans", color=INK).scale(0.34).move_to(ys)
        y_g = VGroup(ys, yl)
        m21 = VGroup(xs, Text("→", font="Sans", color=MUTED).scale(0.5), y_g).arrange(RIGHT, buff=0.35)
        title1 = Text("Many-to-one", font="Sans", weight=BOLD, color=ACCENT).scale(0.36)
        block1 = VGroup(title1, m21).arrange(DOWN, buff=0.3).move_to(UP * 1.0)
        self.play(FadeIn(block1), run_time=1.2)
        formul = Text("y = W_hy h_T + b_y   (readout from last hidden state)", font="Sans", color=INK).scale(0.3)
        formul.next_to(block1, DOWN, buff=0.35)
        self.play(Write(formul), run_time=1.1)
        self.set_dims("use h_T only")
        self.wait(1.4)

        self.play(FadeOut(block1), FadeOut(formul), run_time=0.6)

        # Many-to-many
        self.say("Many-to-many: one output at each time (e.g. tagging).", wait=1.5)
        xs2 = seq_boxes(4)
        ys2 = seq_boxes(4, color=ORANGE_D, label_prefix="y")
        title2 = Text("Many-to-many (same length)", font="Sans", weight=BOLD, color=ACCENT).scale(0.36)
        arrows = VGroup(*[
            Arrow(xs2[i].get_bottom(), ys2[i].get_top(), buff=0.08, color=MUTED, stroke_width=2.5)
            for i in range(4)
        ])
        stack = VGroup(xs2, arrows, ys2).arrange(DOWN, buff=0.15)
        block2 = VGroup(title2, stack).arrange(DOWN, buff=0.25).move_to(UP * 0.6)
        self.play(FadeIn(title2), FadeIn(xs2), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(ys2), run_time=1.4)
        self.set_dims("y_t from h_t each step")
        self.wait(1.4)

        self.play(FadeOut(block2), run_time=0.6)

        # Vanishing intuition
        self.say("Limitation: signals from the far past can shrink (vanishing).", wait=1.6)
        chain = VGroup()
        for i in range(5):
            c = Circle(radius=0.32, color=TEAL_D, fill_opacity=0.15, stroke_width=2.5)
            lab = Text(f"h{i+1}" if i < 4 else "hT", font="Sans", color=INK).scale(0.26).move_to(c)
            chain.add(VGroup(c, lab))
        chain.arrange(RIGHT, buff=0.85).move_to(UP * 0.7)

        link_arrows = VGroup()
        for i in range(4):
            link_arrows.add(
                Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.08, color=MUTED, stroke_width=3)
            )

        self.play(FadeIn(chain), LaggedStart(*[GrowArrow(a) for a in link_arrows], lag_ratio=0.15), run_time=1.5)

        # Shrinking gradient bars under early → late
        bars = VGroup()
        heights = [0.9, 0.55, 0.32, 0.18, 0.1]
        for i, h in enumerate(heights):
            rect = Rectangle(width=0.35, height=h, color=RED_D, fill_opacity=0.45, stroke_width=0)
            rect.next_to(chain[i], DOWN, buff=0.45)
            bars.add(rect)

        bar_lbl = Text("∂ loss / ∂ h   gets smaller toward the past", font="Sans", color=RED_D).scale(0.3)
        bar_lbl.to_edge(DOWN, buff=1.2)

        self.say("If |W_h| is small, multiplying many times → early tokens fade.", wait=1.7)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), Write(bar_lbl), run_time=1.6)
        self.wait(1.2)

        tip = VGroup(
            Text("Intuition only — LSTM / GRU later can keep long memory better.", font="Sans", color=MUTED).scale(0.3),
            Text("You now have: why · cell math · unroll · task shapes.", font="Sans", color=ACCENT).scale(0.32),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.35)

        self.play(FadeOut(bar_lbl), FadeIn(tip), run_time=1.0)
        self.wait(2.2)
