"""One RNN timestep — products → sum → tanh, with tiny 2D numbers."""

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


class RNNCellMath(BrandScene):
    chapter_title = "2 · One Timestep (Math)"

    def construct(self):
        self.setup_branding()
        self.say("Vanilla RNN: one shared cell, one time step.", wait=1.5)

        formula = Text(
            "a_t = W_xh x_t + W_hh h_{t-1} + b_h     →     h_t = tanh(a_t)",
            font="Sans",
            color=ACCENT,
        ).scale(0.32)
        formula.to_edge(UP, buff=1.05)
        self.play(Write(formula), run_time=1.4)
        self.set_dims("d_x = 2   ·   d_h = 2")
        self.wait(1.0)

        # Inputs
        h_vals = [[0.5], [-0.2]]
        x_vals = [[1.0], [0.0]]
        h_grid = number_grid(h_vals, cell=0.55, color=ORANGE_D, font_scale=0.3)
        x_grid = number_grid(x_vals, cell=0.55, color=BLUE_D, font_scale=0.3)
        h_lab = Text("h_{t-1}", font="Sans", color=ORANGE_D).scale(0.34)
        x_lab = Text("x_t", font="Sans", color=BLUE_D).scale(0.34)
        h_g = VGroup(h_lab, h_grid).arrange(DOWN, buff=0.15).shift(LEFT * 4.2 + DOWN * 0.2)
        x_g = VGroup(x_lab, x_grid).arrange(DOWN, buff=0.15).shift(LEFT * 2.4 + DOWN * 0.2)

        self.say("Start from previous memory h_{t-1} and current input x_t.", wait=1.5)
        self.play(FadeIn(h_g), FadeIn(x_g), run_time=1.2)
        self.wait(1.0)

        # Matrices
        Wxh = [[0.5, -0.3], [0.2, 0.4]]
        Whh = [[0.6, 0.1], [-0.2, 0.5]]
        Wxh_g = number_grid(Wxh, cell=0.5, color=TEAL_D, font_scale=0.26)
        Whh_g = number_grid(Whh, cell=0.5, color=TEAL_D, font_scale=0.26)
        Wxh_lab = Text("W_xh", font="Sans", color=TEAL_D).scale(0.3)
        Whh_lab = Text("W_hh", font="Sans", color=TEAL_D).scale(0.3)
        Wxh_block = VGroup(Wxh_lab, Wxh_g).arrange(DOWN, buff=0.12).shift(RIGHT * 0.2 + UP * 0.9)
        Whh_block = VGroup(Whh_lab, Whh_g).arrange(DOWN, buff=0.12).shift(RIGHT * 2.6 + UP * 0.9)

        self.say("Weights are shared across all times — same W every step.", wait=1.5)
        self.play(FadeIn(Wxh_block), FadeIn(Whh_block), run_time=1.2)
        self.wait(1.0)

        # --- W_xh @ x product by product ---
        self.say("First: W_xh × x_t — each weight × each input, then sum per row.", wait=1.6)
        work = VGroup().shift(DOWN * 1.55)

        # Row 0 of W_xh · x
        r0_prods = Text("0.5×1.0 = 0.5    ,    (−0.3)×0.0 = 0", font="Sans", color=INK).scale(0.3)
        r0_sum = Text("row 0 sum → 0.5", font="Sans", color=GREEN_D).scale(0.32)
        r0 = VGroup(r0_prods, r0_sum).arrange(DOWN, buff=0.12)
        self.play(Write(r0_prods), run_time=1.3)
        self.wait(0.8)
        self.play(Write(r0_sum), run_time=0.9)
        self.wait(1.0)

        self.play(FadeOut(r0), run_time=0.5)
        r1_prods = Text("0.2×1.0 = 0.2    ,    0.4×0.0 = 0", font="Sans", color=INK).scale(0.3)
        r1_sum = Text("row 1 sum → 0.2", font="Sans", color=GREEN_D).scale(0.32)
        r1 = VGroup(r1_prods, r1_sum).arrange(DOWN, buff=0.12)
        self.play(Write(r1_prods), run_time=1.2)
        self.wait(0.7)
        self.play(Write(r1_sum), run_time=0.9)
        self.wait(0.9)

        u_grid = number_grid([[0.5], [0.2]], cell=0.55, color=GREEN_D, font_scale=0.3)
        u_lab = Text("u = W_xh x_t", font="Sans", color=GREEN_D).scale(0.3)
        u_g = VGroup(u_lab, u_grid).arrange(DOWN, buff=0.12).move_to(DOWN * 1.55 + RIGHT * 3.5)
        self.play(FadeOut(r1), FadeIn(u_g), run_time=1.0)
        self.wait(1.1)

        # --- W_hh @ h ---
        self.say("Next: W_hh × h_{t-1} — same multiply → product → sum.", wait=1.5)
        self.play(FadeOut(u_g), run_time=0.4)

        h0_prods = Text("0.6×0.5 = 0.30    ,    0.1×(−0.2) = −0.02", font="Sans", color=INK).scale(0.28)
        h0_sum = Text("row 0 sum → 0.28", font="Sans", color=GREEN_D).scale(0.32)
        self.play(Write(h0_prods), run_time=1.3)
        self.wait(0.7)
        self.play(Write(h0_sum), run_time=0.8)
        self.wait(0.9)
        self.play(FadeOut(VGroup(h0_prods, h0_sum)), run_time=0.45)

        h1_prods = Text("(−0.2)×0.5 = −0.10    ,    0.5×(−0.2) = −0.10", font="Sans", color=INK).scale(0.28)
        h1_sum = Text("row 1 sum → −0.20", font="Sans", color=GREEN_D).scale(0.32)
        self.play(Write(h1_prods), run_time=1.3)
        self.wait(0.7)
        self.play(Write(h1_sum), run_time=0.8)
        self.wait(0.9)

        v_grid = number_grid([[0.28], [-0.20]], cell=0.55, color=GREEN_D, font_scale=0.28)
        v_lab = Text("v = W_hh h_{t-1}", font="Sans", color=GREEN_D).scale(0.28)
        v_g = VGroup(v_lab, v_grid).arrange(DOWN, buff=0.12).move_to(DOWN * 1.55 + RIGHT * 3.5)
        self.play(FadeOut(VGroup(h1_prods, h1_sum)), FadeIn(v_g), run_time=1.0)
        self.wait(1.0)

        # Bias and sum
        self.say("Add bias, then apply tanh to each component.", wait=1.5)
        self.play(
            FadeOut(VGroup(h_g, x_g, Wxh_block, Whh_block, formula, v_g)),
            run_time=0.7,
        )

        u2 = number_grid([[0.5], [0.2]], cell=0.5, color=GREEN_D, font_scale=0.28)
        plus1 = Text("+", font="Sans", color=INK).scale(0.45)
        v2 = number_grid([[0.28], [-0.20]], cell=0.5, color=GREEN_D, font_scale=0.26)
        plus2 = Text("+", font="Sans", color=INK).scale(0.45)
        b2 = number_grid([[0.1], [-0.1]], cell=0.5, color=GOLD_D, font_scale=0.28)
        eq = Text("=", font="Sans", color=INK).scale(0.45)
        a2 = number_grid([[0.88], [-0.10]], cell=0.5, color=ORANGE_D, font_scale=0.28)

        u_l = Text("u", font="Sans", color=MUTED).scale(0.28).next_to(u2, UP, buff=0.1)
        v_l = Text("v", font="Sans", color=MUTED).scale(0.28).next_to(v2, UP, buff=0.1)
        b_l = Text("b_h", font="Sans", color=MUTED).scale(0.28).next_to(b2, UP, buff=0.1)
        a_l = Text("a_t", font="Sans", color=ORANGE_D).scale(0.28).next_to(a2, UP, buff=0.1)

        row = VGroup(u2, plus1, v2, plus2, b2, eq, a2).arrange(RIGHT, buff=0.22)
        labs = VGroup(u_l, v_l, b_l, a_l)
        # reposition labels after arrange
        u_l.next_to(u2, UP, buff=0.1)
        v_l.next_to(v2, UP, buff=0.1)
        b_l.next_to(b2, UP, buff=0.1)
        a_l.next_to(a2, UP, buff=0.1)
        add_g = VGroup(row, u_l, v_l, b_l, a_l).move_to(UP * 0.55)

        self.play(FadeIn(add_g), run_time=1.4)
        self.wait(1.4)

        tanh_line = Text("h_t = tanh(a_t)", font="Sans", weight=BOLD, color=ACCENT).scale(0.4)
        tanh_line.move_to(DOWN * 0.55)
        self.play(Write(tanh_line), run_time=0.9)

        h_out = number_grid([[0.706], [-0.100]], cell=0.6, color=ORANGE_D, font_scale=0.3)
        h_out_l = Text("h_t ≈", font="Sans", color=ORANGE_D).scale(0.34)
        hout_g = VGroup(h_out_l, h_out).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.55)
        detail = Text("tanh(0.88) ≈ 0.706    ·    tanh(−0.10) ≈ −0.100", font="Sans", color=MUTED).scale(0.28)
        detail.next_to(hout_g, DOWN, buff=0.25)

        self.say("Nonlinearity per component — this h_t feeds the next step.", wait=1.6)
        self.play(FadeIn(hout_g), Write(detail), run_time=1.4)
        self.set_dims("h_t ∈ R^2")
        self.wait(2.0)
