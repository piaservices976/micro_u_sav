(function() {
  function insertBanner() {
    if (!window.location.pathname.includes('/login')) return;
    if (document.getElementById('pia-login-banner')) return;
    if (!document.body || !document.body.firstElementChild) return;
    var banner = document.createElement('div');
    banner.id = 'pia-login-banner';
    banner.innerHTML = 'BIENVENUE SUR LE PORTAIL DE GESTION DU GROUPE PIA :<br>KALAGA MICRO-U PIA SERVICES CANOPEE OCEAN INDIEN GENIUS INVEST';
    banner.style.cssText = 'text-align:center;font-weight:700;font-size:30px;color:#B7410E;max-width:900px;margin:20px auto;padding:14px 20px;line-height:1.4;';
    document.body.insertBefore(banner, document.body.firstChild);
  }
  insertBanner();
  var observer = new MutationObserver(insertBanner);
  observer.observe(document.documentElement, {childList: true, subtree: true});
})();
