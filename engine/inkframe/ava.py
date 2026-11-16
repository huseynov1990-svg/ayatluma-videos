"""Ava - heroine of I WAS THERE. Local box 0..400 like Eli."""
INK = "#121214"
SKIN = "#e6c9b0"
HAIR = "#8a3b1e"
TEAL = "#2EC4B6"

def ava(x, y, s=1.0, mood="calm", look=0, coat="#2f4a3f", scarf=TEAL, pose="bust", hat=None):
    brow = {"calm": "M164 112 Q177 106 190 110 M210 110 Q223 106 236 112",
            "worried": "M162 106 Q176 114 190 112 M210 112 Q224 114 238 106",
            "scared": "M162 104 Q176 94 190 108 M210 108 Q224 94 238 104",
            "smile": "M164 108 Q177 100 190 106 M210 106 Q223 100 236 108",
            "determined": "M162 104 L190 112 M210 112 L238 104"}[mood]
    mouth = {"calm": f'<path d="M192 188 Q203 192 214 188" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
             "worried": f'<path d="M190 192 Q203 182 216 192" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
             "scared": f'<ellipse cx="203" cy="190" rx="9" ry="11" fill="{INK}"/>',
             "smile": f'<path d="M186 184 Q203 202 220 184" fill="#7a2a2a" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
             "determined": f'<path d="M190 188 L216 186" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'}[mood]
    e = look
    hat_svg = ""
    if hat == "1912":
        hat_svg = f'''<ellipse cx="200" cy="74" rx="118" ry="26" fill="#3a2b2b" stroke="{INK}" stroke-width="7"/>
  <path d="M138 74 Q140 20 200 18 Q260 20 262 74 Z" fill="#3a2b2b" stroke="{INK}" stroke-width="7"/>
  <path d="M146 62 Q200 52 254 62" fill="none" stroke="{TEAL}" stroke-width="9"/>'''
    elif hat == "helmet":
        hat_svg = f'''<path d="M120 100 Q124 26 200 22 Q276 26 280 100 Z" fill="#e8b400" stroke="{INK}" stroke-width="7"/>
  <rect x="108" y="92" width="184" height="18" rx="9" fill="#e8b400" stroke="{INK}" stroke-width="6"/>
  <circle cx="200" cy="58" r="18" fill="#fff6c8" stroke="{INK}" stroke-width="5"/>'''
    torso = f'''<path d="M108 250 Q200 224 292 250 Q326 322 318 440 L82 440 Q74 322 108 250 Z" fill="{coat}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  <path d="M200 262 L200 440" stroke="{INK}" stroke-width="4" opacity="0.5"/>
  <circle cx="186" cy="320" r="7" fill="{INK}" opacity="0.6"/><circle cx="186" cy="370" r="7" fill="{INK}" opacity="0.6"/>
  <path d="M140 236 Q200 270 260 236 L262 262 Q200 296 138 262 Z" fill="{scarf}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
  <path d="M236 262 L250 330 L222 326 Z" fill="{scarf}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'''
    head = f'''
  <path d="M126 150 Q112 52 200 42 Q290 52 276 150 Q270 110 240 92 Q200 80 160 92 Q132 110 126 150 Z" fill="{HAIR}" stroke="{INK}" stroke-width="7"/>
  <path d="M262 150 Q300 220 276 300 Q262 330 250 300 Q268 230 246 170 Z" fill="{HAIR}" stroke="{INK}" stroke-width="6"/>
  <path d="M262 236 L282 244 M258 262 L280 270 M256 288 L272 294" stroke="{INK}" stroke-width="4"/>
  <ellipse cx="200" cy="150" rx="66" ry="78" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>
  <path d="M136 132 Q150 70 210 74 Q258 80 266 128 Q236 98 200 102 Q166 104 136 132 Z" fill="{HAIR}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
  <path d="{brow}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="{177+e}" cy="144" rx="8" ry="11" fill="{INK}"/><ellipse cx="{225+e}" cy="144" rx="8" ry="11" fill="{INK}"/>
  <circle cx="{180+e}" cy="140" r="3" fill="#fff"/><circle cx="{228+e}" cy="140" r="3" fill="#fff"/>
  <path d="M{202+e/2} 150 Q{197+e/2} 164 {206+e/2} 166" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
  <g fill="#b5714f" opacity="0.7"><circle cx="164" cy="168" r="2.5"/><circle cx="172" cy="174" r="2.5"/><circle cx="158" cy="176" r="2.5"/>
  <circle cx="236" cy="168" r="2.5"/><circle cx="244" cy="174" r="2.5"/><circle cx="230" cy="176" r="2.5"/></g>
  {mouth}{hat_svg}'''
    return f'<g transform="translate({x} {y}) scale({s})">{torso}{head}</g>'
