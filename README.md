# cc-ding

A Firefox extension that plays a sound effect when a **golden cookie** appears
in [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/).

## How it works

Golden cookies are rendered in the game as `<div class="shimmer">` elements
inside a `<div id="shimmers">` container. The content script attaches a
`MutationObserver` to that container and plays a chime the moment a shimmer is
added to the page. It also catches a shimmer that's already on screen when the
page finishes loading.

## Files

- `manifest.json` — Manifest V3 extension definition (Firefox / Gecko).
- `content.js` — injected into the Cookie Clicker page; detects golden cookies.
- `popup.html` / `popup.js` — toolbar popup to toggle the sound, set volume, and test it.
- `ding.wav` — the sound effect.
- `icons/` — toolbar icons.
- `gen_assets.py` — regenerates `ding.wav` and the icons using only the Python stdlib.

## Settings

Click the extension's toolbar icon for a popup where you can:

- Turn the sound on/off.
- Adjust the volume.
- Play a test sound.

Settings are saved with `browser.storage.local` and applied live.

## Install (temporary, for testing)

1. Open Firefox and go to `about:debugging#/runtime/this-firefox`.
2. Click **Load Temporary Add-on…**.
3. Select the `manifest.json` file in this folder.
4. Open https://orteil.dashnet.org/cookieclicker/ and wait for a golden cookie.

Temporary add-ons are removed when Firefox restarts. To keep it permanently you
need to package and sign it through [addons.mozilla.org](https://addons.mozilla.org/).

## Notes

- The extension dings for **any** shimmer, which includes the red "wrath"
  cookies from the Grandmapocalypse, since those are also clickable events.
- Browsers may block audio until you interact with the page. In Cookie Clicker
  you're clicking constantly, so this is rarely an issue.

## Regenerating assets

```
python3 gen_assets.py
```
