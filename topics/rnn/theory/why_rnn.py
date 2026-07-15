"""Why RNNs? — sequences need memory; plain MLPs lose order."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import ACCENT, BLUE_D, INK, MUTED, ORANGE_D, RED_D, TEAL_D, BrandScene


class WhyRNNs(BrandScene):
    chapter_title = "1 · Why Recurrent Neural Networks?"

    def construct(self):
        self.setup_branding()
        self.say("Language and time series are sequences — order matters.", wait=1.6)

        tokens = ["the", "cat", "sat"]
        boxes = VGroup()
        for i, tok in enumerate(tokens):
            sq = RoundedRectangle(
                width=1.5, height=0.85, corner_radius=0.1,
                stroke_width=2.5, color=BLUE_D, fill_opacity=0.15,
            )
            lab = Text(tok, font="Sans", color=INK).scale(0.42)
            lab.move_to(sq)
            item = VGroup(sq, lab)
            item.shift(RIGHT * (i - 1) * 2.0)
            boxes.add(item)

        arrows = VGroup(
            Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.12, color=MUTED, stroke_width=3),
            Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.12, color=MUTED, stroke_width=3),
        )
        time_lbl = Text("time →", font="Sans", color=MUTED).scale(0.32).next_to(boxes, DOWN, buff=0.35)

        self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.35), run_time=1.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), Write(time_lbl), run_time=1.2)
        self.set_dims("sequence length T = 3")
        self.wait(1.0)

        self.say("If we treat each token alone, order disappears.", wait=1.5)
        bag = VGroup(
            Text("Bag of words", font="Sans", weight=BOLD, color=RED_D).scale(0.4),
            Text("{ cat, sat, the }  — same set, any order", font="Sans", color=INK).scale(0.34),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=1.15)
        self.play(Write(bag), run_time=1.2)
        self.wait(1.4)

        self.play(FadeOut(bag), FadeOut(VGroup(boxes, arrows, time_lbl)), run_time=0.8)

        # MLP vs order
        self.say("A plain MLP sees one fixed-size vector — no memory of the past.", wait=1.6)
        mlp_in = RoundedRectangle(width=1.8, height=1.0, corner_radius=0.1, color=ORANGE_D, fill_opacity=0.12, stroke_width=2.5)
        mlp_in_l = Text("x only", font="Sans", color=INK).scale(0.36).move_to(mlp_in)
        mlp_box = RoundedRectangle(width=1.6, height=1.0, corner_radius=0.1, color=MUTED, fill_opacity=0.1, stroke_width=2.5).shift(RIGHT * 2.8)
        mlp_l = Text("MLP", font="Sans", color=INK).scale(0.4).move_to(mlp_box)
        mlp_out = Text("y", font="Sans", color=INK).scale(0.4).next_to(mlp_box, RIGHT, buff=0.8)
        a1 = Arrow(mlp_in.get_right(), mlp_box.get_left(), buff=0.15, color=MUTED, stroke_width=3)
        a2 = Arrow(mlp_box.get_right(), mlp_out.get_left(), buff=0.15, color=MUTED, stroke_width=3)
        mlp_g = VGroup(mlp_in, mlp_in_l, mlp_box, mlp_l, mlp_out, a1, a2).move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(mlp_g), run_time=1.3)
        fail = Text("No h_{t-1} — previous words are forgotten", font="Sans", color=RED_D).scale(0.34)
        fail.next_to(mlp_g, DOWN, buff=0.55)
        self.play(Write(fail), run_time=1.0)
        self.wait(1.5)

        self.play(FadeOut(mlp_g), FadeOut(fail), run_time=0.7)

        self.say("RNNs keep a hidden state that depends on the past.", wait=1.5)
        formula = Text("h_t  =  f( h_{t-1} ,  x_t )", font="Sans", weight=BOLD, color=ACCENT).scale(0.5)
        formula.move_to(UP * 0.9)
        self.play(Write(formula), run_time=1.3)
        self.set_dims("h_t ∈ R^{d_h}   ·   x_t ∈ R^{d_x}")

        # Simple recurrence cartoon
        xt = RoundedRectangle(width=1.2, height=0.7, corner_radius=0.08, color=BLUE_D, fill_opacity=0.15, stroke_width=2.5)
        xt_l = Text("x_t", font="Sans", color=INK).scale(0.36).move_to(xt)
        cell = RoundedRectangle(width=1.6, height=1.1, corner_radius=0.1, color=TEAL_D, fill_opacity=0.18, stroke_width=2.5).shift(RIGHT * 2.4)
        cell_l = Text("RNN\ncell", font="Sans", color=INK).scale(0.32).move_to(cell)
        ht = RoundedRectangle(width=1.2, height=0.7, corner_radius=0.08, color=ORANGE_D, fill_opacity=0.15, stroke_width=2.5).shift(RIGHT * 4.8)
        ht_l = Text("h_t", font="Sans", color=INK).scale(0.36).move_to(ht)
        htm = RoundedRectangle(width=1.2, height=0.7, corner_radius=0.08, color=ORANGE_D, fill_opacity=0.15, stroke_width=2.5).shift(RIGHT * 2.4 + DOWN * 1.8)
        htm_l = Text("h_{t-1}", font="Sans", color=INK).scale(0.32).move_to(htm)

        core = VGroup(xt, xt_l, cell, cell_l, ht, ht_l, htm, htm_l).move_to(DOWN * 0.35 + LEFT * 0.2)
        ar_x = Arrow(xt.get_right(), cell.get_left(), buff=0.1, color=MUTED, stroke_width=3)
        ar_h = Arrow(cell.get_right(), ht.get_left(), buff=0.1, color=MUTED, stroke_width=3)
        ar_m = Arrow(htm.get_top(), cell.get_bottom(), buff=0.1, color=ORANGE_D, stroke_width=3)

        self.play(FadeIn(core), GrowArrow(ar_x), GrowArrow(ar_h), GrowArrow(ar_m), run_time=1.6)

        bullets = VGroup(
            Text("Same cell reused at every time step", font="Sans", color=INK).scale(0.32),
            Text("h_t carries information forward in time", font="Sans", color=INK).scale(0.32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=1.05)
        self.say("Memory + shared weights — that is the RNN idea.", wait=1.4)
        self.play(LaggedStart(*[FadeIn(b) for b in bullets], lag_ratio=0.3), run_time=1.2)
        self.wait(2.0)
