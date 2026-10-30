# -*- coding: utf-8 -*-
"""
GenPark Magic UI FastMCP Server
"""

import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from client import GenParkMagicUI

mcp = FastMCP("genpark-magic-ui")
magic = GenParkMagicUI()

@mcp.tool()
def solve_flex_layout(
    container_width: float,
    container_height: float,
    items_json: str,
    gap: float = 16.0,
    justify_content: str = "space_between",
    align_items: str = "center"
) -> str:
    """
    Solves 1D flexbox row layout coordinates (x, y, w, h) with flex-grow and flex-shrink.
    """
    items = json.loads(items_json)
    res = magic.solve_flex_layout(container_width, container_height, items, gap, justify_content, align_items)
    return json.dumps(res, indent=2)

@mcp.tool()
def generate_design_tokens_palette(
    primary_hex: str = "#6366f1",
    dark_mode: bool = True
) -> str:
    """
    Generates a 10-shade design system token palette with WCAG 2.1 contrast ratios.
    """
    res = magic.generate_design_tokens_palette(primary_hex, dark_mode)
    return json.dumps(res, indent=2)

@mcp.tool()
def compute_fluid_modular_scale(
    base_font_px: float = 16.0,
    ratio: float = 1.25,
    min_viewport_px: float = 375.0,
    max_viewport_px: float = 1440.0,
    steps: int = 5
) -> str:
    """
    Computes fluid typography tokens using CSS clamp() and modular scaling ratios.
    """
    res = magic.compute_fluid_modular_scale(base_font_px, ratio, min_viewport_px, max_viewport_px, steps)
    return json.dumps(res, indent=2)

def main():
    print("Testing Magic UI:")
    print(compute_fluid_modular_scale(16.0, 1.25))

if __name__ == "__main__":
    main()
