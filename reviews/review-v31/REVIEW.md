# v3.1 — SELF-review (NOT independent)

No independent-reviewer dispatch tool was available in this session, so this is the author's own
strict check. It must not count as the loop's ≥8.2 gate. An independent review is still owed.

## Round-0 items → status
| Round-0 item | v3.1 |
|---|---|
| P1-1 btn intro overridden by `both` | fixed: btnShrink/cut use `forwards`; intro visible f0–f54 |
| P1-2 ghost ripple | fixed: `.ripple` base opacity 0, `forwards`; ripple also clamped inside ring (scale ≤1) |
| P1-3 cross-dissolve hand-off | fixed: bars morph (baked 31-key path, emphasized) into the exact source nose halves (nose − (131.5,147)); hard swap to whole nose path at 1.95s (diff ≤45/255 on 14 AA px), hard swap to lion nose at 2.50s (diff ≤7/255) |
| P1-4 shine rects | removed |
| P1-5 loudness | −16.0 LUFS I, −2.4 dBTP (ffmpeg ebur128, wav and both mp4) |
| P1-6 colour / encode | bg #fff / #000, ink #202624 / #f5f5f7; bt709 tv tagged; flat bg Y=235 / 16 → RGB 255 / 0 |
| P2 staging | camera 2.8× on the nose → 1× (1.9–3.5s, emphasized) |
| P2 competing shapes | outline draw removed; ring grows (×1.6, recentred to mane) as the mane boundary, fades 2.92–3.27 |
| P2 muddy grey lion | clip-circle reveal from the nose (r 0→128, 2.52–3.27s); no opacity fade |
| P2 cursor on morph | tip at (24,28) outside bars; fades 1.42–1.77 |
| P2 holds / blink | blink removed; last motion ends 5.59s → 1.91s clean hold |
| P2 over-scored SFX | 5 cues only: click 1.41, glide 1.45, swell 1.90→2.52, thump 2.52, resolve 3.85 |
| P3 click sync | click at 1.41 = press bottom (1.408) / tap bottom (1.417) |
| P3 bowtie | gone (seam corners kept on the shared silhouette line) |
| P3 sub-black | flat black is 16; isolated codec overshoot pixels (≤6/frame, edges) remain — see caveat |

Extra: frames are rendered by "baking" each frame's animated values into static styles, so no compositor
resampling. Final frame is pixel-identical (max diff 0) to the source SVG in light and dark; live playback
also bakes at the end → identical.

## Self-scores (author's view, discount accordingly)
concept 8.0 · craft 8.0 · timing & easing 7.8 · brand fidelity 8.6 · sound 7.5 · light/dark parity 8.8 → ~8.1

## Remaining (self-identified)
- P2: 2.0–2.5s the ▶ shrinks to nose size before the lion appears; it reads as a small glyph inside a large ring for ~0.5s.
- P3: 0–1.4s has no sound (by the brief's five-cue spec).
- P3: the ring is a circle and the mane is a 12-gon, so a hairline of ring shows outside the mane notches while it fades (2.92–3.27s).
- P3: x264 at CRF 12 leaves a few isolated edge pixels outside 16–235 per frame (displays clip them).
