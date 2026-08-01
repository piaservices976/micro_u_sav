(function() {
  function insertBanner() {
    if (!window.location.pathname.includes('/login')) return;
    if (document.getElementById('pia-login-banner')) return;
    if (!document.body || !document.body.firstElementChild) return;
    var banner = document.createElement('div');
    banner.id = 'pia-login-banner';
    banner.innerHTML = 'BIENVENUE SUR LE PORTAIL DE GESTION DU GROUPE PIA :<br>KALAGA MICRO-U PIA SERVICES CANOPEE OCEAN INDIEN GENIUS INVEST';
    banner.style.cssText = 'display:block;width:100%;box-sizing:border-box;background:#ffffff;border-bottom:3px solid #B7410E;text-align:center;font-weight:800;letter-spacing:0.5px;color:#B7410E;padding:18px 16px;line-height:1.6;font-size:clamp(14px, 2vw, 26px);';
    document.body.insertBefore(banner, document.body.firstChild);
  }
  insertBanner();
  var observer = new MutationObserver(insertBanner);
  observer.observe(document.documentElement, {childList: true, subtree: true});
})();
