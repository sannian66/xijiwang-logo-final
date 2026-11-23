# v3 "Pause → Play → Nose" — Review

**Overall: 5.2 / 10. Verdict: not ready to deliver. The concept is sound, but there are six P1 defects.**

| Area | Score |
|---|---|
| Concept clarity | 6.5 |
| Craft | 4.5 |
| Timing & easing | 6.0 |
| Brand fidelity | 5.0 |
| Sound | 4.5 |
| Light/dark parity | 6.0 |

The final frame matches the source SVG geometrically (diff shows only anti-aliasing). The source nose really is a ▶, so the idea holds up. Execution is the weak part.

## P1 (must fix)
1. **The button intro never plays (0.0–0.9s).** On `.btn`, `fadeOut … both` back-fills `opacity:1` and `btnShrink … both` back-fills `scale(1.9)`, so `btnIn` gets overridden. Frame 0 already shows the full-size bars. Fix: `btnShrink .75s var(--emph) 1.9s forwards, fadeOut .18s linear 2.6s forwards`.
2. **A ghost ripple disc shows before the click (0–1.36s).** `.ripple … both` back-fills `opacity:.14`, leaving a grey blob between the bars (Y 215 on a 245 background in light mode, 34 in dark). Fix: change the fill to `forwards`.
3. **The play→nose hand-off is a cross-dissolve, not a hand-off (2.60–2.78s).** At the swap the stroked play triangle is 45×42 px, while the nose is 37×37 px, has rounded corners and sits about 2 px to the left. Both fade at once, so the ink dips to Y≈82 at f162 and the frame visibly flickers. Fix: in `build.py`, emit `{{NOSE}}` mapped into the button's local coordinates (`x' = (20+.9x−138.35)/0.9`, `y' = (14+.9y−146.3)/0.9`), split it into two halves as the `to` paths of `morphL`/`morphR`, and set `.bar{stroke-width:0}`. Then swap with no fade: `.btn` gets `fadeOut 1ms step-end 2.65s forwards` and `.nose` gets `fadeIn 1ms step-start 2.65s both`.
4. **The zh shine shows the glyphs before the wordmark arrives (3.5–4.3s, dark mode).** `style="animation-delay:3.5s"` sweeps white through `#zhShape` while the glyphs are still hidden, so you see slices of 西/几/媒 (zoom_word_d.png). Fix: delete both `.shine` rects. Gloss sweeps are dated and off-brief.
5. **Loudness: −13.8 LUFS, true peak −0.1 dBTP** (spec: −16 LUFS, ≤ −1.5 dBTP). In `sfx3.py`, replace `st*=0.89/np.abs(st).max()` with LUFS normalisation (pyloudnorm) to −16, or mux through `loudnorm=I=-16:TP=-1.5:LRA=7` (two-pass).
6. **Colour and encoding.**
   - The background is `--bg:#f5f5f7`, not pure white like the other finals. Use `#fff`.
   - The ink is `--ink:#1d1f1e`, but the source fill is `#202624`. Use the source value.
   - The MP4s are limited-range with untagged colour, and white decodes to 244. Encode with `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`, then check that #fff decodes to 255.

## P2
- **Staging is weak.** The opening hero is tiny: the bars are 83×92 px and the ring about 197 px across a 2560 px frame. Proposal: wrap `.lockup` in `<g class="cam">` and run `@keyframes cam{from{transform:scale(2.8)}to{transform:none}}` for 1.7s with `var(--emph)` from 1.9s, origin `138.35px 146.3px`. The button then opens at hero size and the camera pulls back as the lion forms. Shorten `center` to 1.0s.
- **Competing shapes (2.0–2.8s).** `ringOut` (circle → 1.65×) fades while `.outline` draws the mane separately. Drop the outline draw. Let the ring grow to the mane radius (`scale(1.62)`), then reveal the fill from the nose with a clip circle: `<clipPath id="grow"><circle cx="131.5" cy="147" r="0"/></clipPath>`, `@keyframes grow{to{r:125px}}` over .7s with `var(--emph)`.
- **Muddy grey lion (2.85–3.4s).** `.mane fadeIn` produces a translucent grey lion under the hairlines. The clip reveal above fixes this.
- **The cursor covers the morph (1.45–1.9s).** The tip sits on the right bar. Change `translate(4 6)` to `translate(24 28)` and set `cursorOut .35s var(--soft) 1.42s forwards`.
- **Holds.** The shine and the blink (6.0s) keep it moving until about 6.5s, leaving roughly 1.0s of clean hold. Remove the `.eyes` blink, a character gimmick that's off-brief, to get a hold of at least 1.5s.
- **SFX are over-scored (Mickey-Mousing).** There are about 40 cue layers in 7.5s. In `sfx3.py`, delete the eye plucks, zh ticks and en sparkles. Keep click → glide → swell → thump → resolve.

## P3
- The click sound at 1.33s comes about 8 frames before the visual press bottom (`press` hits 40% at 1.46s). Move `add(clk,1.40…)` or set `.press` delay to 1.25s.
- Mid-morph (around 1.55s) `barR` collapses to a degenerate quad and gives a brief bowtie. Fix 3 resolves it.
- In dark mode, YMIN is 8, below legal black. Clamp in the encode.
- The light and dark files are otherwise identical, timing included.

**Evidence** (all in `/workspace/work/anim/review-v3/`):
- `sheet_l.png`, `sheet_d.png`: contact sheets.
- `zoom_btn_l.png`: frames 0–222, every 6th.
- `zoom_word_d.png`: the ghost glyphs.
- `f0000_zoom.png`: frame 0.
- `src_on_bg.png` + `diff_final.png`: final frame against the source SVG.
