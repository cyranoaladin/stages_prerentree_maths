/* Écran de revue de la lecture assistée.
 *
 * Deux principes tenus ici :
 *
 * - le LaTeX proposé par un modèle est rendu par katex.render() à partir d'une chaîne,
 *   jamais injecté en HTML. La source reste affichée à côté du rendu : on doit pouvoir
 *   comparer ce qui est écrit et ce qui est montré ;
 * - une décision humaine s'ajoute à la proposition de l'IA, elle ne la remplace pas
 *   dans l'affichage : les deux restent visibles après enregistrement.
 */
(function () {
  "use strict";

  function rendreLatex(cible, source) {
    if (!cible) { return; }
    cible.textContent = "";
    if (!source) { return; }
    if (typeof window.katex === "undefined") {
      cible.textContent = source;      // sans KaTeX, la source vaut mieux que rien
      return;
    }
    try {
      window.katex.render(source, cible, {
        throwOnError: false, trust: false, strict: false, displayMode: false
      });
    } catch (e) {
      cible.textContent = source;
    }
  }

  function rendreTousLesLatex(racine) {
    var noeuds = (racine || document).querySelectorAll("[data-latex]");
    Array.prototype.forEach.call(noeuds, function (n) {
      rendreLatex(n, n.getAttribute("data-latex"));
    });
  }

  function poster(url, corps) {
    // nexusFetch pose le jeton anti-CSRF : l'oublier sur un seul appel produirait
    // un refus que seul l'utilisateur découvrirait.
    return window.nexusFetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(corps || {})
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (data) {
        if (!r.ok) { throw new Error(data.detail || ("HTTP " + r.status)); }
        return data;
      });
    });
  }

  function Ecran(racine) {
    this.racine = racine;
    this.studentId = racine.getAttribute("data-student");
    this.page = parseInt(racine.getAttribute("data-page") || "1", 10);
    this.etat = racine.querySelector("[data-etat-run]");
    this.monter();
  }

  Ecran.prototype.message = function (texte) {
    if (this.etat) { this.etat.textContent = texte || ""; }
  };

  Ecran.prototype.monter = function () {
    var self = this;
    var boutons = this.racine.querySelectorAll("[data-lancer]");
    Array.prototype.forEach.call(boutons, function (b) {
      b.addEventListener("click", function () {
        var quoi = b.getAttribute("data-lancer");
        var corps = {};
        var libelle = quoi === "lancer" ? "PRIMARY" : "AVEUGLE";
        if (!window.confirm("Lancer la lecture " + libelle + " ? Des appels facturés "
                            + "peuvent être émis pour les pages non encore lues.")) {
          return;
        }
        Array.prototype.forEach.call(boutons, function (x) { x.disabled = true; });
        self.message("Lecture " + libelle + " en cours…");
        poster("/eleve/" + self.studentId + "/transcription/" + quoi, corps)
          .then(function () { window.location.reload(); })
          .catch(function (err) {
            self.message("Échec : " + err.message);
            Array.prototype.forEach.call(boutons, function (x) { x.disabled = false; });
          });
      });
    });
  };

  function Bloc(element, studentId) {
    this.element = element;
    this.studentId = studentId;
    this.id = element.getAttribute("data-bloc");
    this.edition = element.querySelector("[data-bloc-edition], .bloc-edition");
    this.monter();
  }

  Bloc.prototype.monter = function () {
    var self = this;
    var actions = this.element.querySelectorAll("[data-action]");
    Array.prototype.forEach.call(actions, function (bouton) {
      bouton.addEventListener("click", function () {
        var action = bouton.getAttribute("data-action");
        if (action === "modifier") { self.ouvrirEdition(); return; }
        if (action === "relancer") { self.relancer(); return; }
        var note = null;
        if (action === "rejeter" || action === "illisible") {
          note = window.prompt("Motif (facultatif) :", "") || null;
        }
        self.envoyer({ action: action, note: note });
      });
    });

    var valider = this.element.querySelector("[data-valider-edition]");
    if (valider) {
      valider.addEventListener("click", function () {
        var verbatim = self.element.querySelector("[data-edition-verbatim]");
        var latex = self.element.querySelector("[data-edition-latex]");
        var note = self.element.querySelector("[data-edition-note]");
        self.envoyer({
          action: "modifier",
          verbatim: verbatim ? verbatim.value : "",
          latex: latex && latex.value ? latex.value : null,
          note: note && note.value ? note.value : null
        });
      });
    }

    var champLatex = this.element.querySelector("[data-edition-latex]");
    var apercu = this.element.querySelector("[data-apercu-latex]");
    if (champLatex && apercu) {
      var maj = function () { rendreLatex(apercu, champLatex.value); };
      champLatex.addEventListener("input", maj);
      maj();
    }
  };

  Bloc.prototype.ouvrirEdition = function () {
    if (this.edition) { this.edition.hidden = !this.edition.hidden; }
  };

  Bloc.prototype.relancer = function () {
    if (!window.confirm("Relancer la lecture de cette page sans utiliser le cache ? "
                        + "Un appel facturé sera émis.")) { return; }
    poster("/eleve/" + this.studentId + "/transcription/lancer", { force: true })
      .then(function () { window.location.reload(); })
      .catch(function (err) { window.alert("Échec : " + err.message); });
  };

  Bloc.prototype.envoyer = function (corps) {
    var self = this;
    poster("/eleve/" + this.studentId + "/transcription/bloc/" + this.id, corps)
      .then(function () { window.location.reload(); })
      .catch(function (err) { window.alert("Échec : " + err.message); });
  };

  document.addEventListener("DOMContentLoaded", function () {
    rendreTousLesLatex(document);
    var bandeau = document.querySelector("[data-transcription]");
    if (!bandeau) { return; }
    var ecran = new Ecran(bandeau);
    var blocs = document.querySelectorAll("[data-bloc]");
    Array.prototype.forEach.call(blocs, function (b) {
      new Bloc(b, ecran.studentId);
    });

    var attestation = document.querySelector("[data-attestation]");
    if (attestation) {
      var bouton = attestation.querySelector("[data-attester]");
      if (bouton) {
        bouton.addEventListener("click", function () {
          var note = attestation.querySelector("[data-attestation-note]");
          if (!window.confirm("Vous attestez avoir comparé la page originale et la "
                              + "transcription, et que tout contenu pertinent est "
                              + "représenté ou explicitement marqué. Confirmer ?")) {
            return;
          }
          poster("/eleve/" + attestation.getAttribute("data-student")
                 + "/transcription/page/" + attestation.getAttribute("data-page")
                 + "/attester",
                 { attested: true, note: note && note.value ? note.value : null })
            .then(function () { window.location.reload(); })
            .catch(function (err) { window.alert("Échec : " + err.message); });
        });
      }
    }

    var image = document.querySelector("[data-image-page]");
    if (image) {
      var zoom = 1, rotation = 0;
      var appliquer = function () {
        image.style.transform = "scale(" + zoom + ") rotate(" + rotation + "deg)";
      };
      var boutonsZoom = document.querySelectorAll("[data-zoom]");
      Array.prototype.forEach.call(boutonsZoom, function (b) {
        b.addEventListener("click", function () {
          zoom = b.getAttribute("data-zoom") === "+"
            ? Math.min(zoom * 1.25, 6) : Math.max(zoom / 1.25, 0.25);
          appliquer();
        });
      });
      // Rotation réelle : elle change les pixels envoyés au modèle, pas seulement
      // l'affichage. Elle produit une pièce dérivée et invalide le cache de lecture.
      var reelles = document.querySelectorAll("[data-rotation-reelle]");
      Array.prototype.forEach.call(reelles, function (b) {
        b.addEventListener("click", function () {
          var degres = parseInt(b.getAttribute("data-rotation-reelle"), 10);
          if (!window.confirm("Tourner réellement cette page de " + degres
                              + "° ? L'image envoyée au modèle change ; l'original "
                              + "et le rendu de base restent intacts, et la page "
                              + "devra être relue.")) { return; }
          var racine = document.querySelector("[data-transcription]");
          poster("/eleve/" + racine.getAttribute("data-student") + "/copie/rendu/"
                 + racine.getAttribute("data-page") + "/rotation", { degrees: degres })
            .then(function () { window.location.reload(); })
            .catch(function (err) { window.alert("Échec : " + err.message); });
        });
      });

      var rot = document.querySelector("[data-rotation]");
      if (rot) {
        rot.addEventListener("click", function () {
          rotation = (rotation + 90) % 360;      // affichage seulement
          appliquer();
        });
      }
    }
  });
})();
