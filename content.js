// CC Ding - plays a sound when a golden cookie (shimmer) appears in Cookie Clicker.
(() => {
  "use strict";

  const DEFAULTS = { enabled: true, volume: 0.7 };
  let settings = { ...DEFAULTS };

  const soundUrl = browser.runtime.getURL("ding.wav");

  // Preload the audio so playback is instant when a cookie appears.
  const audio = new Audio(soundUrl);
  audio.preload = "auto";

  function playDing() {
    if (!settings.enabled) return;
    try {
      audio.pause();
      audio.currentTime = 0;
      audio.volume = settings.volume;
      const p = audio.play();
      if (p && typeof p.catch === "function") {
        // Autoplay can be blocked until the user interacts with the page.
        // In Cookie Clicker the user is clicking constantly, so this is rare.
        p.catch(() => {});
      }
    } catch (e) {
      // Ignore playback errors; nothing we can do without user interaction.
    }
  }

  // Golden cookies are <div class="shimmer"> added inside <div id="shimmers">.
  // "wrath" shimmers (red, from the Grandmapocalypse) also use .shimmer; we
  // ding for any shimmer appearing since they're all clickable opportunities.
  function isGoldenShimmer(node) {
    return (
      node &&
      node.nodeType === Node.ELEMENT_NODE &&
      node.classList &&
      node.classList.contains("shimmer")
    );
  }

  function watch(container) {
    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.addedNodes) {
          if (isGoldenShimmer(node)) {
            playDing();
            return; // one ding per mutation batch is plenty
          }
        }
      }
    });
    observer.observe(container, { childList: true });

    // In case a shimmer is already on screen when we start watching.
    if (container.querySelector(".shimmer")) {
      playDing();
    }
  }

  // The #shimmers container may not exist immediately after load; wait for it.
  function init() {
    const existing = document.getElementById("shimmers");
    if (existing) {
      watch(existing);
      return;
    }
    const bodyObserver = new MutationObserver(() => {
      const el = document.getElementById("shimmers");
      if (el) {
        bodyObserver.disconnect();
        watch(el);
      }
    });
    bodyObserver.observe(document.documentElement, {
      childList: true,
      subtree: true,
    });
  }

  // Load saved settings, then start.
  browser.storage.local
    .get(DEFAULTS)
    .then((stored) => {
      settings = { ...DEFAULTS, ...stored };
    })
    .catch(() => {})
    .finally(init);

  // React to settings changes from the popup live.
  browser.storage.onChanged.addListener((changes, area) => {
    if (area !== "local") return;
    if (changes.enabled) settings.enabled = changes.enabled.newValue;
    if (changes.volume) settings.volume = changes.volume.newValue;
  });
})();
