#!/usr/bin/env python3
"""
gen_calib_pattern.py

生成相机标定板图（棋盘格、对称圆点格、非对称圆点格）。

依赖：Pillow, numpy
pip install pillow numpy

示例：
python gen_calib_pattern.py --type chessboard --rows 6 --cols 9 --square_mm 25 --dpi 300 --out chessboard.png
"""

import argparse
from PIL import Image, ImageDraw
import numpy as np
import math
import os

def mm_to_px(mm, dpi):
    """毫米转换为像素"""
    return int(round(mm * dpi / 25.4))

def make_chessboard(rows, cols, square_px, margin_px=100, bg_color=(255,255,255), fg_color=(0,0,0)):
    """生成棋盘格图像。rows, cols 为格子数（内角点+1）或方格数，square_px 方格像素大小。"""
    W = cols * square_px
    H = rows * square_px
    img = Image.new("RGB", (W + 2*margin_px, H + 2*margin_px), bg_color)
    draw = ImageDraw.Draw(img)
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                x0 = margin_px + c * square_px
                y0 = margin_px + r * square_px
                draw.rectangle([x0, y0, x0 + square_px - 1, y0 + square_px - 1], fill=fg_color)
    return img

def make_circle_grid(rows, cols, square_px, circle_diameter_px=None, margin_px=100, bg_color=(255,255,255), fg_color=(0,0,0)):
    """生成对称圆点格，rows x cols 的点阵，点间距 square_px"""
    if circle_diameter_px is None:
        circle_diameter_px = int(round(square_px * 0.6))
    W = (cols - 1) * square_px
    H = (rows - 1) * square_px
    img = Image.new("RGB", (W + 2*margin_px, H + 2*margin_px), bg_color)
    draw = ImageDraw.Draw(img)
    r = circle_diameter_px / 2.0
    for i in range(rows):
        for j in range(cols):
            cx = margin_px + j * square_px
            cy = margin_px + i * square_px
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fg_color)
    return img

def make_asymmetric_circle_grid(rows, cols, square_px, circle_diameter_px=None, margin_px=100, bg_color=(255,255,255), fg_color=(0,0,0)):
    """
    生成非对称圆点格（常见的 OpenCV asymmetricGrid）：列方向偶数列向右偏移半个间距。
    rows: 行数（在 OpenCV 命名中一般是 points per column）
    cols: 列数（points per row）
    """
    if circle_diameter_px is None:
        circle_diameter_px = int(round(square_px * 0.6))
    # 计算格子实际宽度：由于奇偶列交错，宽度为 (cols-1 + 0.5) * square_px
    W = int(round(((cols - 1) + 0.5) * square_px))
    H = (rows - 1) * square_px
    img = Image.new("RGB", (W + 2*margin_px, H + 2*margin_px), bg_color)
    draw = ImageDraw.Draw(img)
    r = circle_diameter_px / 2.0
    for i in range(rows):
        for j in range(cols):
            offset = 0.5 * square_px if (j % 2 == 1) else 0.0
            cx = margin_px + int(round(j * square_px + offset))
            cy = margin_px + i * square_px
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fg_color)
    return img

def save_with_dpi(img, out_path, dpi):
    """保存图片并设置 DPI（PNG 支持），如果希望 PDF，可用 out_path.pdf"""
    # PIL 的 save 支持 dpi 参数 (tuple)
    ext = os.path.splitext(out_path)[1].lower()
    if ext == '':
        out_path += '.png'
    if ext == '.pdf':
        img.save(out_path, "PDF", resolution=dpi)
    else:
        img.save(out_path, dpi=(dpi, dpi))
    print(f"Saved {out_path}")

def parse_args():
    p = argparse.ArgumentParser(description="Generate camera calibration patterns")
    p.add_argument("--type", default="chessboard", choices=["chessboard", "circles", "asymmetric_circles"], help="pattern type")
    p.add_argument("--rows", type=int, default=6, help="rows (squares or points vertically)")
    p.add_argument("--cols", type=int, default=9, help="cols (squares or points horizontally)")
    p.add_argument("--square_mm", type=float, default=25.0, help="square / spacing size in millimeters")
    p.add_argument("--dpi", type=int, default=300, help="print DPI (dots per inch)")
    p.add_argument("--margin_mm", type=float, default=20.0, help="margin around pattern in mm")
    p.add_argument("--out", default="calib_pattern.png", help="output filename (png or pdf)")
    p.add_argument("--bg", default="white", help="background color (name or hex)")
    p.add_argument("--fg", default="black", help="foreground color (name or hex)")
    return p.parse_args()

def color_from_str(s):
    # 简单支持常见颜色名或 hex RGB 如 "#rrggbb"
    s = s.strip()
    if s.startswith("#"):
        s = s.lstrip("#")
        if len(s) == 6:
            return tuple(int(s[i:i+2],16) for i in (0,2,4))
    common = {
        "white": (255,255,255),
        "black": (0,0,0),
        "gray": (128,128,128),
    }
    return common.get(s.lower(), (0,0,0))

def main():
    args = parse_args()
    square_px = mm_to_px(args.square_mm, args.dpi)
    margin_px = mm_to_px(args.margin_mm, args.dpi)
    bg_color = color_from_str(args.bg)
    fg_color = color_from_str(args.fg)

    print(f"Generating {args.type} rows={args.rows} cols={args.cols}, square={args.square_mm}mm -> {square_px}px, dpi={args.dpi}")

    if args.type == "chessboard":
        img = make_chessboard(args.rows, args.cols, square_px, margin_px=margin_px, bg_color=bg_color, fg_color=fg_color)
    elif args.type == "circles":
        # rows, cols for points: points per column x points per row
        img = make_circle_grid(args.rows, args.cols, square_px, circle_diameter_px=int(round(square_px*0.6)), margin_px=margin_px, bg_color=bg_color, fg_color=fg_color)
    else:
        img = make_asymmetric_circle_grid(args.rows, args.cols, square_px, circle_diameter_px=int(round(square_px*0.6)), margin_px=margin_px, bg_color=bg_color, fg_color=fg_color)

    save_with_dpi(img, args.out, args.dpi)

if __name__ == "__main__":
    main()
