// Every page opens in light (like the app). The sun/moon switch changes only the page you're on.
(function(){
  var root=document.documentElement, key="cr-theme";
  function mode(){return root.getAttribute("data-site")==="dark"?"dark":"light"}
  function paint(){var m=mode();root.setAttribute("data-mode",m);var b=document.querySelector(".theme");if(b){b.setAttribute("aria-label",m==="dark"?"Switch to light":"Switch to dark");b.setAttribute("aria-pressed",m==="dark"?"true":"false")}}
  try{localStorage.removeItem(key)}catch(e){}
  paint();
  document.addEventListener("DOMContentLoaded",function(){
    paint();
    var b=document.querySelector(".theme");if(!b)return;b.hidden=false;
    b.addEventListener("click",function(){var n=mode()==="dark"?"light":"dark";root.setAttribute("data-site",n);paint()});
  });
})();
// Home page: each phone shows the app "thinking", then its answer appears line by line, once it scrolls into view.
document.addEventListener("DOMContentLoaded",function(){
  var phones=document.querySelectorAll(".h-ph");
  if(!phones.length||!("IntersectionObserver" in window))return;
  try{if(window.matchMedia("(prefers-reduced-motion: reduce)").matches)return}catch(e){}
  phones.forEach(function(ph,i){
    var screen=ph.querySelector(".h-ph-screen"),img=screen&&screen.querySelector("img");if(!img){if(screen&&screen.classList.contains("live"))live(ph,screen);return}
    var cover=document.createElement("span");cover.className="h-cover";cover.setAttribute("aria-hidden","true");
    cover.innerHTML='<span class="h-dots"><i></i><i></i><i></i></span>';
    function place(){var w=screen.clientWidth;cover.style.top=(img.classList.contains("h-shift")?30:Math.round(30+w*0.165))+"px"}
    window.addEventListener("resize",place);
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.disconnect();screen.appendChild(cover);place();cover.offsetWidth;ph.classList.add("play")}})},{threshold:.3});
    io.observe(ph);
  });
});

// Hero phones: the question is typed in, the app thinks, then the answer types out.
function live(ph,screen){
  var front=ph.classList.contains("h-ph-front");
  var els=[].slice.call(screen.querySelectorAll("[data-type]"));
  var parts=[].slice.call(screen.querySelectorAll(".lv-a,.lv-dots"));

  function wait(ms){return new Promise(function(r){setTimeout(r,ms)})}
  function type(el,byWord,speed){
    var full=el.getAttribute("data-type"),bits=byWord?full.split(/(\s+)/):full.split(""),i=0;
    el.classList.add("lv-caret");
    return new Promise(function(r){(function step(){
      if(i>=bits.length){el.classList.remove("lv-caret");return r()}
      el.textContent+=bits[i++];setTimeout(step,byWord&&/\s/.test(bits[i-1])?0:speed)})()});
  }
  function show(sel){var e=screen.querySelector(sel);if(e)e.classList.remove("lv-hide");return e}
  function hide(sel){var e=screen.querySelector(sel);if(e)e.classList.add("lv-hide")}
  function run(){
    els.forEach(function(e){e.textContent=""});
    parts.forEach(function(e){e.classList.add("lv-hide")});
    screen.classList.add("lv-run");
    var p=wait(front?2600:500);
    if(!front){
      p=p.then(function(){return type(screen.querySelector(".lv-q"),false,55)})
       .then(function(){show(".lv-dots");return wait(1300)})
       .then(function(){hide(".lv-dots");show(".lv-a");return type(screen.querySelector(".lv-a p"),true,70)});
    }else{
      p=p.then(function(){return type(screen.querySelector(".lv-msg"),false,22)})
       .then(function(){var b=screen.querySelector(".lv-btn");b.classList.add("lv-press");return wait(450)})
       .then(function(){screen.querySelector(".lv-btn").classList.remove("lv-press");show(".lv-dots");return wait(1300)})
       .then(function(){hide(".lv-dots");show(".lv-verdict");return type(screen.querySelector(".lv-verdict b"),true,90)})
       .then(function(){return type(screen.querySelector(".lv-verdict p"),true,60)})
       .then(function(){show(".lv-next");return type(screen.querySelector(".lv-next p"),true,60)});
    }
  }
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.disconnect();run()}})},{threshold:.3});
  io.observe(ph);
}
