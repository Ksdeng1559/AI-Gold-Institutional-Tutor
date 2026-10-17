import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const files={'/':'index.html','/app.js':'app.js','/core.js':'core.js','/style.css':'style.css'};
createServer(async(req,res)=>{const file=files[new URL(req.url,'http://localhost').pathname];if(!file){res.writeHead(404);return res.end('Not found');}try{const data=await readFile(fileURLToPath(new URL('./app/'+file,import.meta.url)));res.writeHead(200,{'Content-Type':file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'text/html','X-Content-Type-Options':'nosniff'});res.end(data);}catch{res.writeHead(500);res.end('Unable to load application');}}).listen(Number(process.env.PORT)||3000,'127.0.0.1',()=>console.log('Journal: http://127.0.0.1:3000'));
