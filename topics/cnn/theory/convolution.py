"""Convolution math: cell-wise multiply → products → sum → output; then kernels→maps→stack."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from branding import (
    ACCENT, BLUE_D, GOLD_D, GREEN_D, INK, MUTED, ORANGE_D, PURPLE_D, RED_D, TEAL_D,
    BrandScene, highlight_window, number_grid,
)


class ConvolutionMath(BrandScene):
    chapter_title = "2 · Convolutional Layers"

    def construct(self):
        self.setup_branding()
        self.say("A kernel slides over the image. Watch: multiply → products → sum → one output.", wait=1.8)

        inp_vals = [
            [1, 2, 0, 1],
            [3, 1, 2, 0],
            [0, 1, 3, 2],
            [2, 0, 1, 1],
        ]
        ker_vals = [
            [1, 0, -1],
            [1, 0, -1],
            [1, 0, -1],
        ]

        inp = number_grid(inp_vals, cell=0.62, color=BLUE_D)
        inp.shift(LEFT * 4.2 + UP * 0.15)
        inp_title = Text("Input", font="Sans", color=BLUE_D).scale(0.3).next_to(inp, UP, buff=0.18)

        ker = number_grid(ker_vals, cell=0.48, color=GOLD_D)
        ker.shift(LEFT * 1.55 + UP * 1.85)
        ker_title = Text("Kernel 3×3", font="Sans", color=GOLD_D).scale(0.28).next_to(ker, UP, buff=0.12)

        self.play(FadeIn(inp), Write(inp_title), FadeIn(ker), Write(ker_title), run_time=1.4)
        self.set_dims("step 1: each pixel × each kernel weight")

        out = number_grid([["?", "?"], ["?", "?"]], cell=0.62, color=GREEN_D)
        out.shift(RIGHT * 4.0 + UP * 0.15)
        out_title = Text("Feature map", font="Sans", color=GREEN_D).scale(0.3).next_to(out, UP, buff=0.18)
        self.play(FadeIn(out), Write(out_title), run_time=1.0)

        formula_bar = Text(
            "output = Σ (inputᵢⱼ × kernelᵢⱼ)  + bias",
            font="Sans", color=ACCENT, weight=BOLD,
        ).scale(0.30)
        formula_bar.to_edge(DOWN, buff=1.05)
        self.play(Write(formula_bar), run_time=1.0)
        self.wait(1.0)

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for idx, (r0, c0) in enumerate(positions):
            # Full detail on first two windows; slightly faster on later ones
            detailed = idx < 2
            self._convolve_window(
                inp, ker, inp_vals, ker_vals, out, idx, r0, c0,
                detailed=detailed,
            )

        self.wait(1.4)
        self.play(
            FadeOut(VGroup(inp, inp_title, ker, ker_title, out, out_title, formula_bar)),
            run_time=0.9,
        )

        # ------------------------------------------------------------------
        # Stride + full output-size formula
        # ------------------------------------------------------------------
        self.say("Stride = how far the kernel jumps. Reminder of the full size formula:", wait=1.6)

        stride_note = VGroup(
            Text("Stride S = 1 → move 1 pixel each step (we just did this)", font="Sans", color=INK).scale(0.34),
            Text("Stride S = 2 → jump 2 pixels → smaller feature map", font="Sans", color=INK).scale(0.34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 1.6)
        self.play(LaggedStart(*[FadeIn(x) for x in stride_note], lag_ratio=0.3), run_time=1.4)
        self.wait(1.2)

        full_formula = Text(
            "W_out = floor( (W − K + 2P) / S ) + 1",
            font="Sans", weight=BOLD, color=ACCENT,
        ).scale(0.44)
        full_formula.move_to(ORIGIN + UP * 0.15)
        self.play(Write(full_formula), run_time=1.1)
        self.set_dims("W=input size · K=kernel · P=padding · S=stride")

        examples = VGroup(
            Text("Example: W=32, K=3, P=1, S=1  →  W_out = 32  (same)", font="Sans", color=INK).scale(0.32),
            Text("Example: W=32, K=3, P=0, S=1  →  W_out = 30  (shrinks)", font="Sans", color=INK).scale(0.32),
            Text("Example: W=32, K=3, P=1, S=2  →  W_out = 16  (halved)", font="Sans", color=INK).scale(0.32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(full_formula, DOWN, buff=0.55)

        for ex in examples:
            self.play(FadeIn(ex, shift=RIGHT * 0.12), run_time=0.8)
            self.wait(1.0)
        self.wait(1.4)

        self.play(FadeOut(VGroup(stride_note, full_formula, examples)), run_time=0.8)

        # ------------------------------------------------------------------
        # Each kernel has a task → one kernel, one map (×5) → stack
        # ------------------------------------------------------------------
        self.say("Each kernel has its own job: it looks for one kind of pattern.", wait=1.7)

        task_intro = Text(
            "One kernel  →  one feature map (one channel)",
            font="Sans", weight=BOLD, color=ACCENT,
        ).scale(0.42)
        task_intro.move_to(ORIGIN)
        self.play(Write(task_intro), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(task_intro), run_time=0.6)

        names = ["horizontal edge", "vertical edge", "corner", "texture", "blob"]
        colors = [RED_D, ORANGE_D, TEAL_D, PURPLE_D, BLUE_D]
        kernels = VGroup()
        feature_maps = VGroup()

        # Input stub farther left so kernel labels have room on their left
        img_stub = Square(1.4, color=BLUE_D, fill_opacity=0.2, stroke_width=2.5).shift(LEFT * 5.5 + DOWN * 0.2)
        img_stub_lbl = Text("image", font="Sans", color=BLUE_D).scale(0.28).next_to(img_stub, UP, buff=0.12)
        self.play(FadeIn(img_stub), Write(img_stub_lbl), run_time=0.9)

        for i in range(5):
            self.say(f"Kernel {i + 1} looks for: {names[i]}  →  builds feature map {i + 1}", wait=1.3)

            k = Square(0.85, color=colors[i], fill_opacity=0.4, stroke_width=2.5)
            k_lbl = Text(f"K{i + 1}", font="Sans", weight=BOLD, color=INK).scale(0.32).move_to(k)
            k.move_to(LEFT * 1.5 + UP * (1.8 - i * 0.85))
            k_lbl.move_to(k)
            k_tag = Text(names[i], font="Sans", color=MUTED).scale(0.26)
            k_tag.next_to(k, LEFT, buff=0.2)
            k_block = VGroup(k_tag, k, k_lbl)

            fmap = Square(0.95, color=colors[i], fill_opacity=0.35, stroke_width=2.5)
            f_lbl = Text(f"map {i + 1}", font="Sans", color=INK).scale(0.26).move_to(fmap)
            f_block = VGroup(fmap, f_lbl)
            f_block.move_to(RIGHT * 2.2 + UP * (1.8 - i * 0.85))

            self.play(FadeIn(k_block), run_time=0.7)
            beam = Arrow(k.get_right(), fmap.get_left(), buff=0.12, color=colors[i], stroke_width=3.5)
            scan = Square(0.35, color=GOLD_D, fill_opacity=0.5, stroke_width=2).move_to(
                img_stub.get_corner(UL) + RIGHT * 0.25 + DOWN * 0.25
            )
            self.play(FadeIn(scan), run_time=0.4)
            self.play(scan.animate.shift(RIGHT * 0.8 + DOWN * 0.8), run_time=0.8, rate_func=linear)
            self.play(GrowArrow(beam), FadeIn(f_block), run_time=0.9)
            self.wait(1.0)
            self.play(FadeOut(beam), FadeOut(scan), run_time=0.45)

            kernels.add(k_block)
            feature_maps.add(f_block)

        rule = Text("5 kernels  →  5 feature maps", font="Sans", weight=BOLD, color=ACCENT).scale(0.4)
        rule.to_edge(DOWN, buff=1.05)
        self.play(Write(rule), run_time=0.9)
        self.wait(1.2)

        # Stack the feature maps along depth (visual Z via offset)
        self.say("Stack the feature maps: depth = number of channels.", wait=1.5)
        self.play(FadeOut(kernels), FadeOut(img_stub), FadeOut(img_stub_lbl), FadeOut(rule), run_time=0.8)

        stack_target = VGroup()
        anims = []
        for i, fm in enumerate(feature_maps):
            target = fm.copy()
            # Fan into a centered depth stack (2D offset mimics depth)
            target.move_to(ORIGIN + RIGHT * i * 0.22 + DOWN * i * 0.22)
            stack_target.add(target)
            anims.append(fm.animate.move_to(target.get_center()))

        stack_lbl = Text("Stacked channels  (H × W × 5)", font="Sans", color=ACCENT).scale(0.38)
        stack_lbl.to_edge(UP, buff=1.2)

        self.play(*anims, Write(stack_lbl), run_time=1.8)
        self.set_dims("K filters → K channels in the output volume")
        brace_note = Text(
            "Later layers: more kernels → thicker channel stacks",
            font="Sans", color=INK,
        ).scale(0.34).to_edge(DOWN, buff=1.05)
        self.play(Write(brace_note), run_time=0.9)
        self.wait(2.2)

    # ------------------------------------------------------------------
    def _convolve_window(
        self, inp, ker, inp_vals, ker_vals, out, out_idx, r0, c0, *, detailed: bool,
    ):
        """Multiply each cell, list products, then sum into the feature map."""
        self.say(
            f"Window top-left at ({r0},{c0}): multiply each pair first — do not jump to the total yet.",
            wait=1.4 if detailed else 1.1,
        )
        win = highlight_window(inp, 4, 4, r0, c0, 3, color=GOLD_D)
        self.play(Create(win), run_time=0.7)

        # Build a products panel in the center
        products = []
        product_cells = VGroup()
        for di in range(3):
            for dj in range(3):
                a = inp_vals[r0 + di][c0 + dj]
                b = ker_vals[di][dj]
                products.append(a * b)

        # Header
        prod_title = Text("Products (input × weight)", font="Sans", color=GOLD_D).scale(0.28)
        prod_title.move_to(ORIGIN + UP * 0.95 + RIGHT * 0.3)

        # 3×3 grid of product values (start empty / dash)
        prod_grid = number_grid([["—"] * 3 for _ in range(3)], cell=0.52, color=ORANGE_D, font_scale=0.24)
        prod_grid.move_to(ORIGIN + RIGHT * 0.3 + DOWN * 0.15)
        self.play(Write(prod_title), FadeIn(prod_grid), run_time=0.8)

        # Fill each product one by one
        for n, (di, dj) in enumerate([(di, dj) for di in range(3) for dj in range(3)]):
            a = inp_vals[r0 + di][c0 + dj]
            b = ker_vals[di][dj]
            p = a * b
            # Highlight matching cells
            in_cell = inp[(r0 + di) * 4 + (c0 + dj)]
            k_cell = ker[di * 3 + dj]
            self.play(
                in_cell[0].animate.set_fill(BLUE_D, opacity=0.45),
                k_cell[0].animate.set_fill(GOLD_D, opacity=0.55),
                run_time=0.35 if detailed else 0.22,
            )
            eq = Text(f"{a} × {b} = {p}", font="Sans", color=ACCENT).scale(0.30)
            eq.next_to(prod_grid, DOWN, buff=0.35)
            self.play(FadeIn(eq), run_time=0.35 if detailed else 0.22)

            cell = prod_grid[di * 3 + dj]
            new_txt = Text(str(p), font="Sans", color=INK).scale(0.28).move_to(cell[0])
            self.play(
                cell[0].animate.set_fill(ORANGE_D, opacity=0.35),
                Transform(cell[1], new_txt),
                run_time=0.4 if detailed else 0.28,
            )
            self.play(FadeOut(eq), run_time=0.25 if detailed else 0.15)
            self.play(
                in_cell[0].animate.set_fill(BLUE_D, opacity=0.12),
                k_cell[0].animate.set_fill(GOLD_D, opacity=0.12),
                run_time=0.25 if detailed else 0.15,
            )
            if detailed:
                self.wait(0.35)

        # Summation step
        total = sum(products)
        self.set_dims("step 2: add all 9 products together")
        self.say(f"Now sum every product:  {' + '.join(str(p) for p in products)}", wait=1.5 if detailed else 1.2)

        sum_txt = Text(f"Σ = {total}", font="Sans", weight=BOLD, color=GREEN_D).scale(0.45)
        sum_txt.next_to(prod_grid, DOWN, buff=0.4)
        self.play(Write(sum_txt), run_time=0.8)
        self.wait(1.0 if detailed else 0.8)

        self.say(f"Write {total} into the feature map (this is one output pixel).", wait=1.3)
        cell = out[out_idx]
        new_txt = Text(str(total), font="Sans", weight=BOLD, color=INK).scale(0.34).move_to(cell[0])
        fly = sum_txt.copy()
        self.play(
            fly.animate.move_to(cell.get_center()).scale(0.5),
            cell[0].animate.set_fill(GREEN_D, opacity=0.4),
            Transform(cell[1], new_txt),
            run_time=1.1,
        )
        self.wait(0.9)
        self.play(
            FadeOut(win), FadeOut(prod_title), FadeOut(prod_grid), FadeOut(sum_txt), FadeOut(fly),
            run_time=0.7,
        )
        self.wait(0.5)
