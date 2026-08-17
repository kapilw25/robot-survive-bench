┌─────────────────┬────────────────────┬────────────────────────────────────────┬─────────────────────────────────┐
│  🧩 Component   │      ✅ Real       │       🎭 Stand-in / placeholder        │         🛠️ Made real by         │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 🖼️ Dataset      │ Real LIBERO frames │ shown as stills; not the substrate the │ task3 (videos) + Option A       │
│ frames (5)      │  from HF           │  scores came from                      │                                 │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 🌍 Substrate    │ -                  │ toy 2D PIL cartoon (ToyVisualEnv), not │ LIBERO/MuJoCo (libero_env.py)   │
│                 │                    │  physics                               │                                 │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 👁️ Perception   │ Gemini-ER2 sees    │ state_text hands over exact            │ drop coordinates on LIBERO      │
│                 │ the image          │ coordinates -> brain needn't look      │                                 │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 🤖 Actions      │ skill API is real  │ pick/place teleport the mug; no        │ _skill_to_primitive (OSC) TODO  │
│                 │                    │ grasp/physics                          │                                 │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 🌀 OOD          │ applied            │ "transparent" = a color tint;          │ real materials/occlusion in sim │
│                 │ per-episode        │ "clutter" = 3 drawn boxes              │                                 │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 🔌 Fireworks    │ calls are real     │ text-only (until this turn)            │ enabling send_image now         │
│ vision          │                    │                                        │                                 │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 📊 RSR metric   │ formula correct    │ vacuous (always 1.0) - no              │ inject failures on LIBERO       │
│                 │                    │ perturbations injected                 │                                 │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 📊 WAS metric   │ formula correct    │ always "-" - no VLA baseline has run   │ run pi0-FAST/V-JEPA/DreamZero   │
│                 │                    │                                        │ (stubs)                         │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 🎯 Success test │ computed           │ a coordinate proximity check, not task │ BDDL goal check in LIBERO       │
│                 │                    │  semantics                             │                                 │
├─────────────────┼────────────────────┼────────────────────────────────────────┼─────────────────────────────────┤
│ 🔢 Sample size  │ real runs          │ n=3 (1 task x 3 splits), not           │ many tasks x seeds              │
│                 │                    │ significant                            │                                 │
└─────────────────┴────────────────────┴────────────────────────────────────────┴─────────────────────────────────┘