"""Why Attention — RNN bottleneck vs soft lookup over all tokens."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import ACCENT, BLUE_D, GOLD_D, INK, MUTED, ORANGE_D, RED_D, TEAL_D, BrandScene


def terms_key(lines: list[str]) -> VGroup:
    rows = VGroup(*[Text(line, font="Sans", color=INK).scale(0.24) for line in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.08
    )
    title = Text("Key", font="Sans", weight=BOLD, color=ACCENT).scale(0.26)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    box = SurroundingRectangle(body, buff=0.14, corner_radius=0.08, color=MUTED, stroke_width=1.5)
    box.set_fill("#F7F9FB", opacity=1.0)
    g = VGroup(box, body)
    body.move_to(box.get_center())
    g.to_corner(DL, buff=0.22).shift(UP * 0.85)
    return g


class WhyAttention(BrandScene):
    chapter_title = "1 · Why Attention?"

    def construct(self):
        self.setup_branding()
        self.say("RNNs pass memory through one chain — early words can fade.", wait=1.6)

        toks = ["the", "cat", "sat"]
        boxes = VGroup()
        for i, t in enumerate(toks):
            b = RoundedRectangle(width=1.35, height=0.75, corner_radius=0.08, color=BLUE_D, fill_opacity=0.15, stroke_width=2.5)
            lab = Text(t, font="Sans", color=INK).scale(0.36).move_to(b)
            boxes.add(VGroup(b, lab).shift(RIGHT * (i - 1) * 2.1))
        arrows = VGroup(*[
            Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.12, color=MUTED, stroke_width=3)
            for i in range(2)
        ])
        h_chain = Text("h₀ → h₁ → h₂  (one path)", font="Sans", color=ORANGE_D).scale(0.32)
        h_chain.next_to(boxes, DOWN, buff=0.45)

        self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), run_time=1.4)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), Write(h_chain), run_time=1.2)
        self.set_dims("sequence T = 3")
        self.wait(1.0)

        problem = Text("Bottleneck: everything squeezed into the latest h_t", font="Sans", color=RED_D).scale(0.34)
        problem.move_to(DOWN * 1.7)
        self.say("Long-range links must hop through every step.", wait=1.5)
        self.play(Write(problem), run_time=1.0)
        self.wait(1.3)

        self.play(FadeOut(VGroup(boxes, arrows, h_chain, problem)), run_time=0.7)

        self.say("Attention: each token soft-looks at every token in parallel.", wait=1.6)
        idea = Text(
            "output_i  =  Σ_j  α_{ij}  ·  value_j",
            font="Sans",
            weight=BOLD,
            color=ACCENT,
        ).scale(0.42)
        idea.move_to(UP * 1.4)
        self.play(Write(idea), run_time=1.3)

        # Query sat looking at all
        q = RoundedRectangle(width=1.4, height=0.7, corner_radius=0.08, color=ORANGE_D, fill_opacity=0.18, stroke_width=2.5)
        q_l = Text("sat (query)", font="Sans", color=INK).scale(0.28).move_to(q)
        q_g = VGroup(q, q_l).move_to(LEFT * 3.2 + DOWN * 0.1)

        keys = VGroup()
        for i, t in enumerate(toks):
            b = RoundedRectangle(width=1.2, height=0.6, corner_radius=0.08, color=TEAL_D, fill_opacity=0.15, stroke_width=2)
            lab = Text(t, font="Sans", color=INK).scale(0.30).move_to(b)
            keys.add(VGroup(b, lab))
        keys.arrange(RIGHT, buff=0.35).move_to(RIGHT * 1.5 + DOWN * 0.1)

        self.play(FadeIn(q_g), FadeIn(keys), run_time=1.2)
        links = VGroup(*[
            Arrow(q_g.get_right(), keys[j].get_left(), buff=0.1, color=GOLD_D if j == 1 else MUTED, stroke_width=3 if j == 1 else 2)
            for j in range(3)
        ])
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.25), run_time=1.4)
        ring = SurroundingRectangle(keys[1], color=GOLD_D, buff=0.06, stroke_width=3.5)
        self.play(Create(ring), run_time=0.6)

        self.say("α_{ij} says how much token i borrows from token j.", wait=1.5)
        key = terms_key([
            "α_{ij} — attention weight",
            "value_j — content from token j",
            "parallel — all pairs at once",
        ])
        self.play(FadeIn(key), run_time=0.8)
        self.wait(2.0)
