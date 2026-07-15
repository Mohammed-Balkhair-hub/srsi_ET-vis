"""One RNN timestep — row·column formulas fill u and v, then a_t → h_t."""

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
    g.to_corner(DL, buff=0.18).shift(UP * 0.95)
    return g


def cell_at(grid: VGroup, cols: int, r: int, c: int) -> VGroup:
    return grid[r * cols + c]


def row_group(grid: VGroup, cols: int, r: int) -> VGroup:
    return VGroup(*[cell_at(grid, cols, r, c) for c in range(cols)])


def yellow_ring(mobs: VGroup | Mobject) -> SurroundingRectangle:
    return SurroundingRectangle(mobs, color=GOLD_D, buff=0.05, stroke_width=3.5)


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
            "x_t — input vector (column)",
            "h_{t-1} — previous hidden",
            "W_xh — input weights",
            "W_hh — recurrent weights",
            "b_h — bias",
            "a_t — pre-activation",
            "u = W_xh x_t   (row · column)",
            "v = W_hh h_{t-1}",
            "h_t — new hidden state",
        ])
        self.play(FadeIn(key), run_time=0.8)

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

        u_grid = number_grid([["—"], ["—"]], cell=0.5, color=GREEN_D, font_scale=0.28)
        u_lab = Text("u = W_xh x_t", font="Sans", color=GREEN_D).scale(0.26)
        u_g = VGroup(u_lab, u_grid).arrange(DOWN, buff=0.1)

        v_grid = number_grid([["—"], ["—"]], cell=0.5, color=GREEN_D, font_scale=0.26)
        v_lab = Text("v = W_hh h_{t-1}", font="Sans", color=GREEN_D).scale(0.24)
        v_g = VGroup(v_lab, v_grid).arrange(DOWN, buff=0.1)

        mats = VGroup(h_g, x_g, Wxh_block, Whh_block, u_g).arrange(RIGHT, buff=0.45)
        mats.move_to(UP * 0.95 + RIGHT * 0.75)

        self.say("Start from previous memory h_{t-1} and current input x_t.", wait=1.4)
        self.play(FadeIn(h_g), FadeIn(x_g), run_time=1.1)
        self.wait(0.8)

        self.say("Weights are shared across all times — same W every step.", wait=1.4)
        self.play(FadeIn(Wxh_block), FadeIn(Whh_block), FadeIn(u_g), run_time=1.2)
        self.wait(0.9)

        # Work panel: mid-right, away from key and matrices
        work_anchor = DOWN * 1.05 + RIGHT * 1.5
        work = VGroup()
        rings = VGroup()

        def clear_work(clear_rings: bool = True):
            nonlocal work, rings
            anims = []
            if len(work) > 0:
                anims.append(FadeOut(work))
            if clear_rings and len(rings) > 0:
                anims.append(FadeOut(rings))
            if anims:
                self.play(*anims, run_time=0.4)
            if len(work) > 0:
                self.remove(work)
            work = VGroup()
            if clear_rings:
                if len(rings) > 0:
                    self.remove(rings)
                rings = VGroup()

        def light(*mobs):
            nonlocal rings
            new = VGroup(*[yellow_ring(m) for m in mobs])
            if len(rings) > 0:
                self.play(ReplacementTransform(rings, new), run_time=0.4)
            else:
                self.play(FadeIn(new), run_time=0.4)
            rings = new

        def show_row_formula(eq_line: str, expand_line: str):
            """Arrange both lines BEFORE showing — never stack at one point."""
            nonlocal work
            if len(work) > 0:
                self.play(FadeOut(work), run_time=0.35)
                self.remove(work)
                work = VGroup()

            title = Text(eq_line, font="Sans", color=INK).scale(0.29)
            expand = Text(expand_line, font="Sans", color=GREEN_D).scale(0.29)
            block = VGroup(title, expand).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            block.move_to(work_anchor)
            work = block

            # Reveal top line, then green expansion under it (already spaced)
            self.play(FadeIn(title), run_time=0.7)
            self.wait(1.0)
            self.play(FadeIn(expand), run_time=0.75)
            self.wait(1.1)

        def fill_entry(grid: VGroup, idx: int, value: str):
            cell = grid[idx]
            new_txt = Text(value, font="Sans").scale(0.28).set_color(INK).move_to(cell[0])
            old = cell[1]
            self.play(Transform(old, new_txt), run_time=0.7)
            light(cell)
            self.wait(0.7)

        # ========== u = W_xh @ x_t ==========
        self.say("u = W_xh x_t : each row of W_xh dots the column x_t.", wait=1.6)

        light(row_group(Wxh_g, 2, 0), x_grid)
        show_row_formula(
            "u_0  =  [0.5 ,  −0.3]  ·  [1.0 ,  0.0]",
            "=  0.5×1.0  +  (−0.3)×0.0  =  0.5",
        )
        fill_entry(u_grid, 0, "0.5")

        light(row_group(Wxh_g, 2, 1), x_grid)
        show_row_formula(
            "u_1  =  [0.2 ,  0.4]  ·  [1.0 ,  0.0]",
            "=  0.2×1.0  +  0.4×0.0  =  0.2",
        )
        fill_entry(u_grid, 1, "0.2")
        self.wait(0.8)

        # ========== v = W_hh @ h ==========
        self.say("Same for v = W_hh h_{t-1} — row of W_hh · column h_{t-1}.", wait=1.5)
        clear_work()
        v_g.next_to(u_g, RIGHT, buff=0.4)
        self.play(FadeIn(v_g), run_time=0.8)

        light(row_group(Whh_g, 2, 0), h_grid)
        show_row_formula(
            "v_0  =  [0.6 ,  0.1]  ·  [0.5 ,  −0.2]",
            "=  0.6×0.5  +  0.1×(−0.2)  =  0.28",
        )
        fill_entry(v_grid, 0, "0.28")

        light(row_group(Whh_g, 2, 1), h_grid)
        show_row_formula(
            "v_1  =  [−0.2 ,  0.5]  ·  [0.5 ,  −0.2]",
            "=  (−0.2)×0.5  +  0.5×(−0.2)  =  −0.20",
        )
        fill_entry(v_grid, 1, "−0.20")
        self.wait(0.8)

        # ========== a_t = u + v + b ==========
        self.say("Add bias: a_t = u + v + b_h  (pre-activation).", wait=1.5)
        clear_work()
        self.play(
            FadeOut(VGroup(h_g, x_g, Wxh_block, Whh_block, formula, u_g, v_g, key)),
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
        add_row.move_to(UP * 1.0)

        self.play(FadeIn(add_row), run_time=1.2)
        light(u2, v2, b2)
        self.wait(1.0)
        light(a2)
        self.wait(1.2)

        # Final tanh: layout as one arranged column — no leftover green work
        self.say("Apply tanh to each component of a_t → new hidden h_t.", wait=1.5)
        clear_work()
        light(a2)

        tanh_line = Text("h_t = tanh(a_t)", font="Sans", weight=BOLD, color=ACCENT).scale(0.4)
        d0 = Text("tanh(0.88) ≈ 0.706", font="Sans", color=INK).scale(0.32)
        d1 = Text("tanh(−0.10) ≈ −0.100", font="Sans", color=INK).scale(0.32)
        h_out = number_grid([[0.706], [-0.100]], cell=0.55, color=ORANGE_D, font_scale=0.28)
        h_out_l = Text("h_t", font="Sans", color=ORANGE_D).scale(0.32)
        hout = VGroup(h_out_l, h_out).arrange(DOWN, buff=0.12)

        finale = VGroup(tanh_line, d0, d1, hout).arrange(DOWN, buff=0.28)
        finale.move_to(DOWN * 1.15)
        work = finale
        self.play(FadeIn(finale), run_time=1.2)
        self.wait(0.6)
        light(h_out)
        self.set_dims("h_t ∈ R^2")
        self.wait(2.0)
