"""Shared HUD: KAUST logo, captions, dimension badges — light (white) theme."""

from __future__ import annotations

from pathlib import Path

from manim import *

ASSET_DIR = Path(__file__).resolve().parents[2] / "assets"
LOGO_PATH = ASSET_DIR / "kaust-academy.png"

# Light theme palette
BG = "#FFFFFF"
INK = "#1a1a1a"
ACCENT = "#0B3D5C"
CAPTION = "#8A5A00"
MUTED = "#5a6570"
BADGE_FILL = "#F0F4F8"
BADGE_STROKE = "#0B3D5C"
GOLD_D = "#B8860B"
BLUE_D = "#1e5a8a"
GREEN_D = "#1b6b3a"
RED_D = "#a33b2a"
ORANGE_D = "#c45c12"
PURPLE_D = "#6b3d8a"
TEAL_D = "#0d7377"


def _bg(scene: Scene) -> None:
    scene.camera.background_color = BG


def logo_mobject(width: float = 1.35) -> Mobject:
    if not LOGO_PATH.exists():
        return Text("KAUST Academy", color=INK).scale(0.28)
    img = ImageMobject(str(LOGO_PATH))
    img.set_width(width)
    # Soft backing so the logo separates from white
    backing = RoundedRectangle(
        width=img.width + 0.18,
        height=img.height + 0.14,
        corner_radius=0.06,
        stroke_width=1,
        color=MUTED,
        fill_color=WHITE,
        fill_opacity=1,
    )
    backing.move_to(img)
    return Group(backing, img)


def add_kaust_logo(scene: Scene, width: float = 1.35) -> Mobject:
    """Pin logo top-right (fixed in frame for 3D scenes)."""
    logo = logo_mobject(width=width)
    logo.to_corner(UR, buff=0.28)
    if isinstance(scene, ThreeDScene):
        scene.add_fixed_in_frame_mobjects(logo)
    else:
        scene.add(logo)
    return logo


def title_card(text: str, scale: float = 0.55) -> Text:
    return Text(text, font="Sans", weight=BOLD).scale(scale).set_color(INK)


def hud_caption(text: str, scale: float = 0.34, color=CAPTION) -> Text:
    return Text(text, font="Sans").scale(scale).set_color(color)


def dims_badge(text: str, scale: float = 0.32, color=BADGE_STROKE) -> VGroup:
    """Sticky shape / tensor-dimension chip."""
    label = Text(text, font="Sans", weight=BOLD).scale(scale).set_color(color)
    box = SurroundingRectangle(label, buff=0.12, corner_radius=0.08, color=color, stroke_width=1.8)
    box.set_fill(BADGE_FILL, opacity=1.0)
    return VGroup(box, label)


class BrandScene(Scene):
    """2D scene with logo + mutable caption + optional dims badge."""

    chapter_title: str = ""

    def setup_branding(self, title: str | None = None) -> None:
        _bg(self)
        self.logo = add_kaust_logo(self)
        t = title or self.chapter_title
        self.title_mob = title_card(t, scale=0.48).to_corner(UL, buff=0.32)
        self.caption = hud_caption("").to_edge(DOWN, buff=0.32)
        self.dims = dims_badge("").to_corner(UL, buff=0.32).shift(DOWN * 0.85)
        self.dims.set_opacity(0)
        self._dims_visible = False
        self.add(self.title_mob, self.caption, self.dims)

    def say(self, msg: str, wait: float = 1.4) -> None:
        new_c = hud_caption(msg).to_edge(DOWN, buff=0.32)
        self.play(Transform(self.caption, new_c), run_time=0.55)
        if wait:
            self.wait(wait)

    def set_dims(self, text: str, wait: float = 0.7) -> None:
        new_d = dims_badge(text).to_corner(UL, buff=0.32).shift(DOWN * 0.85)
        if not getattr(self, "_dims_visible", False):
            self.dims.become(new_d)
            self.play(FadeIn(self.dims), run_time=0.55)
            self._dims_visible = True
        else:
            self.play(Transform(self.dims, new_d), run_time=0.55)
        if wait:
            self.wait(wait)


class BrandThreeDScene(ThreeDScene):
    """3D scene with fixed-in-frame branding."""

    chapter_title: str = ""

    def setup_branding(self, title: str | None = None) -> None:
        _bg(self)
        self.logo = add_kaust_logo(self)
        t = title or self.chapter_title
        self.title_mob = title_card(t, scale=0.45).to_corner(UL, buff=0.28)
        self.caption = hud_caption("").to_edge(DOWN, buff=0.28)
        # Do NOT add an empty dims chip (looks like a blank box on white)
        self.dims = None
        self._dims_visible = False
        self.add_fixed_in_frame_mobjects(self.title_mob, self.caption)

    def say(self, msg: str, wait: float = 1.4) -> None:
        new_c = hud_caption(msg).to_edge(DOWN, buff=0.28)
        self.remove(self.caption)
        self.remove_fixed_in_frame_mobjects(self.caption)
        self.caption = new_c
        self.add_fixed_in_frame_mobjects(self.caption)
        self.play(FadeIn(self.caption), run_time=0.5)
        if wait:
            self.wait(wait)

    def set_dims(self, text: str, wait: float = 0.7) -> None:
        """Replace dims HUD as fixed-in-frame so it never rotates with the 3D view."""
        new_d = dims_badge(text).to_corner(UL, buff=0.28).shift(DOWN * 0.85)
        if self.dims is not None:
            self.remove(self.dims)
            self.remove_fixed_in_frame_mobjects(self.dims)
        self.dims = new_d
        self.add_fixed_in_frame_mobjects(self.dims)
        self._dims_visible = True
        self.play(FadeIn(self.dims), run_time=0.5)
        if wait:
            self.wait(wait)


# ---------------------------------------------------------------------------
# Shared visual primitives for numeric grids
# ---------------------------------------------------------------------------

def number_grid(values, cell=0.55, color=BLUE_D, font_scale=0.28) -> VGroup:
    """values: 2D list of numbers → VGroup of cells (row-major)."""
    rows, cols = len(values), len(values[0])
    cells = VGroup()
    for i in range(rows):
        for j in range(cols):
            sq = Square(side_length=cell, stroke_width=2.2, color=color, fill_opacity=0.12)
            val = values[i][j]
            if isinstance(val, float):
                txt = Text(f"{val:g}", font="Sans").scale(font_scale).set_color(INK)
            else:
                txt = Text(str(val), font="Sans").scale(font_scale).set_color(INK)
            txt.move_to(sq)
            item = VGroup(sq, txt)
            item.move_to(RIGHT * j * cell + DOWN * i * cell)
            cells.add(item)
    cells.move_to(ORIGIN)
    return cells


def highlight_window(grid: VGroup, rows: int, cols: int, r0: int, c0: int, k: int, color=GOLD_D) -> SurroundingRectangle:
    """Surround the k×k block whose top-left is (r0,c0) in a rows×cols grid VGroup."""
    idxs = [r0 * cols + c0 + di * cols + dj for di in range(k) for dj in range(k)]
    group = VGroup(*[grid[i] for i in idxs])
    return SurroundingRectangle(group, color=color, buff=0.04, stroke_width=3.5)
