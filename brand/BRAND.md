# tv.bunhub.dev — Brand Guidelines v0.1 ("Jellynaut")

Status: draft for Jason's review. Nothing here is deployed; `branding.xml` on jserver is untouched.
Source of truth for tokens: `tokens/palette.json` → `tokens/tokens.css`. Board: `board/brand-board-v0.1.png`.

## 1. Concept

Reference: `jellynaut.jpg` — one engraved, charcoal astronaut drifting in a near-black void, holding the only light in the frame: a neon jellyfish. 
The bunhub spin: **the jellyfish is a bun.** A baozi dome (pleats fan from the crown) whose tentacles trail like a spectrum. 
The brand idea is *quiet hero, loud light*: the UI recedes into void and hull-grey; color appears only where something is alive (play, resume, live, request).

- Name: **tv.bunhub** (lowercase, always, set in Major Mono Display). Long form: *Bunhub TV*.
- Tagline: **drift in. press play.** (alt: *the quiet part of the universe*; *light in the dark*)
- Place in the universe: bunhub = the house (La Croix whispers, white baozi, lavender llama). tv = the night side of the house: same cast, lights off, glow on.
- Mascot cameo rule: the lavender house llama may wear the suit (Jellynaut Grungy). Never replace the jelly-bun as the primary mark.

## 2. Palette

Dark-only brand. Void is the canvas; spectrum colors are light sources, not fills.

| Role | Name | Hex | Use |
|---|---|---|---|
| Canvas | void | `#0F161E` | backgrounds (sampled from jellynaut.jpg) |
| Surface | hull | `#27323E` | cards, panels, suit grey |
| Ink | rim | `#F0EECF` | text, outlines (the cream engraving edge) |
| Secondary | fleece | `#B49FCC` | house llama lavender, secondary text, taglines |
| Primary | play | `#0BF591` | play, focus ring, primary button |
| Highlight | volt | `#F8ED0F` | now/new, badges |
| Warm | coral | `#F64C60` | resume, continue watching |
| Live | live | `#F42EE3` | requests, live TV / DVR |
| Alert | signal | `#F42A36` | errors/destructive only |
| Warn | amber | `#E5B620` | warnings, pending |

Glow spectrum: play → volt → coral → live. Used for progress bars, the logo tentacles, loading states, and splash accents. Max two spectrum hues per screen; never a rainbow wallpaper.

Contrast (WCAG, computed):

| Color | Hex | on void | on hull |
|---|---|---|---|
| rim | `#F0EECF` | 15.5:1 | 11.1:1 |
| fleece | `#B49FCC` | 7.6:1 | 5.4:1 |
| play | `#0BF591` | 12.6:1 | 9.0:1 |
| volt | `#F8ED0F` | 14.8:1 | 10.6:1 |
| coral | `#F64C60` | 5.3:1 | 3.8:1 |
| live | `#F42EE3` | 5.5:1 | 3.9:1 |
| signal | `#F42A36` | 4.5:1 | 3.2:1 |
| amber | `#E5B620` | 9.6:1 | 6.9:1 |

Void text on a play-green button: 12.6:1. Signal red and live magenta are for strokes/glow/large type on void, not small body text on hull.

## 3. Logo

- **Mark: jelly-bun** — cream rim bell, five pleats in spectrum, nine tentacles with spores. Files: `logo/jellybun-mark.svg` (vector, glow filter), PNGs at 2048/512, on-void 2048, 180 touch icon.
- **Lockup: horizontal** — mark + `tv.bunhub` + tagline + `BUNHUB.DEV / TV` — `logo/lockup-horizontal-*.png`.
- Clear space: one bell-pleat width (~ 1/10 of mark width) on all sides. Min size: 24 px mark-only (drop glow + spores below 48 px), 160 px lockup.
- One-color: rim `#F0EECF` on void, or void on play. No gradients on the wordmark.
- Don't: put the mark on light backgrounds, recolor the rim, outline the wordmark, add the llama inside the bell, use more than the spectrum order above.

## 4. Type

All OFL, already installed on the MacBook.

- Wordmark/splash titles: **Major Mono Display**, lowercase only.
- UI + copy: **Google Sans Flex**, ROND 100, weights 400/500/700.
- Metadata/badges/codes: **Atkinson Hyperlegible Mono**.

Web: self-host the three families (no Google Fonts call from a public host).

## 5. Voice

Plain, warm, a little dry. Same copy law as bunhub: honest errors ("the stream went quiet", never "something went wrong"). Empty states: "nothing drifting here yet."

## 6. Splash / backdrop art rules

- 16:9, 3840×2160 JPEG q97 progressive sRGB (matches jellynaut.jpg), plus 1920×1080 PNG for Jellyfin's splashscreen.
- Near-black void with sparse stars, one focal subject, ≤ 15% of the frame lit by neon. Engraved line texture, no cel-shading, no gradients on the figure.
- Title optional; if present: `tv.bunhub` Major Mono Display in rim, bottom-left, ≥ 8% safe margin.

## 7. Implementation notes (for the tv.bunhub.dev port)

- `tokens/tokens.css` = web tokens. `tokens/jellyfin-custom.css.draft` = Jellyfin CustomCss draft; branding.xml currently carries an intro-skipper `@import` that must be kept.
- Public host: favicon from the mark, `apple-touch-icon-180.png`, OG image from the board crop. Don't push to jserver or Cloudflare until the PM audit (see IDEA.md) finishes.
- Working concurrently with Hermes Desktop: nothing committed. Files live under `brand/` only; `IDEA.md` untouched.

## 8. Open questions for Jason

- Keep the "jelly-bun" mark, or push further toward a pure astronaut/helmet mark?
- Is `tv.bunhub` the on-screen name, or `bunhub tv`?
- Public skin: dark-only (as here), or keep a light fallback?
