// Tap-through examples. Without JavaScript every example and answer is simply shown.
(function(){
  document.documentElement.classList.add("js");
  document.addEventListener("DOMContentLoaded",function(){
    var exs=[].slice.call(document.querySelectorAll(".ex")), chips=document.querySelector(".chips");
    if(!exs.length||!chips)return;
    var reduce=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
    function show(i){
      exs.forEach(function(ex,j){
        ex.classList.toggle("on",i===j);
        var a=ex.querySelector(".answer"),g=ex.querySelector(".go"),t=ex.querySelector(".thinking");
        if(!g)return;a.classList.remove("shown");g.hidden=false;t.classList.remove("on");var si=ex.querySelector(".step-in");if(si)si.classList.remove("done");
      });
      [].forEach.call(chips.children,function(c,j){c.setAttribute("aria-pressed",i===j?"true":"false")});
    }
    exs.forEach(function(ex,i){
      var b=document.createElement("button");b.type="button";b.className="chip";b.textContent=ex.getAttribute("data-chip");
      b.addEventListener("click",function(){show(i)});chips.appendChild(b);
      var go=ex.querySelector(".go"),a=ex.querySelector(".answer"),t=ex.querySelector(".thinking"),si=ex.querySelector(".step-in");
      if(!go)return;
      go.addEventListener("click",function(){
        go.hidden=true;t.classList.add("on");
        setTimeout(function(){t.classList.remove("on");if(si)si.classList.add("done");a.classList.add("shown");var sc=a.querySelector(".device-screen");if(sc)sc.scrollTop=0;a.focus({preventScroll:true});
          a.scrollIntoView({behavior:reduce?"auto":"smooth",block:"nearest"});},reduce?0:900);
      });
    });
    show(0);
  });
})();
