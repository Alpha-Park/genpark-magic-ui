# genpark-magic-ui

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-zero-success)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

GenPark Magic UI is a zero-dependency frontend layout and design token engine implementing flexbox coordinate constraint solving, WCAG 2.1 contrast-compliant color palette generation, and fluid typography `clamp()` modular scales.

```mermaid
flowchart LR
    A[Container Constraints] --> B[Flex Space & Grow/Shrink Engine]
    B --> C[Item Bounding Boxes (x, y, w, h)]
    D[Primary Brand Hex] --> E[Relative Luminance Transform]
    E --> F[10-Shade WCAG Contrast Tokens]
    G[Base Font & Modular Ratio] --> H[Fluid CSS Clamp Interpolator]
```

## Features
- **Flexbox Constraint Solver**: Resolves exact coordinate bounding boxes handling `flex_grow`, `flex_shrink`, and multi-mode justification (`space-between`, `space-around`, `center`).
- **WCAG 2.1 Design Tokens**: Computes 10 shades with sRGB luminance and AA/AAA contrast ratios against light/dark themes.
- **Fluid Typography**: Generates CSS `clamp(min, preferred, max)` responsive typography tokens based on customizable modular ratios.

## Quickstart

```python
from client import GenParkMagicUI

ui = GenParkMagicUI()
res = ui.compute_fluid_modular_scale(base_font_px=16.0, ratio=1.25)
print(res["typography_tokens"]["lg"]["css_clamp"])
```

## License
MIT
