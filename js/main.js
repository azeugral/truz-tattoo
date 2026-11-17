(function(){
'use strict';
var WA='5567998135638';

/* HERO: cada peça abre num detalhe da sombra e afasta até o fechamento inteiro */
var HP=[
  {src:'img/h/costas.webp',peca:'Fechamento de costas',det:'caveira e serpente',alt:'Fechamento de costas com caveira e serpente em preto e cinza',fx:.56,fy:.16,z:3.4},
  {src:'img/h/braco.webp',peca:'Fechamento de braço',det:'leão e rosa',alt:'Fechamento de braço com leão e rosa em preto e cinza',fx:.64,fy:.25,z:3.2},
  {src:'img/h/pescoco.webp',peca:'Pescoço',det:'preto e cinza',alt:'Tatuagem no pescoço em preto e cinza',fx:.46,fy:.55,z:3.2},
  {src:'img/h/perna.webp',peca:'Perna',det:'caveira com cocar',alt:'Caveira com cocar na perna em preto e cinza',fx:.5,fy:.8,z:3}
];
var hImg=document.getElementById('hImg'),hPeca=document.getElementById('hPeca'),hDet=document.getElementById('hDet'),hFio=document.getElementById('hFio');
var pre=HP.map(function(p){var i=new Image();i.src=p.src;return i});
var hi=0,anim=null;
var reduz=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function abrirPeca(k){
  var p=HP[k];
  hImg.src=p.src;hImg.alt=p.alt;
  hPeca.textContent=p.peca;hDet.textContent=p.det;
  if(reduz||!hImg.animate)return;
  hFio.animate([{transform:'scaleX(0)'},{transform:'scaleX(1)'}],{duration:4800,easing:'linear',fill:'forwards'});
  var lim=(p.z-1)/(2*p.z)*100,cl=function(n){return Math.max(-lim,Math.min(lim,n))};
  var tx=cl((.5-p.fx)*100), ty=cl((.5-p.fy)*100);
  if(anim)anim.cancel();
  anim=hImg.animate([
    {transform:'scale('+p.z+') translate('+tx+'%,'+ty+'%)',opacity:.0,offset:0},
    {transform:'scale('+p.z+') translate('+tx+'%,'+ty+'%)',opacity:1,offset:.12},
    {transform:'scale(1) translate(0,0)',opacity:1,offset:1}
  ],{duration:1450,easing:'cubic-bezier(.16,.84,.32,1)',fill:'forwards'});
}
abrirPeca(0);
setInterval(function(){
  if(document.hidden)return;
  hi=(hi+1)%HP.length;
  if(reduz||!hImg.animate){abrirPeca(hi);return}
  var out=hImg.animate([{opacity:1},{opacity:0}],{duration:260,easing:'ease-in',fill:'forwards'});
  out.onfinish=function(){abrirPeca(hi)};
},4800);

/* TRABALHOS */
var P=[
 ['DAGm4IgRZGO_0','fech','Fechamento de costas com caveira e serpente'],
 ['C1pG8jFO1JE_0','real','Leão com coroa de espinhos no ombro'],
 ['CsGr8QBLAwj_0','ret','Retrato realista em preto e cinza'],
 ['CsEHPBIuj-d_0','fech','Fechamento de braço com leão e rosa'],
 ['C22YGRTuKdp_0','rel','Cristo com coroa de espinhos no ombro'],
 ['CsjJsKyO-2f_1','real','Medusa em preto e cinza'],
 ['DAHh4-1NBfL_0','real','Tatuagem no pescoço em preto e cinza'],
 ['CxDgQc1Oq0O_0','fech','Fechamento de braço com lobo e mulher'],
 ['Ct_n5KFuU7U_0','ret','Retrato de rapper com microfone'],
 ['CdIL2e0uHuY_3','real','Gladiador no antebraço'],
 ['C1wg6A5Ij59_0','rel','Cristo no antebraço'],
 ['Ch53UMENJMA_0','fina','Lírio fine line com escrita'],
 ['CxZCrGQNLct_0','fech','Fechamento de costas em andamento'],
 ['C14WL-fvsYZ_0','real','Leão realista no antebraço'],
 ['CsB21y4umL-_0','real','Tatuagem chicana em preto e cinza'],
 ['Cy5-5DsOjhX_0','rel','Cristo e Nossa Senhora'],
 ['CthWJQOR6XP_0','rel','Cristo com terço'],
 ['Ciu1YBcOzzg_1','fina','Borboleta fine line'],
 ['C22tjj4xG7__0','fech','Fechamento de braço com escrita'],
 ['Cw2zRa2OHvZ_0','fech','Elefante no antebraço, homenagem ao filho'],
 ['DRhSv9iDmEK_0','ret','Retrato de mãe na cabeça'],
 ['C10KWoJpJNR_2','real','Olho realista'],
 ['CzljG7fOL_Q_0','fech','Fechamento de braço com rosas e relógio'],
 ['DAHySUENS5g_0','fina','Ramo fine line nas costas'],
 ['CikQVrgOPVf_0','rel','Leão com cruz no ombro'],
 ['CcEjav2tmQ-_0','real','Leoa e filhotes com flores'],
 ['C1reMXANoOv_0','ret','Retrato de cachorro'],
 ['CxNzbNxObFv_0','fech','Peito com mapa e bússola'],
 ['C2zpWMwOsHM_0','real','Cobertura no antebraço'],
 ['CzpUNAfxcZp_0','real','Anjo e máscaras de teatro'],
 ['C3acuF-uNM7_0','real','Escorpião feito à mão livre'],
 ['CevsElfOd-__0','real','Peito em andamento'],
 ['C0R-PmUx_S4_0','real','Personagens de desenho nas costas'],
 ['Cby9WJ4O-kP_0','real','Caveira com cocar na perna'],
 ['CikRPmAuFcW_0','fina','Borboleta delicada no braço'],
 ['C1uXlfJB3GL_0','real','Braço com bússola, coroa e relógio'],
 ['Czo3UAvR4o2_0','real','Bússola no antebraço'],
 ['CxV3suzx4Kc_0','fina','Símbolos pequenos no braço']
];
var NOME={fech:'Fechamento',real:'Realismo',rel:'Religioso',ret:'Retrato',fina:'Fine line e escrita'};
var grade=document.getElementById('grade'),mais=document.getElementById('mais');
var filtro='todos',mostra=24,lista=[];
function render(){
  lista=P.filter(function(p){return filtro==='todos'||p[1]===filtro});
  grade.innerHTML='';
  lista.slice(0,mostra).forEach(function(p,i){
    var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Ampliar: '+p[2]);
    var im=document.createElement('img');im.src='img/g/'+p[0]+'.webp';im.alt=p[2];im.width=640;im.height=800;im.draggable=false;
    b.appendChild(im);b.addEventListener('click',function(){abrir(i)});grade.appendChild(b);
  });
  mais.hidden=lista.length<=mostra;
}
document.querySelectorAll('.filtros button').forEach(function(b){
  b.addEventListener('click',function(){
    document.querySelectorAll('.filtros button').forEach(function(x){x.classList.toggle('on',x===b)});
    filtro=b.dataset.f;mostra=24;render();
  });
});
document.querySelectorAll('.area').forEach(function(a){
  a.addEventListener('click',function(){
    var b=document.querySelector('.filtros button[data-f="fech"]');if(b)b.click();
  });
});
mais.addEventListener('click',function(){mostra+=24;render()});
render();

/* LIGHTBOX */
var lb=document.getElementById('lb'),lbImg=document.getElementById('lbImg'),lbCap=document.getElementById('lbCap'),cur=0;
function mostrar(){var p=lista[cur];lbImg.src='img/g/'+p[0]+'.webp';lbImg.alt=p[2];lbCap.textContent=p[2]+' · '+NOME[p[1]]}
function abrir(i){cur=i;mostrar();lb.hidden=false;document.body.style.overflow='hidden'}
function fechar(){lb.hidden=true;document.body.style.overflow=''}
document.getElementById('lbX').onclick=fechar;
document.getElementById('lbP').onclick=function(){cur=(cur-1+lista.length)%lista.length;mostrar()};
document.getElementById('lbS').onclick=function(){cur=(cur+1)%lista.length;mostrar()};
lb.addEventListener('click',function(e){if(e.target===lb)fechar()});
document.addEventListener('keydown',function(e){
  if(lb.hidden)return;
  if(e.key==='Escape')fechar();
  if(e.key==='ArrowLeft')document.getElementById('lbP').click();
  if(e.key==='ArrowRight')document.getElementById('lbS').click();
});
document.getElementById('lbQ').onclick=function(){
  var p=lista[cur];fechar();
  var f=document.getElementById('form');
  f.ideia.value='Quero algo na linha desta peça do portfólio: '+p[2].toLowerCase()+'.';
  var t={fech:'Fechamento',real:null,rel:'Religioso',ret:'Retrato',fina:'Fine line'}[p[1]];
  if(t){var r=f.querySelector('input[name="tema"][value="'+t+'"]');if(r)r.checked=true}
  document.getElementById('marcar').scrollIntoView({behavior:'smooth'});
  setTimeout(function(){f.nome.focus({preventScroll:true})},700);
};

/* FORMULÁRIO → WhatsApp */
var form=document.getElementById('form');
form.addEventListener('submit',function(e){
  e.preventDefault();
  var nome=form.nome.value.trim(),err=form.querySelector('.erro');
  if(!nome){err.hidden=false;form.nome.focus();return}
  err.hidden=true;
  var v=function(n){var el=form.querySelector('[name="'+n+'"]:checked');return el?el.value:''};
  var L=['Olá, Truz! Sou *'+nome+'* e quero um orçamento.',''];
  if(v('tema'))L.push('*Tema/estilo:* '+v('tema'));
  L.push('*Cobertura:* '+(v('cob')||'Não'));
  if(form.local.value.trim())L.push('*Local:* '+form.local.value.trim());
  if(form.tam.value)L.push('*Tamanho:* '+form.tam.value);
  if(form.disp.value)L.push('*Disponibilidade:* '+form.disp.value);
  if(form.ideia.value.trim())L.push('*Ideia:* '+form.ideia.value.trim());
  L.push('','(pedido enviado pelo site)');
  window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(L.join('\n')),'_blank','noopener');
});
form.nome.addEventListener('input',function(){if(form.nome.value.trim())form.querySelector('.erro').hidden=true});

/* entrada leve ao rolar */
if('IntersectionObserver' in window&&!reduz){
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('vis');io.unobserve(en.target)}})},{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.sec h2,.sec .lead,.areas,.passos3,.sobre,.mapa,.info,.passos,.form').forEach(function(el){el.classList.add('rev');io.observe(el)});
}
})();
