"""One RNN timestep — products → sum → tanh, with yellow cell highlights."""

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
    rows = VGroup(*[
        Text(line, font="Sans", color=INK).scale(0.22) for line in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
    title = Text("Key", font="Sans", weight=BOLD, color=ACCENT).scale(0.24)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    box = SurroundingRectangle(
        body, buff=0.12, corner_radius=0.08, color=MUTED, stroke_width=1.5
    )
    box.set_fill("#F7F9FB", opacity=1.0)
    g = VGroup(box, body)
    body.move_to(box.get_center())
    # Above the bottom caption so they never overlap
    g.to_corner(DL, buff=0.18).shift(UP * 0.95)
    return g


def cell_at(grid: VGroup, cols: int, r: int, c: int) -> VGroup:
    return grid[r * cols + c]


def yellow_ring(mobs: VGroup | Mobject) -> SurroundingRectangle:
    return SurroundingRectangle(mobs, color=GOLD_D, buff=0.04, stroke_width=3.5)


class RNNCellMath(BrandScene):
    chapter_title = "2 · One Timestep (Math)"

    def construct(self):
        self.setup_branding()
        self.say("Vanilla RNN: one shared cell, one time step.", wait=1.5)

        formula = Text(
            "a_t = W_xh x_t + W_hh h_{t-1} + b_h     →     h_t = tanh(a_t)",
            font="Sans",
            color=ACCENT,
        ).scale(0.30)
        formula.to_edge(UP, buff=1.0)
        self.play(Write(formula), run_time=1.3)
        self.set_dims("d_x = 2   ·   d_h = 2")

        key = terms_key([
            "x_t — input vector",
            "h_{t-1} — previous hidden",
            "W_xh — input weights",
            "W_hh — recurrent weights",
            "b_h — bias",
            "a_t — pre-activation",
            "h_t — new hidden state",
            "u = W_xh x_t   v = W_hh h_{t-1}",
        ])
        self.play(FadeIn(key), run_time=0.8)

        # ---- vectors & matrices (upper mid band) ----
        h_grid = number_grid([[0.5], [-0.2]], cell=0.5, color=ORANGE_D, font_scale=0.28)
        x_grid = number_grid([[1.0], [0.0]], cell=0.5, color=BLUE_D, font_scale=0.28)
        h_lab = Text("h_{t-1}", font="Sans", color=ORANGE_D).scale(0.28)
        x_lab = Text("x_t", font="Sans", color=BLUE_D).scale(0.28)
        h_g = VGroup(h_lab, h_grid).arrange(DOWN, buff=0.1)
        x_g = VGroup(x_lab, x_grid).arrange(DOWN, buff=0.1)

        Wxh_g = number_grid([[0.5, -0.3], [0.2, 0.4]], cell=0.48, color=TEAL_D, font_scale=0.24)
        Whh_g = number_grid([[0.6, 0.1], [-0.2, 0.5]], cell=0.48, color=TEAL_D, font_scale=0.24)
        Wxh_lab = Text("W_xh", font="Sans", color=TEAL_D).scale(0.28)
        Whh_lab = Text("W_hh", font="Sans", color=TEAL_D).scale(0.28)
        Wxh_block = VGroup(Wxh_lab, Wxh_g).arrange(DOWN, buff=0.1)
        Whh_block = VGroup(Whh_lab, Whh_g).arrange(DOWN, buff=0.1)

        mats = VGroup(h_g, x_g, Wxh_block, Whh_block).arrange(RIGHT, buff=0.55)
        mats.move_to(UP * 0.85 + RIGHT * 0.55)

        self.say("Start from previous memory h_{t-1} and current input x_t.", wait=1.4)
        self.play(FadeIn(h_g), FadeIn(x_g), run_time=1.1)
        self.wait(0.8)

        self.say("Weights are shared across all times — same W every step.", wait=1.4)
        self.play(FadeIn(Wxh_block), FadeIn(Whh_block), run_time=1.1)
        self.wait(0.9)

        # Dedicated work band under matrices (right of terms key; never overlaps grids)
        work_anchor = DOWN * 1.2 + RIGHT * 1.35
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
                self.play(*anims, run_time=0.45)
            work = VGroup()
            rings = VGroup()

        def show_work(*mobs):
            nonlocal work
            g = VGroup(*mobs).arrange(DOWN, buff=0.18).move_to(work_anchor)
            work = g
            self.play(FadeIn(work), run_time=0.7)
            return g

        def light(*mobs):
            nonlocal rings
            new = VGroup(*[yellow_ring(m) for m in mobs])
            if len(rings) > 0:
                self.play(FadeOut(rings), FadeIn(new), run_time=0.45)
            else:
                self.play(FadeIn(new), run_time=0.45)
            rings = new

        # ========== W_xh @ x : row 0 ==========
        self.say("First: W_xh × x_t — highlight cells, then each product, then sum.", wait=1.5)

        # product 1: W[0,0] * x[0]
        light(cell_at(Wxh_g, 2, 0, 0), cell_at(x_grid, 1, 0, 0))
        p1 = Text("0.5  ×  1.0  =  0.5", font="Sans", color=INK).scale(0.34)
        show_work(p1)
        self.wait(1.1)

        # product 2: W[0,1] * x[1]
        clear_work()
        light(cell_at(Wxh_g, 2, 0, 1), cell_at(x_grid, 1, 1, 0))
        p2 = Text("(−0.3)  ×  0.0  =  0", font="Sans", color=INK).scale(0.34)
        show_work(p2)
        self.wait(1.1)

        # sum row 0
        clear_work()
        light(cell_at(Wxh_g, 2, 0, 0), cell_at(Wxh_g, 2, 0, 1), x_grid)
        s0 = Text("row 0 sum:  0.5 + 0  =  0.5", font="Sans", color=GREEN_D).scale(0.34)
        show_work(s0)
        self.wait(1.2)

        # ========== W_xh @ x : row 1 ==========
        clear_work()
        light(cell_at(Wxh_g, 2, 1, 0), cell_at(x_grid, 1, 0, 0))
        p3 = Text("0.2  ×  1.0  =  0.2", font="Sans", color=INK).scale(0.34)
        show_work(p3)
        self.wait(1.0)

        clear_work()
        light(cell_at(Wxh_g, 2, 1, 1), cell_at(x_grid, 1, 1, 0))
        p4 = Text("0.4  ×  0.0  =  0", font="Sans", color=INK).scale(0.34)
        show_work(p4)
        self.wait(1.0)

        clear_work()
        light(cell_at(Wxh_g, 2, 1, 0), cell_at(Wxh_g, 2, 1, 1), x_grid)
        s1 = Text("row 1 sum:  0.2 + 0  =  0.2", font="Sans", color=GREEN_D).scale(0.34)
        u_grid = number_grid([[0.5], [0.2]], cell=0.48, color=GREEN_D, font_scale=0.26)
        u_lab = Text("u = W_xh x_t", font="Sans", color=GREEN_D).scale(0.28)
        u_g = VGroup(u_lab, u_grid).arrange(DOWN, buff=0.1)
        show_work(s1, u_g)
        self.wait(1.4)

        # ========== W_hh @ h : row 0 ==========
        self.say("Next: W_hh × h_{t-1} — same idea, new cells light yellow.", wait=1.5)
        clear_work()

        light(cell_at(Whh_g, 2, 0, 0), cell_at(h_grid, 1, 0, 0))
        q1 = Text("0.6  ×  0.5  =  0.30", font="Sans", color=INK).scale(0.34)
        show_work(q1)
        self.wait(1.1)

        clear_work()
        light(cell_at(Whh_g, 2, 0, 1), cell_at(h_grid, 1, 1, 0))
        q2 = Text("0.1  ×  (−0.2)  =  −0.02", font="Sans", color=INK).scale(0.34)
        show_work(q2)
        self.wait(1.1)

        clear_work()
        light(cell_at(Whh_g, 2, 0, 0), cell_at(Whh_g, 2, 0, 1), h_grid)
        qs0 = Text("row 0 sum:  0.30 + (−0.02)  =  0.28", font="Sans", color=GREEN_D).scale(0.32)
        show_work(qs0)
        self.wait(1.2)

        # ========== W_hh @ h : row 1 ==========
        clear_work()
        light(cell_at(Whh_g, 2, 1, 0), cell_at(h_grid, 1, 0, 0))
        q3 = Text("(−0.2)  ×  0.5  =  −0.10", font="Sans", color=INK).scale(0.34)
        show_work(q3)
        self.wait(1.0)

        clear_work()
        light(cell_at(Whh_g, 2, 1, 1), cell_at(h_grid, 1, 1, 0))
        q4 = Text("0.5  ×  (−0.2)  =  −0.10", font="Sans", color=INK).scale(0.34)
        show_work(q4)
        self.wait(1.0)

        clear_work()
        light(cell_at(Whh_g, 2, 1, 0), cell_at(Whh_g, 2, 1, 1), h_grid)
        qs1 = Text("row 1 sum:  (−0.10) + (−0.10)  =  −0.20", font="Sans", color=GREEN_D).scale(0.30)
        v_grid = number_grid([[0.28], [-0.20]], cell=0.48, color=GREEN_D, font_scale=0.24)
        v_lab = Text("v = W_hh h_{t-1}", font="Sans", color=GREEN_D).scale(0.26)
        v_g = VGroup(v_lab, v_grid).arrange(DOWN, buff=0.1)
        show_work(qs1, v_g)
        self.wait(1.4)

        # ========== a_t = u + v + b ==========
        self.say("Add bias: a_t = u + v + b_h  (pre-activation).", wait=1.5)
        clear_work()
        self.play(
            FadeOut(VGroup(h_g, x_g, Wxh_block, Whh_block, formula)),
            run_time=0.6,
        )

        u2 = number_grid([[0.5], [0.2]], cell=0.48, color=GREEN_D, font_scale=0.26)
        v2 = number_grid([[0.28], [-0.20]], cell=0.48, color=GREEN_D, font_scale=0.24)
        b2 = number_grid([[0.1], [-0.1]], cell=0.48, color=TEAL_D, font_scale=0.26)
        a2 = number_grid([[0.88], [-0.10]], cell=0.48, color=ORANGE_D, font_scale=0.26)
        plus1 = Text("+", font="Sans", color=INK).scale(0.42)
        plus2 = Text("+", font="Sans", color=INK).scale(0.42)
        eq = Text("=", font="Sans", color=INK).scale(0.42)

        u_l = Text("u", font="Sans", color=MUTED).scale(0.26)
        v_l = Text("v", font="Sans", color=MUTED).scale(0.26)
        b_l = Text("b_h", font="Sans", color=MUTED).scale(0.26)
        a_l = Text("a_t", font="Sans", color=ORANGE_D).scale(0.28)

        u_col = VGroup(u_l, u2).arrange(DOWN, buff=0.1)
        v_col = VGroup(v_l, v2).arrange(DOWN, buff=0.1)
        b_col = VGroup(b_l, b2).arrange(DOWN, buff=0.1)
        a_col = VGroup(a_l, a2).arrange(DOWN, buff=0.1)

        add_row = VGroup(u_col, plus1, v_col, plus2, b_col, eq, a_col).arrange(RIGHT, buff=0.22)
        add_row.move_to(UP * 0.7 + RIGHT * 0.6)

        self.play(FadeIn(add_row), run_time=1.2)
        light(u2, v2, b2)
        self.wait(1.0)
        light(a2)
        self.wait(1.2)

        # ========== tanh ==========
        self.say("Apply tanh to each component of a_t → new hidden h_t.", wait=1.5)
        clear_work()
        light(a2)
        tanh_line = Text("h_t = tanh(a_t)", font="Sans", weight=BOLD, color=ACCENT).scale(0.4)
        d0 = Text("tanh(0.88) ≈ 0.706", font="Sans", color=INK).scale(0.32)
        d1 = Text("tanh(−0.10) ≈ −0.100", font="Sans", color=INK).scale(0.32)
        h_out = number_grid([[0.706], [-0.100]], cell=0.55, color=ORANGE_D, font_scale=0.28)
        h_out_l = Text("h_t", font="Sans", color=ORANGE_D).scale(0.32)
        hout = VGroup(h_out_l, h_out).arrange(DOWN, buff=0.1)
        show_work(tanh_line, d0, d1, hout)
        self.wait(0.8)
        light(h_out)
        self.set_dims("h_t ∈ R^2")
        self.wait(2.0)
