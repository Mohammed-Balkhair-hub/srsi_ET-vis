"""Q, K, V terms, dims, and the 'the cat sat' embedding matrix."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import (
    ACCENT,
    BLUE_D,
    GOLD_D,
    GREEN_D,
    INK,
    MUTED,
    ORANGE_D,
    TEAL_D,
    BrandScene,
    number_grid,
)


def terms_key(lines: list[str]) -> VGroup:
    rows = VGroup(*[Text(line, font="Sans", color=INK).scale(0.20) for line in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.06
    )
    title = Text("Key", font="Sans", weight=BOLD, color=ACCENT).scale(0.22)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    box = SurroundingRectangle(body, buff=0.12, corner_radius=0.08, color=MUTED, stroke_width=1.5)
    box.set_fill("#F7F9FB", opacity=1.0)
    g = VGroup(box, body)
    body.move_to(box.get_center())
    g.to_corner(DL, buff=0.18).shift(UP * 0.95)
    return g


def yellow_ring(m: Mobject) -> SurroundingRectangle:
    return SurroundingRectangle(m, color=GOLD_D, buff=0.05, stroke_width=3.5)


class QKVAndDims(BrandScene):
    chapter_title = "2 · Terms, Dims & Q / K / V"

    def construct(self):
        self.setup_branding()
        self.say("Pack the sentence into a matrix of embeddings.", wait=1.5)

        key = terms_key([
            "T — sequence length (= 3)",
            "d_model — embedding size (= 2)",
            "d_k — query/key size (= 2)",
            "X — token embeddings",
            "Q — what am I looking for?",
            "K — what can match a query?",
            "V — what content to mix in?",
            "W_Q, W_K, W_V — projections",
        ])
        self.play(FadeIn(key), run_time=0.8)

        toks = VGroup(*[
            Text(t, font="Sans", color=BLUE_D).scale(0.34)
            for t in ["the", "cat", "sat"]
        ]).arrange(DOWN, buff=0.35).move_to(LEFT * 4.3 + UP * 0.3)

        X = number_grid([[1.0, 0.0], [0.0, 1.0], [0.2, 0.8]], cell=0.55, color=TEAL_D, font_scale=0.26)
        X_lab = Text("X  (T × d_model)", font="Sans", color=TEAL_D).scale(0.30)
        X_g = VGroup(X_lab, X).arrange(DOWN, buff=0.12).move_to(LEFT * 1.2 + UP * 0.35)

        self.play(FadeIn(toks), FadeIn(X_g), run_time=1.3)
        self.set_dims("T = 3   ·   d_model = 2")
        self.wait(1.0)

        self.say("Three roles from the same X — Query, Key, Value.", wait=1.5)
        roles = VGroup(
            Text("Q  — query: what am I looking for?", font="Sans", color=ORANGE_D).scale(0.30),
            Text("K  — key: what label / match signal do I expose?", font="Sans", color=GREEN_D).scale(0.30),
            Text("V  — value: what content do I give if selected?", font="Sans", color=BLUE_D).scale(0.30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 2.6 + UP * 0.5)
        self.play(LaggedStart(*[FadeIn(r) for r in roles], lag_ratio=0.3), run_time=1.6)
        self.wait(1.2)

        self.play(FadeOut(roles), run_time=0.5)
        proj = Text("Q = X W_Q    K = X W_K    V = X W_V", font="Sans", weight=BOLD, color=ACCENT).scale(0.34)
        proj.move_to(DOWN * 1.15 + RIGHT * 1.2)
        self.play(Write(proj), run_time=1.2)
        self.set_dims("W_Q ∈ R^{2×2}   ·   Q,K,V ∈ R^{3×2}")

        self.say("Toy setup: W_Q = W_K = W_V = I  →  Q = K = V = X.", wait=1.6)
        note = Text("Identity keeps the numbers readable — same idea with learned W.", font="Sans", color=MUTED).scale(0.28)
        note.next_to(proj, DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=0.8)

        rings = VGroup(yellow_ring(X_g))
        qkv = Text("Q = K = V = X", font="Sans", color=GOLD_D).scale(0.36)
        qkv.next_to(X_g, UP, buff=0.25)
        self.play(FadeIn(rings), FadeIn(qkv), run_time=0.9)
        self.wait(2.0)
