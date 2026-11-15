#!/usr/bin/env python3
"""Generate SkinRx by Burds Family Practice SVG emblems and atmospheric hero banner."""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "src/assets/img"

# Official SkinRx by Burds Family Practice palette tokens
DEEP_ESPRESSO = "#26211F"
DUSTY_BLUSH = "#C3B1AC"
DEEP_MAUVE = "#6E525C"
SOFT_SAGE = "#BCCCC1"
SOFT_CREAM = "#F5F2EF"


def emblem(ring_color, leaf_color, accent_color, bg=None):
    """Build a crisp SkinRx botanical-profile seal SVG in the requested colors."""
    back = f'<rect width="100" height="100" rx="22" fill="{bg}"/>' if bg else ""

    # Double outer seal rings echoing the official SkinRx circular mark
    rings = (
        f'<g fill="none" stroke="{ring_color}" stroke-linecap="round">'
        '<circle cx="50" cy="50" r="43" stroke-width="2.6"/>'
        f'<circle cx="50" cy="50" r="38" stroke="{accent_color}" stroke-width="1.35" stroke-opacity="0.72"/>'
        "</g>"
    )

    # Three organic botanical leaves curving up-left, paired with a clean aesthetic profile line
    leaves = (
        f'<g fill="none" stroke="{leaf_color}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">'
        # Outer left leaf
        '<path d="M 41 58 C 30 55 24 44 26 33 C 36 35 43 44 41 58 Z"/>'
        # Center tall leaf
        '<path d="M 45 50 C 37 39 38 25 45 18 C 52 25 53 39 45 50 Z"/>'
        # Right inner leaf curving toward brow
        '<path d="M 50 53 C 48 41 53 29 61 25 C 63 36 58 47 50 53 Z"/>'
        # Sweeping stem/neck ribbon
        '<path d="M 41 78 C 40 66 44 58 50 53"/>'
        '<path d="M 48 80 C 48 68 51 60 57 54"/>'
        "</g>"
    )

    # Minimalist serene facial profile silhouette on the right
    profile = (
        f'<path d="M 65 29 C 70 33 71 39 70 43 '
        'L 75 50 L 71 53 C 72 56 71 58 69 59 '
        'C 71 61 70 63 68 65 '
        'C 69 70 64 73 57 73 '
        'C 54 73 51 75 50 79" '
        f'fill="none" stroke="{ring_color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    # Delicate 4-point clinical radiance spark
    spark = (
        f'<path d="M 27 68 Q 27 73 32 73 Q 27 73 27 78 Q 27 73 22 73 Q 27 73 27 68 Z" '
        f'fill="{accent_color}"/>'
    )

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
        'role="img" aria-label="SkinRx by Burds Family Practice emblem">'
        f"{back}{rings}{leaves}{profile}{spark}</svg>\n"
    )


def hero_banner_bg():
    """Atmospheric Deep Espresso, Dusty Blush, Deep Mauve, and Soft Sage full-bleed SVG."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 720" '
        'preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        "<defs>"
        '<radialGradient id="mauveCenter" cx="50%" cy="44%" r="54%">'
        f'<stop offset="0%" stop-color="{DEEP_MAUVE}" stop-opacity="0.58"/>'
        f'<stop offset="55%" stop-color="{DEEP_ESPRESSO}" stop-opacity="0.65"/>'
        '<stop offset="100%" stop-color="#1A1615" stop-opacity="0.92"/>'
        "</radialGradient>"
        '<radialGradient id="blushGlow" cx="18%" cy="22%" r="44%">'
        f'<stop offset="0%" stop-color="{DUSTY_BLUSH}" stop-opacity="0.22"/>'
        f'<stop offset="100%" stop-color="{DUSTY_BLUSH}" stop-opacity="0"/>'
        "</radialGradient>"
        '<radialGradient id="sageGlow" cx="84%" cy="74%" r="44%">'
        f'<stop offset="0%" stop-color="{SOFT_SAGE}" stop-opacity="0.18"/>'
        f'<stop offset="100%" stop-color="{SOFT_SAGE}" stop-opacity="0"/>'
        "</radialGradient>"
        '<linearGradient id="silkWave" x1="0%" y1="0%" x2="100%" y2="0%">'
        '<stop offset="0%" stop-color="#1E1918" stop-opacity="0.72"/>'
        f'<stop offset="50%" stop-color="{DEEP_MAUVE}" stop-opacity="0.34"/>'
        '<stop offset="100%" stop-color="#1E1918" stop-opacity="0.78"/>'
        "</linearGradient>"
        "</defs>"
        f'<rect width="1600" height="720" fill="{DEEP_ESPRESSO}"/>'
        '<rect width="1600" height="720" fill="url(#mauveCenter)"/>'
        '<rect width="1600" height="720" fill="url(#blushGlow)"/>'
        '<rect width="1600" height="720" fill="url(#sageGlow)"/>'
        f'<g fill="none" stroke="{SOFT_CREAM}" stroke-opacity="0.07" stroke-width="1.4">'
        '<circle cx="800" cy="245" r="245"/>'
        '<circle cx="800" cy="245" r="325" stroke-dasharray="6 10"/>'
        '<circle cx="800" cy="245" r="415" stroke-opacity="0.045"/>'
        "</g>"
        '<path d="M 0 548 C 280 500 540 600 840 558 C 1140 516 1380 590 1600 544 L 1600 720 L 0 720 Z" fill="url(#silkWave)"/>'
        '<path d="M 0 606 C 320 648 640 562 980 612 C 1260 652 1460 584 1600 604 L 1600 720 L 0 720 Z" fill="#181413" fill-opacity="0.62"/>'
        f'<path d="M 0 548 C 280 500 540 600 840 558 C 1140 516 1380 590 1600 544" fill="none" stroke="{DUSTY_BLUSH}" stroke-opacity="0.20" stroke-width="1.5"/>'
        f'<path d="M 0 606 C 320 648 640 562 980 612 C 1260 652 1460 584 1600 604" fill="none" stroke="{SOFT_SAGE}" stroke-opacity="0.18" stroke-width="1.2"/>'
        f'<path d="M 0 116 C 340 162 660 66 1020 112 C 1300 148 1480 96 1600 118" fill="none" stroke="{DUSTY_BLUSH}" stroke-opacity="0.12" stroke-width="1.2"/>'
        "</svg>\n"
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    OUT.joinpath("emblem-dark.svg").write_text(
        emblem(DEEP_ESPRESSO, DEEP_MAUVE, DUSTY_BLUSH), encoding="utf-8"
    )
    OUT.joinpath("emblem-light.svg").write_text(
        emblem(SOFT_CREAM, SOFT_SAGE, DUSTY_BLUSH), encoding="utf-8"
    )
    OUT.joinpath("favicon.svg").write_text(
        emblem(SOFT_CREAM, SOFT_SAGE, DUSTY_BLUSH, bg=DEEP_ESPRESSO), encoding="utf-8"
    )
    OUT.joinpath("hero-banner-bg.svg").write_text(hero_banner_bg(), encoding="utf-8")
    print("wrote emblem-dark.svg, emblem-light.svg, favicon.svg, hero-banner-bg.svg")


if __name__ == "__main__":
    main()
