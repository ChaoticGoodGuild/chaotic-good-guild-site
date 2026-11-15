/* The Guild is for adults. On a first visit this asks once whether the visitor is 18 or older and remembers a yes.
   The page underneath stays in place (search engines treat an age check like this as fine). */
(function () {
  const root = document.documentElement;
  if (!root.classList.contains("cgg-gate")) return;
  const behind = Array.from(document.body.children);
  behind.forEach(el => el.setAttribute("inert", ""));
  const box = document.createElement("div");
  box.className = "gate";
  box.innerHTML =
    '<div class="gate-card" role="dialog" aria-modal="true" aria-labelledby="gateH" aria-describedby="gateP">' +
    '<img src="/assets/logo.png" alt="" width="345" height="360">' +
    '<h2 id="gateH">Grown misfits only</h2>' +
    '<p id="gateP">Some of the Guild\'s tales are written for adults. Before you come in: are you 18 or older?</p>' +
    '<div class="gate-go"><button type="button" class="back-btn" data-yes>I\'m 18 or older</button>' +
    '<button type="button" class="sp-ghost" data-no>I\'m not</button></div>' +
    '<p class="gate-fine"><a href="/privacy/">Privacy</a></p></div>';
  document.body.appendChild(box);
  box.querySelector("[data-yes]").focus();
  box.querySelector("[data-yes]").addEventListener("click", () => {
    try { localStorage.setItem("cgg.adult", "yes"); } catch (e) {}
    root.classList.remove("cgg-gate");
    behind.forEach(el => el.removeAttribute("inert"));
    box.remove();
  });
  box.querySelector("[data-no]").addEventListener("click", () => {
    box.querySelector(".gate-card").innerHTML =
      '<img src="/assets/logo.png" alt="" width="345" height="360">' +
      '<h2 id="gateH" tabindex="-1">Not yet, then</h2>' +
      '<p>The Guild\'s door will be here when you\'re 18. Until then: be kind, stay curious, and make the good kind of trouble.</p>';
    box.querySelector("#gateH").focus();
  });
})();
