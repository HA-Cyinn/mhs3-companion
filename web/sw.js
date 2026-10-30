"use strict";
// Bump VERSION after regenerating the assets so clients refresh their cache.
const VERSION = "v7";
const CACHE = `mhs3-${VERSION}`;

self.addEventListener("install", (event) => {
  event.waitUntil(
    fetch("precache.json").then((r) => r.json()).then((files) =>
      caches.open(CACHE).then((c) => c.addAll(files))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Cache first: everything is local, so the app opens instantly and works offline.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(caches.match(event.request).then((hit) => hit || fetch(event.request)));
});
