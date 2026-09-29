async function refresh(){
 const p=await fetch("/api/projects").then(r=>r.json());
 const m=await fetch("/api/metrics").then(r=>r.json());
 const avg=p.reduce((s,x)=>s+x.progress,0)/(p.length||1);
 const d=p.reduce((s,x)=>s+(x.delayed_activities||0),0);
 document.querySelector("#stats").innerHTML='<div class="stat"><small>Projects</small><br><b>'+p.length+'</b></div><div class="stat"><small>Average progress</small><br><b>'+(avg*100).toFixed(1)+'%</b></div><div class="stat"><small>Delayed activities</small><br><b>'+d+'</b></div>';
 document.querySelector("#rows").innerHTML=p.map(x=>'<tr><td>'+x.name+'</td><td>'+(x.progress*100).toFixed(1)+'%</td><td>'+x.delayed_activities+'</td><td>'+x.status+'</td></tr>').join("");
 document.querySelector("#metrics").textContent=JSON.stringify(m,null,2);
}
refresh();