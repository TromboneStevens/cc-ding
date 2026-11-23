const DEFAULTS = { enabled: true, volume: 0.7 };

const enabledEl = document.getElementById("enabled");
const volumeEl = document.getElementById("volume");
const testEl = document.getElementById("test");

const testAudio = new Audio(browser.runtime.getURL("ding.wav"));

async function load() {
  const s = { ...DEFAULTS, ...(await browser.storage.local.get(DEFAULTS)) };
  enabledEl.checked = s.enabled;
  volumeEl.value = s.volume;
}

enabledEl.addEventListener("change", () => {
  browser.storage.local.set({ enabled: enabledEl.checked });
});

volumeEl.addEventListener("input", () => {
  browser.storage.local.set({ volume: Number(volumeEl.value) });
});

testEl.addEventListener("click", () => {
  testAudio.currentTime = 0;
  testAudio.volume = Number(volumeEl.value);
  testAudio.play().catch(() => {});
});

load();
