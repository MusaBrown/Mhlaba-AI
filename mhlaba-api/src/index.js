/**
 * MHLABA API Server
 * Uses YOUR API key - users don't need to enter anything!
 */

const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// ============================================
// CONFIGURE YOUR AI PROVIDER HERE
// ============================================

// Option 1: OpenAI (Recommended)
const AI_PROVIDER = process.env.AI_PROVIDER || 'openai'; // 'openai' or 'anthropic'
const OPENAI_API_KEY = process.env.OPENAI_API_KEY; // Set in Render/dashboard
const OPENAI_MODEL = process.env.OPENAI_MODEL || 'gpt-3.5-turbo';

// Option 2: Anthropic
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const ANTHROPIC_MODEL = process.env.ANTHROPIC_MODEL || 'claude-3-haiku-20240307';

// Option 3: Groq (Fast & Cheap!)
const GROQ_API_KEY = process.env.GROQ_API_KEY;
const GROQ_MODEL = process.env.GROQ_MODEL || 'llama3-8b-8192';

// ============================================

// CORS - Allow your Netlify frontend
const corsOptions = {
  origin: [
    'http://localhost:3000',
    'http://localhost:5173',
    // Add your Netlify domain after deployment:
    // 'https://mhlaba-ai-xxx.netlify.app',
  ],
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type'],
  credentials: true
};

app.use(cors(corsOptions));
app.use(express.json());

// Health check
app.get('/api/health', (req, res) => {
  const keyStatus = AI_PROVIDER === 'openai' && OPENAI_API_KEY ? 'configured' :
                    AI_PROVIDER === 'anthropic' && ANTHROPIC_API_KEY ? 'configured' :
                    AI_PROVIDER === 'groq' && GROQ_API_KEY ? 'configured' : 'missing';
  
  res.json({ 
    status: 'ok', 
    provider: AI_PROVIDER,
    key_status: keyStatus,
    model: AI_PROVIDER === 'openai' ? OPENAI_MODEL :
           AI_PROVIDER === 'anthropic' ? ANTHROPIC_MODEL :
           AI_PROVIDER === 'groq' ? GROQ_MODEL : 'unknown'
  });
});

// Chat completion - uses YOUR API key!
app.post('/api/chat', async (req, res) => {
  const { messages, stream = false } = req.body;
  
  try {
    let response;
    let requestBody;
    let headers;
    let apiUrl;
    
    if (AI_PROVIDER === 'openai') {
      // OpenAI API
      if (!OPENAI_API_KEY) {
        return res.status(500).json({ error: 'OpenAI API key not configured' });
      }
      
      apiUrl = 'https://api.openai.com/v1/chat/completions';
      headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      };
      requestBody = {
        model: OPENAI_MODEL,
        messages,
        temperature: 0.7,
        max_tokens: 2048,
        stream
      };
      
    } else if (AI_PROVIDER === 'anthropic') {
      // Anthropic API
      if (!ANTHROPIC_API_KEY) {
        return res.status(500).json({ error: 'Anthropic API key not configured' });
      }
      
      apiUrl = 'https://api.anthropic.com/v1/messages';
      headers = {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      };
      requestBody = {
        model: ANTHROPIC_MODEL,
        messages: messages.filter(m => m.role !== 'system'),
        system: messages.find(m => m.role === 'system')?.content,
        max_tokens: 2048,
        temperature: 0.7,
        stream
      };
      
    } else if (AI_PROVIDER === 'groq') {
      // Groq API (Fast & Cheap!)
      if (!GROQ_API_KEY) {
        return res.status(500).json({ error: 'Groq API key not configured' });
      }
      
      apiUrl = 'https://api.groq.com/openai/v1/chat/completions';
      headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GROQ_API_KEY}`
      };
      requestBody = {
        model: GROQ_MODEL,
        messages,
        temperature: 0.7,
        max_tokens: 2048,
        stream
      };
      
    } else {
      return res.status(500).json({ error: 'No AI provider configured' });
    }
    
    // Make request to AI provider
    response = await fetch(apiUrl, {
      method: 'POST',
      headers,
      body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      console.error('AI API Error:', error);
      return res.status(response.status).json({ 
        error: error.error?.message || `API Error: ${response.status}` 
      });
    }
    
    if (stream) {
      // Stream response
      res.setHeader('Content-Type', 'text/event-stream');
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
      // Non-stream response
      const data = await response.json();
      
      // Normalize response format
      let normalizedResponse;
      if (AI_PROVIDER === 'anthropic') {
        normalizedResponse = {
          message: {
            role: 'assistant',
            content: data.content?.[0]?.text || data.completion || ''
          }
        };
      } else {
        // OpenAI / Groq format
        normalizedResponse = {
          message: {
            role: 'assistant',
            content: data.choices?.[0]?.message?.content || ''
          }
        };
      }
      
      res.json(normalizedResponse);
    }
    
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Simple generate endpoint
app.post('/api/generate', async (req, res) => {
  const { prompt } = req.body;
  
  try {
    const messages = [
      { role: 'system', content: 'You are MHLABA, a helpful AI assistant.' },
      { role: 'user', content: prompt }
    ];
    
    // Reuse chat endpoint logic
    req.body = { messages, stream: false };
    
    // Forward to chat handler
    const response = await fetch(`http://localhost:${PORT}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    
    const data = await response.json();
    res.json(data);
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 MHLABA API running on port ${PORT}`);
  console.log(`🤖 AI Provider: ${AI_PROVIDER}`);
  console.log(`🔑 API Key: ${AI_PROVIDER === 'openai' && OPENAI_API_KEY ? '✅ Configured' : 
                              AI_PROVIDER === 'anthropic' && ANTHROPIC_API_KEY ? '✅ Configured' :
                              AI_PROVIDER === 'groq' && GROQ_API_KEY ? '✅ Configured' : '❌ Missing'}`);
});
