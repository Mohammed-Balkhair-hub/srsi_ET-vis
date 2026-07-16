"""Pretrained CNNs — backbone features, flatten to an embedding, swap the head."""

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
)

FROZEN = BLUE_D      # weights fixed
TRAIN = GREEN_D      # weights update


def terms_key(lines: list[str]) -> VGroup:
    rows = VGroup(*[
        Text(line, font="Sans", color=INK).scale(0.21) for line in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    title = Text("Key", font="Sans", weight=BOLD, color=ACCENT).scale(0.24)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    box = SurroundingRectangle(body, buff=0.12, corner_radius=0.08, color=MUTED, stroke_width=1.5)
    box.set_fill("#F7F9FB", opacity=1.0)
    g = VGroup(box, body)
    body.move_to(box.get_center())
    g.to_corner(DL, buff=0.18).shift(UP * 0.9)
    return g


def block_stack(n: int, side: float, color, depth: float = 0.11) -> VGroup:
    g = VGroup()
    for i in range(n):
        sq = Square(side_length=side, fill_opacity=0.30, stroke_width=2.0, color=color)
        sq.shift(RIGHT * i * depth + DOWN * i * depth)
        g.add(sq)
    g.move_to(ORIGIN)
    return g


def feature_volume(channels: int, color, height: float, width: float, depth: float = 0.07) -> VGroup:
    """Faux stack of many channel-planes → a 'high channel' feature map."""
    g = VGroup()
    for i in range(channels):
        r = Rectangle(width=width, height=height, color=color, stroke_width=1.5, fill_opacity=0.16)
        r.shift(RIGHT * i * depth + UP * i * depth)
        g.add(r)
    g.move_to(ORIGIN)
    return g


def embedding_vector(values, color=GOLD_D, cell_w: float = 0.72, cell_h: float = 0.30) -> VGroup:
    """A real column vector: numbered cells wrapped in square brackets."""
    cells = VGroup()
    for v in values:
        sq = Rectangle(width=cell_w, height=cell_h, color=color, stroke_width=1.5, fill_opacity=0.16)
        t = Text(f"{v:+.2f}", font="Sans", color=INK).scale(0.22).move_to(sq)
        cells.add(VGroup(sq, t))
    cells.arrange(DOWN, buff=0.03)
    y_top = cells.get_top()[1] + 0.05
    y_bot = cells.get_bottom()[1] - 0.05
    lx = cells.get_left()[0] - 0.1
    rx = cells.get_right()[0] + 0.1
    tick = 0.12
    lb = VGroup(
        Line([lx, y_bot, 0], [lx, y_top, 0], color=color, stroke_width=2.5),
        Line([lx, y_top, 0], [lx + tick, y_top, 0], color=color, stroke_width=2.5),
        Line([lx, y_bot, 0], [lx + tick, y_bot, 0], color=color, stroke_width=2.5),
    )
    rb = VGroup(
        Line([rx, y_bot, 0], [rx, y_top, 0], color=color, stroke_width=2.5),
        Line([rx, y_top, 0], [rx - tick, y_top, 0], color=color, stroke_width=2.5),
        Line([rx, y_bot, 0], [rx - tick, y_bot, 0], color=color, stroke_width=2.5),
    )
    return VGroup(lb, cells, rb)


def mini_nn(layer_sizes, color, node_r: float = 0.10, layer_gap: float = 0.75, node_gap: float = 0.30):
    """A small fully-connected net: columns of nodes + edges between layers."""
    layers = []
    for li, n in enumerate(layer_sizes):
        col = VGroup(*[
            Circle(radius=node_r, color=color, fill_opacity=0.55, stroke_width=1.8)
            for _ in range(n)
        ]).arrange(DOWN, buff=node_gap)
        col.shift(RIGHT * li * layer_gap)
        layers.append(col)
    edges = VGroup()
    for a, b in zip(layers, layers[1:]):
        for na in a:
            for nb in b:
                ln = Line(na.get_center(), nb.get_center(), color=color, stroke_width=1.0)
                ln.set_stroke(opacity=0.35)
                edges.add(ln)
    net = VGroup(edges, *layers)
    net.move_to(ORIGIN)
    return net, layers, edges


def state_chip(swatch_color, label: str) -> VGroup:
    sw = Square(0.24, color=swatch_color, fill_opacity=0.55, stroke_width=1.6)
    tx = Text(label, font="Sans", color=INK).scale(0.24).next_to(sw, RIGHT, buff=0.14)
    return VGroup(sw, tx)


class PretrainedModels(BrandScene):
    chapter_title = "6 · Pretrained Models & Embeddings"

    def construct(self):
        self.setup_branding()

        key = terms_key([
            "backbone — pretrained conv feature extractor",
            "feature map — C×H×W activations (many channels)",
            "flatten → embedding z (a vector)",
            "head — small trainable neural net",
            "cos sim — how alike two embeddings are",
        ])
        self.play(FadeIn(key), run_time=0.7)
        self.say("Train a CNN once on millions of images — then reuse it everywhere.", wait=1.6)

        # =====================================================================
        # STAGE 1 — the pretrained network on its original task
        # =====================================================================
        badge = RoundedRectangle(width=3.2, height=0.6, corner_radius=0.1,
                                 color=TEAL_D, fill_opacity=0.15, stroke_width=2.2)
        badge_l = Text("Pretrained on ImageNet", font="Sans", weight=BOLD, color=TEAL_D).scale(0.30)
        badge_g = VGroup(badge, badge_l).move_to(UP * 2.4 + RIGHT * 0.3)
        self.play(FadeIn(badge_g), run_time=0.8)

        Y = 0.35
        img = Square(1.0, color=INK, fill_opacity=0.08, stroke_width=2.2).move_to([-5.4, Y, 0])
        img_l = Text("your image", font="Sans", color=INK).scale(0.24).next_to(img, DOWN, buff=0.14)

        backbone = block_stack(5, 0.95, PURPLE_D).move_to([-3.5, Y, 0])
        bb_l = Text("backbone", font="Sans", weight=BOLD, color=PURPLE_D).scale(0.28).next_to(backbone, UP, buff=0.5)

        fvol = feature_volume(8, PURPLE_D, height=1.0, width=0.42).move_to([-1.95, Y, 0])
        fvol_l = Text("feature map", font="Sans", color=MUTED).scale(0.22).next_to(fvol, UP, buff=0.16)
        fvol_d = Text("C×H×W", font="Sans", color=MUTED).scale(0.20).next_to(fvol, DOWN, buff=0.14)

        emb = embedding_vector([0.31, 0.86, -0.10, 0.62, -0.42, 0.20], color=GOLD_D).move_to([-0.35, Y, 0])
        emb_l = Text("embedding z", font="Sans", weight=BOLD, color=GOLD_D).scale(0.26).next_to(emb, UP, buff=0.16)

        head, head_layers, _ = mini_nn([3, 4], ORANGE_D)
        head.move_to([2.15, Y, 0])
        head_l = Text("head (NN)", font="Sans", weight=BOLD, color=ORANGE_D).scale(0.28).next_to(head, UP, buff=0.3)
        out = Text("1000 classes", font="Sans", color=INK).scale(0.26).next_to(head, RIGHT, buff=0.4)

        a1 = Arrow(img.get_right(), backbone.get_left(), buff=0.1, color=GOLD_D, stroke_width=3)
        a2 = Arrow(backbone.get_right(), fvol.get_left(), buff=0.1, color=GOLD_D, stroke_width=3)

        self.play(FadeIn(img), FadeIn(img_l), GrowArrow(a1),
                  FadeIn(backbone), FadeIn(bb_l), run_time=1.2)
        self.say("The backbone is a stack of conv blocks — the learned feature extractor.", wait=1.5)
        self.play(GrowArrow(a2), FadeIn(fvol), FadeIn(fvol_l), FadeIn(fvol_d), run_time=1.1)
        self.set_dims("output = a deep, many-channel feature map")
        self.wait(0.8)

        # Flatten the volume into the embedding vector (fancy transform)
        flat_arrow = Arrow(fvol.get_right(), emb.get_left(), buff=0.12, color=GOLD_D, stroke_width=3)
        flat_l = Text("flatten", font="Sans", color=GOLD_D).scale(0.22).next_to(flat_arrow, UP, buff=0.08)
        self.say("Flatten that volume into one long vector — this is the embedding z.", wait=1.4)
        self.play(GrowArrow(flat_arrow), FadeIn(flat_l), run_time=0.7)
        self.play(TransformFromCopy(fvol, emb), FadeIn(emb_l), run_time=1.2)
        self.set_dims("z ∈ R^d  (e.g. d = 512)")
        self.wait(0.6)

        # Head classifies the embedding
        a3 = Arrow(emb.get_right(), head.get_left(), buff=0.12, color=MUTED, stroke_width=2.5)
        a4 = Arrow(head.get_right(), out.get_left(), buff=0.12, color=MUTED, stroke_width=2.5)
        self.say("The head is a small neural net that maps z → class scores.", wait=1.5)
        self.play(GrowArrow(a3), FadeIn(head), FadeIn(head_l), run_time=1.1)
        self.play(GrowArrow(a4), FadeIn(out), run_time=0.8)
        self.wait(1.0)

        # =====================================================================
        # STAGE 2 — transfer: FREEZE backbone (blue), TRAIN new head (green)
        # =====================================================================
        self.play(FadeOut(badge_g), run_time=0.4)
        legend = VGroup(
            state_chip(FROZEN, "frozen · weights fixed"),
            state_chip(TRAIN, "training · weights update"),
        ).arrange(RIGHT, buff=0.6).move_to(UP * 2.45 + RIGHT * 0.2)
        self.say("New task? FREEZE the backbone — keep its features exactly as they are.", wait=1.6)
        self.play(FadeIn(legend[0]), run_time=0.5)
        frozen_ring = SurroundingRectangle(VGroup(backbone, fvol), color=FROZEN, buff=0.12, stroke_width=3)
        frozen_tag = Text("frozen", font="Sans", weight=BOLD, color=FROZEN).scale(0.26).next_to(backbone, DOWN, buff=0.7)
        self.play(
            backbone.animate.set_color(FROZEN).set_fill(FROZEN, opacity=0.18),
            fvol.animate.set_color(FROZEN).set_fill(FROZEN, opacity=0.16),
            Create(frozen_ring), FadeIn(frozen_tag),
            run_time=1.1,
        )
        self.wait(0.6)

        # Swap the head for a fresh trainable net
        self.say("Swap in a NEW head and put it in training mode (only these weights change).", wait=1.7)
        new_head, new_layers, _ = mini_nn([3, 3], TRAIN)
        new_head.move_to(head.get_center())
        new_head_l = Text("new head", font="Sans", weight=BOLD, color=TRAIN).scale(0.28).next_to(new_head, UP, buff=0.3)
        classes = ["Cat", "Dog", "Bird"]
        new_out = VGroup(*[
            Text(c, font="Sans", color=TRAIN).scale(0.26).next_to(node, RIGHT, buff=0.35)
            for c, node in zip(classes, new_layers[-1])
        ])
        self.play(
            FadeOut(VGroup(head, head_l, out, a4)),
            FadeIn(legend[1]),
            run_time=0.7,
        )
        a4n = Arrow(new_head.get_right(), new_out.get_left(), buff=0.15, color=TRAIN, stroke_width=2.5)
        train_tag = Text("training", font="Sans", weight=BOLD, color=TRAIN).scale(0.26).next_to(new_head, DOWN, buff=0.3)
        self.play(FadeIn(new_head), FadeIn(new_head_l), FadeIn(train_tag), run_time=1.0)
        self.play(GrowArrow(a4n), LaggedStart(*[FadeIn(c) for c in new_out], lag_ratio=0.3), run_time=1.0)
        self.set_dims("train only the new head — fast, little data")
        # pulse the trainable head to signal "learning"
        self.play(Indicate(new_head, color=TRAIN, scale_factor=1.12), run_time=0.7)
        self.play(Indicate(new_head, color=TRAIN, scale_factor=1.12), run_time=0.7)
        self.wait(1.2)

        # =====================================================================
        # STAGE 3 — embeddings for similarity (two different vectors)
        # =====================================================================
        self.say("Skip the head entirely — the embedding itself describes the image.", wait=1.6)
        self.play(
            FadeOut(VGroup(
                img, img_l, a1, backbone, bb_l, a2, fvol, fvol_l, fvol_d,
                flat_arrow, flat_l, emb, emb_l, a3, new_head, new_head_l,
                new_out, a4n, train_tag, frozen_ring, frozen_tag, legend, key,
            )),
            run_time=0.8,
        )

        img_a = Square(0.8, color=INK, fill_opacity=0.08, stroke_width=2.2).move_to([-5.6, 1.25, 0])
        la = Text("image A", font="Sans", color=INK).scale(0.22).next_to(img_a, DOWN, buff=0.1)
        img_b = Square(0.8, color=INK, fill_opacity=0.08, stroke_width=2.2).move_to([-5.6, -1.45, 0])
        lb = Text("image B", font="Sans", color=INK).scale(0.22).next_to(img_b, DOWN, buff=0.1)

        shared = block_stack(5, 0.85, FROZEN).move_to([-3.5, -0.1, 0])
        shared.set_fill(FROZEN, opacity=0.18)
        shared_l = Text("same frozen backbone", font="Sans", weight=BOLD, color=FROZEN).scale(0.24).next_to(shared, UP, buff=0.25)
        shared_s = Text("(shared weights)", font="Sans", color=MUTED).scale(0.20).next_to(shared_l, DOWN, buff=0.05)

        fva = feature_volume(6, FROZEN, height=0.62, width=0.32).move_to([-1.9, 1.25, 0])
        fvb = feature_volume(6, FROZEN, height=0.62, width=0.32).move_to([-1.9, -1.45, 0])
        feat_l = Text("features", font="Sans", color=MUTED).scale(0.20).next_to(fva, UP, buff=0.12)

        za = embedding_vector([0.31, 0.86, -0.10, 0.62, -0.42, 0.20], color=GOLD_D,
                              cell_w=0.62, cell_h=0.26).move_to([0.5, 1.25, 0])
        zb = embedding_vector([0.27, 0.80, -0.18, 0.69, -0.35, 0.14], color=GOLD_D,
                              cell_w=0.62, cell_h=0.26).move_to([0.5, -1.45, 0])
        zla = Text("z_A", font="Sans", weight=BOLD, color=GOLD_D).scale(0.28).next_to(za, UP, buff=0.12)
        zlb = Text("z_B", font="Sans", weight=BOLD, color=GOLD_D).scale(0.28).next_to(zb, UP, buff=0.12)

        self.play(FadeIn(img_a), FadeIn(la), FadeIn(img_b), FadeIn(lb),
                  FadeIn(shared), FadeIn(shared_l), FadeIn(shared_s), run_time=1.1)
        ar_a = Arrow(img_a.get_right(), shared.get_left() + UP * 0.35, buff=0.1, color=MUTED, stroke_width=2.2)
        ar_b = Arrow(img_b.get_right(), shared.get_left() + DOWN * 0.35, buff=0.1, color=MUTED, stroke_width=2.2)
        self.play(GrowArrow(ar_a), GrowArrow(ar_b), run_time=0.8)

        oa = Arrow(shared.get_right() + UP * 0.3, fva.get_left(), buff=0.1, color=FROZEN, stroke_width=2.2)
        ob = Arrow(shared.get_right() + DOWN * 0.3, fvb.get_left(), buff=0.1, color=FROZEN, stroke_width=2.2)
        self.play(GrowArrow(oa), FadeIn(fva), FadeIn(feat_l),
                  GrowArrow(ob), FadeIn(fvb), run_time=1.0)

        self.say("Each image → its own feature map → flatten → its own embedding vector.", wait=1.6)
        fa = Arrow(fva.get_right(), za.get_left(), buff=0.12, color=GOLD_D, stroke_width=2.5)
        fb = Arrow(fvb.get_right(), zb.get_left(), buff=0.12, color=GOLD_D, stroke_width=2.5)
        self.play(GrowArrow(fa), TransformFromCopy(fva, za), FadeIn(zla), run_time=1.1)
        self.play(GrowArrow(fb), TransformFromCopy(fvb, zb), FadeIn(zlb), run_time=1.1)
        self.set_dims("two images → two different vectors z_A, z_B")
        self.wait(0.8)

        # Cosine similarity panel (right)
        self.say("Cosine similarity compares the two vectors — close vectors = similar images.", wait=1.7)
        title_c = Text("cosine similarity", font="Sans", weight=BOLD, color=ACCENT).scale(0.26)
        form = Text("cos(z_A, z_B) = (z_A · z_B) / (‖z_A‖ ‖z_B‖)", font="Sans", color=INK).scale(0.22)
        res_hi = Text("= 0.97  → very similar", font="Sans", weight=BOLD, color=GREEN_D).scale(0.24)
        res_lo = Text("unrelated image → ≈ 0.10", font="Sans", color=RED_D).scale(0.22)
        panel = VGroup(title_c, form, res_hi, res_lo).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        panel.move_to([4.35, -0.1, 0])
        pa = Arrow(za.get_right(), panel.get_left() + UP * 0.4, buff=0.15, color=MUTED, stroke_width=2.2)
        pb = Arrow(zb.get_right(), panel.get_left() + DOWN * 0.4, buff=0.15, color=MUTED, stroke_width=2.2)
        self.play(GrowArrow(pa), GrowArrow(pb), run_time=0.7)
        self.play(FadeIn(title_c), Write(form), run_time=1.1)
        self.play(FadeIn(res_hi), run_time=0.6)
        self.play(FadeIn(res_lo), run_time=0.6)
        self.wait(1.4)

        # =====================================================================
        # Summary
        # =====================================================================
        self.play(FadeOut(VGroup(
            img_a, la, img_b, lb, shared, shared_l, shared_s, fva, fvb, feat_l,
            za, zb, zla, zlb, ar_a, ar_b, oa, ob, fa, fb, pa, pb, panel,
        )), run_time=0.7)
        summary = VGroup(
            Text("1. Load a pretrained backbone (frozen features)", font="Sans", color=INK).scale(0.30),
            Text("2a. Add a new trainable head → classify your classes", font="Sans", color=TRAIN).scale(0.30),
            Text("2b. Use embeddings → search / match / retrieve", font="Sans", color=GOLD_D).scale(0.30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(UP * 0.1)
        self.say("Same pretrained CNN — two paths: classify, or compare.", wait=1.6)
        self.play(LaggedStart(*[FadeIn(s) for s in summary], lag_ratio=0.35), run_time=1.4)
        self.set_dims("transfer learning · metric learning")
        self.wait(2.2)
