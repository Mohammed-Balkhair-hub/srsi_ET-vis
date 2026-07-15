"""Copy X → Q,K,V then S = QKᵀ/√d_k and softmax → A (merged 02+03)."""

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

TOKENS = ["the", "cat", "sat"]
X_VALS = [[1.0, 0.0], [0.0, 1.0], [0.2, 0.8]]
A_VALS = [[0.485, 0.239, 0.276], [0.209, 0.424, 0.368], [0.254, 0.389, 0.357]]


def terms_key(lines: list[str]) -> VGroup:
    rows = VGroup(*[Text(line, font="Sans", color=INK).scale(0.18) for line in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.05
    )
    title = Text("Key", font="Sans", weight=BOLD, color=ACCENT).scale(0.20)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    box = SurroundingRectangle(body, buff=0.1, corner_radius=0.08, color=MUTED, stroke_width=1.5)
    box.set_fill("#F7F9FB", opacity=1.0)
    g = VGroup(box, body)
    body.move_to(box.get_center())
    g.to_corner(DL, buff=0.16).shift(UP * 0.95)
    return g


def cell_at(grid: VGroup, cols: int, r: int, c: int) -> VGroup:
    return grid[r * cols + c]


def row_group(grid: VGroup, cols: int, r: int) -> VGroup:
    return VGroup(*[cell_at(grid, cols, r, c) for c in range(cols)])


def yellow_ring(m: Mobject) -> SurroundingRectangle:
    return SurroundingRectangle(m, color=GOLD_D, buff=0.04, stroke_width=3.5)


def labeled_square_matrix(
    values,
    *,
    cell: float,
    color,
    font_scale: float,
    title: str,
    title_color,
    row_words: list[str],
    col_words: list[str],
) -> tuple[VGroup, VGroup]:
    """
    Build a T×T grid with word labels:
      - left of each row = query word
      - above each column = key word
    Returns (whole_block, grid_only).
    """
    grid = number_grid(values, cell=cell, color=color, font_scale=font_scale)
    n = len(row_words)

    row_labs = VGroup(*[
        Text(w, font="Sans", color=MUTED).scale(0.20) for w in row_words
    ])
    for i, lab in enumerate(row_labs):
        lab.next_to(cell_at(grid, n, i, 0), LEFT, buff=0.14)

    col_labs = VGroup(*[
        Text(w, font="Sans", color=MUTED).scale(0.20) for w in col_words
    ])
    for j, lab in enumerate(col_labs):
        lab.next_to(cell_at(grid, n, 0, j), UP, buff=0.10)

    q_tag = Text("query ↓", font="Sans", color=MUTED).scale(0.16)
    k_tag = Text("key →", font="Sans", color=MUTED).scale(0.16)
    q_tag.next_to(row_labs, LEFT, buff=0.08)
    k_tag.next_to(col_labs, UP, buff=0.06)

    title_m = Text(title, font="Sans", color=title_color).scale(0.24)
    title_m.next_to(VGroup(col_labs, grid), UP, buff=0.22)

    block = VGroup(title_m, col_labs, k_tag, row_labs, q_tag, grid)
    return block, grid


class QKVScores(BrandScene):
    chapter_title = "2 · Q, K, V → Scores → Softmax"

    def construct(self):
        self.setup_branding()
        self.say("Start from embeddings X for “the cat sat”.", wait=1.5)

        key = terms_key([
            "X — input embeddings",
            "Q,K,V — copies/roles of X",
            "S_ij — how related query i is to key j",
            "A_ij — soft weight of that link",
            "W = I in this toy",
        ])
        self.play(FadeIn(key), run_time=0.7)

        toks = VGroup(*[
            Text(t, font="Sans", color=BLUE_D).scale(0.30)
            for t in ["the", "cat", "sat"]
        ]).arrange(DOWN, buff=0.28)

        X = number_grid(X_VALS, cell=0.48, color=TEAL_D, font_scale=0.24)
        X_lab = Text("X  (3 × 2)", font="Sans", color=TEAL_D).scale(0.28)
        X_block = VGroup(X_lab, X).arrange(DOWN, buff=0.1)
        left = VGroup(toks, X_block).arrange(RIGHT, buff=0.35).move_to(LEFT * 3.2 + UP * 0.7)

        self.play(FadeIn(left), run_time=1.2)
        self.set_dims("T = 3   ·   d_model = 2")
        self.wait(0.9)

        # ---- Copy X into Q, K, V ----
        self.say("Make three copies of X — Query, Key, Value (same numbers, different jobs).", wait=1.7)

        def make_mat(name: str, color):
            g = number_grid(X_VALS, cell=0.40, color=color, font_scale=0.20)
            lab = Text(name, font="Sans", color=color).scale(0.26)
            return VGroup(lab, g).arrange(DOWN, buff=0.08)

        Q_g = make_mat("Q  (query)", ORANGE_D)
        K_g = make_mat("K  (key)", GREEN_D)
        V_g = make_mat("V  (value)", BLUE_D)
        copies = VGroup(Q_g, K_g, V_g).arrange(RIGHT, buff=0.4).move_to(RIGHT * 1.8 + UP * 0.85)

        # Ghost copies fly from X
        ghosts = VGroup(*[X.copy().set_opacity(0.45) for _ in range(3)])
        for g in ghosts:
            g.move_to(X.get_center())
        self.add(ghosts)
        targets = [Q_g[1], K_g[1], V_g[1]]
        self.play(
            LaggedStart(*[
                ghosts[i].animate.move_to(targets[i].get_center()).set_opacity(0)
                for i in range(3)
            ], lag_ratio=0.25),
            FadeIn(copies),
            run_time=1.8,
        )
        self.remove(ghosts)

        roles = VGroup(
            Text("Q — what am I looking for?", font="Sans", color=ORANGE_D).scale(0.26),
            Text("K — what can match a query?", font="Sans", color=GREEN_D).scale(0.26),
            Text("V — what content to mix in?", font="Sans", color=BLUE_D).scale(0.26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(DOWN * 0.55 + RIGHT * 1.8)
        self.play(FadeIn(roles), run_time=1.0)

        tip = Text("Usually Q = X W_Q, …  — here W = I so Q = K = V = X", font="Sans", color=MUTED).scale(0.26)
        tip.move_to(DOWN * 1.35 + RIGHT * 1.5)
        self.play(FadeIn(tip), run_time=0.8)
        self.set_dims("Q, K, V ∈ R^{3×2}")
        self.wait(1.2)

        # Clear left clutter; keep Q,K for multiply; park V note
        self.say("Now multiply: scores from Q and K.", wait=1.4)
        self.play(
            FadeOut(VGroup(left, roles, tip, V_g, key)),
            run_time=0.7,
        )

        formula = Text("S = Q Kᵀ / √d_k     →     A = softmax(S)", font="Sans", color=ACCENT).scale(0.30)
        formula.to_edge(UP, buff=1.0)
        self.play(Write(formula), run_time=1.0)

        # Reposition Q,K; build labeled S (rows = query words, cols = key words)
        Q = Q_g[1]
        K = K_g[1]
        blank = [["—", "—", "—"], ["—", "—", "—"], ["—", "—", "—"]]
        S_block, S_grid = labeled_square_matrix(
            blank,
            cell=0.38,
            color=TEAL_D,
            font_scale=0.17,
            title="S  (how related?)",
            title_color=TEAL_D,
            row_words=TOKENS,
            col_words=TOKENS,
        )

        qk = VGroup(Q_g, K_g).arrange(RIGHT, buff=0.4)
        qk.move_to(LEFT * 3.0 + UP * 0.55)
        S_block.move_to(RIGHT * 1.5 + UP * 0.45)

        self.play(
            Q_g.animate.move_to(qk[0].get_center()),
            K_g.animate.move_to(qk[1].get_center()),
            FadeIn(S_block),
            run_time=1.2,
        )
        hint = Text(
            "row = query word    ·    column = key word    ·    S_ij ≈ how much i looks at j",
            font="Sans",
            color=MUTED,
        ).scale(0.24)
        hint.next_to(S_block, DOWN, buff=0.18)
        self.play(FadeIn(hint), run_time=0.7)
        self.set_dims("S ∈ R^{3×3}   ·   d_k = 2")

        work_anchor = DOWN * 1.55 + RIGHT * 0.9
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
                self.play(*anims, run_time=0.3)
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
                self.play(ReplacementTransform(rings, new), run_time=0.3)
            else:
                self.play(FadeIn(new), run_time=0.3)
            rings = new

        def show_formula(eq: str, expand: str):
            nonlocal work
            if len(work) > 0:
                self.play(FadeOut(work), run_time=0.25)
                self.remove(work)
            title = Text(eq, font="Sans", color=INK).scale(0.26)
            exp = Text(expand, font="Sans", color=GREEN_D).scale(0.26)
            block = VGroup(title, exp).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            block.move_to(work_anchor)
            work = block
            self.play(FadeIn(title), run_time=0.6)
            self.wait(0.85)
            self.play(FadeIn(exp), run_time=0.65)
            self.wait(0.85)

        def fill_cell(grid: VGroup, cols: int, r: int, c: int, value: str):
            cell = cell_at(grid, cols, r, c)
            new_txt = Text(value, font="Sans").scale(0.17).set_color(INK).move_to(cell[0])
            self.play(Transform(cell[1], new_txt), run_time=0.5)
            light(cell)
            self.wait(0.35)

        self.say("S_ij: query word (row) vs key word (column).", wait=1.5)

        demos = [
            (0, 0, "the → the", "S = [1,0]·[1,0]/√2 = 0.707", "0.707"),
            (2, 1, "sat → cat", "S = [0.2,0.8]·[0,1]/√2 = 0.566", "0.566"),
            (2, 0, "sat → the", "S = [0.2,0.8]·[1,0]/√2 = 0.141", "0.141"),
        ]
        for r, c, eq, exp, val in demos:
            light(row_group(Q, 2, r), row_group(K, 2, c))
            show_formula(eq, exp)
            fill_cell(S_grid, 3, r, c, val)

        self.say("Fill the rest — each cell is one word–word interaction.", wait=1.2)
        clear_work()
        rest = [
            (0, 1, "0.000"), (0, 2, "0.141"),
            (1, 0, "0.000"), (1, 1, "0.707"), (1, 2, "0.566"),
            (2, 2, "0.481"),
        ]
        for r, c, val in rest:
            light(row_group(Q, 2, r), row_group(K, 2, c))
            fill_cell(S_grid, 3, r, c, val)

        clear_work()
        scale_note = Text("÷√d_k keeps dots from exploding so softmax stays soft.", font="Sans", color=MUTED).scale(0.26)
        scale_note.move_to(work_anchor)
        work = scale_note
        self.play(FadeIn(scale_note), run_time=0.7)
        self.wait(1.0)

        # Softmax → labeled A
        clear_work()
        self.say("Softmax each query row → weights over the / cat / sat.", wait=1.5)
        self.play(FadeOut(hint), run_time=0.3)
        A_block, A_grid = labeled_square_matrix(
            blank,
            cell=0.38,
            color=BLUE_D,
            font_scale=0.17,
            title="A  (attention weights)",
            title_color=BLUE_D,
            row_words=TOKENS,
            col_words=TOKENS,
        )
        # Shift S left a bit; A on the right
        self.play(
            FadeOut(VGroup(Q_g, K_g)),
            S_block.animate.move_to(LEFT * 2.4 + UP * 0.35),
            run_time=0.9,
        )
        A_block.move_to(RIGHT * 2.2 + UP * 0.35)
        self.play(FadeIn(A_block), run_time=0.8)

        light(row_group(S_grid, 3, 2))
        show_formula(
            "row sat → softmax over keys [the, cat, sat]",
            "→  [0.254, 0.389, 0.357]   (most weight on cat)",
        )
        for c, val in enumerate(["0.254", "0.389", "0.357"]):
            fill_cell(A_grid, 3, 2, c, val)

        clear_work()
        self.say("Fill all rows of A — each row is one word’s look-up over the sentence.", wait=1.3)
        for r in range(3):
            for c in range(3):
                if r == 2:
                    continue
                fill_cell(A_grid, 3, r, c, f"{A_VALS[r][c]:.3f}")

        punch = Text("Next: mix values with A  →  O = A V", font="Sans", color=ACCENT).scale(0.30)
        punch.move_to(work_anchor)
        work = punch
        self.play(FadeIn(punch), run_time=0.8)
        self.wait(2.0)
