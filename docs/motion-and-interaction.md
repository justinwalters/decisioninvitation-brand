# Motion and interaction

Motion expresses a thought becoming useful. It should help the viewer see a new condition, a change in state, or a path to the next step. The proposed system is quietly active, not static or restless.

## Motion roles

| Role | Duration | Behavior |
| --- | ---: | --- |
| Control feedback | 120–180 ms | Color or opacity transition; no layout jump |
| Field reveal | 240–360 ms | Opacity and 8–16 px translation toward a stable final position |
| Perspective-to-next-move explanation | 400–600 ms | User-triggered continuity between clearly labeled states |
| Editorial frame opening | Up to 500 ms | One-time reveal of a gap or extension; final state remains useful |

Use a restrained decelerating curve such as `cubic-bezier(.2,.7,.2,1)`. A duration is a ceiling, not a reason to animate. Essential confirmation appears when the system has its receipt; animation must never manufacture progress or hide failure.

## The catalyst behavior

For an explanatory brand animation, reveal the question first, then the condition that changes it, then the next move. Keep every sentence long enough to read. The orange point may appear once in its final place. It never orbits, bounces, pulses, spins, or acts as a loading indicator.

Do not make the Di mark fly apart, turn into a checkmark, or complete a false success action. The logo is a stable identifier. A motion asset may end on the complete signature after the narrative has done its work.

## Accessible and resilient behavior

Under `prefers-reduced-motion: reduce`, show the same final information immediately and remove translation, line drawing, and sequencing delays. Do not hide content before JavaScript runs. Keyboard focus remains visible during transitions, and changing content does not move focus unexpectedly.

No scroll hijacking, cursor replacement, autoplay audio, flashing emphasis, urgency pulses, or mandatory parallax. Pause or stop controls accompany any long-running motion. Captions carry speech; an accessible text equivalent carries essential diagram meaning.

## Product boundary

A brand animation is not evidence of implemented workflow. Label product demonstrations as illustrative if they show unimplemented synthesis, delivery, encryption, or a decision record. Build real controls from the product's behavior contract, not from a decorative animation.
