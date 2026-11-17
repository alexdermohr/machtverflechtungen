/* Progressive enhancement of the committed source catalogue.
   Without JavaScript every registered source remains readable and linkable. */
(() => {
  "use strict";

  const normalize = (value) =>
    String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/ß/g, "ss")
      .toLocaleLowerCase("de");

  const matchesPeriod = (rawYear, period) => {
    if (!period) return true;
    if (period === "unknown") return !rawYear;
    const year = Number(rawYear);
    if (!Number.isInteger(year) || year < 1000) return false;
    if (period === "pre1950") return year < 1950;
    if (period === "1950-1979") return year >= 1950 && year <= 1979;
    if (period === "1980-1999") return year >= 1980 && year <= 1999;
    if (period === "2000-now") return year >= 2000;
    return false;
  };

  function initialize() {
    const root = document.getElementById("mv-source-browser");
    if (!root || root.dataset.ready === "true") return;

    const entries = Array.from(document.querySelectorAll(".mv-source-entry"));
    if (!entries.length) return;
    root.dataset.ready = "true";
    root.innerHTML = [
      '<form class="mv-source-filters" role="search" aria-label="Quellenkatalog filtern">',
      '<div><label for="mv-source-query">Stichwort, Institution oder Quellen-ID</label>',
      '<input id="mv-source-query" type="search" autocomplete="off" placeholder="Quellen durchsuchen"></div>',
      '<div><label for="mv-source-type">Quelltyp</label>',
      '<select id="mv-source-type"><option value="">Alle Quelltypen</option>',
      '<option value="primary">Originaldokumente</option>',
      '<option value="research">Forschung &amp; Dokumentation</option></select></div>',
      '<div><label for="mv-source-tier">Quellenstufe</label>',
      '<select id="mv-source-tier"><option value="">Alle Stufen</option>',
      '<option>A</option><option>B</option><option>C</option>',
      '<option>D</option><option>E</option></select></div>',
      '<div><label for="mv-source-period">Zeitraum</label>',
      '<select id="mv-source-period"><option value="">Alle Zeiträume</option>',
      '<option value="pre1950">Vor 1950</option><option value="1950-1979">1950–1979</option>',
      '<option value="1980-1999">1980–1999</option><option value="2000-now">Ab 2000</option>',
      '<option value="unknown">Ohne Jahresangabe</option></select></div>',
      '<div class="mv-source-filter-footer">',
      '<p id="mv-source-count" role="status" aria-live="polite" aria-atomic="true"></p>',
      '<button type="reset" class="md-button">Filter zurücksetzen</button></div>',
      '</form>'
    ].join("");

    const form = root.querySelector("form");
    const input = root.querySelector("#mv-source-query");
    const kind = root.querySelector("#mv-source-type");
    const tier = root.querySelector("#mv-source-tier");
    const period = root.querySelector("#mv-source-period");
    const count = root.querySelector("#mv-source-count");

    const prepared = entries.map((element) => ({
      element,
      haystack: normalize(element.textContent),
      kind: element.dataset.sourceKind,
      tier: element.dataset.sourceTier,
      year: element.dataset.sourceYear,
    }));

    function update() {
      const words = normalize(input.value).trim().split(/\s+/).filter(Boolean);
      let visible = 0;
      for (const source of prepared) {
        const match =
          words.every((word) => source.haystack.includes(word)) &&
          (!kind.value || source.kind === kind.value) &&
          (!tier.value || source.tier === tier.value) &&
          matchesPeriod(source.year, period.value);
        source.element.hidden = !match;
        if (match) visible += 1;
      }
      count.textContent = visible
        ? visible + " von " + prepared.length + " Quellen angezeigt"
        : "Keine passenden Quellen. Filter zurücksetzen oder Suche ändern.";
    }

    // Links and browser history must reveal a filtered-out source target.
    function revealSource(id) {
      const target = document.getElementById(id);
      if (target?.closest(".mv-source-entry")?.hidden) {
        form.dispatchEvent(new Event("reset", { cancelable: true, bubbles: true }));
      }
    }

    const content = root.closest(".md-content");
    content?.addEventListener("click", (event) => {
      const anchor = event.target?.closest?.('a[href^="#src-"]');
      if (anchor) revealSource(anchor.getAttribute("href").slice(1));
    });
    window.addEventListener("hashchange", () => {
      // Ignore stale listeners after MkDocs instant navigation.
      if (document.getElementById("mv-source-browser") !== root) return;
      const hash = window.location.hash;
      if (hash.startsWith("#src-")) revealSource(hash.slice(1));
    });

    form.addEventListener("input", update);
    form.addEventListener("change", update);
    form.addEventListener("submit", (event) => event.preventDefault());
    form.addEventListener("reset", (event) => {
      event.preventDefault();
      input.value = "";
      kind.value = "";
      tier.value = "";
      period.value = "";
      update();
    });
    update();
  }

  // Initialize on a normal page load and on MkDocs instant navigation.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
  if (typeof document$ !== "undefined" && document$?.subscribe) {
    document$.subscribe(initialize);
  }
})();