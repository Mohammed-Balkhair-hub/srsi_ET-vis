"""Pooling layers — MaxPool then AvgPool, same window walkthrough."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import ACCENT, BLUE_D, GOLD_D, GREEN_D, INK, ORANGE_D, TEAL_D, BrandScene, highlight_window, number_grid


class Pooling(BrandScene):
    chapter_title = "4 · Pooling Layers"

    def construct(self):
        self.setup_branding()
        self.say("Pooling reduces spatial size — keeps what was detected, not exactly where.", wait=1.6)

        vals = [
            [1, 3, 2, 4],
            [5, 2, 1, 0],
            [2, 7, 3, 1],
            [0, 1, 4, 6],
        ]
        windows = [(0, 0), (0, 2), (2, 0), (2, 2)]

        # ================================================================
        # MaxPool
        # ================================================================
        grid = number_grid(vals, cell=0.72, color=BLUE_D)
        grid.shift(LEFT * 3.0 + UP * 0.35)
        g_lbl = Text("Feature map 4×4", font="Sans", color=BLUE_D).scale(0.32).next_to(grid, UP, buff=0.18)

        out = number_grid([["?", "?"], ["?", "?"]], cell=0.85, color=GREEN_D)
        out.shift(RIGHT * 2.8 + UP * 0.35)
        o_lbl = Text("MaxPool → 2×2", font="Sans", color=GREEN_D).scale(0.32).next_to(out, UP, buff=0.18)

        self.play(FadeIn(grid), Write(g_lbl), FadeIn(out), Write(o_lbl), run_time=1.2)
        self.set_dims("MaxPool: 2×2 window, stride 2")

        maxima = [max(vals[r0 + di][c0 + dj] for di in range(2) for dj in range(2)) for r0, c0 in windows]

        for idx, ((r0, c0), mx) in enumerate(zip(windows, maxima)):
            self.say(f"MaxPool: take the largest value in the window → {mx}", wait=1.15)
            win = highlight_window(grid, 4, 4, r0, c0, 2, color=GOLD_D)
            self.play(Create(win), run_time=0.65)
            for di in range(2):
                for dj in range(2):
                    if vals[r0 + di][c0 + dj] == mx:
                        winner = grid[(r0 + di) * 4 + (c0 + dj)]
                        self.play(winner[0].animate.set_fill(GOLD_D, opacity=0.5), run_time=0.5)
            cell = out[idx]
            new_txt = Text(str(mx), font="Sans", weight=BOLD, color=INK).scale(0.38).move_to(cell[0])
            self.play(
                cell[0].animate.set_fill(GREEN_D, opacity=0.4),
                Transform(cell[1], new_txt),
                run_time=0.75,
            )
            self.wait(0.75)
            self.play(FadeOut(win), run_time=0.4)

        self.wait(1.0)
        self.say("Same idea with AveragePool — but take the mean of the window.", wait=1.4)
        self.play(FadeOut(VGroup(grid, g_lbl, out, o_lbl)), run_time=0.8)

        # ================================================================
        # AvgPool — identical layout / walkthrough
        # ================================================================
        grid2 = number_grid(vals, cell=0.72, color=BLUE_D)
        grid2.shift(LEFT * 3.0 + UP * 0.35)
        g2_lbl = Text("Same feature map 4×4", font="Sans", color=BLUE_D).scale(0.32).next_to(grid2, UP, buff=0.18)

        out2 = number_grid([["?", "?"], ["?", "?"]], cell=0.85, color=TEAL_D)
        out2.shift(RIGHT * 2.8 + UP * 0.35)
        o2_lbl = Text("AvgPool → 2×2", font="Sans", color=TEAL_D).scale(0.32).next_to(out2, UP, buff=0.18)

        self.play(FadeIn(grid2), Write(g2_lbl), FadeIn(out2), Write(o2_lbl), run_time=1.2)
        self.set_dims("AvgPool: mean of the 2×2 window")

        averages = []
        for r0, c0 in windows:
            block = [vals[r0 + di][c0 + dj] for di in range(2) for dj in range(2)]
            averages.append(sum(block) / 4)

        for idx, ((r0, c0), avg) in enumerate(zip(windows, averages)):
            # Show as int if whole, else 1 decimal
            avg_s = f"{avg:g}"
            self.say(f"AvgPool: average the four values → {avg_s}", wait=1.15)
            win = highlight_window(grid2, 4, 4, r0, c0, 2, color=ORANGE_D)
            self.play(Create(win), run_time=0.65)
            # Briefly tint all 4 cells equally
            tint = []
            for di in range(2):
                for dj in range(2):
                    cell_g = grid2[(r0 + di) * 4 + (c0 + dj)]
                    tint.append(cell_g[0].animate.set_fill(ORANGE_D, opacity=0.35))
            self.play(*tint, run_time=0.5)

            cell = out2[idx]
            new_txt = Text(avg_s, font="Sans", weight=BOLD, color=INK).scale(0.34).move_to(cell[0])
            self.play(
                cell[0].animate.set_fill(TEAL_D, opacity=0.4),
                Transform(cell[1], new_txt),
                run_time=0.75,
            )
            self.wait(0.75)
            self.play(FadeOut(win), run_time=0.4)

        self.wait(1.0)
        notes = VGroup(
            Text("No learnable parameters — fixed operation", font="Sans", color=INK).scale(0.34),
            Text("MaxPool is the common default in practice", font="Sans", color=INK).scale(0.34),
            Text("AvgPool: softer downsampling (keeps more context)", font="Sans", color=INK).scale(0.34),
            Text("Why pool? Less compute + mild translation invariance", font="Sans", color=INK).scale(0.34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        notes.next_to(VGroup(grid2, out2), DOWN, buff=0.4)

        self.say("Pooling has no weights — Max keeps peaks, Avg keeps a softer summary.", wait=1.4)
        self.play(LaggedStart(*[FadeIn(n) for n in notes], lag_ratio=0.25), run_time=1.8)
        self.wait(2.0)
