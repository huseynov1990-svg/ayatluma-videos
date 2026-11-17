from kit import *
def big_phone(cx, cy, screen, rot=-4, ring=False, s=1.0):
    rings = ""
    if ring:
        rings = "".join(f'<path d="M{-60-i*40} {120+i*10} Q{-90-i*45} 400 {-60-i*40} {680-i*10}" fill="none" stroke="{ACC}" stroke-width="8" opacity="{0.7-i*0.2}" stroke-linecap="round"/>'
                        f'<path d="M{480+i*40} {120+i*10} Q{510+i*45} 400 {480+i*40} {680-i*10}" fill="none" stroke="{ACC}" stroke-width="8" opacity="{0.7-i*0.2}" stroke-linecap="round"/>' for i in range(3))
    return f'''<g transform="translate({cx} {cy}) rotate({rot}) scale({s}) translate(-210 -400)">
  <ellipse cx="210" cy="400" rx="420" ry="520" fill="url(#ylamp)"/>{rings}
  <rect x="0" y="0" width="420" height="800" rx="56" fill="#0b0b0d" stroke="{INK}" stroke-width="12"/>
  <rect x="22" y="22" width="376" height="756" rx="40" fill="#15161b"/>
  <rect x="160" y="40" width="100" height="22" rx="11" fill="#0b0b0d"/>
  {screen}</g>'''

def screen_call(name, sub, timer=None):
    t = text(210, 600, timer, 34, 500, "#cfd3da", "middle") if timer else ""
    return f'''<circle cx="210" cy="250" r="86" fill="#2a2c33" stroke="#3a3c44" stroke-width="4"/>
  <path d="M170 280 Q210 190 250 280 M185 240 A25 25 0 1 1 235 240 A25 25 0 1 1 185 240" fill="#6b7079"/>
  {text(210, 400, name, 46, 800, "#f4f1ea", "middle")}
  {text(210, 450, sub, 28, 500, "#9aa0a8", "middle")}{t}'''

def screen_msg(lines, big=None):
    y = 300; out = ""
    for ln in lines:
        out += text(70, y, ln, 30, 500, "#e8e6e0"); y += 42
    bubble = f'<rect x="46" y="250" width="330" height="{len(lines)*42+40}" rx="22" fill="#2a2c33"/>'
    b = text(210, 560, big, 88, 900, ACC, "middle", 10) if big else ""
    return f'''{text(210, 140, "Unknown", 34, 800, "#f4f1ea", "middle")}{text(210, 180, "Text message · 1:13 AM", 22, 500, "#8a9098", "middle")}{bubble}{out}{b}'''

