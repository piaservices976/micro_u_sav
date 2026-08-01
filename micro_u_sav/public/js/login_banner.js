(function() {
  var ACCENT = '#B7410E';

  function injectStyles() {
    if (document.getElementById('pia-login-banner-style')) return;
    var style = document.createElement('style');
    style.id = 'pia-login-banner-style';
    style.textContent =
      '#pia-login-banner .pia-companies{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 20px;max-width:820px;margin:14px auto 0 auto;padding:0 16px;}' +
      '#pia-login-banner .pia-col{display:flex;flex-direction:column;align-items:center;gap:10px;}' +
      '#pia-login-banner .pia-row{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600;color:#7a2e15;}' +
      '#pia-login-banner .pia-logo{width:26px;height:26px;border-radius:6px;background:#f3ded6;color:' + ACCENT + ';display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex-shrink:0;}' +
      '.navbar-brand{display:none !important;}' +
      '.btn-primary{background-color:' + ACCENT + ' !important;border-color:' + ACCENT + ' !important;}' +
      '@media (max-width:640px){#pia-login-banner .pia-companies{grid-template-columns:1fr;}}';
    document.head.appendChild(style);
  }

  function insertBanner() {
    if (document.getElementById('pia-login-banner')) return;
    if (!document.body || !document.body.firstElementChild) return;
    injectStyles();

    var companies = [
      ['KALAGA', 'MICRO-U'],
      ['PIA SERVICES', 'CANOPEE'],
      ['OCEAN INDIEN', 'GENIUS INVEST']
    ];
    var colsHtml = companies.map(function(col) {
      var rowsHtml = col.map(function(name) {
        var initial = name.trim().charAt(0);
        return '<div class="pia-row"><span class="pia-logo">' + initial + '</span><span>' + name + '</span></div>';
      }).join('');
      return '<div class="pia-col">' + rowsHtml + '</div>';
    }).join('');

    var banner = document.createElement('div');
    banner.id = 'pia-login-banner';
    banner.innerHTML =
      '<div style="font-weight:800;letter-spacing:0.5px;font-size:clamp(14px,2vw,24px);">BIENVENUE SUR LE PORTAIL DE GESTION DU GROUPE PIA :</div>' +
      '<div class="pia-companies">' + colsHtml + '</div>';
    banner.style.cssText = 'display:block;width:100%;box-sizing:border-box;background:#ffffff;border-bottom:3px solid ' + ACCENT + ';text-align:center;color:' + ACCENT + ';padding:18px 16px;line-height:1.5;';
    document.body.insertBefore(banner, document.body.firstChild);
  }

  function replaceLoginHeading() {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    var node;
    while ((node = walker.nextNode())) {
      if (node.nodeValue.indexOf('Se connecter') > -1 && node.nodeValue.indexOf('Frappe') > -1) {
        node.nodeValue = node.nodeValue.replace(/Se connecter.*Frappe/, 'Connexion aux Applications');
      }
    }
  }

  var recoloredLogos = typeof WeakSet !== 'undefined' ? new WeakSet() : null;
  function recolorLogos() {
    var imgs = document.querySelectorAll('img.app-logo');
    imgs.forEach(function(img) {
      if (recoloredLogos) {
        if (recoloredLogos.has(img)) return;
        recoloredLogos.add(img);
      } else if (img.dataset.piaRecolored) {
        return;
      } else {
        img.dataset.piaRecolored = '1';
      }
      fetch(img.src).then(function(r){ return r.text(); }).then(function(svgText) {
        var recolored = svgText.replace(/#171717/gi, ACCENT);
        var blob = new Blob([recolored], {type: 'image/svg+xml'});
        img.src = URL.createObjectURL(blob);
      }).catch(function(){});
    });
  }

  function run() {
    insertBanner();
    replaceLoginHeading();
    recolorLogos();
  }

  run();
  var observer = new MutationObserver(run);
  observer.observe(document.documentElement, {childList: true, subtree: true});
})();
