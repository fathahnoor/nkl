const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(process.argv[2],'utf8');
const tags={};for(const m of html.matchAll(/<script id="([^"]+)" type="application\/json">(.*?)<\/script>/gs))tags[m[1]]={textContent:m[2]};
const base={...JSON.parse(tags.batchInfo.textContent),codes:JSON.parse(tags.codeData.textContent)};
const startup=html.match(/<script>\s*('use strict';.*?)function listButton/s)[1];
function run(stored,legacy){
  const data=new Map();if(stored)data.set('nusuk-copy-batches-v2',JSON.stringify(stored));if(legacy)data.set('nusuk-copy-v1-d089ba09c115e2b0',JSON.stringify(legacy));
  const ctx=vm.createContext({document:{getElementById:id=>tags[id]||{}},localStorage:{getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v)}});
  vm.runInContext(startup,ctx);return JSON.parse(vm.runInContext('JSON.stringify({state,storageReadFailed})',ctx));
}
const legacy={version:1,done:[base.codes[0]],last:base.codes[0]};
let result=run(null,legacy);assert.equal(result.storageReadFailed,false);assert.equal(result.state.batches.length,4);assert.deepEqual(result.state.progress[base.id].done,legacy.done);
const active=result.state.activeBatchId;result=run(result.state);assert.equal(result.state.batches.length,4);assert.equal(result.state.activeBatchId,active);
const custom={id:'personal-batch',name:'Personal',createdAt:new Date().toISOString(),codes:['NG-T0000000']};
const stored={version:2,batches:[base,custom],activeBatchId:custom.id,progress:{[base.id]:{done:legacy.done,last:legacy.last},[custom.id]:{done:custom.codes,last:custom.codes[0]}}};
result=run(stored);assert.equal(result.storageReadFailed,false);const codes=result.state.batches.flatMap(b=>b.codes);assert.equal(codes.length,new Set(codes).size);assert.deepEqual(result.state.progress[custom.id].done,custom.codes);
console.log('PASS: released batches, legacy migration, reload, local overlaps, copy history');
