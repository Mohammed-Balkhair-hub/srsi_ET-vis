"""DPP: determinant = volume = diversity (MDP3 slides 43-45).

Story:
  1. A duplicate frame flattens the box its vectors span → determinant = 0.
  2. det of the similarity (Gram) matrix = squared volume of that box.
  3. The DPP scores a whole set S by det(L~_S) — a submatrix of the CMGK matrix.
  4. For a pair this factors into relevance x diversity: r_i^2 r_j^2 (1 - s^2).
"""

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
    number_grid,
)

VI = BLUE_D       # frame i vector
VJ = ORANGE_D     # frame j vector
BOX = GOLD_D      # spanned parallelogram


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
    g.to_corner(DL, buff=0.18).shift(UP * 0.85)
    return g


def bracket_pair(mob: Mobject, color=INK, tick: float = 0.14, pad: float = 0.12) -> VGroup:
    """Square brackets [ ] hugging a mobject's bounding box."""
    y_top = mob.get_top()[1] + pad
    y_bot = mob.get_bottom()[1] - pad
    lx = mob.get_left()[0] - pad
    rx = mob.get_right()[0] + pad
    lb = VGroup(
        Line([lx, y_bot, 0], [lx, y_top, 0], color=color, stroke_width=3),
        Line([lx, y_top, 0], [lx + tick, y_top, 0], color=color, stroke_width=3),
        Line([lx, y_bot, 0], [lx + tick, y_bot, 0], color=color, stroke_width=3),
    )
    rb = VGroup(
        Line([rx, y_bot, 0], [rx, y_top, 0], color=color, stroke_width=3),
        Line([rx, y_top, 0], [rx - tick, y_top, 0], color=color, stroke_width=3),
        Line([rx, y_bot, 0], [rx - tick, y_bot, 0], color=color, stroke_width=3),
    )
    return VGroup(lb, rb)


def matrix2x2(entries, colors=None, col_w: float = 1.15, row_h: float = 0.7, scale: float = 0.34) -> VGroup:
    """A bracketed 2x2 of text entries. entries = [[a,b],[c,d]]."""
    if colors is None:
        colors = [[INK, INK], [INK, INK]]
    cells = VGroup()
    grid = []
    for i, row in enumerate(entries):
        rowg = []
        for j, e in enumerate(row):
            t = Text(e, font="Sans", color=colors[i][j]).scale(scale)
            t.move_to([j * col_w, -i * row_h, 0])
            cells.add(t)
            rowg.append(t)
        grid.append(rowg)
    cells.move_to(ORIGIN)
    br = bracket_pair(cells, color=INK)
    return VGroup(br, cells)


class DPPDeterminantVolume(BrandScene):
    chapter_title = "DPP · Determinant = Volume"

    def construct(self):
        self.setup_branding()
        if self.dims is not None:
            self.remove(self.dims)
        self.dims = None
        self._dims_visible = False

        key = terms_key([
            "frame  →  a vector in the kernel's RKHS",
            "box  →  parallelepiped the vectors span",
            "det  →  (volume of that box)²",
            "L̃  →  CMGK matrix (relevance × similarity)",
            "DPP  →  P(S) ∝ det(L̃_S)",
        ])
        self.play(FadeIn(key), run_time=0.7)
        self.say("Top-k scores each frame alone, so duplicates flood in — we need a score for a whole SET.", wait=1.8)

        # =====================================================================
        # BEAT 1 — determinant = volume (two vectors span a box)
        # =====================================================================
        self.say("Picture each chosen frame as a vector. Two vectors span a box.", wait=1.5)

        O = np.array([2.6, -1.1, 0.0])
        L = 2.3
        base = 0.16  # base angle of v_i
        theta = ValueTracker(0.20)

        dot = Dot(O, radius=0.05, color=INK)

        def vec_i():
            a = L * np.array([np.cos(base), np.sin(base), 0.0])
            return Arrow(O, O + a, buff=0, color=VI, stroke_width=5, max_tip_length_to_length_ratio=0.12)

        def vec_j():
            ang = base + theta.get_value()
            b = L * np.array([np.cos(ang), np.sin(ang), 0.0])
            return Arrow(O, O + b, buff=0, color=VJ, stroke_width=5, max_tip_length_to_length_ratio=0.12)

        def para():
            a = L * np.array([np.cos(base), np.sin(base), 0.0])
            ang = base + theta.get_value()
            b = L * np.array([np.cos(ang), np.sin(ang), 0.0])
            return Polygon(O, O + a, O + a + b, O + b, color=BOX, stroke_width=2).set_fill(BOX, opacity=0.28)

        def arc():
            return Arc(radius=0.55, start_angle=base, angle=theta.get_value(), arc_center=O, color=MUTED, stroke_width=3)

        vi = always_redraw(vec_i)
        vj = always_redraw(vec_j)
        pg = always_redraw(para)
        ac = always_redraw(arc)
        vi_l = Text("frame i", font="Sans", color=VI).scale(0.24)
        vi_l.add_updater(lambda m: m.next_to(vi.get_end(), RIGHT, buff=0.1))
        vj_l = Text("frame j", font="Sans", color=VJ).scale(0.24)
        vj_l.add_updater(lambda m: m.next_to(vj.get_end(), UP, buff=0.1))

        det_read = always_redraw(
            lambda: Text(f"area² = det = sin²θ = {np.sin(theta.get_value())**2:.2f}",
                         font="Sans", weight=BOLD, color=BOX).scale(0.30).move_to([2.6, -3.0, 0])
        )

        self.play(FadeIn(dot), GrowArrow(vi), FadeIn(vi_l), run_time=0.7)
        self.play(GrowArrow(vj), FadeIn(vj_l), Create(ac), FadeIn(pg), FadeIn(det_read), run_time=0.9)
        self.say("Near-duplicate frames → a skinny box → tiny area.", wait=1.4)

        # Gram matrix on the left
        g_title = Text("similarity (Gram) matrix", font="Sans", color=MUTED).scale(0.26)
        g_mat = matrix2x2([["1", "cos θ"], ["cos θ", "1"]])
        g_group = VGroup(g_title, g_mat).arrange(DOWN, buff=0.25).move_to([-3.6, 0.9, 0])
        det_line = Text("det = 1 − cos²θ = sin²θ", font="Sans", weight=BOLD, color=ACCENT).scale(0.30)
        det_line.next_to(g_group, DOWN, buff=0.4)
        self.play(FadeIn(g_group), run_time=0.9)
        self.play(Write(det_line), run_time=1.0)

        # widen the box
        self.say("Different frames → vectors point apart → a wide box → big area.", wait=1.5)
        self.play(theta.animate.set_value(1.35), run_time=2.0)
        self.wait(0.6)

        # extremes: duplicate (flat) then perpendicular
        self.say("Identical vectors (θ = 0): the box is flat — det = 0.", wait=1.5)
        self.play(theta.animate.set_value(0.04), run_time=1.4)
        self.wait(0.5)
        self.say("Perpendicular (θ = 90°): maximal spread — det = 1.", wait=1.5)
        self.play(theta.animate.set_value(PI / 2), run_time=1.4)
        self.wait(0.6)

        punch = Text("A duplicate flattens the box → det = 0.\nThe determinant refuses duplicates automatically.",
                     font="Sans", weight=BOLD, color=RED_D).scale(0.28)
        punch.move_to([-0.1, -1.7, 0])
        self.play(FadeIn(punch), run_time=0.9)
        self.wait(1.6)

        # clear beat 1 (Key served the geometry beat; matrices below carry their own labels)
        vi_l.clear_updaters()
        vj_l.clear_updaters()
        self.play(FadeOut(VGroup(dot, vi, vj, pg, ac, vi_l, vj_l, det_read, g_group, det_line, punch, key)), run_time=0.7)

        # =====================================================================
        # BEAT 2 — DPP: probability from volume (submatrix of L~)
        # =====================================================================
        self.say("The DPP scores a whole set S by the volume its frames span.", wait=1.5)
        pform = Text("P(S)  ∝  det( L̃_S )", font="Sans", weight=BOLD, color=ACCENT).scale(0.42)
        pform.move_to([0, 2.15, 0])
        self.play(Write(pform), run_time=1.0)

        Lvals = [
            [0.81, 0.30, 0.28, 0.12, 0.10],
            [0.30, 0.64, 0.22, 0.20, 0.09],
            [0.28, 0.22, 0.72, 0.18, 0.14],
            [0.12, 0.20, 0.18, 0.49, 0.15],
            [0.10, 0.09, 0.14, 0.15, 0.36],
        ]
        grid = number_grid(Lvals, cell=0.66, color=MUTED, font_scale=0.24)
        grid.move_to([-3.4, -0.5, 0])
        grid_l = Text("L̃  (all 5 frames)", font="Sans", color=MUTED).scale(0.26).next_to(grid, UP, buff=0.2)
        self.play(FadeIn(grid), FadeIn(grid_l), run_time=1.0)

        cols = 5
        sel = [1, 3]  # S = {2, 4} in 1-based

        def cell(i, j):
            return grid[i * cols + j]

        # keep rows 2 & 4
        self.say("Keep only the rows and columns of the chosen frames — here S = {2, 4}.", wait=1.6)
        row_bands = VGroup(*[
            SurroundingRectangle(VGroup(*[cell(i, j) for j in range(cols)]), color=GOLD_D, buff=0.02, stroke_width=3)
            for i in sel
        ])
        col_bands = VGroup(*[
            SurroundingRectangle(VGroup(*[cell(i, j) for i in range(cols)]), color=TEAL_D, buff=0.02, stroke_width=3)
            for j in sel
        ])
        self.play(Create(row_bands), run_time=0.8)
        self.play(Create(col_bands), run_time=0.8)

        # pulse the 4 intersection cells red
        inter = VGroup(*[cell(i, j) for i in sel for j in sel])
        red_boxes = VGroup(*[
            SurroundingRectangle(cell(i, j), color=RED_D, buff=0.02, stroke_width=3).set_fill(RED_D, opacity=0.18)
            for i in sel for j in sel
        ])
        self.play(FadeIn(red_boxes), run_time=0.6)
        self.play(Indicate(inter, color=RED_D, scale_factor=1.15), run_time=0.8)

        # extract to a 2x2 submatrix
        sub = matrix2x2([["L̃₂₂", "L̃₂₄"], ["L̃₄₂", "L̃₄₄"]], scale=0.32)
        sub_l = Text("L̃_S  (2 × 2)", font="Sans", weight=BOLD, color=RED_D).scale(0.28)
        sub_g = VGroup(sub_l, sub).arrange(DOWN, buff=0.22).move_to([2.6, 0.35, 0])
        self.play(TransformFromCopy(red_boxes, sub), FadeIn(sub_l), run_time=1.1)

        self.say("Big volume → relevant and spread-out → a likely set. Flat volume → redundant → unlikely.", wait=1.9)

        # two candidate outcomes: diverse vs redundant, with probability bars
        div_box = Polygon([0, 0, 0], [1.1, 0, 0], [1.5, 0.95, 0], [0.4, 0.95, 0],
                          color=BOX, stroke_width=2).set_fill(BOX, opacity=0.3)
        red_box = Polygon([0, 0, 0], [1.4, 0, 0], [1.5, 0.14, 0], [0.1, 0.14, 0],
                          color=RED_D, stroke_width=2).set_fill(RED_D, opacity=0.3)
        div_lab = Text("diverse set → high P(S)", font="Sans", color=GREEN_D).scale(0.24)
        red_lab = Text("redundant set → low P(S)", font="Sans", color=RED_D).scale(0.24)
        d_g = VGroup(div_box, div_lab).arrange(DOWN, buff=0.15)
        r_g = VGroup(red_box, red_lab).arrange(DOWN, buff=0.15)
        cmp = VGroup(d_g, r_g).arrange(RIGHT, buff=0.7, aligned_edge=DOWN).move_to([2.7, -2.4, 0])
        self.play(FadeIn(cmp), run_time=1.0)
        self.wait(1.6)

        # clear beat 2 (keep pform)
        self.play(FadeOut(VGroup(grid, grid_l, row_bands, col_bands, red_boxes, sub_g, cmp)), run_time=0.7)

        # =====================================================================
        # BEAT 3 — the pair factorization (slide 45)
        # =====================================================================
        self.say("Plug in the CMGK entries for one pair — diagonal = relevance, off-diagonal = scaled similarity.", wait=1.9)
        ls = matrix2x2([["r_i²", "r_i r_j s"], ["r_i r_j s", "r_j²"]],
                       colors=[[GREEN_D, INK], [INK, GREEN_D]], col_w=1.6, scale=0.34)
        ls_l = Text("L̃_S  for  S = {i, j}", font="Sans", color=MUTED).scale(0.26).next_to(ls, UP, buff=0.22)
        lsg = VGroup(ls_l, ls).move_to([-3.3, 0.2, 0])
        self.play(FadeIn(lsg), run_time=0.9)

        det_eq = VGroup(
            Text("det(L̃_S) = r_i² r_j² − r_i² r_j² s²", font="Sans", color=INK).scale(0.28),
            Text("= r_i² r_j² · (1 − s²)", font="Sans", weight=BOLD, color=ACCENT).scale(0.34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.0, 0.55, 0])
        self.play(Write(det_eq[0]), run_time=1.0)
        self.play(Write(det_eq[1]), run_time=1.0)

        rel = Text("relevance", font="Sans", weight=BOLD, color=GREEN_D).scale(0.26)
        div = Text("diversity", font="Sans", weight=BOLD, color=GOLD_D).scale(0.26)
        rel.next_to(det_eq[1], DOWN, buff=0.35).shift(LEFT * 1.1)
        div.next_to(det_eq[1], DOWN, buff=0.35).shift(RIGHT * 1.2)
        self.play(FadeIn(rel), FadeIn(div), run_time=0.8)
        self.say("Relevance × diversity in one determinant — perfect duplicates (s = 1) score 0.", wait=2.0)
        self.wait(1.6)
