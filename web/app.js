"use strict";

const ATTACK = { p: ["POWER", "🔴", "p"], s: ["SPEED", "🔵", "s"], t: ["TECHNICAL", "🟢", "t"], "?": ["?", "❔", "u"] };
const COUNTER = { p: "s", s: "t", t: "p", "?": null };
const LEVELS = ["Très sensible", "Sensible", "Normal", "Résistant", "Très résistant", "Inconnu"];
const AILMENTS = [["💀", "Poison"], ["🔥", "Brûlure"], ["⚡", "Paralysie"], ["😴", "Sommeil"],
  ["💥", "Fléau explosion"], ["🩸", "Saignement"], ["🙈", "Cécité"]];
const ELEMENTS = [["⚪", "Neutre"], ["🔥", "Feu"], ["💧", "Eau"], ["⚡", "Foudre"], ["🧊", "Glace"], ["🐉", "Dragon"]];

const app = document.getElementById("app");
let monsters = [];
let byId = new Map();
let home = null; // built once and kept in memory so search and scroll survive navigation
let homeScroll = 0;
let rulesView = null;

const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const CREDIT = `<footer class="credit">Projet de fan non officiel. Données et images : <a href="https://game8.co/games/Monster-Hunter-Stories-3" target="_blank" rel="noopener">Game8</a>. Monster Hunter Stories 3 © CAPCOM.</footer>`;
const tag = (c) => `<span class="tag ${ATTACK[c][2]}">${ATTACK[c][0]}</span>`;
const counterTag = (c) => (COUNTER[c] ? tag(COUNTER[c]) : `<span class="tag u">—</span>`);
const firstKnown = (m) => m.s.find((s) => COUNTER[s[1]]);
const img = (m, cls) =>
  m.i ? `<img class="${cls}" src="img/${m.id}.webp" alt="" loading="lazy" decoding="async">`
      : `<span class="${cls} empty"></span>`;

function buildHome() {
  const rows = monsters.map((m) => {
    const k = firstKnown(m);
    const combat = k ? `<div class="combat">${tag(k[1])}<b>→</b>${counterTag(k[1])}</div>` : "";
    return `<a class="row" href="#/m/${m.id}" data-n="${esc(m.n.toLowerCase())}">
      ${img(m, "thumb")}
      <div class="info"><div class="name">${esc(m.n)}</div><div class="elem">${esc(m.e)}</div></div>
      ${combat}</a>`;
  }).join("");

  const el = document.createElement("div");
  el.innerHTML = `
    <div class="top">
      <div class="title"><h1><span>MHS3</span> Companion</h1><button data-go="#/rules">❓ Counters</button></div>
      <input type="search" placeholder="🔎  Rechercher un monstre..." autocomplete="off" aria-label="Rechercher">
    </div>
    <div class="list">${rows}<div class="empty-msg" hidden>Aucun monstre trouvé.</div>${CREDIT}</div>`;

  const input = el.querySelector("input");
  const items = [...el.querySelectorAll(".row")];
  const empty = el.querySelector(".empty-msg");
  let timer;
  input.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      const q = input.value.trim().toLowerCase();
      let shown = 0;
      for (const r of items) {
        const hide = !r.dataset.n.includes(q);
        if (r.hidden !== hide) r.hidden = hide;
        if (!hide) shown++;
      }
      empty.hidden = shown > 0;
    }, 80);
  });
  return el;
}

function resTable(title, labels, values) {
  const lines = labels.map(([icon, name], i) =>
    `<p><span>${icon} ${name}</span><span class="lv${values[i]}">${LEVELS[values[i]]}</span></p>`).join("");
  return `<div><h4>${title}</h4>${lines}</div>`;
}

function monsterView(m) {
  const k = firstKnown(m);
  const main = k ? `<section><h3>Attaque et contre principal</h3><div class="pair">
      <div class="box"><small>TYPE D'ATTAQUE</small><strong class="${ATTACK[k[1]][2]}">${ATTACK[k[1]][1]} ${ATTACK[k[1]][0]}</strong></div>
      <span class="arrow">→</span>
      <div class="box hl" style="border-color:var(--${COUNTER[k[1]]})"><small>TON CONTRE</small><strong class="${COUNTER[k[1]]}">${ATTACK[COUNTER[k[1]]][1]} ${ATTACK[COUNTER[k[1]]][0]}</strong></div>
    </div></section>` : "";
  const states = m.s.map(([n, c]) =>
    `<div class="state"><span class="sn">${esc(n)}</span>${tag(c)}<b>→</b>${counterTag(c)}</div>`).join("");
  const el = document.createElement("div");
  el.innerHTML = `
    <div class="bar"><button class="ghost" data-back>← Retour</button><button class="ghost" data-go="#/">⌂ Accueil</button></div>
    <div class="page">
      <div class="hero">${img(m, "")}<div><h2>${esc(m.n)}</h2><div class="elem">${esc(m.e)}</div></div></div>
      ${main}
      <section><h3>Tous les états d'attaque</h3>${states}</section>
      <section><h3>Résistances</h3><div class="res">
        ${resTable("🧪 Ailments", AILMENTS, m.a)}${resTable("⚔️ Éléments", ELEMENTS, m.r)}</div></section>
              ${CREDIT}
            </div>`;
  return el;
}

function buildRules() {
  const rule = (a, b) => `<div class="rule"><span class="${a}">${ATTACK[a][1]} ${ATTACK[a][0]}</span><em>→ contre →</em><span class="${b}">${ATTACK[b][1]} ${ATTACK[b][0]}</span></div>`;
  const el = document.createElement("div");
  el.innerHTML = `<div class="bar"><button class="ghost" data-back>← Retour</button><button class="ghost" data-go="#/">⌂ Accueil</button></div>
    <div class="page"><h2>Mécanique des counters</h2>${rule("p", "s")}${rule("s", "t")}${rule("t", "p")}${CREDIT}</div>`;
  return el;
}

function route() {
  const hash = location.hash;
  const leavingHome = app.firstChild === home;
  if (hash.startsWith("#/m/")) {
    const m = byId.get(hash.slice(4));
    if (!m) { location.hash = "#/"; return; }
    if (leavingHome) homeScroll = window.scrollY;
    app.replaceChildren(monsterView(m));
    window.scrollTo(0, 0);
  } else if (hash === "#/rules") {
    if (leavingHome) homeScroll = window.scrollY;
    app.replaceChildren(rulesView || (rulesView = buildRules()));
    window.scrollTo(0, 0);
  } else {
    app.replaceChildren(home);
    window.scrollTo(0, homeScroll);
  }
}

app.addEventListener("click", (e) => {
  const go = e.target.closest("[data-go]");
  if (go) { location.hash = go.dataset.go; return; }
  if (e.target.closest("[data-back]")) {
    // history.back() keeps the phone's back gesture and our button consistent.
    if (history.length > 1) history.back(); else location.hash = "#/";
  }
});
window.addEventListener("hashchange", route);

fetch("data.json").then((r) => r.json()).then((data) => {
  monsters = data;
  byId = new Map(data.map((m) => [m.id, m]));
  home = buildHome();
  route();
});

if ("serviceWorker" in navigator) {
  let hasControlledPage = Boolean(navigator.serviceWorker.controller);
  let refreshing = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (!hasControlledPage) {
      hasControlledPage = true;
      return;
    }
    if (refreshing) return;
    refreshing = true;
    window.location.reload();
  });
  navigator.serviceWorker.register("sw.js").catch((error) => {
    console.error("Service worker registration failed:", error);
  });
}
