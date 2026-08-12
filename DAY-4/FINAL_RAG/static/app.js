const $ = (s) => document.querySelector(s);
const input = $('#pdf-input'), dropZone = $('#drop-zone'), form = $('#chat-form'), question = $('#question'), send = $('#send');
function escapeHTML(value){ const d=document.createElement('div'); d.textContent=value; return d.innerHTML; }
function setReady(ready, label='DOCUMENT READY'){ question.disabled=!ready; send.disabled=!ready; $('#ready-dot').textContent=label; $('#ready-dot').style.color=ready?'#597116':'#a04b12'; }
function setProgress(value){ const rounded=Math.round(value); $('#progress-bar').style.width=`${rounded}%`; $('#progress-value').textContent=`${rounded}%`; }
function startProgress(){
  $('#progress-wrap').classList.remove('hidden');
  let progress=3;
  setProgress(progress);
  return window.setInterval(()=>{ progress=Math.min(94,progress+(94-progress)*.085+Math.random()*1.6); setProgress(progress); },700);
}
function resetUploader(){
  input.value=''; $('#file-card').classList.add('hidden'); $('#progress-wrap').classList.add('hidden'); dropZone.classList.remove('hidden'); setProgress(0); setReady(false,'AWAITING DOCUMENT');
}
function addMessage(content, type, sources=[]){ const empty=$('.empty-state'); if(empty) empty.remove(); const m=document.createElement('div');m.className=`message ${type}`;m.innerHTML=escapeHTML(content);$('#messages').append(m); if(sources.length){const meta=document.createElement('div');meta.className='source';meta.textContent=`SOURCES · PAGE${sources.length>1?'S':''} ${sources.join(', ')}`;$('#messages').append(meta)} $('#messages').scrollTop=$('#messages').scrollHeight; return m; }
async function upload(file){
  if(!file || (!file.type.includes('pdf') && !file.name.toLowerCase().endsWith('.pdf'))){alert('Please select a PDF document.');return}
  $('#file-name').textContent=file.name; $('#file-meta').textContent='Reading and indexing…'; $('#file-card').classList.remove('hidden'); dropZone.classList.add('hidden'); setReady(false,'PROCESSING DOCUMENT');
  const timer=startProgress(), data=new FormData(); data.append('file',file);
  try{const r=await fetch('/api/documents',{method:'POST',body:data});const result=await r.json();if(!r.ok)throw new Error(result.detail);window.clearInterval(timer);setProgress(100);$('#file-meta').textContent=`${result.pages} pages · ${result.chunks} passages indexed`;setReady(true);addMessage(`Your document is ready. I’ve indexed ${result.chunks} passages across ${result.pages} pages. What would you like to know?`,'ai')}
  catch(e){window.clearInterval(timer);$('#progress-wrap').classList.add('hidden');setProgress(0);$('#file-meta').textContent=e.message;setReady(false,'UPLOAD FAILED')}
}
$('#browse').onclick=()=>input.click();dropZone.onclick=(e)=>{if(e.target.id!=='browse')input.click()};input.onchange=()=>upload(input.files[0]);['dragover','dragleave','drop'].forEach(event=>dropZone.addEventListener(event,e=>{e.preventDefault();dropZone.classList.toggle('drag',event==='dragover')}));dropZone.addEventListener('drop',e=>upload(e.dataTransfer.files[0]));$('#remove-file').onclick=resetUploader;
const themeToggle=$('#theme-toggle');
function applyTheme(theme){document.documentElement.dataset.theme=theme;localStorage.setItem('aperture-theme',theme);themeToggle.setAttribute('aria-label',`Switch to ${theme==='dark'?'light':'dark'} mode`)}
applyTheme(localStorage.getItem('aperture-theme') || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'));
themeToggle.onclick=()=>applyTheme(document.documentElement.dataset.theme==='dark'?'light':'dark');
form.onsubmit=async(e)=>{e.preventDefault();const q=question.value.trim();if(!q)return;addMessage(q,'user');question.value='';question.disabled=true;send.disabled=true;const waiting=addMessage('Thinking…','ai');try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});const data=await r.json();if(!r.ok)throw new Error(data.detail);waiting.remove();addMessage(data.answer,'ai',data.sources)}catch(err){waiting.textContent=err.message}finally{question.disabled=false;send.disabled=false;question.focus()}};
