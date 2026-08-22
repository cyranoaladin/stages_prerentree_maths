/* Nexus S5 — Correction & Bilans.
   JavaScript minimal, sans dépendance, sans CDN. Trois responsabilités seulement :
   enregistrer ce qui est saisi, afficher l'état de l'enregistrement, et faire circuler
   le clavier. Aucun calcul pédagogique n'a lieu ici : tout vient du serveur. */

(function () {
  "use strict";

  var saveState = null;
  var timers = {};

  function stamp(text, isError) {
    if (!saveState) { saveState = document.getElementById("save-state"); }
    if (!saveState) { return; }
    saveState.textContent = text;
    saveState.classList.toggle("error", !!isError);
  }

  function post(url, payload) {
    // nexusFetch pose le jeton anti-CSRF : l'oublier sur un seul appel produirait
    // un refus que seul l'utilisateur découvrirait.
    return window.nexusFetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (body) {
        if (!res.ok) {
          var detail = body && body.detail;
          if (detail && typeof detail === "object") { detail = detail.message || JSON.stringify(detail); }
          throw new Error(detail || ("erreur " + res.status));
        }
        return body;
      });
    });
  }

  /* ------------------------------------------------------------ critères */
  function readCriterion(root) {
    var codes = [];
    root.querySelectorAll(".code-chip.on").forEach(function (chip) {
      codes.push(chip.getAttribute("data-code"));
    });
    var selected = root.querySelector(".score-btn.selected");
    var statusBtn = root.querySelector(".status-btn.selected");
    var obs = root.querySelector("textarea.obs");
    var alt = root.querySelector("input.alt-method");
    return {
      score_centi: statusBtn ? null : (selected ? parseInt(selected.getAttribute("data-centi"), 10) : null),
      error_codes: codes,
      observation: obs ? obs.value : null,
      accepted_alternative_method: alt ? alt.checked : false,
      scoring_status: statusBtn ? statusBtn.getAttribute("data-status") : null
    };
  }

  function refreshProgress(progress) {
    if (!progress) { return; }
    var bar = document.getElementById("progress-bar");
    var label = document.getElementById("progress-label");
    if (bar) { bar.style.width = progress.percent + "%"; }
    if (label) {
      label.textContent = progress.original_criteria + " critères du sujet · "
        + progress.done + " / " + progress.total + " lignes analytiques renseignées — "
        + progress.percent + " %";
    }
  }

  function saveCriterion(root, immediate) {
    var id = root.getAttribute("data-scoring-id");
    var url = root.getAttribute("data-url");
    clearTimeout(timers[id]);
    var run = function () {
      stamp("Enregistrement…");
      post(url, readCriterion(root)).then(function (body) {
        stamp("✓ Enregistré à " + body.saved_at);
        root.classList.toggle("done", body.scoring_status !== "PENDING");
        root.classList.toggle("pending", body.scoring_status === "PENDING");
        refreshProgress(body.progress);
      }).catch(function (err) {
        stamp("✗ " + err.message, true);
      });
    };
    if (immediate) { run(); } else { timers[id] = setTimeout(run, 600); }
  }

  function fullScoreDisabled(root, disabled) {
    root.querySelectorAll(".code-chip").forEach(function (chip) {
      chip.setAttribute("aria-disabled", disabled ? "true" : "false");
      if (disabled) { chip.classList.remove("on"); }
    });
  }

  function selectScore(root, button) {
    root.querySelectorAll(".score-btn, .status-btn").forEach(function (b) {
      b.classList.remove("selected");
      b.setAttribute("aria-pressed", "false");
    });
    button.classList.add("selected");
    button.setAttribute("aria-pressed", "true");
    var isFull = button.classList.contains("full");
    fullScoreDisabled(root, isFull);
    saveCriterion(root, true);
  }

  function bindCriterion(root) {
    root.querySelectorAll(".score-btn, .status-btn").forEach(function (button) {
      button.addEventListener("click", function () {
        selectScore(root, button);
        // Le focus reste sinon sur le bouton, où les raccourcis sont neutralisés :
        // on le rend au critère pour que la navigation au clavier reprenne.
        root.setAttribute("tabindex", "-1");
        root.focus({ preventScroll: true });
      });
    });
    root.querySelectorAll(".code-chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        if (chip.getAttribute("aria-disabled") === "true") {
          stamp("Un critère intégralement réussi ne porte pas de code d'erreur.", true);
          return;
        }
        chip.classList.toggle("on");
        saveCriterion(root, true);
      });
    });
    var obs = root.querySelector("textarea.obs");
    if (obs) { obs.addEventListener("input", function () { saveCriterion(root, false); }); }
    var alt = root.querySelector("input.alt-method");
    if (alt) { alt.addEventListener("change", function () { saveCriterion(root, true); }); }
  }

  /* --------------------------------------------------------------- items */
  function bindItem(card) {
    var url = card.getAttribute("data-obs-url");
    if (!url) { return; }
    var send = function () {
      var conf = card.querySelector("input[name='confidence']:checked");
      var obs = card.querySelector("textarea.item-obs");
      stamp("Enregistrement…");
      post(url, {
        confidence: conf ? parseInt(conf.value, 10) : null,
        observation: obs ? obs.value : null
      }).then(function (body) { stamp("✓ Enregistré à " + body.saved_at); })
        .catch(function (err) { stamp("✗ " + err.message, true); });
    };
    card.querySelectorAll("input[name='confidence']").forEach(function (input) {
      input.addEventListener("change", send);
    });
    var obs = card.querySelector("textarea.item-obs");
    if (obs) {
      obs.addEventListener("input", function () {
        clearTimeout(timers["item-" + card.id]);
        timers["item-" + card.id] = setTimeout(send, 700);
      });
    }
  }

  /* ------------------------------------------------------------- clavier */
  var order = [];
  var cursor = -1;

  function focusCriterion(index) {
    if (!order.length) { return; }
    cursor = Math.max(0, Math.min(index, order.length - 1));
    var root = order[cursor];
    root.scrollIntoView({ block: "center" });
    root.setAttribute("tabindex", "-1");
    root.focus({ preventScroll: true });
    order.forEach(function (el) { el.classList.remove("focused"); });
    root.classList.add("focused");
  }

  /* Un raccourci ne doit jamais s'activer pendant une saisie. Le test porte sur le
   * nom de balise, sur contenteditable, et sur le rôle ARIA : taper « 0 » dans une
   * observation doit écrire « 0 », pas attribuer zéro point. */
  var TYPING_TAGS = ["input", "textarea", "select", "button", "option"];

  function isTypingContext(target) {
    if (!target || target.nodeType !== 1) { return false; }
    var tag = (target.tagName || "").toLowerCase();
    if (TYPING_TAGS.indexOf(tag) !== -1) { return true; }
    if (target.isContentEditable) { return true; }
    if (target.closest && target.closest("input, textarea, select, button, [contenteditable='true'], [contenteditable='']")) {
      return true;
    }
    var role = (target.getAttribute && target.getAttribute("role")) || "";
    return role === "textbox" || role === "checkbox" || role === "combobox";
  }

  window.nexusIsTypingContext = isTypingContext;

  function bindKeyboard() {
    document.addEventListener("keydown", function (event) {
      if (isTypingContext(event.target) || event.ctrlKey || event.metaKey
        || event.altKey) { return; }
      if (!order.length) { return; }
      var root = order[cursor] || order[0];
      var buttons = root.querySelectorAll(".score-btn");
      var key = event.key;
      if (key === "ArrowRight") { event.preventDefault(); focusCriterion(cursor + 1); return; }
      if (key === "ArrowLeft") { event.preventDefault(); focusCriterion(cursor - 1); return; }
      if (key === "f" || key === "F") {
        var full = root.querySelector(".score-btn.full");
        if (full) { event.preventDefault(); selectScore(root, full); focusCriterion(cursor + 1); }
        return;
      }
      if (key === "n" || key === "N") {
        var na = root.querySelector(".status-btn[data-status='NOT_ANSWERED']");
        if (na) { event.preventDefault(); selectScore(root, na); focusCriterion(cursor + 1); }
        return;
      }
      if (key === "e" || key === "E") {
        var chip = root.querySelector(".code-chip");
        if (chip) { event.preventDefault(); chip.focus(); }
        return;
      }
      if (key === "o" || key === "O") {
        var obs = root.querySelector("textarea.obs");
        if (obs) { event.preventDefault(); obs.focus(); }
        return;
      }
      if (/^[0-9]$/.test(key)) {
        var index = parseInt(key, 10);
        if (index < buttons.length) {
          event.preventDefault();
          selectScore(root, buttons[index]);
          focusCriterion(cursor + 1);
        }
      }
    });
  }

  /* --------------------------------------------------------------- blocs */
  function bindBlocks() {
    document.querySelectorAll("[data-block-url]").forEach(function (block) {
      var url = block.getAttribute("data-block-url");
      var area = block.querySelector("textarea");
      var save = block.querySelector(".block-save");
      if (!save || !area) { return; }
      save.addEventListener("click", function () {
        stamp("Enregistrement…");
        post(url, { content: area.value, approve: true }).then(function (body) {
          stamp("✓ Bloc conservé à " + body.saved_at);
          var badge = block.querySelector(".src-badge");
          if (badge) {
            badge.textContent = "modifié par vous";
            badge.className = "badge src-badge src-human";
          }
        }).catch(function (err) { stamp("✗ " + err.message, true); });
      });
    });
  }

  /* ------------------------------------------------------------- actions */
  function bindActions() {
    document.querySelectorAll("[data-action-url]").forEach(function (button) {
      button.addEventListener("click", function () {
        var url = button.getAttribute("data-action-url");
        var confirmText = button.getAttribute("data-confirm");
        var promptText = button.getAttribute("data-prompt");
        var payload = {};
        if (promptText) {
          var answer = window.prompt(promptText);
          if (!answer) { return; }
          payload[button.getAttribute("data-prompt-field") || "reason"] = answer;
        } else if (confirmText && !window.confirm(confirmText)) { return; }
        button.disabled = true;
        stamp("Traitement…");
        post(url, payload).then(function (body) {
          stamp("✓ Terminé");
          if (body.pdf) { window.open(body.pdf, "_blank", "noopener"); }
          window.location.reload();
        }).catch(function (err) {
          button.disabled = false;
          stamp("✗ " + err.message, true);
          window.alert(err.message);
        });
      });
    });
  }

  function bindTabs() {
    var split = document.querySelector(".split");
    document.querySelectorAll("[data-tab]").forEach(function (button) {
      button.addEventListener("click", function () {
        if (!split) { return; }
        split.classList.remove("tab-pdf", "tab-correction");
        split.classList.add("tab-" + button.getAttribute("data-tab"));
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".criterion[data-scoring-id]").forEach(function (root) {
      bindCriterion(root);
      order.push(root);
    });
    document.querySelectorAll(".item-card[data-obs-url]").forEach(bindItem);
    if (order.length) { bindKeyboard(); cursor = 0; }
    bindBlocks();
    bindActions();
    bindTabs();
    var first = document.querySelector(".criterion.pending");
    if (first && document.body.getAttribute("data-quick") === "1") {
      order.forEach(function (el, i) { if (el === first) { focusCriterion(i); } });
    }
  });
})();
