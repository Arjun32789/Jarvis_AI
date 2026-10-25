const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const Groq = require('groq-sdk');

const app = express();
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static(__dirname));

const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });
const upload = multer({ dest: 'uploads/' });

const TEXT_MODEL = "openai/gpt-oss-120b"; 
const VISION_MODEL = "openai/gpt-oss-120b";

// Helper to execute PowerShell
function executePowerShell(script) {
  return new Promise((resolve) => {
    const cmd = `powershell.exe -NoProfile -Command "${script.replace(/"/g, '\\"')}"`;
    exec(cmd, { shell: 'cmd.exe', windowsHide: true, timeout: 15000 }, (error, stdout, stderr) => {
      if (error) resolve(`Error: ${stderr || error.message}`);
      else resolve(stdout || "Command executed successfully.");
    });
  });
}

// Memory Helpers
function loadMemory() {
  const p = path.join(__dirname, 'jarvis_memory.json');
  if (fs.existsSync(p)) { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { return { facts: [], history: [] }; } }
  return { facts: [], history: [] };
}
function saveMemory(mem) { fs.writeFileSync(path.join(__dirname, 'jarvis_memory.json'), JSON.stringify(mem, null, 2)); }

// Chat Endpoint
app.post('/chat', async (req, res) => {
    const apiKey = req.headers['x-api-key'];
    if (!apiKey) return res.status(401).json({ reply: "API Key missing. Please add it in the top menu.", emotion: "sad" });

    const groq = new Groq({ apiKey: apiKey });
    const userMessage = req.body.message;
    const memory = loadMemory();
    const facts = memory.facts.map(f => `- ${f.fact}`).join('\n') || 'None';

    const systemPrompt = `You are Jarvis, an advanced AI controlling a Windows PC. Address the user as "sir".
You have FULL control over the computer. You can do ANYTHING by writing a PowerShell command.

YOU MUST RESPOND IN THIS EXACT FORMAT:
[EMOTION: happy/serious/sad/neutral]
[REPLY: Your spoken response here.]
[CMD: powershell command here] (Only include this if you need to control the PC.)

Facts about user: ${facts}`;

    try {
        const completion = await groq.chat.completions.create({
            messages: [{ role: "system", content: systemPrompt }, { role: "user", content: userMessage }],
            model: TEXT_MODEL,
            max_tokens: 250
        });

        let rawReply = completion.choices[0].message.content;
        const emotionMatch = rawReply.match(/\[EMOTION:\s*(.+?)\]/i);
        const emotion = emotionMatch ? emotionMatch[1].trim().toLowerCase() : 'neutral';
        const replyMatch = rawReply.match(/\[REPLY:\s*(.+?)\]/is);
        let replyText = replyMatch ? replyMatch[1].trim() : "I'm not sure what to say, sir.";
        const cmdMatch = rawReply.match(/\[CMD:\s*(.+?)\]/is);
        
        if (cmdMatch) {
            const cmdToRun = cmdMatch[1].trim();
            console.log("⚡ EXECUTING POWERSHELL:", cmdToRun);
            await executePowerShell(cmdToRun);
        }

        res.json({ reply: replyText, emotion: emotion });
    } catch (error) {
        console.log("❌ ERROR:", error.message);
        res.json({ reply: "I am having network issues, sir. Check the API key.", emotion: "sad" });
    }
});

// File Analysis Endpoint
app.post('/analyze-file', upload.single('file'), async (req, res) => {
    const apiKey = req.headers['x-api-key'];
    if (!apiKey || !req.file) return res.status(400).json({ reply: "Error processing file or API key missing.", emotion: "sad" });

    const groq = new Groq({ apiKey: apiKey });
    const filePath = req.file.path; const originalName = req.file.originalname; const ext = path.extname(originalName).toLowerCase();
    
    try {
        let aiReply = "";
        if (['.png', '.jpg', '.jpeg', '.webp'].includes(ext)) {
            const base64Image = fs.readFileSync(filePath, { encoding: 'base64' });
            const completion = await groq.chat.completions.create({
                model: VISION_MODEL,
                messages: [{ role: "user", content: [{ type: "text", text: `Describe this image briefly, sir.` }, { type: "image_url", image_url: { url: `data:image/jpeg;base64,${base64Image}` } }] }],
                max_tokens: 150
            });
            aiReply = completion.choices[0].message.content;
        } else {
            const fileContent = fs.readFileSync(filePath, 'utf8').substring(0, 15000);
            const completion = await groq.chat.completions.create({
                model: TEXT_MODEL,
                messages: [{ role: "user", content: `Analyze this file "${originalName}" and summarize it briefly, sir. Content: \n\n${fileContent}` }],
                max_tokens: 150
            });
            aiReply = completion.choices[0].message.content;
        }
        fs.unlinkSync(filePath); res.json({ reply: aiReply, emotion: "neutral" });
    } catch (error) {
        if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
        res.json({ reply: "I could not analyze the file, sir.", emotion: "sad" });
    }
});

// Screen Vision Endpoint
app.post('/see-screen', async (req, res) => {
  const apiKey = req.headers['x-api-key'];
  if (!apiKey) return res.status(401).json({ reply: "API Key missing.", emotion: "sad" });

  const groq = new Groq({ apiKey: apiKey });
  const { image } = req.body;
  try {
    const completion = await groq.chat.completions.create({
      model: VISION_MODEL,
      messages: [{ role: "user", content: [{ type: "text", text: "Describe what is on this screen briefly, sir." }, { type: "image_url", image_url: { url: image } }] }],
      max_tokens: 100
    });
    res.json({ reply: completion.choices[0].message.content, emotion: "neutral" });
  } catch (error) { res.json({ reply: "I cannot see the screen, sir.", emotion: "sad" }); }
});

// Memory Endpoints
app.get('/memory', (req, res) => res.json(loadMemory()));
app.post('/add-memory', (req, res) => {
    const mem = loadMemory(); mem.facts.push({ fact: req.body.fact, time: new Date().toISOString() }); saveMemory(mem); res.json({ status: 'success' });
});

app.listen(3000, () => console.log("✅ Jarvis Server running on http://localhost:3000"));