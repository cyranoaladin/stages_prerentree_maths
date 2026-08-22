/* Rendu mathématique — KaTeX servi localement, aucune requête réseau.
 *
 * Le rendu n'est appliqué qu'aux éléments portant explicitement la classe « math ».
 * C'est délibéré : ces éléments ne contiennent que du texte issu du référentiel
 * interne. Une observation saisie par l'enseignant est échappée par le gabarit et
 * n'est jamais transformée en HTML, donc jamais confiée au moteur.
 */
(function () {
  "use strict";

  var DELIMITERS = [
    { left: "$$", right: "$$", display: true },
    { left: "\\[", right: "\\]", display: true },
    { left: "$", right: "$", display: false },
    { left: "\\(", right: "\\)", display: false }
  ];

  function render(root) {
    if (typeof window.renderMathInElement !== "function") { return false; }
    try {
      window.renderMathInElement(root, {
        delimiters: DELIMITERS,
        throwOnError: false,
        errorColor: "#9E2234",
        strict: false,
        trust: false,
        macros: {
          "\\dfrac": "\\frac",
          "\\code": "\\texttt{#1}"
        }
      });
      return true;
    } catch (e) {
      return false;
    }
  }

  function renderAll() {
    var done = 0;
    document.querySelectorAll(".math").forEach(function (node) {
      if (node.getAttribute("data-math-rendered") === "1") { return; }
      if (render(node)) {
        node.setAttribute("data-math-rendered", "1");
        done += 1;
      }
    });
    document.documentElement.setAttribute("data-math-ready", done > 0 ? "1" : "0");
    return done;
  }

  window.nexusRenderMath = renderAll;

  document.addEventListener("DOMContentLoaded", function () {
    // auto-render.min.js est chargé en defer : il peut ne pas être prêt au premier tour.
    if (!renderAll()) { window.setTimeout(renderAll, 60); }
  });
})();
