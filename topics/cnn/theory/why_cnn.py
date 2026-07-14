"""Why CNNs? — MLP parameter explosion vs local filters."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import ACCENT, BLUE_D, INK, MUTED, ORANGE_D, PURPLE_D, RED_D, TEAL_D, BrandScene


class WhyCNNs(BrandScene):
    chapter_title = "1 · Why Convolutional Neural Networks?"

    def construct(self):
        self.setup_branding()
        self.say("Images make plain MLPs explode in size.", wait=1.6)

        img = Square(2.2, color=BLUE_D, fill_opacity=0.25, stroke_width=2.5)
        img_lbl = Text("64 × 64 × 3", font="Sans", color=INK).scale(0.35).next_to(img, UP, buff=0.2)
        img_grp = VGroup(img, img_lbl).shift(LEFT * 3.5)
        self.play(FadeIn(img_grp), run_time=1.2)
        self.set_dims("64×64×3 = 12,288 inputs")

        flat = VGroup(*[
            Dot(radius=0.06, color=ORANGE_D).shift(UP * (1.4 - i * 0.18))
            for i in range(12)
        ]).shift(LEFT * 0.8)
        dots_lbl = Text("… 12,288 …", font="Sans", color=MUTED).scale(0.28).next_to(flat, DOWN, buff=0.15)
        arrow1 = Arrow(img.get_right(), flat.get_left(), buff=0.15, color=MUTED, stroke_width=3)
        flatten_tag = Text("Flatten", font="Sans", color=ORANGE_D).scale(0.32).next_to(arrow1, UP, buff=0.1)

        self.say("Flattening destroys the 2D layout of pixels.", wait=1.4)
        self.play(GrowArrow(arrow1), Write(flatten_tag), FadeIn(flat), Write(dots_lbl), run_time=1.4)
        self.wait(1.2)

        hidden = VGroup(*[
            Circle(0.18, color=PURPLE_D, fill_opacity=0.35, stroke_width=2.5).shift(UP * (1.2 - i * 0.55))
            for i in range(5)
        ]).shift(RIGHT * 2.8)
        h_lbl = Text("1,024 neurons", font="Sans", color=INK).scale(0.3).next_to(hidden, UP, buff=0.2)
        edges = VGroup()
        for d in flat[::2]:
            for h in hidden:
                edges.add(Line(d.get_right(), h.get_left(), stroke_width=1.0, stroke_opacity=0.35, color=MUTED))

        self.say("One hidden layer: 12,288 × 1,024 ≈ 12.6M parameters!", wait=1.5)
        self.play(Create(edges), FadeIn(hidden), Write(h_lbl), run_time=1.6)

        bomb = Text("~12.6M weights — just for one layer", font="Sans", color=RED_D).scale(0.38)
        bomb.to_edge(DOWN, buff=1.15)
        self.play(Write(bomb), run_time=1.0)
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(img_grp, arrow1, flatten_tag, flat, dots_lbl, edges, hidden, h_lbl, bomb)),
            run_time=0.9,
        )
        problems = VGroup(
            Text("1. Parameter explosion → overfitting + slow training", font="Sans", color=RED_D).scale(0.4),
            Text("2. No spatial awareness — neighbors are forgotten", font="Sans", color=RED_D).scale(0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(ORIGIN)
        self.say("Two fatal problems with MLPs on images:", wait=1.3)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in problems], lag_ratio=0.35), run_time=1.4)
        self.wait(1.5)

        self.play(FadeOut(problems), run_time=0.7)
        bullets = VGroup(
            Text("Local patterns: edges, textures, corners", font="Sans", color=INK).scale(0.36),
            Text("Hierarchy: edges → shapes → parts → objects", font="Sans", color=INK).scale(0.36),
            Text("Translation: a cat is still a cat if it moves", font="Sans", color=INK).scale(0.36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(LEFT * 0.5)

        self.say("Images have local structure — CNNs exploit it.", wait=1.4)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bullets], lag_ratio=0.3), run_time=1.5)
        self.wait(1.4)

        self.play(FadeOut(bullets), run_time=0.7)
        idea = VGroup(
            Text("CNN idea", font="Sans", weight=BOLD, color=ACCENT).scale(0.45),
            Text("Small filter slides across the image", font="Sans", color=INK).scale(0.36),
            Text("Same weights reused everywhere → parameter sharing", font="Sans", color=INK).scale(0.36),
            Text("Stack layers: edges → complex patterns", font="Sans", color=INK).scale(0.36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        self.say("Reuse one tiny filter everywhere — far fewer parameters.", wait=1.4)
        self.play(LaggedStart(*[FadeIn(x) for x in idea], lag_ratio=0.25), run_time=1.6)
        self.wait(1.5)

        compare = Text("3×3×3 filter ≈ 28 params  vs  FC neuron ≈ 12,288", font="Sans", color=TEAL_D).scale(0.36)
        compare.next_to(idea, DOWN, buff=0.55)
        self.play(Write(compare), run_time=1.0)
        self.wait(2.0)
