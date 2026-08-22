/* Téléversement de la copie de l'élève.
 *
 * L'ordre des pages est arrêté ici, dans le navigateur, avant l'envoi : l'utilisateur
 * voit les miniatures, réordonne si besoin, puis confirme. Le serveur enregistre
 * l'ordre reçu et ne le retrie jamais.
 *
 * Ce choix évite une zone d'attente côté serveur où des copies d'élèves non ingérées
 * s'accumuleraient sans statut ni provenance. Tant que « Confirmer » n'est pas
 * cliqué, rien n'a quitté le poste.
 */
(function () {
  "use strict";

  var TYPES_IMAGE = ["image/png", "image/jpeg", "image/webp", "image/tiff"];

  function octets(n) {
    var unites = ["o", "Ko", "Mo", "Go"], i = 0;
    while (n >= 1024 && i < unites.length - 1) { n /= 1024; i += 1; }
    return (i === 0 ? n : n.toFixed(1)) + " " + unites[i];
  }

  function Televersement(racine) {
    this.racine = racine;
    this.studentId = racine.getAttribute("data-student");
    this.limites = JSON.parse(racine.getAttribute("data-limites") || "{}");
    this.fichiers = [];
    this.envoiEnCours = false;
    this.monter();
  }

  Televersement.prototype.monter = function () {
    var self = this;
    this.zone = this.racine.querySelector("[data-zone-depot]");
    this.input = this.racine.querySelector("[data-input-fichiers]");
    this.liste = this.racine.querySelector("[data-liste-pages]");
    this.etat = this.racine.querySelector("[data-etat-upload]");
    this.barre = this.racine.querySelector("[data-barre-upload]");
    this.boutonEnvoyer = this.racine.querySelector("[data-envoyer]");
    this.boutonAnnuler = this.racine.querySelector("[data-annuler]");
    this.champLibelle = this.racine.querySelector("[data-libelle]");
    this.champRemplacer = this.racine.querySelector("[data-remplacer]");

    if (this.input) {
      this.input.addEventListener("change", function () {
        self.ajouter(Array.prototype.slice.call(self.input.files));
        self.input.value = "";
      });
    }
    if (this.zone) {
      ["dragenter", "dragover"].forEach(function (nom) {
        self.zone.addEventListener(nom, function (e) {
          e.preventDefault(); self.zone.classList.add("depot-actif");
        });
      });
      ["dragleave", "drop"].forEach(function (nom) {
        self.zone.addEventListener(nom, function (e) {
          e.preventDefault(); self.zone.classList.remove("depot-actif");
        });
      });
      this.zone.addEventListener("drop", function (e) {
        if (e.dataTransfer && e.dataTransfer.files) {
          self.ajouter(Array.prototype.slice.call(e.dataTransfer.files));
        }
      });
    }
    if (this.boutonEnvoyer) {
      this.boutonEnvoyer.addEventListener("click", function () { self.envoyer(); });
    }
    if (this.boutonAnnuler) {
      this.boutonAnnuler.addEventListener("click", function () { self.vider(); });
    }
  };

  Televersement.prototype.message = function (texte, nature) {
    if (!this.etat) { return; }
    this.etat.textContent = texte || "";
    this.etat.className = "small " + (nature === "erreur" ? "erreur-upload" : "muted");
  };

  Televersement.prototype.ajouter = function (nouveaux) {
    var self = this;
    if (!nouveaux.length) { return; }
    var pdfPresent = this.fichiers.concat(nouveaux).some(function (f) {
      return f.type === "application/pdf" || /\.pdf$/i.test(f.name);
    });
    var imagePresente = this.fichiers.concat(nouveaux).some(function (f) {
      return TYPES_IMAGE.indexOf(f.type) >= 0 || /\.(png|jpe?g|webp|tiff?)$/i.test(f.name);
    });
    if (pdfPresent && imagePresente) {
      this.message("Un envoi porte soit un PDF, soit des images, pas les deux : "
                   + "l'ordre des pages ne serait pas démontrable.", "erreur");
      return;
    }
    nouveaux.forEach(function (f) { self.fichiers.push(f); });
    if (this.limites.max_files && this.fichiers.length > this.limites.max_files) {
      this.fichiers = this.fichiers.slice(0, this.limites.max_files);
      this.message("Limite de " + this.limites.max_files + " fichiers atteinte.", "erreur");
    } else {
      this.message("");
    }
    this.rendre();
  };

  Televersement.prototype.deplacer = function (index, delta) {
    var cible = index + delta;
    if (cible < 0 || cible >= this.fichiers.length) { return; }
    var tmp = this.fichiers[index];
    this.fichiers[index] = this.fichiers[cible];
    this.fichiers[cible] = tmp;
    this.rendre();
  };

  Televersement.prototype.retirer = function (index) {
    this.fichiers.splice(index, 1);
    this.rendre();
  };

  Televersement.prototype.vider = function () {
    this.fichiers = [];
    this.message("Sélection annulée. Rien n'a été envoyé.");
    this.rendre();
  };

  Televersement.prototype.rendre = function () {
    var self = this;
    if (!this.liste) { return; }
    this.liste.textContent = "";
    var total = 0;

    this.fichiers.forEach(function (fichier, index) {
      total += fichier.size;
      var ligne = document.createElement("li");
      ligne.className = "page-a-envoyer";

      var vignette = document.createElement("div");
      vignette.className = "vignette";
      if (fichier.type && fichier.type.indexOf("image/") === 0) {
        var img = document.createElement("img");
        img.alt = "";
        img.src = URL.createObjectURL(fichier);
        img.addEventListener("load", function () { URL.revokeObjectURL(img.src); });
        vignette.appendChild(img);
      } else {
        vignette.textContent = "PDF";
        vignette.classList.add("vignette-pdf");
      }
      ligne.appendChild(vignette);

      var infos = document.createElement("div");
      infos.className = "infos-page";
      var titre = document.createElement("div");
      titre.innerHTML = "";
      var numero = document.createElement("strong");
      numero.textContent = "page " + (index + 1);
      titre.appendChild(numero);
      titre.appendChild(document.createTextNode(" — " + fichier.name));
      infos.appendChild(titre);
      var meta = document.createElement("div");
      meta.className = "small muted";
      meta.textContent = (fichier.type || "type inconnu") + " · " + octets(fichier.size);
      infos.appendChild(meta);
      ligne.appendChild(infos);

      var actions = document.createElement("div");
      actions.className = "actions-page";
      [["↑", -1, "Monter"], ["↓", 1, "Descendre"]].forEach(function (spec) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "btn btn-sm";
        b.textContent = spec[0];
        b.title = spec[2];
        b.addEventListener("click", function () { self.deplacer(index, spec[1]); });
        actions.appendChild(b);
      });
      var supprimer = document.createElement("button");
      supprimer.type = "button";
      supprimer.className = "btn btn-sm";
      supprimer.textContent = "retirer";
      supprimer.addEventListener("click", function () { self.retirer(index); });
      actions.appendChild(supprimer);
      ligne.appendChild(actions);

      self.liste.appendChild(ligne);
    });

    var resume = this.racine.querySelector("[data-resume-selection]");
    if (resume) {
      if (!this.fichiers.length) {
        resume.textContent = "";
      } else {
        var estPdf = this.fichiers.length === 1
          && (this.fichiers[0].type === "application/pdf"
              || /\.pdf$/i.test(this.fichiers[0].name));
        resume.textContent = estPdf
          ? "1 PDF · " + octets(total) + " · la pagination interne du PDF fait foi"
          : this.fichiers.length + " image(s) · " + octets(total)
            + " · l'ordre affiché sera l'ordre des pages";
      }
    }
    if (this.boutonEnvoyer) {
      this.boutonEnvoyer.disabled = !this.fichiers.length || this.envoiEnCours;
    }
    if (this.boutonAnnuler) {
      this.boutonAnnuler.disabled = !this.fichiers.length || this.envoiEnCours;
    }
    if (this.limites.max_bytes && total > this.limites.max_bytes) {
      this.message("La sélection pèse " + octets(total) + ", au-delà de la limite de "
                   + this.limites.max_bytes_lisible + ".", "erreur");
      if (this.boutonEnvoyer) { this.boutonEnvoyer.disabled = true; }
    }
  };

  Televersement.prototype.progression = function (pourcent) {
    if (!this.barre) { return; }
    this.barre.parentNode.hidden = false;
    this.barre.style.width = Math.max(0, Math.min(100, pourcent)) + "%";
  };

  Televersement.prototype.envoyer = function () {
    var self = this;
    if (!this.fichiers.length || this.envoiEnCours) { return; }
    if (!window.confirm("Confirmer l'ordre des " + this.fichiers.length
                        + " page(s) et téléverser ? La pièce deviendra immuable.")) {
      return;
    }
    var donnees = new FormData();
    this.fichiers.forEach(function (f) { donnees.append("fichiers", f, f.name); });
    if (this.champLibelle && this.champLibelle.value) {
      donnees.append("libelle", this.champLibelle.value);
    }
    if (this.champRemplacer && this.champRemplacer.checked) {
      donnees.append("remplacer", "1");
    }

    this.envoiEnCours = true;
    this.rendre();
    this.message("Envoi en cours…");
    this.progression(0);

    var requete = new XMLHttpRequest();
    requete.open("POST", "/eleve/" + this.studentId + "/copie/televerser");
    requete.setRequestHeader("X-Requested-With", "nexus");
    // Requête mutante : le jeton anti-CSRF est obligatoire, y compris en XHR.
    requete.setRequestHeader("X-CSRF-Token",
                             window.nexusCsrf ? window.nexusCsrf() : "");
    requete.upload.addEventListener("progress", function (e) {
      if (e.lengthComputable) { self.progression((e.loaded / e.total) * 100); }
    });
    requete.addEventListener("load", function () {
      self.envoiEnCours = false;
      var reponse = {};
      try { reponse = JSON.parse(requete.responseText); } catch (e) { reponse = {}; }
      if (requete.status >= 200 && requete.status < 300) {
        self.progression(100);
        self.message("Copie rattachée : " + reponse.file_count + " fichier(s), "
                     + (reponse.page_count || "?") + " page(s). Rechargement…");
        window.setTimeout(function () { window.location.reload(); }, 900);
      } else {
        self.progression(0);
        self.message(reponse.detail || ("Échec du téléversement (HTTP "
                                        + requete.status + ")."), "erreur");
        self.rendre();
      }
    });
    requete.addEventListener("error", function () {
      self.envoiEnCours = false;
      self.progression(0);
      self.message("Échec réseau pendant l'envoi. Rien n'a été rattaché.", "erreur");
      self.rendre();
    });
    requete.send(donnees);
  };

  document.addEventListener("DOMContentLoaded", function () {
    var racines = document.querySelectorAll("[data-televersement]");
    Array.prototype.forEach.call(racines, function (racine) {
      new Televersement(racine);
    });
  });
})();
