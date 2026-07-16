"""Pretrained CNNs — backbone features, swap the head, embedding similarity."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from manim import *
from branding import (
    ACCENT,
    BLUE_D,
    GOLD_D,
    GREEN_D,
    INK,
    MUTED,
    ORANGE_D,
    PURPLE_D,
    RED_D,
    TEAL_D,
    BrandScene,
    dims_badge,
)

STEP_DIM = MUTED
STEP_ACTIVE = "#D4A017"


def terms_key(lines: list[str]) -> VGroup:
    rows = VGroup(*[
        Text(line, font="Sans", color=INK).scale(0.22) for line in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    title = Text("Key", font="Sans", weight=BOLD, color=ACCENT).scale(0.24)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    box = SurroundingRectangle(body, buff=0.12, corner_radius=0.08, color=MUTED, stroke_width=1.5)
    box.set_fill("#F7F9FB", opacity=1.0)
    g = VGroup(box, body)
    body.move_to(box.get_center())
    g.to_corner(DL, buff=0.18).shift(UP * 0.95)
    return g


def block_stack(n: int, side: float, color, x: float, y: float = -0.2) -> VGroup:
    g = VGroup()
    for i in range(n):
        sq = Square(side_length=side, fill_opacity=0.32, stroke_width=2.0, color=color)
        sq.shift(RIGHT * i * 0.1 + DOWN * i * 0.1)
        g.add(sq)
    g.move_to([x, y, 0])
    return g


class PretrainedModels(BrandScene):
    chapter_title = "6 · Pretrained Models & Embeddings"

    def construct(self):
        self.setup_branding()

        key = terms_key([
            "backbone — pretrained feature extractor",
            "head — task-specific classifier",
            "embedding z — feature vector",
            "cos sim — similarity between images",
        ])
        self.play(FadeIn(key), run_time=0.7)

        self.say("Train a CNN once on millions of images — reuse it everywhere.", wait=1.6)

        # ---- Pretrained badge ----
        badge = RoundedRectangle(
            width=3.2, height=0.75, corner_radius=0.1,
            color=TEAL_D, fill_opacity=0.15, stroke_width=2.5,
        )
        badge_l = Text("Pretrained on ImageNet", font="Sans", weight=BOLD, color=TEAL_D).scale(0.34)
        badge_g = VGroup(badge, badge_l).move_to(UP * 1.35)
        self.play(FadeIn(badge_g), run_time=1.0)
        self.set_dims("already learned edges, textures, parts")
        self.wait(1.0)

        # ---- Full model L→R ----
        img = Square(1.5, color=BLUE_D, fill_opacity=0.25, stroke_width=2.5).shift(LEFT * 4.8)
        img_l = Text("your image", font="Sans", color=BLUE_D).scale(0.28).next_to(img, DOWN, buff=0.15)

        backbone = block_stack(6, 1.35, PURPLE_D, -1.8)
        bb_l = Text("backbone", font="Sans", color=PURPLE_D).scale(0.30).next_to(backbone, UP, buff=0.2)
        bb_sub = Text("(Conv blocks)", font="Sans", color=MUTED).scale(0.24).next_to(bb_l, DOWN, buff=0.05)

        head = VGroup(*[
            Circle(0.22, color=ORANGE_D, fill_opacity=0.35, stroke_width=2.5).shift(UP * (0.8 - i * 0.55))
            for i in range(4)
        ]).shift(RIGHT * 1.8)
        head_l = Text("head", font="Sans", color=ORANGE_D).scale(0.30).next_to(head, UP, buff=0.2)
        head_sub = Text("(FC + softmax)", font="Sans", color=MUTED).scale(0.24).next_to(head_l, DOWN, buff=0.05)

        out = VGroup(*[
            Text(c, font="Sans", color=INK).scale(0.28)
            for c in ["1000 classes"]
        ]).next_to(head, RIGHT, buff=0.5)

        a1 = Arrow(img.get_right(), backbone.get_left(), buff=0.12, color=GOLD_D, stroke_width=3)
        a2 = Arrow(backbone.get_right(), head.get_left(), buff=0.12, color=GOLD_D, stroke_width=3)
        a3 = Arrow(head.get_right(), out.get_left(), buff=0.12, color=MUTED, stroke_width=2.5)

        self.play(
            FadeIn(img), FadeIn(img_l),
            FadeIn(backbone), FadeIn(bb_l), FadeIn(bb_sub),
            GrowArrow(a1),
            run_time=1.4,
        )
        self.say("Backbone = feature extractor. Head = classifier for the original task.", wait=1.6)
        self.play(
            GrowArrow(a2), FadeIn(head), FadeIn(head_l), FadeIn(head_sub),
            GrowArrow(a3), FadeIn(out),
            run_time=1.3,
        )
        self.wait(1.2)

        # ---- Split & freeze backbone ----
        self.say("For a new task: keep the backbone — swap only the head.", wait=1.6)
        freeze = Text("freeze backbone weights", font="Sans", color=TEAL_D).scale(0.32)
        freeze.next_to(backbone, DOWN, buff=0.35)
        ring_bb = SurroundingRectangle(backbone, color=TEAL_D, buff=0.08, stroke_width=3)
        self.play(Create(ring_bb), FadeIn(freeze), run_time=0.9)

        new_head = VGroup(*[
            Circle(0.22, color=GREEN_D, fill_opacity=0.35, stroke_width=2.5).shift(UP * (0.6 - i * 0.45))
            for i in range(3)
        ]).move_to(head.get_center())
        new_l = Text("new head", font="Sans", color=GREEN_D).scale(0.30).next_to(new_head, UP, buff=0.2)
        new_out = VGroup(*[
            Text(c, font="Sans", color=GREEN_D).scale(0.28)
            for c in ["Cat", "Dog", "Bird"]
        ]).arrange(DOWN, buff=0.12).next_to(new_head, RIGHT, buff=0.45)

        self.play(
            FadeOut(VGroup(head, head_l, head_sub, out, a3)),
            FadeIn(new_head), FadeIn(new_l), FadeIn(new_out),
            run_time=1.2,
        )
        a3n = Arrow(new_head.get_right(), new_out.get_left(), buff=0.12, color=GREEN_D, stroke_width=3)
        self.play(GrowArrow(a3n), run_time=0.7)
        self.set_dims("train only the new head (fast, little data)")
        self.wait(1.3)

        # ---- Feature vector / embedding ----
        self.say("Or stop before the head — the backbone output is an embedding.", wait=1.7)
        self.play(
            FadeOut(VGroup(
                badge_g, img, img_l, backbone, bb_l, bb_sub, freeze, ring_bb,
                new_head, new_l, new_out, a1, a2, a3n,
            )),
            run_time=0.8,
        )

        # Embedding extraction path
        img_a = Square(1.2, color=BLUE_D, fill_opacity=0.25, stroke_width=2.5).shift(LEFT * 4.5 + UP * 0.3)
        la = Text("image A", font="Sans", color=BLUE_D).scale(0.26).next_to(img_a, DOWN, buff=0.12)
        img_b = Square(1.2, color=BLUE_D, fill_opacity=0.25, stroke_width=2.5).shift(LEFT * 4.5 + DOWN * 1.4)
        lb = Text("image B", font="Sans", color=BLUE_D).scale(0.26).next_to(img_b, DOWN, buff=0.12)

        bb_shared = block_stack(5, 1.1, PURPLE_D, -0.5, 0.0)
        bb_tag = Text("same frozen backbone", font="Sans", color=PURPLE_D).scale(0.28).next_to(bb_shared, UP, buff=0.2)

        za = VGroup(*[
            Dot(radius=0.09, color=GOLD_D).shift(UP * (0.9 - i * 0.35))
            for i in range(6)
        ]).shift(RIGHT * 2.2 + UP * 0.3)
        zb = VGroup(*[
            Dot(radius=0.09, color=GOLD_D).shift(UP * (0.9 - i * 0.35))
            for i in range(6)
        ]).shift(RIGHT * 2.2 + DOWN * 1.4)
        zla = Text("z_A", font="Sans", color=GOLD_D).scale(0.30).next_to(za, RIGHT, buff=0.2)
        zlb = Text("z_B", font="Sans", color=GOLD_D).scale(0.30).next_to(zb, RIGHT, buff=0.2)

        self.play(
            FadeIn(img_a), FadeIn(la), FadeIn(img_b), FadeIn(lb),
            FadeIn(bb_shared), FadeIn(bb_tag),
            run_time=1.2,
        )
        ar_a = Arrow(img_a.get_right(), bb_shared.get_left() + UP * 0.5, buff=0.1, color=MUTED, stroke_width=2.5)
        ar_b = Arrow(img_b.get_right(), bb_shared.get_left() + DOWN * 0.5, buff=0.1, color=MUTED, stroke_width=2.5)
        self.play(GrowArrow(ar_a), GrowArrow(ar_b), run_time=0.9)

        self.say("Forward pass → embedding vectors z (no softmax needed).", wait=1.5)
        out_a = Arrow(bb_shared.get_right() + UP * 0.4, za.get_left(), buff=0.1, color=GOLD_D, stroke_width=3)
        out_b = Arrow(bb_shared.get_right() + DOWN * 0.4, zb.get_left(), buff=0.1, color=GOLD_D, stroke_width=3)
        self.play(GrowArrow(out_a), FadeIn(za), FadeIn(zla), run_time=1.0)
        self.play(GrowArrow(out_b), FadeIn(zb), FadeIn(zlb), run_time=1.0)
        self.set_dims("z ∈ R^d  (e.g. d = 512)")

        # ---- Cosine similarity ----
        self.say("Compare embeddings — cosine similarity measures how alike two images are.", wait=1.7)
        formula = Text(
            "cos(z_A, z_B)  =  (z_A · z_B) / (||z_A|| ||z_B||)",
            font="Sans",
            color=ACCENT,
        ).scale(0.30)
        formula.move_to(DOWN * 1.55 + RIGHT * 0.5)
        self.play(Write(formula), run_time=1.2)

        # Simple numeric demo
        sim_high = Text("similar pair  →  cos ≈ 0.92  (same breed)", font="Sans", color=GREEN_D).scale(0.28)
        sim_low = Text("different pair →  cos ≈ 0.18  (unrelated)", font="Sans", color=RED_D).scale(0.28)
        examples = VGroup(sim_high, sim_low).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        examples.next_to(formula, DOWN, buff=0.22)
        self.play(FadeIn(examples), run_time=1.0)

        ring_z = SurroundingRectangle(VGroup(za, zb), color=GOLD_D, buff=0.15, stroke_width=3)
        self.play(Create(ring_z), run_time=0.6)
        self.wait(1.2)

        # Summary strip
        self.play(FadeOut(VGroup(formula, examples, ring_z)), run_time=0.5)
        summary = VGroup(
            Text("1. Load pretrained backbone", font="Sans", color=INK).scale(0.30),
            Text("2a. New head → classify your classes", font="Sans", color=GREEN_D).scale(0.30),
            Text("2b. Embeddings → search / match / retrieve", font="Sans", color=GOLD_D).scale(0.30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 1.45)
        self.say("Same pretrained CNN — two paths: classify or compare.", wait=1.6)
        self.play(LaggedStart(*[FadeIn(s) for s in summary], lag_ratio=0.35), run_time=1.4)
        self.set_dims("transfer learning · metric learning")
        self.wait(2.2)
