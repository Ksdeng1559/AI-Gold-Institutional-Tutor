// ASSETS and SEED are embedded by scripts/build-news.mjs. Sites dispatch owns authentication.
const NEWS_KEY='news/latest.json';
const json=(body,status=200)=>Response.json(body,{status,headers:{'Cache-Control':'no-store'}});
const toolList=[{name:'read_news_snapshot',description:'Read the current shared gold and crypto news snapshot.',inputSchema:{type:'object',properties:{},additionalProperties:false}},{name:'publish_news_snapshot',description:'Replace the shared news snapshot after verifying original sources. Owner-private Site only.',inputSchema:{type:'object',properties:{snapshot:{type:'object'}},required:['snapshot'],additionalProperties:false}}];
export function validateSnapshot(value){
 if(!value||typeof value!=='object'||!Array.isArray(value.stories)||value.stories.length>30||!value.stories.length)throw Error('Provide 1–30 source-backed stories.');
 if(!Number.isFinite(Date.parse(value.updated_at))||Date.parse(value.updated_at)>Date.now()+300000)throw Error('Invalid snapshot timestamp.');
 if(typeof value.method!=='string'||typeof value.schedule_status!=='string')throw Error('Missing source method or schedule state.');
 const seen=new Set();for(const s of value.stories){for(const field of['id','asset','topic','title','summary','relevance','source','url','published_at','period','verification'])if(typeof s[field]!=='string'||!s[field].trim()||s[field].length>1500)throw Error('Invalid story field: '+field);
 if(!['Gold','Crypto'].includes(s.asset)||!Array.isArray(s.regions)||!s.regions.length||s.regions.some(r=>!['Asia','London / Europe','US / New York','Global'].includes(r)))throw Error('Invalid story tags.');
 if(seen.has(s.id))throw Error('Duplicate story ID.');seen.add(s.id);
 const u=new URL(s.url);if(u.protocol!=='https:'||u.username||u.password)throw Error('Use safe HTTPS original-source links.');
 if(!Number.isFinite(Date.parse(s.published_at))||Date.parse(s.published_at)>Date.parse(value.updated_at)+300000)throw Error('Invalid publication date.');}
 if(value.market_data!==undefined){
  if(!value.market_data||Array.isArray(value.market_data)||typeof value.market_data!=='object')throw Error('Invalid market data.');
  for(const [key,m] of Object.entries(value.market_data)){
   if(!['gold','btc','wti','brent','us10y'].includes(key)||m.provider!=='Alpha Vantage')throw Error('Invalid market provider or series.');
   if(typeof m.value!=='number'||!Number.isFinite(m.value)||m.value<=0)throw Error('Invalid market value.');
   for(const k of ['instrument','unit','function','observed_at','timezone','kind','note'])if(typeof m[k]!=='string'||!m[k].trim()||m[k].length>600)throw Error('Invalid market metadata: '+k);
   if(!/^\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})?)?$/.test(m.observed_at)||!Number.isFinite(Date.parse(m.observed_at)))throw Error('Invalid observation date.');
   if(!Number.isFinite(Date.parse(m.retrieved_at))||Date.parse(m.retrieved_at)>Date.now()+300000)throw Error('Invalid market retrieval.');
   if(!['reference quote','daily observation'].includes(m.kind))throw Error('Invalid market kind.');
  }
 }
 if(value.briefings!==undefined){
  if(!value.briefings||Array.isArray(value.briefings)||typeof value.briefings!=='object')throw Error('Invalid briefings.');
  for(const [session,b]of Object.entries(value.briefings)){
   if(!['Asia','London','New York'].includes(session)||b.session!==session)throw Error('Invalid briefing session.');
   for(const k of['session_date','session_open_at','prepared_at','news_cutoff','summary','focus','handover','coverage'])if(typeof b[k]!=='string'||!b[k].trim()||b[k].length>2000)throw Error('Invalid briefing field: '+k);
   for(const k of['session_date','session_open_at','prepared_at','news_cutoff'])if(!Number.isFinite(Date.parse(b[k])))throw Error('Invalid briefing time.');
   if(Date.parse(b.prepared_at)>Date.now()+300000||Date.parse(b.news_cutoff)>Date.parse(b.prepared_at)+300000)throw Error('Invalid briefing cutoff.');
   if(!Array.isArray(b.sources)||b.sources.length>15)throw Error('Invalid briefing sources.');
   for(const s of b.sources){const u=new URL(s.url);if(u.protocol!=='https:'||u.username||u.password||!s.title||!s.source||!Number.isFinite(Date.parse(s.published_at)))throw Error('Invalid briefing source.');}
   if(!Array.isArray(b.drivers)||b.drivers.length>8||b.drivers.some(d=>['title','observation','watch'].some(k=>typeof d[k]!=='string'||d[k].length>1500)))throw Error('Invalid briefing drivers.');
   if(!Array.isArray(b.scenarios)||b.scenarios.length>5||b.scenarios.some(d=>typeof d.condition!=='string'||typeof d.response!=='string'))throw Error('Invalid briefing scenarios.');
   if(!Array.isArray(b.questions)||b.questions.length>12||b.questions.some(q=>typeof q!=='string'||q.length>600))throw Error('Invalid briefing questions.');
   if(!Array.isArray(b.catalysts)||b.catalysts.length>12)throw Error('Invalid catalysts.');
   for(const c of b.catalysts){if(typeof c.name!=='string'||typeof c.verification!=='string'||(c.at!==null&&!Number.isFinite(Date.parse(c.at))))throw Error('Invalid catalyst time or evidence.');if(c.url!==null&&new URL(c.url).protocol!=='https:')throw Error('Invalid catalyst source.');}
  }
 }
 if(JSON.stringify(value).length>100000)throw Error('Snapshot too large.');return value;
}
async function read(env){const object=await env.BUCKET?.get(NEWS_KEY);return object?await object.json():SEED;}
async function write(env,value){if(!env.BUCKET)throw Error('Persistent news storage unavailable.');const prior=await read(env);value={...value,market_data:{...(prior.market_data||{}),...(value.market_data||{})},briefings:{...(prior.briefings||{}),...(value.briefings||{})}};validateSnapshot(value);for(const [key,m] of Object.entries(value.market_data||{})){if(prior.market_data?.[key]&&Date.parse(m.retrieved_at)<Date.parse(prior.market_data[key].retrieved_at))throw Error('A newer market snapshot already exists.');}if(Date.parse(value.updated_at)<Date.parse(prior.updated_at))throw Error('A newer snapshot already exists. Read it before retrying.');await env.BUCKET.put(NEWS_KEY,JSON.stringify(value),{httpMetadata:{contentType:'application/json'}});return {saved:true,updated_at:value.updated_at,stories:value.stories.length,briefing_sessions:Object.keys(value.briefings)};}
export default {async fetch(request,env){
 const url=new URL(request.url);
 try{
  const journalResponse=await journalRoute(request,env);if(journalResponse)return journalResponse;
  if(url.pathname==='/api/health'&&request.method==='GET')return json({mode:'hosted',configured:false,journal_storage:!!env.BUCKET});
  if(url.pathname.startsWith('/api/mt5/'))return json({error:'MT5 is local to your computer. Run the local journal application to connect; the hosted dashboard accepts imports.'},409);
  if(url.pathname==='/api/news'&&request.method==='GET')return json(await read(env));
  // Access is enforced by the unchanged owner-only Sites policy. Dispatch validates service access.
  if(url.pathname==='/api/news'&&request.method==='PUT'){if(Number(request.headers.get('Content-Length')||0)>150000)return json({error:'Too large'},413);return json(await write(env,await request.json()));}
  if(url.pathname==='/mcp'&&request.method==='POST'){
   const message=await request.json();const {id,method,params={}}=message;let result;
   if(method==='server/discover')result={supportedVersions:['2026-07-28'],capabilities:{tools:{}}};
   else if(method==='initialize')result={protocolVersion:'2025-03-26',capabilities:{tools:{}},serverInfo:{name:'Gold News Desk',version:'1.0.0'}};
   else if(method==='notifications/initialized')return new Response(null,{status:202});
   else if(method==='tools/list')result={tools:toolList};
   else if(method==='tools/call'){
    try{const data=params.name==='read_news_snapshot'?await read(env):params.name==='publish_news_snapshot'?await write(env,params.arguments?.snapshot):(()=>{throw Error('Unknown tool');})();result={content:[{type:'text',text:JSON.stringify(data)}]};}
    catch(error){result={isError:true,content:[{type:'text',text:error.message}]};}
   }else return json({jsonrpc:'2.0',id,error:{code:-32601,message:'Unknown method'}});
   return json({jsonrpc:'2.0',id,result});
  }
  const path=url.pathname==='/'?'/index.html':url.pathname;const body=ASSETS[path];if(body===undefined)return json({error:'Not found'},404);
  const type=path.endsWith('.html')?'text/html; charset=utf-8':path.endsWith('.css')?'text/css':path.endsWith('.js')?'application/javascript':'text/plain';
  return new Response(body,{headers:{'Content-Type':type,'X-Content-Type-Options':'nosniff','Cache-Control':'no-cache'}});
 }catch(error){return json({error:error.message||'News service unavailable'},400);}
}};
