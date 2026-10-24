export default function handler(req,res){
 res.setHeader('Cache-Control','private, no-store');
 const path=new URL(req.url,'https://preview.invalid').pathname;
 if(path==='/api/health'&&req.method==='GET')return res.status(200).json({mode:'preview',configured:false,journal_storage:false,research_mode:'dated snapshot copy'});
 return res.status(503).json({error:'Private journal and write APIs remain on the original terminal until the PostgreSQL migration is complete.'});
}
