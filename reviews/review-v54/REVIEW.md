# v5.4 review: 西几王传媒 lion logo animation (round 4)

**Overall: 8.0 / 10** (v5.1 6.2 → v5.2 6.8 → v5.3 7.4)
Concept clarity 8.5 · Craft 7.5 · Timing & easing 8 · Brand fidelity 8.5 · Interaction states 7.5 · Sound 8

**Verdict: not ship as the final master yet. It is fine to send as a client preview.** There is no P1 left. Two P2s are visible on a 2K screen, and both are about an hour of work.

## Prior items
- **Mane iris: FIXED.** The mane now reads as growing out from behind the face. Ink coverage is 50% at f140, 90% at f152 and settles at f166, so the growth runs the full 0.4s instead of the old 0.2s (z-mane.png).
- **中文 wipe: FIXED.** The fade+rise is clean, with no sliced glyphs at f212–f230 (z-zh.png).
- **Cursor covers ❚❚: PARTIAL.** The nudge works, but it moves the cursor onto the J and W, the nose and mouth (z-cursor.png, f400–f500).
- **Ripple: FIXED** (removed).
- **▶ pop: FIXED.** f104 shows ▶ at about 40% opacity.
- **X dots the J: PARTIAL.** At f90–f94 (1.50–1.57s) the X still sits directly above the J stem (z-jw.png).
- **Audio:** noise hits 2.2–2.3s on the growth, and the chord at 2.6s lands on the settle (94% coverage). Measured: intro −16.1 LUFS / −4.6 dBTP, demo −16.0 LUFS / −1.8 dBTP. Specs: 2560×1440, 60fps, AAC 48k stereo, 5.4s and 14.2s.

## P1
None.

## P2
1. **Cursor parks on the nose and mouth, 6.68–8.3s and 10.88–12.3s.** Replace the static park with an idle-hide, the macOS pattern. In the `T.forEach` block, add `$('cursor').animate([{opacity:1},{opacity:0}],{delay:t+700,duration:300,fill:'forwards'})`, and before each next tap add `[{opacity:0},{opacity:1}]` at `t-500`. Keep the nudge but change it to `translate(-6px,22px)`, so it never crosses `#f_j`. Add a build-time assert that the cursor bbox does not intersect `#f_j` or `#f_w`.
2. **Mane enters as detached shards, 2.217–2.283s (f133–f137).** Slivers with hard cut edges and a brow-like chevron appear, and it briefly reads like a jack-o'-lantern (z-mane-early.png). Fix: `@keyframes maneIn { from{transform:scale(.68);opacity:0} 20%{opacity:1} to{transform:none;opacity:1} }`, and drop the visibility hack.
3. **Lumpy contours mid-morph, 1.55–1.68s.** The W and J edges wobble (z-wlumps.png, f95), which comes from the uneven DTW correspondence on 220-point polylines. In the morph frame fn, after interpolating, run 2 passes of `q[i]=.25q[i-1]+.5q[i]+.25q[i+1]` with weight `Math.sin(Math.PI*p)`, so the endpoints stay exact. You can also raise `N=220→360` in build52.py.

## P3
1. **X over J at 1.50–1.57s.** Use `arc:-75`, so the vertical gap reads as flight rather than a diacritic.
2. **J–W kiss of about 1–2px at f98–f99.** This is unchanged from v5.3. Offset the W path start by +2u x.
3. **Dead code.** `#revealC`, `#rg`, `#revealMask` and `@keyframes reveal` still animate but nothing uses them. Delete them, and rename `wipe` to `rise`.

## Evidence (this folder)
sheet-intro.png, sheet-demo.png, z-morph.png, z-jw.png, z-jw-touch.png, z-jw-v53vs54.png, z-mane.png, z-mane-early.png, z-lockup.png, z-zh.png, z-toggles.png, z-cursor.png, z-wlumps.png, sheet.py
