// Every page opens in light (like the app). The sun/moon switch changes only the page you're on.
(function(){
  var root=document.documentElement, key="cr-theme";
  function mode(){return root.getAttribute("data-theme")==="dark"?"dark":"light"}
  function paint(){var m=mode();root.setAttribute("data-mode",m);var b=document.querySelector(".theme");if(b){b.setAttribute("aria-label",m==="dark"?"Switch to light":"Switch to dark");b.setAttribute("aria-pressed",m==="dark"?"true":"false")}}
  try{localStorage.removeItem(key)}catch(e){}
  paint();
  document.addEventListener("DOMContentLoaded",function(){
    paint();
    var b=document.querySelector(".theme");if(!b)return;b.hidden=false;
    b.addEventListener("click",function(){var n=mode()==="dark"?"light":"dark";root.setAttribute("data-theme",n);paint()});
  });
})();
