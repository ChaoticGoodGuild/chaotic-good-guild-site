/* Join the Guild: sends the signup form to Netlify Forms without leaving the page, and fills in the visitor's
   alignment if they've taken the test on this device. Nothing is sent until they press the button.
   If the test last came out Evil, the form steps aside for a second-chance letter instead. */
(function () {
  const saved = () => { try { return JSON.parse(localStorage.getItem("cgg.alignment")); } catch (e) { return null; } };
  function apply() {
    const s = saved(), evil = !!(s && /-evil$/.test(s.slug || ""));
    document.querySelectorAll("section.cj").forEach(sec => {
      const open = sec.querySelector(".cj-open"), shut = sec.querySelector(".cj-evil");
      if (!open || !shut || sec.querySelector(".cgg-join.done")) return;
      open.hidden = evil; shut.hidden = !evil;
      const sel = sec.querySelector('select[name="alignment"]');
      if (sel && !evil) sel.value = (s && s.slug) || sec.querySelector("form").dataset.alignment || "";
    });
  }
  apply();
  document.addEventListener("cgg:alignment", apply);

  document.querySelectorAll("form.cgg-join").forEach(form => {
    const msg = form.querySelector(".cj-msg"), btn = form.querySelector("button[type=submit]");
    form.addEventListener("submit", async e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      btn.disabled = true; msg.textContent = "Sealing your letter…"; msg.className = "cj-msg";
      try {
        const r = await fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
                                     body: new URLSearchParams(new FormData(form)).toString() });
        if (!r.ok) throw new Error(r.status);
        form.classList.add("done");
        form.innerHTML = '<p class="cj-done-h">Welcome to the Guild.</p><p class="cj-done">Reynard has your name. Watch for his first letter, and keep an eye on the night sky.</p>';
      } catch (err) {
        btn.disabled = false;
        msg.textContent = "The raven got lost on the way. Please try again in a moment.";
        msg.className = "cj-msg err";
      }
    });
  });
})();
