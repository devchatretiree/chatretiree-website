// Light by default (like the app). The sun/moon switch is remembered on this device only.
(function(){
  var root=document.documentElement, key="cr-theme";
  function mode(){return root.getAttribute("data-theme")==="dark"?"dark":"light"}
  function paint(){var m=mode();root.setAttribute("data-mode",m);var b=document.querySelector(".theme");if(b){b.setAttribute("aria-label",m==="dark"?"Switch to light":"Switch to dark");b.setAttribute("aria-pressed",m==="dark"?"true":"false")}}
  try{var s=localStorage.getItem(key);if(s==="light"||s==="dark")root.setAttribute("data-theme",s)}catch(e){}
  paint();
  document.addEventListener("DOMContentLoaded",function(){
    paint();
    var b=document.querySelector(".theme");if(!b)return;b.hidden=false;
    b.addEventListener("click",function(){var n=mode()==="dark"?"light":"dark";root.setAttribute("data-theme",n);try{localStorage.setItem(key,n)}catch(e){}paint()});
  });
})();
