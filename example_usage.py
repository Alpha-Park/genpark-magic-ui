# -*- coding: utf-8 -*-
import json
from client import GenParkMagicUI

ui = GenParkMagicUI()

# 1. Flexbox Layout Constraint Solver
items = [
    {"id": "logo", "width": 120.0, "height": 40.0, "flex_grow": 0.0},
    {"id": "search_bar", "width": 300.0, "height": 40.0, "flex_grow": 2.0},
    {"id": "user_avatar", "width": 40.0, "height": 40.0, "flex_grow": 0.0}
]
layout = ui.solve_flex_layout(container_width=1000.0, container_height=60.0, items=items, gap=20.0)
print("Flexbox Layout Solution:")
for item in layout["layout_items"]:
    print(f"  {item['item_id']}: Pos=({item['x']}, {item['y']}) Size=({item['width']}x{item['height']})")

# 2. Design Tokens Palette with WCAG Contrast
tokens = ui.generate_design_tokens_palette(primary_hex="#6366f1", dark_mode=True)
print()
print(f"Primary Base: {tokens['primary_base_hex']} (Luminance: {tokens['primary_relative_luminance']})")
print(f"Shade 500: {tokens['shades']['500']['hex']} - Contrast vs Dark: {tokens['shades']['500']['contrast_against_dark']}:1 (AA: {tokens['shades']['500']['wcag_aa_compliant']})")

# 3. Fluid Modular Scale Typography Tokens
scale = ui.compute_fluid_modular_scale(base_font_px=16.0, ratio=1.25, steps=4)
print()
print("Fluid Typography Clamp Tokens:")
for label, data in scale["typography_tokens"].items():
    print(f"  {label}: {data['min_px']}px -> {data['max_px']}px | CSS: {data['css_clamp']}")
