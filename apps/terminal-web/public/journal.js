'use strict';
// Pure functions are also exported for offline financial and import verification.
function parseCSV(text) {
  const rows=[]; let row=[],field='',quoted=false;
  text=text.replace(/^\uFEFF/,'');
  for(let i=0;i<text.length;i++) {
    const c=text[i];
    if(c==='"') { if(quoted&&text[i+1]==='"'){field+='"';i++;}else quoted=!quoted; }
    else if(c===','&&!quoted){row.push(field);field='';}
    else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(field);if(row.some(v=>v.trim()))rows.push(row);row=[];field='';}
    else field+=c;
  }
  if(quoted)throw Error('CSV contains an unclosed quoted field.');
  row.push(field);if(row.some(v=>v.trim()))rows.push(row);
  if(rows.length<2)throw Error('CSV needs a header and at least one record.');
  const headers=rows.shift().map(v=>v.trim());
  if(headers.some(v=>!v)||new Set(headers).size!==headers.length)throw Error('CSV headers must be unique and nonempty.');
  if(rows.some(r=>r.length!==headers.length))throw Error('CSV rows do not match the header. Use a comma-delimited export.');
  return rows.map(r=>Object.fromEntries(headers.map((h,i)=>[h,r[i]])));
}
function money(value){
  if(typeof value==='number'&&Number.isFinite(value))return value;
  if(typeof value!=='string'||!value.trim()||!/^[-+]?\d+(\.\d+)?$/.test(value.trim()))throw Error('Net P/L must be a finite plain number, without separators or currency symbols.');
  const n=Number(value);if(!Number.isFinite(n))throw Error('Net P/L is out of range.');return n;
}
function day(value){
  if(typeof value!=='string')throw Error('Closing dates must be ISO date strings.');
  if(/^\d{4}-\d{2}-\d{2}$/.test(value)){
    const d=new Date(value+'T12:00:00Z');if(Number.isNaN(+d)||d.toISOString().slice(0,10)!==value)throw Error('Invalid closing date.');return value;
  }
  if(!/^\d{4}-\d{2}-\d{2}T.*(Z|[+-]\d{2}:\d{2})$/.test(value)||Number.isNaN(Date.parse(value)))throw Error('Use ISO closing times with a timezone, or YYYY-MM-DD.');
  return new Intl.DateTimeFormat('en-CA',{timeZone:'America/Vancouver',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(value));
}
function reviewRows(rows,fields,from,through){
  if(!fields.id||!fields.net||!fields.date)throw Error('Map the unique ID, closing date and net P/L fields.');
  if(!from||!through||from>through)throw Error('Choose a valid date range.');
  const seen=new Set(),clean=[];
  for(const r of rows){
    const id=String(r[fields.id]??'').trim();
    if(!id||seen.has(id))throw Error('Missing or duplicate position IDs. Reconcile records before analysis.');
    seen.add(id);const closingDay=day(r[fields.date]),net=money(r[fields.net]);
    if(closingDay>=from&&closingDay<=through)clean.push({id,date:closingDay,net,symbol:fields.symbol?String(r[fields.symbol]??''):''});
  }
  return clean;
}
function metrics(rows){
  const n=rows.length,w=rows.filter(r=>r.net>0),l=rows.filter(r=>r.net<0),b=n-w.length-l.length;
  const grossWins=w.reduce((a,r)=>a+r.net,0),grossLosses=-l.reduce((a,r)=>a+r.net,0),net=rows.reduce((a,r)=>a+r.net,0);
  return {count:n,wins:w.length,losses:l.length,breakevens:b,net,
    winRate:n?w.length/n:null,profitFactor:grossLosses?grossWins/grossLosses:null,
    profitFactorState:!n?'no trades':!grossLosses?'no losing trades':'calculated',expectancy:n?net/n:null};
}
function arraysIn(value,path='$',out=[],depth=0){
  if(depth>7||!value||typeof value!=='object')return out;
  if(Array.isArray(value)&&value.length&&value.every(x=>x&&typeof x==='object'&&!Array.isArray(x))){out.push({path,rows:value});return out;}
  if(!Array.isArray(value))for(const [key,item]of Object.entries(value))arraysIn(item,path+'.'+key,out,depth+1);
  return out;
}
if(typeof module!=='undefined')module.exports={parseCSV,money,day,reviewRows,metrics,arraysIn};

if(typeof document!=='undefined'){
const $=id=>document.getElementById(id);
let state={local:false,tools:[],result:null,arrays:[],rows:[],source:null,reviewed:[],stats:null,mode:'unknown',currency:'',retrieved:null};
const imageURLs=[];
const attachments=[];
state.hosted=false;state.workspaceRevision=null;state.loadedEvidence=[];
const nowDay=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'America/Vancouver',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
const today=nowDay();$('throughDate').value=today;$('reviewDate').value=today;
const lastWeek=new Date(today+'T12:00:00Z');lastWeek.setUTCDate(lastWeek.getUTCDate()-6);$('fromDate').value=lastWeek.toISOString().slice(0,10);
function status(text,error=false){$('status').textContent=text;$('status').classList.toggle('error',error);}
async function api(path,body){
  const response=await fetch(path,{method:body===undefined?'GET':'POST',headers:{'Content-Type':'application/json','X-Journal-Request':'1'},body:body===undefined?undefined:JSON.stringify(body)});
  let payload;try{payload=await response.json();}catch{throw Error('The service did not return a valid response. Import a file here or check Data connections.');}
  if(!response.ok)throw Error(payload.error||'Private journal request failed.');return payload;
}
function invalidate(){$('saveWorkspace').disabled=true;state.stats=null;state.reviewed=[];$('confirmed').checked=false;for(const id of['net','winrate','pf','expectancy'])$(id).textContent='—';$('winDetail').textContent='Completed positions only';renderDailyMetrics();}
function renderTable(rows){
  $('rowCount').textContent=rows.length+' records';
  const columns=[...new Set(rows.flatMap(r=>Object.keys(r)))].filter(k=>rows.some(r=>r[k]===null||typeof r[k]!=='object')).slice(0,12);
  $('ledgerHead').replaceChildren();$('ledgerBody').replaceChildren();
  if(!rows.length){const tr=document.createElement('tr'),td=document.createElement('td');td.className='empty';td.textContent='No records in this view.';tr.append(td);$('ledgerBody').append(tr);return;}
  const header=document.createElement('tr');for(const column of columns){const th=document.createElement('th');th.textContent=column;header.append(th);}$('ledgerHead').append(header);
  for(const row of rows.slice(0,250)){const tr=document.createElement('tr');for(const col of columns){const td=document.createElement('td');td.textContent=typeof row[col]==='object'?'[nested data]':String(row[col]??'');tr.append(td);}$('ledgerBody').append(tr);}
  $('rowCount').textContent=rows.length+' records';
}
function fillFields(){
  state.rows=state.arrays[Number($('arrayPath').value)]?.rows||[];
  const fields=[...new Set(state.rows.flatMap(Object.keys))].filter(k=>state.rows.some(r=>r[k]===null||typeof r[k]!=='object'));
  for(const [id,hints] of [['idField',['position_id','ticket','id']],['dateField',['closed_at','time_close','close_time','date']],['netField',['net_profit','net_pnl','net']],['symbolField',['symbol','instrument']]]){
    $(id).replaceChildren(new Option('Choose field',''));for(const field of fields)$(id).add(new Option(field,field));
    $(id).value=hints.find(h=>fields.includes(h))||'';
  }
  invalidate();renderTable(state.rows);
}
function loadData(payload,source,retrieved=null){
  const arrays=arraysIn(payload);if(!arrays.length)throw Error('No array of records found. Use a statement CSV or JSON containing position records.');
  state.arrays=arrays;state.source=source;state.retrieved=retrieved;state.mode='unknown';$('accountMode').value='unknown';$('currency').value='';
  $('arrayPath').replaceChildren();arrays.forEach((a,i)=>$('arrayPath').add(new Option(a.path+' · '+a.rows.length+' rows',String(i))));
  $('mappingPanel').hidden=false;$('sourceLabel').textContent=source;$('coverage').textContent='Source records loaded. History completeness and account mode require verification.';
  $('ledgerHint').textContent='Preview of source records (first 250). Review the mapping and reconciliation below before calculating.';fillFields();
}
$('arrayPath').addEventListener('change',fillFields);
for(const id of['fromDate','throughDate','accountMode','currency','idField','netField','dateField','symbolField'])$(id).addEventListener('change',invalidate);
$('confirmed').addEventListener('change',()=>{if(!$('confirmed').checked){state.stats=null;state.reviewed=[];$('saveWorkspace').disabled=true;renderDailyMetrics();for(const id of['net','winrate','pf','expectancy'])$(id).textContent='—';}});
$('importFile').addEventListener('change',async e=>{
 const file=e.target.files[0];if(!file)return;invalidate();
 try{if(file.size>10_000_000)throw Error('Use an export smaller than 10 MB.');const text=await file.text();loadData(file.name.toLowerCase().endsWith('.csv')?parseCSV(text):JSON.parse(text),'UPLOADED SNAPSHOT');status('Loaded '+file.name+'. Verify account mode, currency and completed-position rows before analysis.');}catch(err){status(err.message,true);}finally{e.target.value='';}
});
$('sample').addEventListener('click',()=>{
 const sample=[85,-40,62,0,-35,110].map((net,i)=>({position_id:'SAMPLE-'+(i+1),closed_at:today,symbol:'XAUUSD',net_profit:net}));
 loadData(sample,'FICTIONAL SAMPLE · NOT MT5');$('accountMode').value='demo';$('currency').value='USD';status('Fictional sample loaded for interface exploration. These are not your trades. Confirm the sample mapping to view its calculations.');
});
$('analyze').addEventListener('click',()=>{
 try{
  if(!$('confirmed').checked)throw Error('Complete the reconciliation confirmation first.');
  const mode=$('accountMode').value,currency=$('currency').value.trim().toUpperCase();
  if(mode==='unknown'||!/^[A-Z]{3}$/.test(currency))throw Error('Confirm account mode and a three-letter result currency.');
  const fields={id:$('idField').value,date:$('dateField').value,net:$('netField').value,symbol:$('symbolField').value};
  const reviewed=reviewRows(state.rows,fields,$('fromDate').value,$('throughDate').value),m=metrics(reviewed);
  state.reviewed=reviewed;state.stats=m;state.mode=mode;state.currency=currency;state.fields=fields;
  const fmt=n=>n===null?'—':new Intl.NumberFormat('en-CA',{style:'currency',currency}).format(n);
  $('net').textContent=m.count?fmt(m.net):'—';$('expectancy').textContent=fmt(m.expectancy);$('winrate').textContent=m.winRate===null?'—':(m.winRate*100).toFixed(1)+'%';
  $('pf').textContent=m.profitFactor===null?m.profitFactorState:m.profitFactor.toFixed(2);
  $('winDetail').textContent=m.wins+' wins / '+m.losses+' losses / '+m.breakevens+' flat';
  renderTable(reviewed);$('coverage').textContent=m.count+' reviewed completed positions in selected date range · '+mode+' · '+currency+' · denominator includes breakevens. Source completeness remains user-verified.';
  $('saveWorkspace').disabled=!m.count;renderDailyMetrics();status('Calculated reviewed results. Save the reviewed snapshot for your dashboard; MAE/MFE require a matched intratrade path.');
 }catch(err){status(err.message,true);}
});
async function health(){try{const h=await api('/api/health');state.local=h.mode==='local';state.hosted=h.mode==='hosted'&&h.journal_storage;if(state.hosted){$('connectionStatus').textContent='Private journal ready · MT5 offline';$('connect').textContent='MT5 setup';$('transport').textContent='Hosted journal · import files or run the local MT5 service';}else if(state.local){$('attachmentHint').textContent='Local mode: screenshots stay in this tab; attach originals separately. Hosted private storage supports saved attachments.';}if(state.local){$('transport').textContent='Local service ready · '+(h.configured?'token configured':'token required');$('connectionStatus').textContent='Local service · MT5 unverified';}}catch{state.local=false;}}
$('connect').addEventListener('click',async()=>{
 if(state.hosted){$('setup').scrollIntoView({behavior:'smooth'});status('MT5 runs on your computer. Follow the local setup guide below or import a statement export here.');return;}
 $('connect').disabled=true;status('Discovering read-only tools from local MT5…');
 try{const health=await api('/api/health');if(!health.configured)throw Error('Set MT5_MCP_TOKEN privately before starting the local service.');
  const response=await api('/api/mt5/tools',{});state.local=true;state.tools=response.tools;
  if(!state.tools.length)throw Error('Connected, but no supported read-only tools were discovered.');
  $('toolSelect').replaceChildren();for(const t of state.tools)$('toolSelect').add(new Option(t.name,t.name));$('toolSelect').disabled=false;$('readTool').disabled=false;
  $('connectionStatus').textContent='MT5 tools connected';$('transport').textContent='Native MCP · read-only allowlist';$('lastRead').textContent=response.retrieved_at;
  toolChanged();status('MT5 tools discovered. Read account information to verify account type, then inspect a bounded history range.');
 }catch(err){$('connectionStatus').textContent='MT5 not connected';status(err.message,true);}finally{$('connect').disabled=false;}
});
function toolChanged(){const tool=state.tools.find(t=>t.name===$('toolSelect').value);$('toolSchema').textContent=JSON.stringify(tool?.inputSchema||{},null,2);$('toolArgs').value='{}';}
$('toolSelect').addEventListener('change',toolChanged);
$('readTool').addEventListener('click',async()=>{
 $('readTool').disabled=true;$('useResult').disabled=true;
 try{const args=JSON.parse($('toolArgs').value);if(!args||Array.isArray(args)||typeof args!=='object')throw Error('Arguments must be a JSON object.');
 const response=await api('/api/mt5/call',{name:$('toolSelect').value,arguments:args});state.result=response;$('rawResult').textContent=JSON.stringify(response,null,2);$('lastRead').textContent=response.retrieved_at;
 $('useResult').disabled=!/history/.test(response.tool);status('MT5 read completed: '+response.tool+'. Inspect the returned data and its coverage.');
 }catch(err){status(err.message,true);}finally{$('readTool').disabled=false;}
});
$('useResult').addEventListener('click',()=>{
 try{const r=state.result;let payload=r.result.structuredContent;
 if(!payload){const parts=(r.result.content||[]).filter(c=>c.type==='text').map(c=>{try{return JSON.parse(c.text);}catch{return null;}}).filter(Boolean);payload=parts.length===1?parts[0]:Object.fromEntries(parts.map((p,i)=>['result'+i,p]));}
 loadData(payload,'MT5 SNAPSHOT · '+r.tool,r.retrieved_at);status('MT5 history loaded for review. Raw orders and deals must be reconciled to completed positions before calculating.');$('mappingPanel').scrollIntoView({behavior:'smooth'});
 }catch(err){status(err.message,true);}
});
function evidence(){return {format:'gold-journal-v1',source:state.source,source_retrieved_at:state.retrieved,exported_at:new Date().toISOString(),account_mode:state.mode,currency:state.currency,time_zone:'America/Vancouver',range:{from:$('fromDate').value,through:$('throughDate').value},mapping:state.fields||null,metrics:state.stats,reviewed_positions:state.reviewed,metric_basis:'user-confirmed fully closed unique positions; net after costs; win rate includes breakevens; no verified MAE/MFE',date:$('reviewDate').value,session:$('session').value,process:$('process').value,notes:$('notes').value,experiment:$('experiment').value};}
function dailyEvidence(){const entry=evidence();entry.range={from:entry.date,through:entry.date};entry.reviewed_positions=state.reviewed.filter(r=>r.date===entry.date);entry.metrics=metrics(entry.reviewed_positions);entry.evidence=[...state.loadedEvidence,...attachments.filter(a=>a.saved).map(a=>a.saved)];return entry;}
function renderDailyMetrics(){const root=$('dailyMetrics');if(!root)return;root.replaceChildren();const m=metrics(state.reviewed.filter(r=>r.date===$('reviewDate').value));const text=m.count?m.count+' closed positions · Net '+m.net.toFixed(2)+' '+state.currency+' · Win rate '+(m.winRate*100).toFixed(1)+'% · Expectancy '+m.expectancy.toFixed(2):'No reviewed closed positions for this date. You can still save observations and evidence.';root.textContent=text;}
$('reviewDate').addEventListener('change',renderDailyMetrics);renderDailyMetrics();
function download(){const url=URL.createObjectURL(new Blob([JSON.stringify(dailyEvidence(),null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='gold-journal-'+($('reviewDate').value||today)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),500);}
$('export').addEventListener('click',download);
function applySaved(entry){
 for(const url of imageURLs)URL.revokeObjectURL(url);imageURLs.length=0;attachments.length=0;$('images').replaceChildren();state.loadedEvidence=entry.evidence||[];for(const a of state.loadedEvidence){const link=document.createElement('a');link.href='/api/evidence/'+encodeURIComponent(a.id);link.textContent='Attached evidence: '+a.name;link.className='evidence-link';$('images').append(link);}
 if(entry.reviewed_positions?.length){const rows=entry.reviewed_positions.map(r=>({position_id:r.id,closed_at:r.date,net_profit:r.net,symbol:r.symbol}));loadData(rows,entry.source,entry.source_retrieved_at);$('fromDate').value=entry.range.from;$('throughDate').value=entry.range.through;$('accountMode').value=entry.account_mode;$('currency').value=entry.currency;$('confirmed').checked=true;$('analyze').click();}
 $('reviewDate').value=entry.date;$('session').value=entry.session;$('process').value=entry.process;$('notes').value=entry.notes;$('experiment').value=entry.experiment;renderDailyMetrics();
}
async function showSaved(){try{const r=await api('/api/reviews');$('savedReviews').replaceChildren();if(!r.records.length){const p=document.createElement('p');p.className='caption';p.textContent='No saved daily reviews yet.';$('savedReviews').append(p);return;}const heading=document.createElement('h3');heading.textContent='Saved daily reviews';$('savedReviews').append(heading);for(const row of r.records){const entry=row.review,box=document.createElement('article');box.className='savedreview';const title=document.createElement('b');title.textContent=entry.date+' · '+entry.session;const p=document.createElement('p');p.textContent=entry.notes.slice(0,180);const btn=document.createElement('button');btn.className='quiet';btn.textContent='Load review';btn.onclick=()=>{applySaved(entry);status('Loaded the saved review. The saved original remains unchanged; saving again creates another review.');};box.append(title,p,btn);for(const a of entry.evidence||[]){const link=document.createElement('a');link.href='/api/evidence/'+encodeURIComponent(a.id);link.textContent='Download '+a.name;link.className='evidence-link';link.setAttribute('download','');box.append(link);}$('savedReviews').append(box);}if(r.has_more){const n=document.createElement('p');n.className='caption';n.textContent='Showing the latest 50 reviews.';$('savedReviews').append(n);}}catch(err){$('savedReviews').textContent='Saved reviews unavailable: '+err.message;}}
$('saveReview').addEventListener('click',async()=>{
 $('saveReview').disabled=true;
 try{if(!$('reviewDate').value||!$('notes').value.trim())throw Error('Add a review date and your observations first.');
 if(!state.local&&!state.hosted){download();status('Private saving is unavailable. Daily evidence downloaded instead.');return;}
 const entry=dailyEvidence();if(state.hosted){for(const attachment of attachments){if(attachment.saved)continue;const r=await fetch('/api/evidence',{method:'POST',headers:{'Content-Type':attachment.file.type,'X-Journal-Request':'1','X-Evidence-Name':encodeURIComponent(attachment.file.name)},body:attachment.file});const payload=await r.json();if(!r.ok)throw Error(payload.error||'Evidence upload failed.');attachment.saved=payload;}entry.evidence=[...state.loadedEvidence,...attachments.map(a=>a.saved)];}
 const r=await api('/api/reviews',entry);status('Daily review saved '+(state.hosted?'privately with '+entry.evidence.length+' attachments.':'locally.')+' Notion and Discord handoff remains manual.');showSaved();
 }catch(err){status(err.message,true);}finally{$('saveReview').disabled=false;}
});
$('screenshots').addEventListener('change',e=>{for(const file of e.target.files){if(attachments.length+state.loadedEvidence.length>=10||attachments.reduce((sum,a)=>sum+a.file.size,0)+state.loadedEvidence.reduce((sum,a)=>sum+a.size,0)+file.size>40_000_000){status('Use at most ten evidence files, under 40 MB in total.',true);break;}if(!['image/png','image/jpeg','image/webp','application/pdf'].includes(file.type)||file.size>8_000_000){status('Use PNG, JPEG, WebP or PDF evidence under 8 MB.',true);continue;}const attachment={file},figure=document.createElement('figure'),caption=document.createElement('figcaption');attachments.push(attachment);caption.textContent=file.name+' · '+(file.size/1024).toFixed(0)+' KB';if(file.type.startsWith('image/')){const img=document.createElement('img');img.src=URL.createObjectURL(file);attachment.url=img.src;imageURLs.push(img.src);img.alt='Trading screenshot: '+file.name;figure.append(img);}else{const label=document.createElement('p');label.textContent='PDF evidence · saved as an attachment; no extraction';figure.append(label);}const remove=document.createElement('button');remove.className='quiet';remove.textContent='Remove';remove.onclick=()=>{const i=attachments.indexOf(attachment);if(i>=0)attachments.splice(i,1);if(attachment.url)URL.revokeObjectURL(attachment.url);figure.remove();};figure.append(caption,remove);$('images').append(figure);}e.target.value='';});
async function workspaceInfo(){if(!state.hosted)return;try{const r=await api('/api/journal');state.workspaceRevision=r.revision;state.savedWorkspace=r.workspace;$('workspaceSaveState').textContent=r.workspace?'Saved dashboard snapshot: '+r.workspace.range.from+' → '+r.workspace.range.through+' · '+r.workspace.metrics.count+' positions · '+r.workspace.currency+'. Save replaces this summary; daily reviews stay separate.':'No private dashboard snapshot saved yet.';}catch(err){$('workspaceSaveState').textContent='Private snapshot unavailable: '+err.message;}}
$('saveWorkspace').addEventListener('click',async()=>{if(!state.stats||!state.reviewed.length)return;$('saveWorkspace').disabled=true;try{if(!state.hosted)throw Error('Open the hosted journal to save a dashboard snapshot. Local evidence can be downloaded separately.');const r=await api('/api/journal',{workspace:evidence(),revision:state.workspaceRevision});state.workspaceRevision=r.revision;state.savedWorkspace=r.workspace;$('workspaceSaveState').textContent='Reviewed snapshot saved privately. Its results are now available on the terminal overview.';status('Dashboard snapshot saved. Daily reviews remain separate.');}catch(err){status(err.message,true);}finally{$('saveWorkspace').disabled=!state.stats?.count;}});
$('loadWorkspace').addEventListener('click',async()=>{await workspaceInfo();if(!state.savedWorkspace){status('No saved private snapshot is available. Import and review your closed-position records first.');return;}applySaved(state.savedWorkspace);status('Loaded the saved reviewed snapshot. Calculations were checked again in this browser.');});
$('clear').addEventListener('click',()=>{invalidate();state.arrays=[];state.rows=[];state.source=null;state.result=null;state.retrieved=null;state.fields=null;state.mode='unknown';state.currency='';$('mappingPanel').hidden=true;$('sourceLabel').textContent='NO SOURCE';$('rawResult').textContent='No response yet.';$('useResult').disabled=true;$('accountMode').value='unknown';$('currency').value='';$('rowCount').textContent='0 records';renderTable([]);for(const url of imageURLs)URL.revokeObjectURL(url);imageURLs.length=0;attachments.length=0;state.loadedEvidence=[];$('images').replaceChildren();$('notes').value='';$('experiment').value='';$('process').value='unknown';$('coverage').textContent='No history coverage verified.';status('Workspace cleared. Previously saved local reviews remain in the local database.');});
health().then(()=>{if(state.local||state.hosted)showSaved();workspaceInfo();});
}
