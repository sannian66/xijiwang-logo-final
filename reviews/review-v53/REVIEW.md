# v5.3 review: 西几王传媒 lion logo animation (round 3)

**Overall: 7.4 / 10** (v5.1 6.2 → v5.2 6.8)
Concept clarity 8 · Craft 7 · Timing & easing 7 · Brand fidelity 8.5 · Interaction states 7.5 · Sound 7.5

**Verdict: not ship yet, but close.** Most prior items are fixed. The mane is still only half-fixed: it no longer pops as a hard disc, but it reads as a soft iris, and 70% of its 0.75s runs after it is already finished.

## Prior items
- **P1 mane pop: PARTIAL.** The edge is now soft, but f133–f140 still read as a filled disc. Measured: the mane reaches about 105u, the mask ends at r 165, and the curve front-loads the growth. So the visible reveal is f133–f144 (0.2s), followed by about 0.55s where nothing changes.
- **X over J/W: FIXED.** There is no ink overlap in f84–f102. The J–W gap is tight (about 3px) at f98.
- **Chord timing: PARTIAL.** The mane finishes at 2.40s. The audio dips to −21.9 dB RMS (2.40–2.55), and the loudest window, −13.6 dB (2.55–3.0), still lands on a static frame.
- **Cursor target: FIXED.** The tip sits on the ▶ base (z-cursor.png).
- **Loudness: FIXED.** Both mp4s measure −16.0 LUFS, with peaks of −4.2 and −1.7 dBTP.
- **P3s:** ▶ is opaque, pause greying is removed, and W md is .6 (all FIXED). The ripple is fainter but still visible. The 中文 wipe is still clipped.

## P1
**Mane reads as an iris, 2.20–2.40s.** Fix in template53.html:
- In `#revealC` and `.maneIn`, use `animation: … .6s cubic-bezier(.2,0,0,1) 2.2s both`.
- `@keyframes reveal { from { r: 64px } to { r: 135px } }`. With the feather below, the solid edge then sweeps from about 51u to 108u, so the full time is spent on visible growth and the end state is fully opaque.
- `#rg` stops `.93`→`.80` and `1`→`1`, a feather of about 22u, so the tufts emerge instead of sitting behind a disc edge.
- `maneIn` `scale(.97)` → `scale(.92)`, so the tufts push outward.

The visible growth then ends at about 2.75s, so the 2.55/2.60 chord lands inside it.

## P2
1. **Cursor covers the right ❚❚ bar and the J in the pause state** (6.5–8.7, 10.7–12.7s; z-tog-detail.png f396–f401). In the script, after each `tap`, add `$('cursor').animate([{transform:'none'},{transform:'translate(12px,10px)'}],{delay:t+180,duration:320,easing:E,fill:'forwards'})`. Return it with the mirror animation at `t-420`.
2. **Sound accent.** If P1 is not done, change `add(pad,2.55,…)` to `2.36` and the bells from `2.6` to `2.40`. With P1 done, keep 2.55/2.6 and change the mane noise to `d=.6`.
3. **中文 wipe shows sliced glyphs, 3.55–3.75s** (f213–f226: "西厂王伕"). Replace the clip `wipe` with per-character `opacity 0→1; translateY(6px)→0` over `.4s var(--emph)`, keeping the `.05s` stagger.

## P3
1. **X dots the J ("ĵ"), 1.40–1.60s.** In `CFG.x`, change `arc:-60` to `-48` and `ms:1.20` to `1.26`, so the X travels over the J–W gap.
2. **▶ cuts on at 60% size between f103 and f104.** Add a 2-frame fade: `g.style.opacity = Math.min(1, cl((t-PT)/.033))`.
3. **Ripple ring** (f390–f400) is still a geometric circle around an organic mane. Delete `$('ripple').animate(…)`.

## Checks
- **Specs:** 2560×1440, 60fps, AAC 48k stereo. Intro 5.4s, demo 14.2s.
- **Onsets:** 0.10 / 1.72 / 2.06 / 2.20 / 2.60, then 6.49 / 8.69 / 10.69 / 12.69. Tap scale bottoms out on each click.
- **Lockup:** centred (bbox 696–1867 px). Final frame is clean.
- **Toggle morph:** ▶↔❚❚ split morph is clean over about 7 frames, with no grey flash.

## Evidence (this folder)
sheet-intro.png, z-morph.png, z-jw.png, z-mane.png, z-slide.png, z-final.png, sheet-demo.png, z-toggles.png, z-tog-detail.png, z-cursor.png, sheet.py
