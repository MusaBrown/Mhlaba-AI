/**
 * MHLABA API Server
 * Proxies requests to Ollama and handles CORS
 */

const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Ollama configuration
const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://localhost:11434';
const DEFAULT_MODEL = process.env.DEFAULT_MODEL || 'llama3.2';

// CORS - Allow your Netlify frontend
const corsOptions = {
  origin: [
    'http://localhost:3000',
    'http://localhost:5173',
    // Add your Netlify domain after deployment
    // 'https://mhlaba-ai-xxx.netlify.app',
    // Or allow all (less secure)
    // '*'
  ],
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
};

app.use(cors(corsOptions));
app.use(express.json());

// Health check
app.get('/api/health', async (req, res) => {
  try {
    const response = await fetch(`${OLLAMA_HOST}/api/tags`);
    if (response.ok) {
      res.json({ status: 'ok', ollama: 'connected' });
    } else {
      res.status(503).json({ status: 'error', message: 'Ollama not responding' });
    }
  } catch (error) {
    res.status(503).json({ status: 'error', message: error.message });
  }
});

// List available models
app.get('/api/models', async (req, res) => {
  try {
    const response = await fetch(`${OLLAMA_HOST}/api/tags`);
    const data = await response.json();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Generate completion
app.post('/api/generate', async (req, res) => {
  const { prompt, model = DEFAULT_MODEL, stream = false, context, options } = req.body;
  
  try {
    const response = await fetch(`${OLLAMA_HOST}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        prompt,
        stream,
        context,
        options: {
          temperature: 0.7,
          num_predict: 2048,
          ...options
        }
      })
    });
    
    if (stream) {
      // Stream response
      res.setHeader('Content-Type', 'application/x-ndjson');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
      
      const reader = response.body.getReader();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        res.write(value);
      }
      
      res.end();
    } else {
      const data = await response.json();
      res.json(data);
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Chat completion (conversational)
app.post('/api/chat', async (req, res) => {
  const { messages, model = DEFAULT_MODEL, stream = false } = req.body;
  
  try {
    const response = await fetch(`${OLLAMA_HOST}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        messages,
        stream,
        options: {
          temperature: 0.7,
          num_predict: 2048
        }
      })
    });
    
    if (stream) {
      res.setHeader('Content-Type', 'application/x-ndjson');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
      
      const reader = response.body.getReader();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        res.write(value);
      }
      
      res.end();
    } else {
      const data = await response.json();
      res.json(data);
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Pull/download a model
app.post('/api/pull', async (req, res) => {
  const { model } = req.body;
  
  try {
    const response = await fetch(`${OLLAMA_HOST}/api/pull`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: model, stream: false })
    });
    
    const data = await response.json();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 MHLABA API running on port ${PORT}`);
  console.log(`🔗 Connected to Ollama at ${OLLAMA_HOST}`);
  console.log(`🤖 Default model: ${DEFAULT_MODEL}`);
});
