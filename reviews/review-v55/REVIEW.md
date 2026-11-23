# v5.5 review: 西几王传媒 lion logo animation (round 5)

**Overall: 8.4 / 10** (v5.1 6.2 → v5.2 6.8 → v5.3 7.4 → v5.4 8.0)
Concept clarity 8.5 · Craft 8 · Timing & easing 8.5 · Brand fidelity 8.5 · Interaction states 8 · Sound 8

**Verdict: not ship as the final master yet. Ship it once the P2 below is fixed; that is a two-line CSS change, and no further review round is needed.** There is no P1.

## v5.4 items
- **Lumpy morph contours: FIXED.** The J and W edges are clean through f84–f110 (z-morph.png, z-jw.png). One note: build55 samples at N=360 but still writes M2=260 points per shape. That is harmless.
- **X over J: FIXED.** At 1.47–1.57s the X clearly reads as in flight, not as a diacritic.
- **J–W kiss: FIXED to a near-miss.** The shapes no longer merge. The closest gap is 2.2px at f99 (z-jw-touch.png), which is invisible in motion.
- **Dead code and the rise rename: FIXED.**
- **Cursor idle: MOSTLY FIXED.** The cursor now fades out after taps 1–3 and back in before the next one (z-cursor1.png).
- **Mane shards: PARTIAL.** The opacity ramp only turns the shards grey. At f133–f137 (2.22–2.28s) separate wedge-shaped fragments still show, along with a hairline chevron under the chin at f136. It still briefly reads like a jack-o'-lantern (z-mane-early.png). Opacity reaches 56–69% exactly while the ring is still broken. The ring only joins up at scale ≈0.81 (f138).
- **Lockup, 中文 and English:** clean (z-lockup.png). Toggle morphs are clean (z-toggles*.png).
- **Audio:** unchanged from v5.4, and the hits stay in sync (onsets at 1.72, 2.06, 2.2, 2.6, then 6.49, 8.69, 10.69, 12.69s). Measured: intro −16.1 LUFS / −4.6 dBTP, demo −16.0 LUFS / −1.8 dBTP. Specs: 2560×1440, 60fps, AAC 48k, 5.4s and 14.2s.

## P1
None.

## P2
1. **Mane fragments at 2.22–2.28s.** Hold the mane invisible until the ring has joined up. Keep the scale move, which is the only property that the `from`/`to` frames animate, and add opacity-only stops:
   `@keyframes maneIn { from{transform:scale(.68);opacity:0} 16%{opacity:0} 32%{opacity:1} to{transform:none;opacity:1} }`

## P3
1. **Cursor parks after the last tap, 12.7–13.4s.** It covers ▶ and the J, then exits through the W at 13.4–13.9s (z-cursor2.png, f770–f830). Fix: drop the `i < T.length-1` guard so the last tap fades out at t+260 too, and delete the 13.4s exit animation. This gives a clean end card for about 0.85s.
2. **The nudge (10,14) passes over the J while the cursor fades** (f404–f416). Use `translate(-6px,22px)`.
3. **The mane rumble at 2.2s fires on a frame that is almost invisible.** Once P2 is in, move it to about 2.27s.

## Evidence (this folder)
sheet-intro.png, sheet-demo.png, z-morph.png, z-jw.png, z-jw-touch.png, z-mane.png, z-mane-early.png, z-lockup.png, z-cursor1.png, z-cursor2.png, z-toggles.png, z-toggles2.png, sheet.py, mk.py, mk2.py
