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
  const REMOVED_ROOMS=new Set(['Innovation Suite']);
  const ROOM_RENAMES={
    'Huddle Room':'Focus Pod',
    'Small Room':'Mini Board Room',
    'Medium Room':'Medium Board Room',
    'Large Room':'Large Board Room',
    'Executive Boardroom':'Leadership Hub',
    'Ideation Space':'Innovation Hub',
    'Innovation Suite':'Concept Studio',
    'Desk':'Workstation',
    'Open Space':'Collab Area',
    'Focus Room':'Huddle Room',
    'Training Room':'Multi Purpose Hall'
  };
  // The three category tabs carry SecureTech's own wording too.
  const TAB_RENAMES={
    'Meeting rooms':'Conference Rooms',
    'Meeting Rooms':'Conference Rooms',
    'Individual Spaces':'Office Rooms',
    'Training Spaces':'Large Venue'
  };
  function enhanceHero(main){
    if(main.classList.contains('st-hero-ready'))return;
    main.classList.add('st-hero-ready');
    const hero=main.querySelector('.hero');
    const left=hero?.querySelector('.left');
    if(!hero || !left)return;
      const title=left.querySelector('.title');
      if(title){
        title.innerHTML='Design your workspace <span>in 3D</span>';
      }
    if(!hero.querySelector('.st-hero-art')){
      const art=document.createElement('div');
      art.className='st-hero-art';
      art.innerHTML='<div class="st-wall-note">Better<br>Spaces<br>Brighter<br>Ideas</div>';
      hero.append(art);
    }
  }
  function enhanceFrontPage(){
    const main=document.querySelector('main.front-page');
    if(!main)return;
    main.classList.add('st-reference-ready');
    enhanceHero(main);
    main.querySelectorAll('.tabs .tab').forEach(tab=>{
      const label=[...tab.childNodes].find(n=>n.nodeType===3 && n.textContent.trim());
      const next=TAB_RENAMES[(label?label.textContent:tab.textContent).trim()];
      if(!next)return;
      if(label)label.textContent=next; else tab.textContent=next;
    });
    // Switching tabs re-renders the card list, so cards are enhanced per card
    // rather than once per page - a page-level guard would leave every tab
    // after the first one unstyled.
    main.querySelectorAll('.room-button').forEach((card,index)=>{
      card.classList.toggle('st-priority-room', index<3);
      if(card.classList.contains('st-reference-card'))return;
      const roomTitle=card.querySelector('.title')?.textContent.trim();
      if(!roomTitle)return;
      // Hidden, not removed: the list is React-owned, and detaching a node
      // from it breaks the reconciler on the next tab switch.
      if(REMOVED_ROOMS.has(roomTitle)){card.classList.add('st-room-hidden');return;}
      card.classList.add('st-reference-card');
      card.dataset.stRoom=roomTitle;
      const shot=card.querySelector('.image img');
      if(shot)shot.src=shot.getAttribute('src').replace(/\?.*$/,'')+'?st=2';
      if(ROOM_RENAMES[roomTitle])card.querySelector('.title').textContent=ROOM_RENAMES[roomTitle];
      if(!card.querySelector('.st-actions')){
        const href=card.querySelector('a[href*="/room/"]')?.getAttribute('href') || '#/';
        const actions=document.createElement('div');
        actions.className='st-actions';
        actions.innerHTML=`<a class="st-customize" href="${href}">Tailor Your Environment <span>→</span></a>`;
        card.append(actions);
      }
    });
  }
  document.addEventListener('click',e=>{
    const target=e.target.closest('button,a');if(!target || target.closest('.local-workspace'))return;
    const text=target.textContent.trim();
    if(text==='Log in' || text==='My designs' || text.startsWith('Save changes') || text==='Share' || /^Share\s*(Login required|Saved on this device)/.test(text)){
      e.preventDefault();e.stopImmediatePropagation();
      if(text.startsWith('Save changes'))save();else if(text.startsWith('Share'))share();else open();
    }
  },true);
  const REMOVED_SECTIONS=new Set(['Documentation','Room Link']);
  function labels(){
    enhanceFrontPage();
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
      mark.className='print-brand-mark';mark.src='./images/securetech-mark.png';mark.alt='SecureTech AV Designs';
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
    // Summary sections this build does not use. They share the generic
    // .coverage-module markup, so they are matched by their heading and tagged
    // for local-adapter.css to hide.
    document.querySelectorAll('main section').forEach(section=>{
      if(section.classList.contains('st-section-hidden'))return;
      const heading=section.querySelector('.header > h2');
      if(heading && REMOVED_SECTIONS.has(heading.textContent.trim()))section.classList.add('st-section-hidden');
    });
  }
  function init(){
    labels();new MutationObserver(labels).observe(document.getElementById('root'),{childList:true,subtree:true});
    const incoming=new URL(location.href).searchParams.get('design');
    if(incoming){try{const plan=validate(JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(incoming),c=>c.charCodeAt(0)))));const url=new URL(location.href);url.searchParams.delete('design');history.replaceState(null,'',url);load(plan).catch(e=>open(e.message));}catch{open('This design link is invalid.');}}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();

// ── SecureTech room palette ──────────────────────────────────────────────────
// The 3D room ships in flat greys. This repaints every room's surfaces to the
// SecureTech scheme. The scene is published on window.__stScene by the hook the
// Flask layer injects while serving the bundle (see secure/app.py) - r3f keeps
// its scene in its own reconciler, so there is no DOM route to it.
(() => {
  const PALETTE = {
    warmWhite: { hex: '#F5F5F2', name: 'Warm White',  role: 'Main Walls',      note: 'Bright, clean and professional' },
    walnut:    { hex: '#6F4E37', name: 'Walnut Wood', role: 'Accent Wall',     note: 'Adds warmth and premium feel' },
    sage:      { hex: '#D9D6CF', name: 'Sage / Grey', role: 'Side Panels',     note: 'Subtle and modern' },
    charcoal:  { hex: '#3D3D3D', name: 'Charcoal',    role: 'Trim',            note: 'Reduces glare and looks premium' },
    taupe:     { hex: '#918A84', name: 'Taupe',       role: 'Curtains',        note: 'Warm, soft and recessive' },
    beige:     { hex: '#B0A794', name: 'Beige',       role: 'Flooring / Carpet', note: 'Neutral and elegant' },
    timber:    { hex: '#A8763F', name: 'Natural Wood', role: 'Tables / Desks',    note: 'Warm and inviting' },
    rug:       { hex: '#5A2320', name: 'Dark Maroon', role: 'Carpet',           note: 'Grounds the room in the brand' },
  };
  const WALL_GROUPS = ['leftwall', 'rightwall', 'backwall', 'videowall'];
  // Structure meshes that make up the wall itself, as opposed to glazing,
  // curtains and the acoustic panels hung on it.
  const STRUCTURE = /^(base|shadow-fixer|top|pillar|doorframe)/;

  // Materials are shared between meshes - `base` and `shadow-fixer` on two
  // different walls can be the very same instance - so painting one in place
  // would repaint the others. Each mesh gets its own clone the first time it is
  // touched, and the clone is reused on later passes.
  function paint(mesh, hex) {
    if (!mesh.isMesh || !mesh.material) return;
    const list = [].concat(mesh.material);
    const painted = list.map(m => {
      if (!m) return m;
      let target = m;
      if (!m.userData || !m.userData.stPainted) {
        target = m.clone();
        target.userData = Object.assign({}, target.userData, { stPainted: true });
      }
      if (target.color && '#' + target.color.getHexString().toUpperCase() !== hex.toUpperCase()) {
        target.color.set(hex);
        target.needsUpdate = true;
      }
      return target;
    });
    mesh.material = Array.isArray(mesh.material) ? painted : painted[0];
  }

  // THREE is bundled, so its classes are not reachable by name. The Texture
  // constructor is borrowed from a texture the scene already has (the screens
  // carry one), which is enough to build our own. 1000 is RepeatWrapping.
  const WOOD_URL = './images/textures/walnut-slats.png';
  const REPEAT_WRAPPING = 1000;
  let woodTexture = null, woodPending = false;
  function woodFor(scene) {
    if (woodTexture || woodPending) return woodTexture;
    let Texture = null;
    scene.traverse(n => {
      if (Texture || !n.isMesh) return;
      for (const m of [].concat(n.material || []))
        if (m && m.map && m.map.constructor) { Texture = m.map.constructor; break; }
    });
    if (!Texture) return null;
    woodPending = true;
    const img = new Image();
    img.onload = () => {
      const tex = new Texture(img);
      tex.wrapS = tex.wrapT = REPEAT_WRAPPING;
      tex.repeat.set(4, 2);
      tex.colorSpace = 'srgb';
      tex.needsUpdate = true;
      woodTexture = tex;
      woodPending = false;
    };
    img.onerror = () => { woodPending = false; };
    img.src = WOOD_URL;
    return null;
  }

  function grain(mesh, tex) {
    if (!mesh.isMesh || !tex) return;
    for (const m of [].concat(mesh.material)) {
      if (!m || m.map === tex) continue;
      m.map = tex;
      // The tint would otherwise multiply into the texture and darken it.
      if (m.color) m.color.set('#ffffff');
      if ('roughness' in m) m.roughness = 0.72;
      m.needsUpdate = true;
    }
  }

  function apply() {
    const scene = window.__stScene;
    if (!scene) return false;
    const wood = woodFor(scene);
    scene.traverse(node => {
      // Tables and desks in warm natural timber rather than the reference
      // greys. The name test is anchored and excludes the table-mounted
      // devices - "Table Mic Pro" would otherwise be painted like furniture.
      if (/^(maintable|table[-_ ]?(top|leg|campfire|classroom|t?leg)?$|table-|desk)/i.test(node.name || '')
          && !/mic|nav|scheduler|phone|codec|screen|display/i.test(node.name || '')) {
        node.traverse(part => paint(part, PALETTE.timber.hex));
        return;
      }
      if (node.isMesh && node.geometry && !node.userData.stTopChecked) {
        node.userData.stTopChecked = true;
        node.geometry.computeBoundingBox();
        const bb = node.geometry.boundingBox.clone().applyMatrix4(node.matrixWorld);
        const w = bb.max.x - bb.min.x, h = bb.max.y - bb.min.y, d = bb.max.z - bb.min.z;
        if (w > 1 && d > 0.6 && h < 0.3 && bb.min.y > 0.5 && bb.min.y < 1.05)
          node.userData.stIsTableTop = true;
      }
      if (node.userData.stIsTableTop) { paint(node, PALETTE.timber.hex); return; }
      if (node.name === 'floor') paint(node, PALETTE.beige.hex);
      else if (/^carpet/.test(node.name)) paint(node, PALETTE.rug.hex);
      else if (node.name === 'ceiling') paint(node, PALETTE.warmWhite.hex);
    });
    for (const wallName of WALL_GROUPS) {
      const wall = scene.getObjectByName(wallName);
      if (!wall) continue;
      const accent = wallName === 'videowall';
      wall.traverse(node => {
        if (!node.isMesh) return;
        const name = node.name || '';
        if (/^glass/.test(name)) return;             // glazing stays clear
        if (/curtain|Line00/.test(name)) {           // drapes in taupe
          paint(node, PALETTE.taupe.hex);
          return;
        }
        if (STRUCTURE.test(name)) {
          // Once the timber texture is on, the surface must stay white: a
          // walnut tint would multiply into the image and muddy it. Until the
          // texture loads the flat walnut stands in for it.
          if (accent && wood) grain(node, wood);
          else paint(node, accent ? PALETTE.walnut.hex : PALETTE.warmWhite.hex);
          return;
        }
        // Anything else hung on a wall is acoustic treatment - the panels in
        // the reference scheme.
        paint(node, PALETTE.sage.hex);
      });
    }
    return true;
  }

  window.__stPalette = PALETTE;
  window.__stApplyPalette = apply;
  // The app rebuilds meshes on room, step and layout changes, and there is no
  // event for it, so the palette is simply re-asserted. paint() early-outs when
  // a colour already matches, so a steady state costs one traversal.
  setInterval(apply, 400);
  apply();
})();
