// Running inside the securetechav.com shell? The site header is already
// above us, so flag it for the CSS that hides this app's own top bar.
try { if (window.self !== window.top) document.documentElement.classList.add('st-embedded'); } catch (e) { document.documentElement.classList.add('st-embedded'); }

// Local-only persistence adapter. No Cisco account is impersonated or required.
(() => {
  const key = 'webex-clone-designs-v1';
  const read = () => { try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch { return []; } };
  const current = () => window.room?.roomPlan;
  function designURL(plan) {
    const encoded=btoa(String.fromCharCode(...new TextEncoder().encode(JSON.stringify(plan))));
    const url=new URL(location.href);url.search='';url.searchParams.set('design',encoded);url.hash='#/room/mediumroom/summary';
    return url.href;
  }
  let dialog;
  const button = (text, action) => { const el=document.createElement('button');el.type='button';el.textContent=text;el.onclick=action;return el; };
  const download = (plan) => {
    const url=URL.createObjectURL(new Blob([JSON.stringify(plan,null,2)],{type:'application/json'}));
    const a=document.createElement('a');a.href=url;a.download=(plan.title || 'workspace').replace(/[^a-z0-9 -]/gi,'')+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  };
  function validate(plan) {
    if(!plan || typeof plan!=='object' || Array.isArray(plan) || !plan.roomType || !plan.roomShape || !Number.isFinite(plan.roomShape.width) || !Number.isFinite(plan.roomShape.length)) throw new Error('Choose a room JSON file exported from this app.');
    if(JSON.stringify(plan).length>1000000) throw new Error('Room files must be smaller than 1 MB.');
    return plan;
  }
  async function load(plan) {
    validate(plan);dialog?.close();
    if(!document.querySelector('main.room-designer')) {
      location.hash='#/room/mediumroom/summary';
      await new Promise((resolve,reject)=>{let n=0;const id=setInterval(()=>{if(document.querySelector('main.room-designer') && current()){clearInterval(id);resolve();}else if(++n>150){clearInterval(id);reject(new Error('Room editor did not load.'));}},100);});
    }
    const transfer=new DataTransfer();transfer.items.add(new File([JSON.stringify(plan)],'workspace.json',{type:'application/json'}));
    document.querySelector('main.room-designer').dispatchEvent(new DragEvent('drop',{bubbles:true,cancelable:true,dataTransfer:transfer}));
  }
  function save() {
    const plan=current();if(!plan) return open('Open a room first to save a design.');
    const name=prompt('Design name',plan.title || 'My workspace');if(!name?.trim())return;
    const designs=read();const existing=designs.find(d=>d.name===name.trim());
    const entry={id:existing?.id || crypto.randomUUID(),name:name.trim(),updated:new Date().toISOString(),plan:JSON.parse(JSON.stringify({...plan,title:name.trim()}))};
    const next=[entry,...designs.filter(d=>d.id!==entry.id)];
    try{localStorage.setItem(key,JSON.stringify(next));open('Design saved on this device.');}catch{open('Browser storage is full. Export your design as JSON instead.');}
  }
  async function share() {
    if(!current())return open('Open a room first to share it.');
    const url=designURL(current());
    open('This link contains the room design. It works wherever this local app is running at the same address.');
    const input=document.createElement('textarea');input.readOnly=true;input.value=url;dialog.append(input);
    dialog.append(button('Copy design link',async()=>{try{await navigator.clipboard.writeText(url);input.select();}catch{input.select();}}));
  }
  function open(message='Designs are saved in this browser. Export JSON to keep a portable backup.') {
    dialog?.remove();dialog=document.createElement('dialog');dialog.className='local-workspace';
    const heading=document.createElement('h2');heading.textContent='My designs';dialog.append(heading);
    const description=document.createElement('p');description.textContent=message;dialog.append(description);
    const actions=document.createElement('div');actions.className='local-actions';
    if(current())actions.append(button('Save current design',save),button('Export room JSON',()=>download(current())),button('Share design',share));
    const input=document.createElement('input');input.type='file';input.accept='.json';input.hidden=true;
    input.onchange=async()=>{try{const file=input.files[0];if(!file)return;if(file.size>1000000)throw new Error('Room files must be smaller than 1 MB.');await load(validate(JSON.parse(await file.text())));}catch(e){open(e.message);}};
    actions.append(button('Import room JSON',()=>input.click()),input);dialog.append(actions);
    const list=document.createElement('div');list.className='local-design-list';
    for(const entry of read()) {
      const row=document.createElement('div');row.className='local-design-row';const name=document.createElement('strong');name.textContent=entry.name;row.append(name);
      row.append(button('Open',()=>load(entry.plan).catch(e=>open(e.message))),button('Export',()=>download(entry.plan)),button('Delete',()=>{if(confirm(`Delete "${entry.name}" from this browser?`)){localStorage.setItem(key,JSON.stringify(read().filter(d=>d.id!==entry.id)));open();}}));list.append(row);
    }
    if(!list.children.length){const empty=document.createElement('p');empty.textContent='No saved designs yet.';list.append(empty);}
    dialog.append(list,button('Close',()=>dialog.close()));document.body.append(dialog);dialog.showModal();
  }
  document.addEventListener('click',e=>{
    const target=e.target.closest('button,a');if(!target || target.closest('.local-workspace'))return;
    const text=target.textContent.trim();
    if(text==='Log in' || text==='My designs' || text.startsWith('Save changes') || text==='Share' || /^Share\s*(Login required|Saved on this device)/.test(text)){
      e.preventDefault();e.stopImmediatePropagation();
      if(text.startsWith('Save changes'))save();else if(text.startsWith('Share'))share();else open();
    }
  },true);
  function labels(){
    document.querySelectorAll('button').forEach(el=>{
      const text=el.textContent.trim();
      if(text==='Log in')el.textContent='My designs';
      if(text.startsWith('Save changes') || /^Share\s*(Login required|Saved on this device)/.test(text)){
        el.disabled=false;
        for(const child of el.querySelectorAll('*'))if(child.children.length===0 && child.textContent==='Login required')child.textContent='Saved on this device';
      }
    });
    // Printed blueprints lead with the SecureTech mark; the reference credit line is replaced.
    document.querySelectorAll('.blueprint-hero .container').forEach(container=>{
      if(container.querySelector('.print-brand'))return;
      const credit=[...container.querySelectorAll('.print-only')].find(el=>/^Blueprint from/.test(el.textContent.trim()));
      if(!credit)return;
      credit.classList.add('print-credit-hidden');
      credit.nextElementSibling?.classList.add('print-credit-hidden');
      const header=document.createElement('div');
      header.className='print-brand print-only';
      const mark=document.createElement('img');
      mark.className='print-brand-mark';mark.src='/images/securetech-mark.png';mark.alt='SecureTech AV Designs';
      const name=document.createElement('div');name.className='print-brand-name';name.textContent='SecureTech AV Designs';
      const site=document.createElement('a');site.className='print-brand-site';site.href='https://securetechav.com';site.textContent='securetechav.com';
      header.append(mark,name,site);
      container.prepend(header);
    });
    // The header entry point was removed, so the design library lives in the room menu.
    document.querySelectorAll('.room-menu').forEach(menu=>{
      if(menu.querySelector('.local-designs-entry'))return;
      const share=[...menu.querySelectorAll('button')].find(b=>/^Share/.test(b.textContent.trim()));
      if(!share)return;
      const entry=document.createElement('button');
      entry.type='button';entry.className='menu-button local-designs-entry';
      entry.innerHTML='<span class="icon save"></span><span class="menu-button-label">My designs<span class="menu-button-info">Saved on this device</span></span><span class="grow"></span><span class="icon arrow-right"></span>';
      entry.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();open();},true);
      share.after(entry);
    });
    if(current())document.querySelectorAll('a').forEach(el=>{if(el.textContent.trim()==='Link to this room')el.href=designURL(current());});
    document.querySelectorAll('p').forEach(el=>{if(el.textContent.includes('Warning: The room has not been saved yet.'))el.textContent='Use My designs to save on this device, or use the room link to carry this configuration to another browser running this app.';});
  }
  function init(){
    labels();new MutationObserver(labels).observe(document.getElementById('root'),{childList:true,subtree:true});
    const incoming=new URL(location.href).searchParams.get('design');
    if(incoming){try{const plan=validate(JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(incoming),c=>c.charCodeAt(0)))));const url=new URL(location.href);url.searchParams.delete('design');history.replaceState(null,'',url);load(plan).catch(e=>open(e.message));}catch{open('This design link is invalid.');}}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
