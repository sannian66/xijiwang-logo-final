# v3.1 "Pause → Play → Nose": Independent Review

**Overall: 7.0 / 10. Verdict: no-ship as it stands. Two P1 fixes, both small, take it to about 7.8 and make it shippable.**

| Area | Score |
|---|---|
| Concept clarity | 7.0 |
| Craft | 6.5 |
| Timing & easing | 6.0 |
| Brand fidelity | 8.5 |
| Sound | 7.5 |
| Light/dark parity | 8.5 |

## What's verified clean
- **Final frame matches the source.** Frame f449 against the source SVG, rendered in Chromium at the same placement: max diff 0 in both light and dark.
- **Encode.** bt709 tagged, tv range, white at Y=235.
- **Loudness.** WAV and both MP4s measure −16.0 LUFS and −2.4 dBTP.
- **Sync.** The click onset is at 1.405 s; the press bottom is at 1.408 s.
- **Swaps.** No pops at 1.95, 2.50, 3.30, 5.02 or 5.60 s.
- **Hold.** Motion ends at 5.60 s, leaving a 1.9 s hold.
- **Parity.** Light and dark timing is identical.
- **Every v3 P1 is fixed.**

## P1
1. **The ring pumps at 1.93–2.80 s, which reads as a bounce.** `ringGrow` (1.6× over 0.7 s) fights `cam` (2.8→1 over 1.6 s). The ring's on-screen diameter goes 549 → **660** (2.07 s) → 363 px, so it swells and then collapses, which breaks the no-bounce rule.
   - Fix in `template31.html`: `.ringwrap{animation: ringGrow 1.6s var(--emph) 1.9s forwards}`.
   - With the same curve and duration, the net scale (2.8−1.8p)(1+0.6p) only ever decreases.
2. **Seam notches show in the morph at hero scale (f91–f117, 1.52–1.95 s).** The rounded seam corners leave V-notches and small steps on the top and bottom edges where the halves meet. See `zoom_seam_l.png`. This is the largest the shape ever appears on screen, so it is visible.
   - Fix in `morph31.py` `shapes()`:
     - `r=2.5*max(0,1-q/0.5)`, so the corners go sharp before the halves touch.
     - Overlap the halves with `xL=L(-3.5,0.95,q); xR=L(3.5,-0.95,q)`.

## P2
3. **Dead air at 2.0–2.55 s.** The ▶ shrinks about 5× inside an empty ring before any lion appears, so the "▶ is the nose" beat goes limp. Pull the reveal 150 ms earlier:
   - `btnShrink .45s`
   - move `.btn cut`, `.nose hold0` and `.reveal` to **2.35s**
   - `#growC … 2.37s`
   - `sfx31.py T['thump']=2.37`, and move `swell` to 1.75 so it stays about 0.6 s long.
4. **Ring and mane collide at 2.85–3.10 s.** The mane spikes poke through the 1.6× ring while it fades out slowly (`off` at 2.92 s). Fix: `off .22s var(--soft) 2.62s forwards`, so the ring dissolves into the bloom before the spikes reach it. Alternatively, scale it to the mane's circumradius (~1.72).
5. **The HTML deliverable may not morph in Safari.** The morph uses CSS `d: path()`, which WebKit doesn't support as far as I know (not checked in Safari). If so, Safari viewers see the bars hold and then hard-cut to ▶ at 1.95 s. Fix: drive `d` from the same baked keyframes with SMIL `<animate attributeName="d" keyTimes=… values=…>`, or with JS in `seek`.

## P3
6. **Thump arrives early.** It hits at 2.52 s, but the first visible bloom pixels appear at about 2.60 s (5 frames later). Fix: `T['thump']=2.57`, or apply fix 3.
7. **A face fragment flashes at 2.60–2.68 s.** The clip opens from the nose, so a crescent grin and eyes show before the mane, which looks a little creepy in dark mode. Fix: `@keyframes grow{from{r:20px}}`, with the clip starting just past the nose.
8. **Silent cold open.** There is no audio for 0–1.4 s while the ring draws and the cursor arrives. Optional: a −18 dB soft tick or air at 0.2 s in `sfx31.py`.
9. **The dark encode undershoots to YMIN 9** (edge ringing at crf 12). Cosmetic. Optional: append `lutyuv=y='clip(val,16,235)'`.

## Evidence (this folder)
- `sheet_l.png`, `sheet_d.png`: every 0.25 s.
- `zoom_morph_l.png`: 1.30–2.67 s.
- `zoom_reveal_l.png`, `zoom_reveal_d.png`: 2.50–3.55 s.
- `zoom_seam_l.png`: f88–f118, full resolution.
- `zoom_word_l.png`, `zoom_word_d.png`: the wordmark.
- `src_l.png`, `src_d.png`, `diff_final_*.png`, `srccmp.py`: final frame against the source.
- `mp4last_*.png`: last frame decoded from the MP4.
