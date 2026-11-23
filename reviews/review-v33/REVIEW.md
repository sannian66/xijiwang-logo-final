# v3.3 "Pause → Play → Nose": Independent Review

**Overall: 8.1 / 10 (v3.2 was 7.8). Verdict: ship. There are no P1s.**

The face-fragment bug is gone. The dead air is closed. The final frame matches the source exactly, and loudness is on spec. That still leaves v3.3 0.1 short of the 8.2 target, for two reasons:
- The hero beat is now a 100 ms opacity dissolve rather than a reveal (P2).
- The morph still snaps, because its length changed but its curve did not.

Fixing P2 plus P3-1 should clear 8.2.

| Area | v3.2 | v3.3 |
|---|---|---|
| Concept clarity | 7.5 | 7.5 |
| Craft | 7.5 | 8.4 |
| Timing & easing | 7.0 | 7.6 |
| Brand fidelity | 9.0 | 9.0 |
| Sound | 8.0 | 8.0 |
| Light/dark parity | 9.0 | 9.0 |

## v3.2 items: status

- **P2-1 face fragment: fixed.** I checked every frame from f126 to f155 in light and dark (`zoom_reveal_l.png`, `zoom_reveal_d.png`).
  - The first ink frame is f133 (2.217 s). It already contains the whole face hole plus a ring of mane.
  - There are no floating eyebrows, mouth or crescent in any frame.
  - `R0 = 86` is larger than the face-hole radius of 84, which is why this works.
- **P2-2 "pop": partly fixed, and it has turned into a new problem (see P2).** The curve and the 900 ms duration are in place, but the iris now happens almost entirely inside the 0.1 s fade (`curves.txt`).
  - At f138 (2.300 s), opacity reaches 1.0 and the radius has already covered 65% of its travel (86 → 113 of 128).
  - What the eye reads is a grey-to-black lion dissolving in over 6 frames. The last 35% of the radius, from 2.30 to 3.1 s, is mane-tip growth that is barely visible while the camera is pulling back.
  - It no longer pops, but it no longer reads as the lion growing out of the ▶ either.
- **P3 dead air at 2.10–2.37 s: fixed.**
  - The morph is visually done at about 2.00 s.
  - The ring fades over 2.00–2.22 s (`RINGOFF = 2.00` in the delivered HTML).
  - The button cuts to the nose at 2.20 s and the lion appears at f133 (2.217 s).
  - What remains is about 0.15 s of a small ▶ in a fading ring, which works as a breath.
- **The ring is concentric with the ▶ (bbox).** At f120 the ring centre is (1284.5, 749.5) and the ▶ bbox centre is (1279.5, 750.0).
  - Optically it is still slightly off; see P3-5.
- **P3 luma excursions: not fixed. The new `lutyuv` clip is a no-op.**
  - It clips before x264, and the overshoot is created by the encoder's quantisation ringing on hard edges.
  - The decoded MP4s are statistically identical to v3.2 (`r103.py`):

| file | outside 16–235, max/frame | mean | outside 5–246 (R103 tolerance) |
|---|---|---|---|
| v3.3 light | 0.210% | 0.128% | max 0.0002% |
| v3.3 dark | 0.171% | 0.098% | max 0.0005% |
| v3.2 light | 0.210% | 0.127% | max 0.0002% |
| v3.2 dark | 0.167% | 0.098% | max 0.0006% |

  - signalstats gives YMIN 0 (dark) and YMAX 255 (light).
  - Nearly every frame has some excursion: 449 of 450 frames in each file (`luma_light.txt`, `luma_dark.txt`).
  - The handoff's "≤0.21%" is accurate, but the cause it gives ("fixed in encode") is not.
- **P3 morph rhythm: not really changed.** `MD = 600` is in place, but the curve is still emphasized `cubic(.2,0,0,1)`.
  - Peak speed is 4.05× linear, right at the start.
  - Progress goes 10% at 1.500 s → 50% at 1.570 s → 90% at 1.773 s, so 10→90% takes 273 ms. The extra 100 ms all went into the settle tail, which is why it feels the same.

## Verified clean

- **Spec.**
  - Video: 2560×1440, 60/1 fps, 450 frames, 7.500 s, h264 yuv420p.
  - Colour metadata: bt709 primaries, transfer and matrix, tv range.
  - Audio: AAC 48 kHz stereo, start 0.000.
  - The WAV is 24-bit / 48 kHz, 7.500 s.
- **Loudness** (ffmpeg `ebur128=peak=true`).
  - The WAV and both MP4s read −16.0 LUFS, LRA 4.6, True Peak −2.3 dBTP. That is within the ≤ −1.5 spec.
  - The sfx33.py limiter never engages (1 iteration, 0 dB gain reduction).
- **Final frame against the source SVG** (`srccmp33.py`).
  - The delivered `-play.html` seeked to 7.483 s, against the source rendered in Chromium at the same layout: **max diff 0** in light and dark.
  - The MP4 last frame (f449), decoded with `accurate_rnd`, against the source: max 14 (light) and 15 (dark). The mean is 0.05, there are no pixels with a diff above 16, and white decodes to 255.
  - Note that ffmpeg's default fast swscale decodes Y235 white as 253. Use `flags=accurate_rnd+full_chroma_int` for QC frame grabs.
- **Light/dark parity.**
  - The mean |α_light − α_dark| is 0.00024 overall, and 0.00145 at worst (f45). The only systematic difference is the cursor, which is white with a black stroke in both modes, by design.
  - Ring fade, reveal and wordmark timings are identical between the two (`sheet_l.png`, `sheet_d.png`, `zoom_reveal_*`).
- **Sync.**
  - Every v3.3 cue matches the visuals:

| cue | audio | visual |
|---|---|---|
| tick | 0.20 | btnIn |
| click | 1.41 | press bottom 1.408 |
| release | 1.52 | — |
| glide | 1.45–2.05 | morph |
| swell | 1.70 → 2.21 | crests at the thump |
| thump | 2.21 | first lion ink at f133, 2.217 |
| resolve | 3.85 | zh rise at 3.80 |

  - MP4 onsets match the WAV (`onset.py`).
- **Reproducibility.** Re-running a read-only copy of `sfx33.py` (`sfxprobe*.py`) reproduces the delivered WAV to within 1.4e-7.

## The unexplained onset at about 2.425 s: explained

**It is not an event. It is the plate reverb's sub-bass interfering with the dry thump body.** (Evidence: `sfxprobe3.txt`.)

- **Only one cue is active.** The thump group, which starts at 2.21 s, is the only thing sounding in 2.30–2.55 s: a sine at 46+34·e^(−16t) Hz, a 0.12 s noise click and the air tail. Nothing else in `T` is near 2.42 s.
- **The dry bus is smooth.** Its Hilbert envelope decays monotonically: −8.3 dB at 2.375 s, −9.0 at 2.400, −9.6 at 2.425.
- **The reverb return is not.**
  - `verb()` convolves the whole mix, sub-bass included, with a seeded white-noise IR (`rng` seed 33, exp(−3.6t), low-passed at 5.5 kHz).
  - Its ~47 Hz return swells from −39 dB (2.375) to **−21.8 dB at 2.405** and then drops to −43 dB (2.440).
  - Because it is phase-random against the dry sine, it first cancels and then reinforces. The mix goes **−10.9 dB at 2.400 → −8.9 dB at 2.420**, then back to −10.8 at 2.445.
- **The result is a +2.0 dB swell over about 20 ms**, centred at 2.415–2.425 s, about 205 ms after the hit.
  - On a subwoofer or good headphones it reads as a soft second "flam" in the thump. On laptop or phone speakers it is inaudible.
  - The limiter is not involved: gain reduction is 0 dB throughout.

## P1

None.

## P2

1. **The reveal reads as an opacity dissolve, not as the lion growing out of the nose.** (2.20–2.30 s, `zoom_reveal_l.png` f133–f138.)
   - **What happens now.** The 100 ms linear `fadeIn` hides the iris: radius travel is 65% done when opacity reaches 1.
     - In light mode the viewer sees a 17%, 33%, 50%, 67%, 83% grey lion. That kind of flat-ink cross-dissolve looks less premium than a shape-led move.
     - It also blurs the hit: the visual weight peaks around 2.25–2.30 s, while the thump peaks at 2.215 s, an audio lead of about 40–80 ms.
   - **Fix in `template33.html`** (the recommended one): make it scale-led from the nose, and keep the fade only as anti-aliasing cover.
     - `.reveal { transform-origin: 131.5px 147px; animation: grow .7s var(--decel) 2.2s both, fadeIn .05s linear 2.2s both, cut .001s linear 3.3s forwards; }`
     - `@keyframes grow { from { transform: scale(.72); } to { transform: scale(1); } }`. At .72, the mouth sits 27 units from the nose and the eyes 43, so nothing collides with the fixed `.nose`.
     - In `drive()`, set `R0 = R1 = 128` so the circle clip is static, or drop the clip-path.
     - The `transform-origin` is in the reveal's local user space, because `svg * { transform-box: view-box }` and the parent is `translate(20 14) scale(.9)`. Check with a frame grab that the nose stays put.
   - **Alternative, more "brand"**: replace the circle `<clipPath>` with the mane's outer silhouette scaled about the nose from 0.70 to 1.0 over 700 ms decel. The mane then visibly grows outward along its own scalloped contour.
   - **Either way, re-run `cov33.py`.** The first ink frame must still contain the complete face hole.
   - **Sound.** `T['thump']` can stay at 2.21: with a 50 ms fade, the first full-weight frame is f135 (2.25 s).
   - Expected gain: +0.3 Concept and +0.3 Timing.

## P3

1. **The morph still snaps (1.45–2.05 s).**
   - `morph33.py` already supports `MORPH_EASE=soft`, which is `cubic(.4,0,.2,1)`. Build with `MORPH_EASE=soft python3 build33.py template33.html v34.html`. Measured result:
     - Peak speed drops from 4.05× to 2.73× linear.
     - Progress becomes 10% at 1.557 s, 50% at 1.660 s, 90% at 1.830 s.
     - It gains about 60 ms of anticipation after the click (1.41), and the 50% point lands in the middle of the morph window.
   - Keep `MD = 600`.
   - In `sfx33.py` GLIDE, change the pitch curve to match: `x=np.minimum(t/MD,1); p=x*x*(3-2*x)` in place of `p=1-(1-np.minimum(t/MD,1))**3`.
2. **A one-frame seam hairline at f94 (1.567 s)** (`zoom_seam94.png`, `seam94_l/d.png`).
   - When the two halves abut exactly, Chromium anti-aliases each edge separately. That leaves a 1 px vertical line at x=1285, from 33→80 in light and 244→193 in dark (about 21% contrast), about 160 px tall.
   - In `shapes()`, this is the frame where `q ≈ 0.787` and `xL == xR == 0`. Any continuous close passes through such a frame, so retiming will not remove it.
   - Fix in `template33.html` `drive()`: draw the morph as one path. `BL.setAttribute('d', lerpPath(ML,x)+' '+lerpPath(MR,x))`, then hide `.barR` between 1.45 and 2.05 s.
   - Check that both subpaths wind the same way. If they don't, the overlap becomes a hole under nonzero fill; reverse the right half in `morph33.py` if needed.
   - Then re-run `seam33.py`, which needs frames re-extracted to `fl/` and `fd/`.
3. **Sub-bass "flam" at about 2.41–2.43 s** (explained above).
   - In `sfx33.py`, high-pass the reverb send. At the top of `verb(x)`, add `x = sosfilt(butter(2,180,'highpass',fs=SR,output='sos'),x)`. Keeping a sub-bass thump out of the plate is standard practice.
   - Re-run the loudness loop.
   - Confirm with `sfxprobe3.py`: the mix envelope over 2.30–2.55 s should now decay monotonically, like the dry bus.
4. **Luma excursions persist, and the claimed fix is a no-op.**
   - The excursions are encoder ringing. They are 0.10–0.21% of pixels per frame, and only 0.0002–0.0006% go beyond the 5–246 band. That is well inside EBU R103's 1% gamut tolerance, so it is not a delivery blocker for web or social.
   - Actions:
     - (a) Remove the `lutyuv` from `enc33.sh`, or keep it but stop citing it as the fix.
     - (b) Correct HANDOFF §8 to "decoded Y excursions are x264 ringing, ≤0.21% of pixels, within R103 tolerance".
     - (c) If a broadcaster demands hard 16–235, deliver a ProRes 422 HQ master (`-c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le`) and re-measure it with `r103.py`. I did not test this.
   - Don't use x264 `-qp 0`. It does measure clean (`enctest/results.txt`), but it needs the High 4:4:4 Predictive profile, which most players can't decode.
   - Lowering CRF to 8 or setting `psy-rd=0` changes almost nothing: about 0.11–0.16% either way.
5. **The ▶ is not optically centred in the ring.** At f120, the triangle's centroid is 20 px (at 2K) left of the ring centre, about 3.7% of the ring diameter. Play glyphs normally get nudged right.
   - The ▶ is the nose and must not move. Nudge the ring instead, about half of the 4.3 local units:
     - `<g transform="translate(-2.2 0) rotate(-90)"><circle class="ring" …/>` in `template33.html`.
     - Give `.ripple` the same offset.
   - This is optional. Check it against the "ring centre = nose centre" rule from v3.2. A 2-unit static offset does not bring back v3.2's ring-drift problem, because the drift came from animation.
6. **Optional: hand the ring to the reveal.** The ring fades out (2.00–2.22 s) just before the lion arrives.
   - Delay `RINGOFF` to 2.18 and fade it over 0.12 s while the lion scales up. The circle of the play button then becomes the lion's silhouette.
   - This would raise Concept, but it is not required.
7. **Reproducibility housekeeping.**
   - `build33.py` reads the logo from another project's uploads (`/workspace/projects/0b4d0196-…/files/uploads/…svg`). Point it at `assets/xijiwang-horizontal-primary-af6d799ceb5b.svg`.
   - `run33.sh` does `cd /workspace/work/anim`, which is outside this repo. Use a relative path.
   - `build33.py` defaults `RINGOFF` to 2.00, while the v3.2 review and the handoff mention 2.10. 2.00 is what shipped, so record it in the notes.

## Evidence (all in reviews/review-v33/)

- `sheet_l.png`, `sheet_d.png`: every 0.25 s.
- `zoom_reveal_l.png`, `zoom_reveal_d.png`: f126–f155, cropped around the nose.
- `zoom_morph_l.png`: f84–f130.
- `zoom_seam_l.png`, `zoom_seam_d.png`, `zoom_seam94.png`, `seam94_l.png`, `seam94_d.png`: the hairline.
- `curves.py` → `curves.txt`: reveal radius and fade per frame, plus morph progress under each easing.
- `lumarange.py`, `luma_light.txt`, `luma_dark.txt`, `r103.py`: per-frame luma range.
- `enctest/rd.py`, `enctest/results.txt`: the encoder ringing test.
- `onset.py` → `onset_wav.txt`, plus `sfxprobe.py`, `sfxprobe2.py`, `sfxprobe3.py` and their `.txt` outputs: onset and limiter analysis, and the dry/wet split.
- `srccmp33.py`, `src_*.png`, `html_last_*.png`, `mp4last_*.png`, `diff_*.png`: final frame against the source.
- `parity.py`: light/dark coverage.
- `seam33.py`: the hairline detector.
- The frame dumps were deleted to save space. Regenerate them with:
  `ffmpeg -i ../../deliverables/xijiwang-logo-v3.3-play-2K-60fps-light.mp4 -vsync 0 -start_number 0 fl/f%04d.png`
  and the same for `fd/` with the dark file.
