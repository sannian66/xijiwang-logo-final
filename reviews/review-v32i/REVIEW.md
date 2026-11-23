# v3.2 "Pause → Play → Nose": Independent Review

**Overall: 7.8 / 10. Verdict: ship (conditional). There are no P1s. I recommend the P2 fix before a hero placement.**

| Area | Score |
|---|---|
| Concept clarity | 7.5 |
| Craft | 7.5 |
| Timing & easing | 7.0 |
| Brand fidelity | 9.0 |
| Sound | 8.0 |
| Light/dark parity | 9.0 |

## v3.1 items: status
- **Ring pump: fixed.** The ring's on-screen diameter now only shrinks: 550 → 426 px across f108–f144 (`ring_diam` measured per frame).
- **Seam notches: fixed.** Corners are sharp before the halves touch, with no V-notch at f89–f100 (`zoom_seam_l.png`).
- **Safari morph: fixed in code.** The JS sets the `d` and `r` attributes, with no CSS `d:path()`. `seek` and live playback both morph in Chromium. I could not launch WebKit here (host libs missing), so Safari itself is unverified.
- **Ring/mane collision: fixed.** The ring is fully gone by about 2.46 s.
- **Sound fixes.** The thump onset is 2.380 s and the first fill frame is f143 (2.383 s). A tick at 0.20 s is added.
- **Face fragment (v3.1 #7): not fixed.** The code comment says it is solved; the frames show it is not.

## Verified clean
- **Final frame.** f449 against the source SVG: max diff 0 in light and dark.
- **Loudness.** WAV and both MP4s read −16.0 LUFS, −2.5 dBTP, LRA 5.
- **Encode.** bt709 / tv, 450 frames, A/V start 0.
- **Sync.** Audio onsets in the MP4 are 0.20, 1.41, 2.38 and 3.87 s.
- **Swaps.** No pops at 1.95, 2.35, 3.30, 5.02 or 5.60 s.
- **Parity.** Coverage difference between light and dark is ≤0.0015 (mean).

## P2
1. **Face fragment flashes at 2.38–2.43 s (f143–f145).** The eyebrows, the mouth and a smile-shaped crescent of mane float with no head. It is more noticeable now because it lands exactly on the thump (`zoom_bloom_l/d.png`).
   - Geometry, measured from the nose centre: mouth ≤37, eyes ≤60, face hole 40–84, mane outer 124.
   - Starting the clip at R0=20 guarantees the fragment.
   - Fix in `template32.html` `drive()`: set `R0 = 86` so the whole face hole is inside on the first frame, and keep `GD = 750`.
   - Add a short fade so the start isn't a hard disc: `.reveal{animation: fadeIn .1s linear 2.37s both}`.
   - Alternative: animate `scale(.45→1)` on `.reveal` about the nose instead of an iris.
2. **The bloom reads as a pop, not a reveal.** The expo curve takes r from 34 to 77 in 4 frames, so the lion is fully shown about 100 ms after it starts. Use `EXPO → cubic(.05,.7,.1,1)` (the M3 decelerate curve) with `GD = 900`.

## P3
3. **Residual dead air at 2.10–2.37 s.** A tiny ▶ sits low in a large, empty, off-centre ring: the ring centre rises 37 px while the ▶ stays on the nose.
   - Set `G0 = 2200`.
   - Move `.btn cut` and `.nose hold0` to `2.20s`.
   - Set `RINGOFF = 2.10`.
   - Set `T['thump'] = 2.21`.
4. **Luma excursions.** Dark YMIN is 0 and light YMAX is 255 throughout (crf 12 edge ringing), which is worse than v3.1. A broadcast QC check would flag it. Fix: append `,lutyuv=y='clip(val,16,235)'` after `format=yuv420p` in `enc32.sh`.
5. **The morph snaps.** It goes from 15% to 70% in 3 frames (1.50–1.55 s). It is acceptable, but a 0.6 s duration would let the hero beat breathe.

## Evidence (all in /workspace/work/anim/review-v32i/)
- `sheet_l.png`, `sheet_d.png`: every 0.25 s.
- `zoom_morph_l.png`: 1.30–2.60 s.
- `zoom_reveal_l.png`, `zoom_reveal_d.png`: 2.30–3.40 s.
- `zoom_bloom_l.png`, `zoom_bloom_d.png`: f141–f148, full resolution.
- `zoom_seam_l.png`.
- `zoom_word_l.png`, `zoom_word_d.png`: the wordmark.
- `src_*.png`, `diff_final_*.png`, `srccmp.py`: final frame against the source.
- `mp4last_*.png`: last frame decoded from each MP4.
- `wk.py`: the JS/Safari probe. WebKit would not launch in this sandbox.
