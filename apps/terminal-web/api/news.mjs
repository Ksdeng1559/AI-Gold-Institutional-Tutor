export default function handler(req,res){
 res.setHeader('Cache-Control','private, no-store');
 if(req.method!=='GET'){res.setHeader('Allow','GET');return res.status(405).json({error:'Preview research is read-only.'});}
 try {const snapshot=JSON.parse(process.env.GOLD_PREVIEW_SNAPSHOT||'null');if(!snapshot?.updated_at||!Array.isArray(snapshot.stories))throw Error();return res.status(200).json(snapshot);}
 catch{return res.status(503).json({error:'No dated research copy configured.'});}
}
