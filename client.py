# -*- coding: utf-8 -*-
"""
GenPark Magic UI Client
Zero-dependency flexbox/grid layout constraint solver, OKLCH/sRGB design tokens generator,
and fluid typography Golden Ratio / Modular Scale calculator.
"""

import math
from typing import Dict, List, Any, Optional

class GenParkMagicUI:
    """
    Computes CSS flexbox/grid bounding boxes, generates WCAG-compliant design token palettes,
    and calculates fluid modular scales.
    """

    def solve_flex_layout(
        self,
        container_width: float,
        container_height: float,
        items: List[Dict[str, Any]],
        gap: float = 16.0,
        justify_content: str = "space_between",
        align_items: str = "center"
    ) -> Dict[str, Any]:
        """
        Solves 1D flexbox row layout coordinates (x, y, w, h) with flex-grow and flex-shrink.
        """
        if container_width <= 0 or container_height <= 0:
            raise ValueError("Container dimensions must be positive.")
        if not items:
            return {"container": {"w": container_width, "h": container_height}, "items": []}

        n = len(items)
        total_gaps = max(0, n - 1) * gap
        base_widths = [item.get("width", 100.0) for item in items]
        total_base_w = sum(base_widths)
        available_w = container_width - total_gaps

        final_widths = list(base_widths)

        if total_base_w < available_w:
            # Flex grow distribution
            free_space = available_w - total_base_w
            grow_factors = [item.get("flex_grow", 0.0) for item in items]
            total_grow = sum(grow_factors)
            if total_grow > 0:
                for i in range(n):
                    final_widths[i] += free_space * (grow_factors[i] / total_grow)
        elif total_base_w > available_w:
            # Flex shrink distribution
            overflow = total_base_w - available_w
            shrink_factors = [item.get("flex_shrink", 1.0) for item in items]
            weighted_shrink = sum(s * w for s, w in zip(shrink_factors, base_widths))
            if weighted_shrink > 0:
                for i in range(n):
                    reduction = overflow * (shrink_factors[i] * base_widths[i] / weighted_shrink)
                    final_widths[i] = max(10.0, base_widths[i] - reduction)

        # Positioning based on justify_content
        allocated_w = sum(final_widths) + total_gaps
        extra_space = max(0.0, container_width - allocated_w)

        coords = []
        if justify_content == "center":
            curr_x = extra_space / 2.0
            step_gap = gap
        elif justify_content == "space_between" and n > 1:
            curr_x = 0.0
            step_gap = gap + (extra_space / (n - 1))
        elif justify_content == "space_around" and n > 0:
            space_unit = extra_space / (n * 2)
            curr_x = space_unit
            step_gap = gap + space_unit * 2
        else: # flex_start
            curr_x = 0.0
            step_gap = gap

        for i, item in enumerate(items):
            w = round(final_widths[i], 2)
            h = min(container_height, item.get("height", container_height))
            
            # Align items (cross-axis: y)
            if align_items == "flex_start":
                y = 0.0
            elif align_items == "flex_end":
                y = container_height - h
            else: # center
                y = (container_height - h) / 2.0

            coords.append({
                "item_id": item.get("id", f"item_{i}"),
                "x": round(curr_x, 2),
                "y": round(y, 2),
                "width": w,
                "height": round(h, 2)
            })
            curr_x += w + step_gap

        return {
            "container": {"width": container_width, "height": container_height},
            "item_count": n,
            "allocated_width": round(sum(final_widths) + total_gaps, 2),
            "free_space_remaining": round(max(0.0, container_width - (sum(final_widths) + total_gaps)), 2),
            "layout_items": coords
        }

    def generate_design_tokens_palette(
        self,
        primary_hex: str = "#6366f1",
        dark_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Generates a 10-shade design system token palette with WCAG 2.1 contrast ratios.
        """
        hex_clean = primary_hex.lstrip("#")
        if len(hex_clean) == 3:
            hex_clean = "".join(c * 2 for c in hex_clean)
        if len(hex_clean) != 6:
            hex_clean = "6366f1"

        r = int(hex_clean[0:2], 16) / 255.0
        g = int(hex_clean[2:4], 16) / 255.0
        b = int(hex_clean[4:6], 16) / 255.0

        def rel_luminance(red, green, blue):
            def ch_lin(c):
                return c / 12.92 if c <= 0.04045 else math.pow((c + 0.055) / 1.055, 2.4)
            return 0.2126 * ch_lin(red) + 0.7152 * ch_lin(green) + 0.0722 * ch_lin(blue)

        lum_primary = rel_luminance(r, g, b)

        # Shades from 50 (lightest) to 900 (darkest)
        shade_keys = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
        palette = {}

        for k in shade_keys:
            # lightness multiplier
            t = (k - 50) / 850.0  # 0 to 1
            if t < 0.5:
                # tint towards white
                factor = 1.0 - (t * 2.0)
                sr = r + (1.0 - r) * factor * 0.9
                sg = g + (1.0 - g) * factor * 0.9
                sb = b + (1.0 - b) * factor * 0.9
            else:
                # shade towards dark slate
                factor = (t - 0.5) * 2.0
                sr = r * (1.0 - factor * 0.75)
                sg = g * (1.0 - factor * 0.75)
                sb = b * (1.0 - factor * 0.75)

            ir = max(0, min(255, int(round(sr * 255))))
            ig = max(0, min(255, int(round(sg * 255))))
            ib = max(0, min(255, int(round(sb * 255))))
            hex_shade = f"#{ir:02x}{ig:02x}{ib:02x}"
            
            lum_shade = rel_luminance(sr, sg, sb)
            # Contrast against white (#ffffff)
            cr_white = (1.0 + 0.05) / (lum_shade + 0.05) if 1.0 > lum_shade else (lum_shade + 0.05) / (1.0 + 0.05)
            # Contrast against dark (#0f172a, lum ~ 0.01)
            cr_dark = (lum_shade + 0.05) / (0.01 + 0.05)

            palette[str(k)] = {
                "hex": hex_shade,
                "relative_luminance": round(lum_shade, 4),
                "contrast_against_white": round(cr_white, 2),
                "contrast_against_dark": round(cr_dark, 2),
                "wcag_aa_compliant": cr_dark >= 4.5 if dark_mode else cr_white >= 4.5
            }

        return {
            "primary_base_hex": f"#{hex_clean}",
            "primary_relative_luminance": round(lum_primary, 4),
            "dark_mode_optimized": dark_mode,
            "shades": palette
        }

    def compute_fluid_modular_scale(
        self,
        base_font_px: float = 16.0,
        ratio: float = 1.25,
        min_viewport_px: float = 375.0,
        max_viewport_px: float = 1440.0,
        steps: int = 5
    ) -> Dict[str, Any]:
        """
        Computes fluid typography tokens using CSS clamp() and modular scaling ratios.
        """
        if steps <= 0:
            raise ValueError("Steps must be positive.")

        scale_tokens = {}
        labels = ["sm", "base", "md", "lg", "xl", "2xl", "3xl", "4xl"]

        for step in range(steps):
            label = labels[step] if step < len(labels) else f"step_{step}"
            power = step - 1  # 0 -> sm (ratio^-1), 1 -> base (ratio^0), 2 -> md (ratio^1)

            # Desktop target
            max_size = base_font_px * math.pow(ratio, power)
            # Mobile target (compressed ratio)
            mobile_ratio = 1.0 + (ratio - 1.0) * 0.6
            min_size = base_font_px * math.pow(mobile_ratio, power)

            # Fluid clamp slope & intercept
            slope = (max_size - min_size) / (max_viewport_px - min_viewport_px)
            y_intercept = min_size - slope * min_viewport_px

            slope_vw = round(slope * 100.0, 3)
            intercept_rem = round(y_intercept / 16.0, 3)
            min_rem = round(min_size / 16.0, 3)
            max_rem = round(max_size / 16.0, 3)

            clamp_str = f"clamp({min_rem}rem, {slope_vw}vw + {intercept_rem}rem, {max_rem}rem)"

            scale_tokens[label] = {
                "min_px": round(min_size, 1),
                "max_px": round(max_size, 1),
                "css_clamp": clamp_str
            }

        return {
            "base_font_px": base_font_px,
            "modular_ratio": ratio,
            "min_viewport_px": min_viewport_px,
            "max_viewport_px": max_viewport_px,
            "typography_tokens": scale_tokens
        }
