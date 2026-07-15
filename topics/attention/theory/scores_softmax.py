"""Scores S = QK^T / sqrt(d_k) and row-wise softmax → A."""

from __future__ import annotations

import math
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

TOKENS = ["the", "cat", "sat"]
X_VALS = [[1.0, 0.0], [0.0, 1.0], [0.2, 0.8]]
# XX^T
S_RAW = [[1.0, 0.0, 0.2], [0.0, 1.0, 0.8], [0.2, 0.8, 0.68]]
SCALE = math.sqrt(2)
S_SCALED = [[round(v / SCALE, 3) for v in row] for row in S_RAW]
# softmax rows (precomputed)
A_VALS = [[0.485, 0.239, 0.276], [0.209, 0.424, 0.368], [0.254, 0.389, 0.357]]


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


def cell_at(grid: VGroup, cols: int, r: int, c: int) -> VGroup:
    return grid[r * cols + c]


def row_group(grid: VGroup, cols: int, r: int) -> VGroup:
    return VGroup(*[cell_at(grid, cols, r, c) for c in range(cols)])


def col_group(grid: VGroup, rows: int, cols: int, c: int) -> VGroup:
    return VGroup(*[cell_at(grid, cols, r, c) for r in range(rows)])


def yellow_ring(m: Mobject) -> SurroundingRectangle:
    return SurroundingRectangle(m, color=GOLD_D, buff=0.04, stroke_width=3.5)


class ScoresSoftmax(BrandScene):
    chapter_title = "3 · Scores → Softmax"

    def construct(self):
        self.setup_branding()
        self.say("Compare every query to every key — then soft-normalize.", wait=1.5)

        key = terms_key([
            "S = Q Kᵀ / √d_k  — scores",
            "A = softmax(S) — weights (rows → 1)",
            "√d_k — keeps dots from exploding",
            "Q = K = X in this toy",
        ])
        self.play(FadeIn(key), run_time=0.7)

        formula = Text("S = Q Kᵀ / √d_k     →     A = softmax(S)  (per row)", font="Sans", color=ACCENT).scale(0.30)
        formula.to_edge(UP, buff=1.0)
        self.play(Write(formula), run_time=1.2)
        self.set_dims("Q,K: 3×2   ·   S,A: 3×3   ·   d_k = 2")

        Q = number_grid(X_VALS, cell=0.42, color=ORANGE_D, font_scale=0.22)
        K = number_grid(X_VALS, cell=0.42, color=GREEN_D, font_scale=0.22)
        Q_lab = Text("Q", font="Sans", color=ORANGE_D).scale(0.28)
        K_lab = Text("K", font="Sans", color=GREEN_D).scale(0.28)
        Q_g = VGroup(Q_lab, Q).arrange(DOWN, buff=0.08)
        K_g = VGroup(K_lab, K).arrange(DOWN, buff=0.08)

        S_grid = number_grid([["—", "—", "—"], ["—", "—", "—"], ["—", "—", "—"]], cell=0.42, color=TEAL_D, font_scale=0.20)
        S_lab = Text("S = QKᵀ/√d_k", font="Sans", color=TEAL_D).scale(0.24)
        S_g = VGroup(S_lab, S_grid).arrange(DOWN, buff=0.08)

        mats = VGroup(Q_g, K_g, S_g).arrange(RIGHT, buff=0.55).move_to(UP * 0.55 + RIGHT * 0.9)
        self.play(FadeIn(mats), run_time=1.2)

        work_anchor = DOWN * 1.25 + RIGHT * 1.5
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

        def show_formula(eq: str, expand: str):
            nonlocal work
            if len(work) > 0:
                self.play(FadeOut(work), run_time=0.3)
                self.remove(work)
            title = Text(eq, font="Sans", color=INK).scale(0.28)
            exp = Text(expand, font="Sans", color=GREEN_D).scale(0.28)
            block = VGroup(title, exp).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            block.move_to(work_anchor)
            work = block
            self.play(FadeIn(title), run_time=0.65)
            self.wait(0.9)
            self.play(FadeIn(exp), run_time=0.7)
            self.wait(0.9)

        def fill_cell(grid: VGroup, cols: int, r: int, c: int, value: str):
            cell = cell_at(grid, cols, r, c)
            new_txt = Text(value, font="Sans").scale(0.20).set_color(INK).move_to(cell[0])
            self.play(Transform(cell[1], new_txt), run_time=0.55)
            light(cell)
            self.wait(0.45)

        self.say("Each score = (query row) · (key row) / √d_k. Fill S entry by entry.", wait=1.6)

        # Demonstrate a few representative entries: (0,0), (0,2), (2,1), then fill rest quickly
        demos = [
            (0, 0, "S_00 = [1,0]·[1,0] / √2", "= 1.0 / 1.414 = 0.707", "0.707"),
            (0, 2, "S_02 = [1,0]·[0.2,0.8] / √2", "= 0.2 / 1.414 = 0.141", "0.141"),
            (2, 1, "S_21 = [0.2,0.8]·[0,1] / √2", "= 0.8 / 1.414 = 0.566", "0.566"),
        ]
        for r, c, eq, exp, val in demos:
            light(row_group(Q, 2, r), row_group(K, 2, c))
            show_formula(eq, exp)
            fill_cell(S_grid, 3, r, c, val)

        self.say("Fill the remaining scores the same way.", wait=1.2)
        clear_work()
        rest = [(0, 1, "0.000"), (1, 0, "0.000"), (1, 1, "0.707"), (1, 2, "0.566"), (2, 0, "0.141"), (2, 2, "0.481")]
        for r, c, val in rest:
            light(row_group(Q, 2, r), row_group(K, 2, c))
            fill_cell(S_grid, 3, r, c, val)

        self.say("Why ÷√d_k? Larger d_k → bigger dots → softmax too sharp.", wait=1.6)
        scale_note = Text("Scale keeps attention soft enough to train.", font="Sans", color=MUTED).scale(0.28)
        scale_note.move_to(work_anchor)
        work = scale_note
        self.play(FadeIn(scale_note), run_time=0.7)
        self.wait(1.2)

        # Softmax for sat row
        clear_work()
        self.say("Softmax on one row (query = sat) — weights sum to 1.", wait=1.5)
        A_grid = number_grid([["—", "—", "—"], ["—", "—", "—"], ["—", "—", "—"]], cell=0.42, color=BLUE_D, font_scale=0.20)
        A_lab = Text("A = softmax(S)", font="Sans", color=BLUE_D).scale(0.24)
        A_g = VGroup(A_lab, A_grid).arrange(DOWN, buff=0.08)
        A_g.next_to(S_g, RIGHT, buff=0.45)
        self.play(FadeIn(A_g), run_time=0.8)

        light(row_group(S_grid, 3, 2))
        show_formula(
            "row sat:  softmax([0.141, 0.566, 0.481])",
            "→  [0.254, 0.389, 0.357]   (largest on cat)",
        )
        for c, val in enumerate(["0.254", "0.389", "0.357"]):
            fill_cell(A_grid, 3, 2, c, val)

        self.say("Fill all rows of A the same way.", wait=1.2)
        clear_work()
        for r in range(3):
            for c in range(3):
                if r == 2:
                    continue
                fill_cell(A_grid, 3, r, c, f"{A_VALS[r][c]:.3f}")
        self.wait(1.8)
