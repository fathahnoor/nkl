const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(process.argv[2],'utf8');
const tags={};for(const m of html.matchAll(/<script id="([^"]+)" type="application\/json">(.*?)<\/script>/gs))tags[m[1]]={textContent:m[2]};
const base={...JSON.parse(tags.batchInfo.textContent),codes:JSON.parse(tags.codeData.textContent)};
const startup=html.match(/<script>\s*('use strict';.*?)function listButton/s)[1];
function run(stored,legacy,backup){
  const data=new Map();if(stored)data.set('nusuk-copy-batches-v2',JSON.stringify(stored));if(legacy)data.set('nusuk-copy-v1-d089ba09c115e2b0',JSON.stringify(legacy));
  const ctx=vm.createContext({document:{getElementById:id=>tags[id]||{}},localStorage:{getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v)}});
  vm.runInContext(startup,ctx);
  if(backup){ctx.testBackup=backup;vm.runInContext('function render(){};'+html.match(/(function mergeBackup\(value\).*?)\n\$\('batchSelect'\)/s)[1]+';mergeBackup(testBackup);',ctx);}
  return JSON.parse(vm.runInContext('JSON.stringify({state,storageReadFailed})',ctx));
}
const legacy={version:1,done:[base.codes[0]],last:base.codes[0]};
let result=run(null,legacy);assert.equal(result.storageReadFailed,false);assert.equal(result.state.batches.length,4);assert.deepEqual(result.state.progress[base.id].done,legacy.done);
const active=result.state.activeBatchId;result=run(result.state);assert.equal(result.state.batches.length,4);assert.equal(result.state.activeBatchId,active);
const custom={id:'personal-batch',name:'Personal',createdAt:new Date().toISOString(),codes:['NG-T0000000']};
const stored={version:2,batches:[base,custom],activeBatchId:custom.id,progress:{[base.id]:{done:legacy.done,last:legacy.last},[custom.id]:{done:custom.codes,last:custom.codes[0]}}};
result=run(stored);assert.equal(result.storageReadFailed,false);const codes=result.state.batches.flatMap(b=>b.codes);assert.equal(codes.length,new Set(codes).size);assert.deepEqual(result.state.progress[custom.id].done,custom.codes);
const previousBase={...base,codes:base.codes.slice(0,-2)};
const previous={version:2,batches:[previousBase],activeBatchId:base.id,progress:{[base.id]:{done:legacy.done,last:legacy.last}}};
result=run(previous);assert.equal(result.storageReadFailed,false);assert.deepEqual(result.state.batches[0].codes,base.codes);assert.deepEqual(result.state.progress[base.id].done,legacy.done);
result=run(result.state,null,previous);assert.deepEqual(result.state.batches[0].codes,base.codes);assert.deepEqual(result.state.progress[base.id].done,legacy.done);
const personalOverlap={...custom,codes:[base.codes.at(-1)]};
const overlapState={...previous,batches:[previousBase,personalOverlap],progress:{...previous.progress,[custom.id]:{done:personalOverlap.codes,last:personalOverlap.codes[0]}}};
result=run(overlapState);assert.equal(result.storageReadFailed,false);const unique=result.state.batches.flatMap(b=>b.codes);assert.equal(unique.length,new Set(unique).size);assert.deepEqual(result.state.progress[custom.id].done,personalOverlap.codes);
console.log('PASS: releases, reload, copy history, extended baseline, old backup restore, personal overlaps');
