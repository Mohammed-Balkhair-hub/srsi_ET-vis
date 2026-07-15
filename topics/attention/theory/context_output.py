"""O = A V — context vector for 'sat' with clear text meaning."""

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

A_SAT = [0.254, 0.389, 0.357]
V_ROWS = [[1.0, 0.0], [0.0, 1.0], [0.2, 0.8]]
O_SAT = [0.326, 0.674]
A_FULL = [[0.485, 0.239, 0.276], [0.209, 0.424, 0.368], [0.254, 0.389, 0.357]]
O_FULL = [[0.540, 0.460], [0.282, 0.718], [0.326, 0.674]]


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


def cell_at(grid: VGroup, cols: int, r: int, c: int) -> VGroup:
    return grid[r * cols + c]


class ContextOutput(BrandScene):
    chapter_title = "3 · Context Vector (O = AV)"

    def construct(self):
        self.setup_branding()
        self.say("Mix values with attention weights — that is the new token vector.", wait=1.5)

        key = terms_key([
            "A — attention weights",
            "V — values (= X here)",
            "O = A V — outputs",
            "o_i = Σ_j A_ij v_j",
        ])
        self.play(FadeIn(key), run_time=0.7)

        formula = Text("o_i = Σ_j A_ij v_j      ⇔      O = A V", font="Sans", weight=BOLD, color=ACCENT).scale(0.36)
        formula.to_edge(UP, buff=1.0)
        self.play(Write(formula), run_time=1.2)
        self.set_dims("A: 3×3   ·   V: 3×2   ·   O: 3×2")

        # Alpha row for sat
        a_grid = number_grid([[A_SAT[0]], [A_SAT[1]], [A_SAT[2]]], cell=0.5, color=BLUE_D, font_scale=0.24)
        a_lab = Text("α (row sat)", font="Sans", color=BLUE_D).scale(0.26)
        labels = VGroup(*[Text(t, font="Sans", color=MUTED).scale(0.24) for t in ["the", "cat", "sat"]])
        a_rows = VGroup()
        for i in range(3):
            a_rows.add(VGroup(labels[i], a_grid[i]).arrange(RIGHT, buff=0.15))
        a_block = VGroup(a_lab, *a_rows).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        V = number_grid(V_ROWS, cell=0.5, color=TEAL_D, font_scale=0.24)
        V_lab = Text("V", font="Sans", color=TEAL_D).scale(0.28)
        V_g = VGroup(V_lab, V).arrange(DOWN, buff=0.1)

        top = VGroup(a_block, V_g).arrange(RIGHT, buff=1.0).move_to(UP * 0.55 + RIGHT * 0.8)
        self.play(FadeIn(top), run_time=1.2)

        work_anchor = DOWN * 1.2 + RIGHT * 1.3
        work = VGroup()
        rings = VGroup()

        def clear_work():
            nonlocal work, rings
            anims = []
            if len(work) > 0:
                anims.append(FadeOut(work))
            if len(rings) > 0:
                anims.append(FadeOut(rings))
            if anims:
                self.play(*anims, run_time=0.35)
            if len(work) > 0:
                self.remove(work)
            if len(rings) > 0:
                self.remove(rings)
            work = VGroup()
            rings = VGroup()

        def light(*mobs):
            nonlocal rings
            new = VGroup(*[yellow_ring(m) for m in mobs])
            if len(rings) > 0:
                self.play(ReplacementTransform(rings, new), run_time=0.35)
            else:
                self.play(FadeIn(new), run_time=0.35)
            rings = new

        def show_block(*lines: tuple[str, str]):
            """lines: (text, color_name)"""
            nonlocal work
            if len(work) > 0:
                self.play(FadeOut(work), run_time=0.3)
                self.remove(work)
            colors = {"ink": INK, "green": GREEN_D, "orange": ORANGE_D, "muted": MUTED, "accent": ACCENT}
            mobs = []
            for text, cname in lines:
                mobs.append(Text(text, font="Sans", color=colors[cname]).scale(0.28))
            block = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            block.move_to(work_anchor)
            work = block
            self.play(LaggedStart(*[FadeIn(m) for m in mobs], lag_ratio=0.35), run_time=1.2)
            self.wait(1.0)

        self.say("Query = sat. Weight each value, then sum.", wait=1.5)
        light(a_grid, V)
        show_block(
            ("o_sat = 0.254·v_the + 0.389·v_cat + 0.357·v_sat", "ink"),
            ("v_the=[1,0]  v_cat=[0,1]  v_sat=[0.2,0.8]", "muted"),
        )

        clear_work()
        show_block(
            ("= 0.254[1,0] + 0.389[0,1] + 0.357[0.2,0.8]", "ink"),
            ("= [0.326 ,  0.674]", "green"),
        )

        o_grid = number_grid([[O_SAT[0]], [O_SAT[1]]], cell=0.55, color=ORANGE_D, font_scale=0.26)
        o_lab = Text("o_sat", font="Sans", color=ORANGE_D).scale(0.30)
        o_g = VGroup(o_lab, o_grid).arrange(DOWN, buff=0.1).move_to(UP * 0.4 + RIGHT * 4.2)
        self.play(FadeIn(o_g), run_time=0.8)
        light(o_grid)
        self.wait(1.0)

        self.say("Largest weight was on cat — sat's vector leans toward cat.", wait=1.7)
        meaning = Text(
            "Meaning: “sat” borrows most from “cat” in this toy.",
            font="Sans",
            color=ACCENT,
        ).scale(0.32)
        meaning.move_to(work_anchor)
        if len(work) > 0:
            self.play(FadeOut(work), run_time=0.3)
            self.remove(work)
        work = meaning
        self.play(FadeIn(meaning), run_time=0.8)
        ring_cat = yellow_ring(a_grid[1])
        self.play(Create(ring_cat), run_time=0.5)
        self.wait(1.4)

        # Full O
        clear_work()
        self.play(FadeOut(ring_cat), FadeOut(VGroup(top, o_g, formula)), run_time=0.6)
        self.say("Do this for every query row → full output O = A V.", wait=1.5)

        A = number_grid(A_FULL, cell=0.48, color=BLUE_D, font_scale=0.20)
        V2 = number_grid(V_ROWS, cell=0.48, color=TEAL_D, font_scale=0.22)
        O = number_grid(O_FULL, cell=0.48, color=ORANGE_D, font_scale=0.22)
        full = VGroup(
            VGroup(Text("A", font="Sans", color=BLUE_D).scale(0.28), A).arrange(DOWN, buff=0.1),
            Text("×", font="Sans", color=INK).scale(0.4),
            VGroup(Text("V", font="Sans", color=TEAL_D).scale(0.28), V2).arrange(DOWN, buff=0.1),
            Text("=", font="Sans", color=INK).scale(0.4),
            VGroup(Text("O", font="Sans", color=ORANGE_D).scale(0.28), O).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.28).move_to(UP * 0.35 + RIGHT * 0.6)

        self.play(FadeIn(full), run_time=1.3)
        light(O)
        self.set_dims("O ∈ R^{3×2} — new vectors for the / cat / sat")
        punch = Text("Next layers use O — attention mixes information across tokens.", font="Sans", color=ACCENT).scale(0.30)
        punch.move_to(DOWN * 1.5)
        work = punch
        self.play(FadeIn(punch), run_time=0.9)
        self.wait(2.0)
