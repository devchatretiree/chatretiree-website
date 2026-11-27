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
  var parts=[].slice.call(screen.querySelectorAll(".lv-a,.lv-dots,.lv-after"));

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
       .then(function(){hide(".lv-dots");show(".lv-a");return type(screen.querySelector(".lv-a p"),true,70)})
       .then(function(){return wait(350)}).then(function(){[].forEach.call(screen.querySelectorAll(".lv-after"),function(e){e.classList.remove("lv-hide")})});
    }else{
      var cmp=screen.querySelector(".lv-front"),box=cmp.querySelector(".lv-in"),sent=screen.querySelector(".lv-sent");
      sent.classList.add("lv-hide");box.classList.add("lv-ph");box.textContent="Paste or type it here";
      p=p.then(function(){box.textContent="";box.classList.remove("lv-ph");cmp.classList.add("lv-typing");return type(box,false,22)})
       .then(function(){var b=screen.querySelector(".lv-btn");b.classList.add("lv-press");return wait(450)})
       .then(function(){screen.querySelector(".lv-btn").classList.remove("lv-press");cmp.classList.remove("lv-typing");box.textContent="Paste or type it here";box.classList.add("lv-ph");sent.classList.remove("lv-hide");return wait(350)})
       .then(function(){show(".lv-dots");return wait(1300)})
       .then(function(){hide(".lv-dots");show(".lv-verdict");return type(screen.querySelector(".lv-verdict b"),true,90)})
       .then(function(){return type(screen.querySelector(".lv-verdict p"),true,60)})
       .then(function(){show(".lv-next");return type(screen.querySelector(".lv-next p"),true,60)});
    }
  }
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.disconnect();run()}})},{threshold:.3});
  io.observe(ph);
}
// The sky follows the visitor's own clock, like the app: dawn, day, golden hour, dusk and night.
// The sun (or moon, in its real phase) sits on a low arc near the top. Nothing about the visitor is sent anywhere.
document.addEventListener("DOMContentLoaded",function(){
  var heroes=document.querySelectorAll(".h-hero");if(!heroes.length)return;
  var now=new Date(),h=now.getHours()+now.getMinutes()/60;
  var sky=h>=6&&h<9?"dawn":h>=9&&h<16?"day":h>=16&&h<18?"golden":h>=18&&h<20.5?"dusk":"night";
  var dark=sky==="dusk"||sky==="night";
  var t=dark?((((h-18)%24)+24)%24)/12:(h-6)/13;t=Math.min(1,Math.max(0,t));
  var x=.12+.76*t,y=.075-.045*Math.sin(Math.PI*t);
  // Moon phase: days since a known new moon, over the 29.53-day cycle.
  var f=((now.getTime()-Date.UTC(2000,0,6,18,14))/864e5/29.530588853)%1;if(f<0)f+=1;
  var r=16,k=Math.cos(2*Math.PI*f),wax=f<.5,rx=Math.max(.01,Math.abs(k)*r);
  var d=f<.02||f>.98?"":"M20 4A16 16 0 0 "+(wax?1:0)+" 20 36A"+rx.toFixed(2)+" 16 0 0 "+(wax?(k>0?0:1):(k>0?1:0))+" 20 4z";
  // The Home screen picture follows the same clock: the app's evening sky after dark.
  if(dark)[].forEach.call(document.querySelectorAll('img[src*="app/home.webp"]'),function(im){im.src=im.src.replace("app/home.webp","app/home-night.webp")});
  heroes.forEach(function(hero){
    hero.setAttribute("data-sky",sky);
    var body=hero.querySelector(".sky-body");if(body){body.style.setProperty("--x",x.toFixed(3));body.style.setProperty("--y",y.toFixed(3))}
    var lit=hero.querySelector(".moon-lit");if(lit){if(d)lit.setAttribute("d",d);else lit.remove()}
    var stars=hero.querySelector(".sky-stars");
    if(stars&&dark&&!stars.childNodes.length){
      var seed=7;function rnd(){seed=(seed*16807)%2147483647;return seed/2147483647}
      for(var i=0;i<46;i++){var s=document.createElement("i");s.style.left=(rnd()*100).toFixed(1)+"%";s.style.top=(rnd()*100).toFixed(1)+"%";
        var z=rnd()<.15?3:2;s.style.width=s.style.height=z+"px";s.style.animationDelay=(-rnd()*4).toFixed(2)+"s";s.style.animationDuration=(3+rnd()*4).toFixed(2)+"s";stars.appendChild(s)}
    }
  });
});
