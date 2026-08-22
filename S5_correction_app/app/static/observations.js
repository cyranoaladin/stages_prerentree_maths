/* Observations générales de la correction.
 *
 * Ce code vivait dans une balise <script> du gabarit. Deux raisons de l'en sortir :
 * la politique de sécurité du contenu interdit le script inline, et une requête
 * mutante doit porter le jeton anti-CSRF — ce que l'inline ne faisait pas.
 */
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    var bouton = document.getElementById("save-general");
    if (!bouton) { return; }
    var url = bouton.getAttribute("data-url");
    bouton.addEventListener("click", function () {
      var formulaire = document.getElementById("general-form");
      var charge = {};
      formulaire.querySelectorAll("textarea, input, select").forEach(function (champ) {
        if (champ.name === "observed_duration_minutes") {
          charge[champ.name] = champ.value ? parseInt(champ.value, 10) : null;
        } else if (champ.name) { charge[champ.name] = champ.value; }
      });
      window.nexusFetch(url, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(charge)
      }).then(function (r) { return r.json(); }).then(function (corps) {
        document.getElementById("save-state").textContent =
          "✓ Observations enregistrées à " + corps.saved_at;
      }).catch(function () {
        document.getElementById("save-state").textContent =
          "Échec de l'enregistrement des observations.";
      });
    });
  });
})();
