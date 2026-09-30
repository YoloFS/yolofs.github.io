#!/usr/bin/env python3
"""YoloFS 小红书轮播 v2：6 张 1080x1440，去AI味：真实标题、真实事故原话、真实arxiv号。"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1440
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BI, RI = 2, 2
N = 6  # total cards

AMBER = (245, 165, 36)
RED = (229, 72, 77)
GREEN = (23, 201, 100)
BLUE = (76, 154, 255)
WHITE = (244, 246, 251)
MUTED = (154, 164, 178)
DIM = (110, 120, 135)
PANEL = (22, 30, 46)
LINE = (38, 48, 68)

def font(bold, size):
    return ImageFont.truetype(BOLD if bold else REG, size, index=BI if bold else RI)

def base():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, bot = (17, 24, 40), (9, 12, 20)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    for cx, cy, r, a in [(930, 210, 260, 22), (120, 1250, 300, 16)]:
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(245, 165, 36, a), width=3)
        img = Image.alpha_composite(img.convert("RGBA"), ring).convert("RGB")
        d = ImageDraw.Draw(img)
    return img, d

def header(d):
    d.text((72, 58), "YoloFS", font=font(True, 42), fill=AMBER)
    d.text((W - 72, 66), "SOSP '26 · PRAGUE", font=font(False, 30), fill=MUTED, anchor="ra")
    d.line([(72, 128), (W - 72, 128)], fill=LINE, width=2)

def footer(d, page):
    d.text((72, 1368), "yolofs.github.io", font=font(False, 26), fill=DIM)
    d.text((W - 72, 1368), f"{page} / {N}", font=font(False, 26), fill=DIM, anchor="ra")

def wrap(d, text, fnt, max_w):
    # word-aware for pure-ASCII text (English), char-based for CJK
    if " " in text and all(ord(c) < 128 for c in text):
        out, line = [], ""
        for w in text.split(" "):
            cand = (line + " " + w).strip()
            if d.textlength(cand, font=fnt) <= max_w:
                line = cand
            else:
                if line: out.append(line)
                line = w
        if line: out.append(line)
        return out
    out, line = [], ""
    for ch in text:
        if d.textlength(line + ch, font=fnt) <= max_w:
            line += ch
        else:
            out.append(line); line = ch
    if line: out.append(line)
    return out

def panel_box(d, xy, radius=28, fill=PANEL, outline=None, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def chip(d, x, y, text, bg, fnt_size=30, fg=(10, 14, 22)):
    f = font(True, fnt_size)
    tw = d.textlength(text, font=f)
    pad_x, pad_y = 26, 12
    d.rounded_rectangle([x, y, x + tw + pad_x * 2, y + fnt_size + pad_y * 2], radius=20, fill=bg)
    d.text((x + pad_x, y + pad_y - 2), text, font=f, fill=fg)
    return tw + pad_x * 2

def tag_outline(d, x, y, text, fnt_size=32, color=AMBER):
    f = font(True, fnt_size)
    tw = d.textlength(text, font=f)
    pad_x, pad_y = 28, 14
    d.rounded_rectangle([x, y, x + tw + pad_x * 2, y + fnt_size + pad_y * 2],
                        radius=22, outline=color, width=2)
    d.text((x + pad_x, y + pad_y - 2), text, font=f, fill=color)

def arrow_down(d, x, y1, y2, color=MUTED, width=5):
    d.line([(x, y1), (x, y2)], fill=color, width=width)
    d.polygon([(x - 16, y2 - 22), (x + 16, y2 - 22), (x, y2)], fill=color)

# ---------------- card 1: announcement ----------------
def card1():
    img, d = base(); header(d); footer(d, 1)
    tag_outline(d, 72, 250, "YoloFS · SOSP '26")
    d.text((72, 350), "别让 Agent", font=font(True, 148), fill=WHITE)
    d.text((72, 525), "梭哈你的文件", font=font(True, 148), fill=AMBER)
    # English paper title, typeset as a title block
    d.line([(72, 755), (80, 885)], fill=AMBER, width=8)
    d.text((112, 750), "Don't Let AI Agents YOLO Your Files:", font=font(True, 44), fill=WHITE)
    d.text((112, 812), "Information and Control in Agent-Native Filesystems", font=font(False, 36), fill=MUTED)
    d.line([(72, 950), (W - 72, 950)], fill=LINE, width=2)
    d.text((72, 990), "yolofs.github.io", font=font(False, 36), fill=WHITE)
    d.text((72, 1050), "github.com/YoloFS/YoloFS", font=font(False, 36), fill=MUTED)
    img.save(f"{OUT}/card1_announce.png")

# ---------------- card 2: real incidents ----------------
def card2():
    img, d = base(); header(d); footer(d, 2)
    d.text((72, 190), "先看几个真实事故", font=font(True, 62), fill=WHITE)
    d.text((72, 275), "都来自论文分析的 290 份公开事故报告", font=font(False, 34), fill=MUTED)
    quotes = [
        ("“擦除整个 home 目录，", "毁掉 iCloud 里的全部文档”"),
        ("“依赖的构建脚本，", "顺手读走了你的 SSH key”"),
    ]
    y = 390
    for l1, l2 in quotes:
        panel_box(d, [72, y, W - 72, y + 250])
        d.line([(72, y), (86, y + 250)], fill=RED, width=10)
        d.text((116, y + 60), l1, font=font(True, 44), fill=WHITE)
        d.text((116, y + 130), l2, font=font(True, 44), fill=WHITE)
        y += 286
    d.text((72, y + 20), "更离谱的是：68% 的 Agent 毫无察觉，", font=font(True, 42), fill=AMBER)
    d.text((72, y + 80), "11% 还会撒谎：谎称修好了，伪造测试结果。", font=font(True, 42), fill=AMBER)
    # numbers strip
    sy = y + 180
    panel_box(d, [72, sy, W - 72, sy + 170])
    stats = [("290 份", "公开报告"), ("39%", "由删除引起"), ("40%", "无法恢复")]
    sw = (W - 144) // 3
    for i, (num, label) in enumerate(stats):
        x = 72 + i * sw
        d.text((x + sw / 2, sy + 30), num, font=font(True, 52), fill=WHITE, anchor="ma")
        d.text((x + sw / 2, sy + 105), label, font=font(False, 30), fill=MUTED, anchor="ma")
    img.save(f"{OUT}/card2_incidents.png")

# ---------------- card 3: the concept ----------------
def card3():
    img, d = base(); header(d); footer(d, 3)
    d.text((72, 180), "怎么办？换个思路", font=font(True, 56), fill=WHITE)
    d.text((72, 270), "Agent 原生文件系统", font=font(True, 72), fill=AMBER)
    rows = [("introspect", "看清影响", "看清每条命令到底动了哪些文件", AMBER),
            ("undo", "一键后悔", "覆盖、删除都能 undo，不用事前审批", GREEN),
            ("gate", "按需放行", "读走就退不回来，敏感路径先拦", BLUE)]
    y = 430
    for en, cn, desc, col in rows:
        panel_box(d, [72, y, W - 72, y + 220])
        d.line([(72, y), (86, y + 220)], fill=col, width=10)
        chip(d, 116, y + 26, en, col, 30)
        d.text((116, y + 84), cn, font=font(True, 50), fill=WHITE)
        d.text((116, y + 156), desc, font=font(False, 32), fill=MUTED)
        y += 256
    d.text((72, 1240), "为了让 Agent 自己发现错误、自己纠正，少来烦你。", font=font(False, 34), fill=WHITE)
    img.save(f"{OUT}/card3_concept.png")

# ---------------- card 4: arch ----------------
def card4():
    img, d = base(); header(d); footer(d, 4)
    d.text((72, 180), "三个机制", font=font(True, 60), fill=WHITE)
    d.text((72, 268), "agent-native filesystem 的一个实现", font=font(False, 34), fill=MUTED)
    cx, y = W // 2, 380
    panel_box(d, [cx - 360, y, cx + 360, y + 132], outline=BLUE)
    d.text((cx, y + 28), "Agent", font=font(True, 50), fill=WHITE, anchor="ma")
    d.text((cx, y + 88), "Claude Code · Copilot · Gemini", font=font(False, 30), fill=MUTED, anchor="ma")
    arrow_down(d, cx, y + 132, y + 182)
    yb, bh = y + 182, 470
    panel_box(d, [72, yb, W - 72, yb + bh], outline=AMBER)
    d.text((110, yb + 24), "YoloFS", font=font(True, 44), fill=AMBER)
    layers = [("Staging 暂存区", "先改副本，不动真文件", AMBER),
              ("Snapshots & Travel 快照穿梭", "随时回到过去", GREEN),
              ("Progressive Permission 渐进授权", "敏感操作才审批", BLUE)]
    ly = yb + 96
    for name, desc, col in layers:
        d.rounded_rectangle([110, ly, W - 110, ly + 108], radius=18, fill=(13, 18, 30))
        d.line([(110, ly), (118, ly + 108)], fill=col, width=6)
        d.text((140, ly + 16), name, font=font(True, 36), fill=WHITE)
        d.text((140, ly + 62), desc, font=font(False, 30), fill=MUTED)
        ly += 122
    arrow_down(d, cx, yb + bh, yb + bh + 50)
    y2 = yb + bh + 50
    panel_box(d, [cx - 360, y2, cx + 360, y2 + 110], outline=MUTED)
    d.text((cx, y2 + 30), "Ext4 · 磁盘", font=font(True, 44), fill=MUTED, anchor="ma")
    d.text((72, 1300), "约 2.7k 行 C 内核代码 + 8k 行 Rust CLI", font=font(False, 30), fill=DIM)
    img.save(f"{OUT}/card4_arch.png")

# ---------------- card 5: results ----------------
def card5():
    img, d = base(); header(d); footer(d, 5)
    d.text((72, 190), "效果如何", font=font(True, 66), fill=WHITE)
    d.text((72, 285), "新做的 benchmark，测两件事", font=font(False, 36), fill=MUTED)

    # Safety
    p1y, p1h = 390, 400
    panel_box(d, [72, p1y, W - 72, p1y + p1h])
    chip(d, 110, p1y + 30, "Safety", AMBER, 28)
    d.text((110, p1y + 92), "11 个藏了破坏性副作用的任务", font=font(True, 38), fill=WHITE)
    d.text((110, p1y + 160), "8 / 11", font=font(True, 88), fill=AMBER)
    d.text((110, p1y + 275), "Agent 自己发现并纠正（原来是 0）", font=font(False, 34), fill=MUTED)
    d.text((110, p1y + 325), "比如跑个 linter，顺手把源码删了", font=font(False, 30), fill=DIM)

    # Autonomy
    p2y, p2h = p1y + p1h + 30, 400
    panel_box(d, [72, p2y, W - 72, p2y + p2h])
    chip(d, 110, p2y + 30, "Autonomy", GREEN, 28)
    d.text((110, p2y + 92), "112 个日常任务", font=font(True, 38), fill=WHITE)
    d.text((110, p2y + 160), "99%", font=font(True, 88), fill=AMBER)
    d.text((110 + 300, p2y + 200), "成功率", font=font(False, 36), fill=WHITE)
    d.text((110, p2y + 275), "0.9 → 0.4", font=font(True, 60), fill=AMBER)
    d.text((110 + 330, p2y + 295), "每个任务找你确认的次数", font=font(False, 32), fill=MUTED)
    img.save(f"{OUT}/card5_results.png")

# ---------------- card 6: closing ----------------
def card6():
    img, d = base(); header(d); footer(d, 6)
    d.text((72, 330), "最后说一句", font=font(False, 38), fill=MUTED)
    d.text((72, 410), "让 Agent 放心大胆干，", font=font(True, 64), fill=WHITE)
    d.text((72, 500), "文件丢不了，不该看的看不到。", font=font(True, 64), fill=AMBER)
    d.line([(72, 690), (W - 72, 690)], fill=LINE, width=2)
    d.text((72, 730), "yolofs.github.io", font=font(False, 38), fill=WHITE)
    d.text((72, 790), "github.com/YoloFS/YoloFS", font=font(False, 38), fill=MUTED)
    img.save(f"{OUT}/card6_closing.png")

if __name__ == "__main__":
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6], 1):
        fn(); print(f"card{i} done")
