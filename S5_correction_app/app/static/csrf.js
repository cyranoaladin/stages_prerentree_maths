/* Jeton anti-CSRF, partagé par tous les scripts de l'application.
 *
 * Le serveur pose un cookie « nexus_csrf » signé, lisible par ce script — il doit
 * l'être pour être renvoyé en en-tête — mais inaccessible à une autre origine grâce à
 * SameSite=Strict. Toute requête mutante doit le renvoyer dans « X-CSRF-Token ».
 *
 * « nexusFetch » enveloppe fetch() pour que ce soit systématique : oublier le jeton
 * sur un seul appel produirait un 403 en production, découvert par l'utilisateur.
 */
(function () {
  "use strict";

  function jeton() {
    var trouve = document.cookie.split(";").map(function (c) { return c.trim(); })
      .filter(function (c) { return c.indexOf("nexus_csrf=") === 0; })[0];
    return trouve ? decodeURIComponent(trouve.slice("nexus_csrf=".length)) : "";
  }

  window.nexusCsrf = jeton;

  window.nexusFetch = function (url, options) {
    options = options || {};
    var methode = (options.method || "GET").toUpperCase();
    var entetes = {};
    Object.keys(options.headers || {}).forEach(function (k) {
      entetes[k] = options.headers[k];
    });
    entetes["X-Requested-With"] = entetes["X-Requested-With"] || "nexus";
    if (["GET", "HEAD", "OPTIONS"].indexOf(methode) === -1) {
      entetes["X-CSRF-Token"] = jeton();
    }
    options.headers = entetes;
    options.credentials = options.credentials || "same-origin";
    return fetch(url, options);
  };
})();
