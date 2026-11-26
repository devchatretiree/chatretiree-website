// Light/dark switch, remembered on this device only. The page works without it.
(function(){
  var root=document.documentElement, key="cr-theme";
  function mode(){var t=root.getAttribute("data-theme");if(t)return t;return window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}
  function paint(){var m=mode();root.setAttribute("data-mode",m);var b=document.querySelector(".theme");if(b){b.setAttribute("aria-label",m==="dark"?"Switch to light":"Switch to dark");b.setAttribute("aria-pressed",m==="dark"?"true":"false")}}
  try{var s=localStorage.getItem(key);if(s==="light"||s==="dark")root.setAttribute("data-theme",s)}catch(e){}
  paint();
  document.addEventListener("DOMContentLoaded",function(){
    paint();
    var b=document.querySelector(".theme");if(!b)return;b.hidden=false;
    b.addEventListener("click",function(){var n=mode()==="dark"?"light":"dark";root.setAttribute("data-theme",n);try{localStorage.setItem(key,n)}catch(e){}paint()});
  });
  if(window.matchMedia)matchMedia("(prefers-color-scheme: dark)").addEventListener("change",paint);
})();
