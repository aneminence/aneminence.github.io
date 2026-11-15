'use strict';
const grid = document.getElementById('project-grid');
projects.forEach(data => {
 const card=document.createElement('button'); card.type='button'; card.className='project'; card.dataset.category=data.category; card.dataset.project=data.id;
 card.setAttribute('aria-label','查看 '+data.title+' 项目详情');
 const template=document.getElementById('visual-'+data.id);
 if(template) card.append(template.content.cloneNode(true));
 else {const visual=document.createElement('div');visual.className='project-visual visual-asset';const image=document.createElement('img');image.src=data.image;image.alt=data.alt;image.width=1200;image.height=800;visual.append(image);card.append(visual);}
 const info=document.createElement('div');info.className='project-info';const copy=document.createElement('div');
 [['span',data.type,'project-tag'],['h3',data.title,''],['p',data.subtitle,''],['p',data.status,'project-status']].forEach(([tag,text,cls])=>{const el=document.createElement(tag);el.textContent=text;el.className=cls;copy.append(el)});
 const arrow=document.createElement('span');arrow.className='project-arrow';arrow.textContent='↗';arrow.setAttribute('aria-hidden','true');info.append(copy,arrow);card.append(info);grid.append(card);
 card.querySelectorAll('img').forEach(img=>{img.loading='lazy';img.decoding='async';img.addEventListener('error',()=>{img.hidden=true;const fallback=document.createElement('p');fallback.className='image-fallback';fallback.textContent='图片暂时无法加载 · 查看项目说明 ↗';img.parentElement.append(fallback);},{once:true});});
});
document.querySelector('.work-count b').textContent=String(projects.length).padStart(2,'0');
document.querySelectorAll('.filter-chip[data-filter]').forEach(b=>{b.querySelector('span').textContent=String(projects.filter(p=>b.dataset.filter==='all'||p.category===b.dataset.filter).length).padStart(2,'0')});
const header = document.getElementById('site-header');
const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 35);
window.addEventListener('scroll',onScroll,{passive:true});onScroll();
const navToggle = document.getElementById('nav-toggle');
const nav = document.getElementById('main-nav');
navToggle.addEventListener('click',()=>{const open = nav.classList.toggle('open');navToggle.setAttribute('aria-expanded',String(open));navToggle.setAttribute('aria-label',open?'关闭导航菜单':'打开导航菜单');});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');navToggle.setAttribute('aria-expanded','false');navToggle.setAttribute('aria-label','打开导航菜单');}));
const filters = [...document.querySelectorAll('.filter-chip[data-filter]')];
const cards = [...document.querySelectorAll('.project')];
function applyFilter(filter){
 filters.forEach(b=>{const selected=b.dataset.filter===filter;b.classList.toggle('active',selected);b.setAttribute('aria-pressed',String(selected));});
 cards.forEach(card=>{card.hidden = filter!=='all' && card.dataset.category!==filter;});
 const count=cards.filter(c=>!c.hidden).length;
 document.getElementById('filter-status').textContent='显示 '+count+' 件作品';
 document.getElementById('empty-state').hidden=count>0;
}
filters.forEach(button=>button.addEventListener('click',()=>applyFilter(button.dataset.filter)));
document.getElementById('reset-filter').addEventListener('click',()=>{applyFilter('all');filters[0].focus()});
document.querySelectorAll('[data-division]').forEach(link=>link.addEventListener('click',()=>applyFilter(link.dataset.division)));
const modal = document.getElementById('project-modal');
const modalPanel = modal.querySelector('.modal-panel');
const closeBtn = document.getElementById('modal-close');
let returnFocus = null;
function openProject(id,trigger){const data=projects.find(p=>p.id===id);if(!data)return;returnFocus=trigger||document.activeElement;
 document.getElementById('modal-type').textContent=data.type;
 document.getElementById('modal-title').textContent=data.title;
 document.getElementById('modal-subtitle').textContent=data.subtitle;
 document.getElementById('modal-description').textContent=data.description;
 document.getElementById('modal-field').textContent=data.field;
 document.getElementById('modal-status').textContent=data.status;
 const image=document.getElementById('modal-image');const fallback=document.getElementById('modal-image-fallback');image.hidden=false;fallback.hidden=true;image.onerror=()=>{image.hidden=true;fallback.hidden=false;};image.src=data.image;image.alt=data.alt;
 const link=document.getElementById('modal-link');link.hidden=!data.url;if(data.url){link.href=data.url;link.textContent=data.linkLabel||'了解更多';}
 document.querySelector('main').inert=true;document.querySelector('header').inert=true;document.querySelector('footer').inert=true;
 modal.hidden=false;modalPanel.scrollTop=0;document.body.classList.add('modal-open');closeBtn.focus();}
function closeProject(){document.querySelector('main').inert=false;document.querySelector('header').inert=false;document.querySelector('footer').inert=false;modal.hidden=true;document.body.classList.remove('modal-open');if(returnFocus&&returnFocus.focus)returnFocus.focus();}
cards.forEach(card=>card.addEventListener('click',()=>openProject(card.dataset.project,card)));
closeBtn.addEventListener('click',closeProject);
document.getElementById('modal-return').addEventListener('click',closeProject);
modal.addEventListener('click',e=>{if(e.target===modal)closeProject()});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'&&!modal.hidden)closeProject();
 if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');navToggle.setAttribute('aria-expanded','false');navToggle.setAttribute('aria-label','打开导航菜单');navToggle.focus();}
 if(e.key==='Tab'&&!modal.hidden){const items=[...modalPanel.querySelectorAll('button,a,[tabindex]:not([tabindex="-1"])')].filter(n=>!n.disabled&&!n.hidden);const first=items[0],last=items[items.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}
});
document.getElementById('year').textContent=new Date().getFullYear();

applyFilter("all");

