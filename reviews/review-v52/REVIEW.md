# v5.2 review: 西几王传媒 lion logo animation

**Overall: 6.8 / 10** (v5.1 scored 6.2)
Concept clarity 7.5 · Craft 6.5 · Timing & easing 6.5 · Brand fidelity 7.5 · Interaction states 6.5 · Sound 6.5

**Verdict:** Clear progress and the story now reads (XJW → face → ▶ → lion → lockup). It is not ready to ship yet: the mane reveal, the hero beat, has turned from a "radar sweep" into a 4-frame black-disc pop. One P1 and four P2s are still open.

## Prior P1s
1. **Icon never seen complete:** FIXED. The finished icon holds at 1.3× from 2.28 to 2.95s (0.67s).
2. **Mane looked like a radar sweep:** FIXED, but it introduced a new P1 (below).
3. **X collides with J and goes lumpy:** PARTIAL. The glyphs stay clean, but X still passes across J (reading as "ĵ") and then over W's left arm from 1.43 to 1.63s (f86–f98).
4. **▶ flashes grey on toggle back to play:** FIXED. ▶ luminance falls steadily from 70 to 0 over about 30 frames at 8.7s and 12.7s, with no lighter frame.

## P1
**Mane "coin" pop, 2.22–2.28s (f133–f137).** With `--emph` over r 56→150, nearly all the growth lands in about 80ms. The only in-between frames show a hard-edged black disc with the face cut out of it, so it reads as a porthole flashing on rather than a mane growing out.
Fix in template52.html:
- `#revealC { animation: reveal .75s cubic-bezier(.3,0,.1,1) 2.2s both; }`
- `@keyframes reveal { from { r: 78px } … }`. This starts the reveal outside the face plate, so mane tips appear first.
- Swap `clipPath#revealClip` for a `<mask>` with a radialGradient whose edge fades from stop .88 to 1.0 (about 14 user units).
- In `@keyframes maneIn`, change `scale(.94)` to `scale(.97)`.

## P2
1. **X still crosses J and then W, 1.43–1.63s.** In `CFG.x`, change `arc: -40` to `arc: -72` and `rot: -10` to `rot: 0`, so the X passes above J's cap height. Then check f86–f98 for zero ink overlap.
2. **The biggest sound accent lands on a static frame.** The pad and bells (about −12 dBFS RMS) hit at 2.70/2.75s, nearly 0.5s after the mane lands and before the slide starts. In sfx52.py, change `add(pad,2.7,…)` to `2.24` and the bell loop `2.75` to `2.26`. If you keep the P1 fix (0.75s reveal), use 2.6 and 2.62 instead. Keep the mane noise at 2.17 and set `d=.75`.
3. **The cursor clicks the lower-right cheek, about 145px from the ▶ button.** The demo teaches the wrong target. Change the cursor wrapper `translate(176 166)` to `translate(116 116)`, so the tip sits on the ▶'s lower-right corner without covering the glyph.
4. **Loudness mismatch between the two files.** Intro measures −16.1 LUFS with a −4.5 dBTP peak. Demo measures −17.1 LUFS with a −1.6 dBTP peak, driven by click transients. In `click()`, change `.8*g` to `.6*g`, then master both files with `loudnorm=I=-16:TP=-1.5:LRA=7` (two-pass).

## P3
1. **▶ fades in semi-grey at 1.72–1.82s.** This is the same grey-flicker class as the old P1. In `playIntro`, set `g.style.opacity = 1` and change `lerp(.4,1,b)` to `lerp(.6,1,b)`.
2. **Pause greys the whole emblem and moves the wordmark.** The emblem drops to about 85% ink and `.title` shifts −3px to 75% opacity, so the brand mark is no longer pure black and the wordmark reacts to an icon control. Remove `opacity` from `.lockup`, remove the `--pt` transform and opacity from `.title`, and change `.maneState` `* .05` to `* .03`.
3. **The ripple is a perfect r=98 circle around an organic mane** and reads as a UI focus ring. In the `#ripple` keyframes, change opacity `.22` to `.12`, or drop it.
4. **W bulges mid-morph at about 1.6s.** Change `CFG.w.md` from `.72` to `.6` to shorten the ugly middle.
5. **The 中文 wipe's hard vertical clip edges at 3.4–3.6s look mechanical.** Change the wipe duration from `.55s` to `.45s` and the stagger from `.065s` to `.05s`.

## Checks
- **Specs:** 2560×1440 at 60fps, AAC 48k stereo. Intro is 5.0s and demo 14.2s.
- **Sound sync:** event onsets at 0.10 / 1.72 / 2.06 / 2.20 / 2.74, plus 6.48 / 8.68 / 10.68 / 12.68. These line up with the visuals except the 2.74 accent (P2-2).

Evidence files in this folder: `sheet-intro-s.png`, `z-morph.png`, `z-xj.png`, `z-mane.png`, `z-mane-ff.png`, `z-slide.png`, `z-toggles.png`, `emb380.png`.
