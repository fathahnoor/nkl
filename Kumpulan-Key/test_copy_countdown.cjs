// In-memory browser and clock: never writes test progress into a real browser.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(process.argv[2],'utf8');
const script=html.match(/<script>\s*('use strict';.*?)<\/script>/s)[1];
function browser(saved=new Map(),start=100000,clipboardWorks=true){
  let now=start,nextTimer=0,writes=0;
  const timers=new Map(),elements=new Map(),events={};
  function element(){return {textContent:'',value:'',open:false,hidden:false,disabled:false,style:{},dataset:{},classList:{toggle(){}},listeners:{},addEventListener(name,fn){this.listeners[name]=fn;},replaceChildren(){},append(){},focus(){},select(){},setSelectionRange(){},remove(){},showModal(){this.open=true;},close(){this.open=false;}};}
  for(const m of html.matchAll(/<script id="([^"]+)" type="application\/json">(.*?)<\/script>/gs))elements.set(m[1],{...element(),textContent:m[2]});
  const document={getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id);},createElement:element,body:{append(){}},execCommand(){return false;},addEventListener(name,fn){events[name]=fn;}};
  class Clock extends Date{constructor(...args){super(...(args.length?args:[now]));}static now(){return now;}}
  const ctx=vm.createContext({document,Date:Clock,Intl,window:{isSecureContext:true},navigator:{clipboard:{async writeText(){writes++;if(!clipboardWorks)throw Error('blocked');}}},localStorage:{getItem:k=>saved.get(k)||null,setItem:(k,v)=>saved.set(k,v)},setTimeout(fn,ms){const id=++nextTimer;timers.set(id,{fn,at:now+ms});return id;},clearTimeout:id=>timers.delete(id)});
  vm.runInContext(script,ctx);
  return {ctx,saved,el:id=>document.getElementById(id),get:expr=>JSON.parse(vm.runInContext('JSON.stringify('+expr+')',ctx)),call:expr=>vm.runInContext(expr,ctx),writes:()=>writes,now:()=>now,advance(ms,runTimers=true){now+=ms;if(runTimers)for(const [id,t] of [...timers])if(t.at<=now){timers.delete(id);t.fn();}},visible(){events.visibilitychange?.();}};
}
(async()=>{
  let b=browser(),code=b.get('codes[0]'),batch=b.get('state.activeBatchId');
  await b.call('copy(codes[0],true)');
  assert.equal(b.get('done.length'),0,'copy must not immediately consume the code');
  assert.equal(b.el('nextCode').textContent,code);
  assert.match(b.el('copyHint').textContent,/10/);
  assert.equal(b.el('next').disabled,true);
  await b.call('copy(codes[0],true)');assert.equal(b.writes(),1,'double tap must not copy twice');
  b.call('switchBatch(state.batches.find(x=>x.id!==state.activeBatchId).id)');assert.equal(b.get('state.activeBatchId'),batch);
  b.advance(9999);assert.equal(b.get('done.length'),0);assert.match(b.el('copyHint').textContent,/1/);
  b.advance(1);assert.deepEqual(b.get('done'),[code]);assert.notEqual(b.el('nextCode').textContent,code);
  b.advance(500);await b.call('copy(last,false)');assert.equal(b.get('done.length'),1);assert.equal(b.get('Boolean(state.pendingCopy)'),false,'recopy must not consume another code');
  b.advance(500);await b.call('copy(codes.find(c=>!done.includes(c)),true)');
  const second=b.get('state.pendingCopy.code'),deadline=b.get('state.pendingCopy.deadline');
  b=browser(b.saved,b.now()+3000);assert.equal(b.get('done.length'),1);assert.equal(b.el('nextCode').textContent,second);
  b.advance(deadline-b.now(),false);b.visible();assert.equal(b.get('done.length'),2,'returning from background must finish an expired countdown');
  b.advance(500);await b.call('copy(codes.find(c=>!done.includes(c)),true)');
  b=browser(b.saved,b.now()+11000);assert.equal(b.get('done.length'),3,'reload after deadline must finish pending copy');assert.equal(b.writes(),0);
  const m=browser(new Map(),200000,false);await m.call('copy(codes[0],true)');assert.equal(m.el('manual').open,true);assert.equal(m.get('done.length'),0);assert.equal(m.get('Boolean(state.pendingCopy)'),false);
  m.el('manualCancel').listeners.click();assert.equal(m.get('Boolean(state.pendingCopy)'),false);
  m.advance(500);await m.call('copy(codes[0],true)');m.el('manualDone').listeners.click();assert.equal(m.get('done.length'),0);assert.match(m.el('copyHint').textContent,/10/);m.advance(10000);assert.equal(m.get('done.length'),1);
  console.log('PASS: delayed completion, countdown boundary, double tap, batch lock, reload/background, recopy, manual failure/cancel/confirm');
})().catch(e=>{console.error(e);process.exitCode=1;});
