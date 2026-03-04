import React, { useState, useEffect, useRef, useCallback } from 'react'
import { 
  Plus, MessageSquare, Settings, Trash2, 
  Send, Copy, Check, MoreHorizontal, X,
  Menu, Sparkles, Cpu, Download, AlertCircle
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { v4 as uuidv4 } from 'uuid'
import * as webllm from "@mlc-ai/web-llm"

// Storage keys
const STORAGE_KEYS = {
  CONVERSATIONS: 'mhlaba_conversations',
  CURRENT_CONVERSATION: 'mhlaba_current_conversation',
  SELECTED_MODEL: 'mhlaba_selected_model'
}

// Available models - all run in browser, no API key needed!
const AVAILABLE_MODELS = [
  {
    id: "Llama-3.1-8B-Instruct-q4f32_1-MLC",
    name: "Llama 3.1 8B",
    description: "Fast & capable - Good for most tasks",
    size: "4.5 GB",
    quant: "q4f32"
  },
  {
    id: "Phi-3-mini-4k-instruct-q4f32_1-MLC",
    name: "Phi-3 Mini",
    description: "Small & fast - Great for quick responses",
    size: "1.8 GB",
    quant: "q4f32"
  },
  {
    id: "Qwen2.5-7B-Instruct-q4f32_1-MLC",
    name: "Qwen 2.5 7B",
    description: "Excellent multilingual support",
    size: "4.3 GB",
    quant: "q4f32"
  },
  {
    id: "Mistral-7B-Instruct-v0.3-q4f32_1-MLC",
    name: "Mistral 7B",
    description: "High quality responses",
    size: "4.5 GB",
    quant: "q4f32"
  },
  {
    id: "gemma-2-2b-it-q4f32_1-MLC",
    name: "Gemma 2 2B",
    description: "Tiny but mighty - Fastest option",
    size: "1.6 GB",
    quant: "q4f32"
  }
]

// Suggestion chips
const SUGGESTIONS = [
  "Explain quantum computing in simple terms",
  "Help me write a Python function to sort a list",
  "What are the best practices for React hooks?",
  "Create a workout plan for beginners",
  "Write a short poem about technology"
]

// Code block component
function CodeBlock({ language, value }) {
  const [copied, setCopied] = useState(false)
  
  const handleCopy = () => {
    navigator.clipboard.writeText(value)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  
  return (
    <div className="code-block">
      <div className="code-header">
        <span>{language || 'code'}</span>
        <button className="code-copy-btn" onClick={handleCopy}>
          {copied ? <Check size={14} /> : <Copy size={14} />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>
      <SyntaxHighlighter
        language={language || 'text'}
        style={vscDarkPlus}
        customStyle={{ margin: 0, borderRadius: '0 0 8px 8px' }}
      >
        {value}
      </SyntaxHighlighter>
    </div>
  )
}

// Message component
function Message({ message }) {
  const [copied, setCopied] = useState(false)
  const isUser = message.role === 'user'
  
  const handleCopy = () => {
    navigator.clipboard.writeText(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  
  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className={`message-avatar ${message.role}`}>
        {isUser ? 'You' : 'M'}
      </div>
      <div className="message-content">
        <div className="message-header">
          <span className="message-author">{isUser ? 'You' : 'MHLABA'}</span>
          <span className="message-time">
            {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        <div className="message-body">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '')
                const value = String(children).replace(/\n$/, '')
                
                if (!inline && match) {
                  return <CodeBlock language={match[1]} value={value} />
                }
                
                return (
                  <code className={className} {...props}>
                    {children}
                  </code>
                )
              }
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        <div className="message-actions">
          <button className="message-action-btn" onClick={handleCopy}>
            {copied ? <Check size={14} /> : <Copy size={14} />}
            {copied ? 'Copied' : 'Copy'}
          </button>
        </div>
      </div>
    </div>
  )
}

// Model Selector Modal
function ModelSelector({ isOpen, onClose, selectedModel, onSelectModel, onLoadModel, loading, progress }) {
  if (!isOpen) return null
  
  const selectedModelInfo = AVAILABLE_MODELS.find(m => m.id === selectedModel)
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">
            <Cpu size={20} style={{ marginRight: 8, verticalAlign: 'middle' }}/>
            Select AI Model
          </h2>
          <button className="modal-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>
        
        <div className="modal-body">
          <p style={{ color: 'var(--text-secondary)', marginBottom: 20, fontSize: 14 }}>
            Models run entirely in your browser using WebGPU. No API keys needed!
          </p>
          
          {loading && (
            <div className="progress-container" style={{ marginBottom: 20 }}>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${progress.percent}%` }}
                />
              </div>
              <div className="progress-text">
                <span>{progress.text}</span>
                <span>{progress.percent}%</span>
              </div>
            </div>
          )}
          
          <div className="model-list">
            {AVAILABLE_MODELS.map(model => (
              <div 
                key={model.id}
                className={`model-item ${selectedModel === model.id ? 'selected' : ''}`}
                onClick={() => onSelectModel(model.id)}
              >
                <div className="model-radio">
                  <div className={`radio-circle ${selectedModel === model.id ? 'checked' : ''}`} />
                </div>
                <div className="model-info">
                  <div className="model-name">{model.name}</div>
                  <div className="model-description">{model.description}</div>
                  <div className="model-meta">
                    <span className="model-size">
                      <Download size={12} />
                      {model.size}
                    </span>
                    <span className="model-quant">{model.quant}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="webgpu-warning" style={{ marginTop: 20 }}>
            <AlertCircle size={16} />
            <span>
              Requires Chrome/Edge with WebGPU enabled. 
              <a href="chrome://flags/#enable-unsafe-webgpu" target="_blank" rel="noopener">
                Enable here
              </a>
            </span>
          </div>
        </div>
        
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
          <button 
            className="btn btn-primary" 
            onClick={onLoadModel}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Load Model'}
          </button>
        </div>
      </div>
    </div>
  )
}

// Main App
function App() {
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [input, setInput] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [selectedModel, setSelectedModel] = useState(AVAILABLE_MODELS[0].id)
  const [isModelSelectorOpen, setIsModelSelectorOpen] = useState(false)
  const [loadingModel, setLoadingModel] = useState(false)
  const [loadProgress, setLoadProgress] = useState({ text: '', percent: 0 })
  const [engine, setEngine] = useState(null)
  const [modelLoaded, setModelLoaded] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [error, setError] = useState(null)
  
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const abortControllerRef = useRef(null)
  
  // Load data from localStorage on mount
  useEffect(() => {
    const savedConversations = localStorage.getItem(STORAGE_KEYS.CONVERSATIONS)
    const savedCurrent = localStorage.getItem(STORAGE_KEYS.CURRENT_CONVERSATION)
    const savedModel = localStorage.getItem(STORAGE_KEYS.SELECTED_MODEL)
    
    if (savedConversations) {
      setConversations(JSON.parse(savedConversations))
    }
    if (savedCurrent) {
      setCurrentConversationId(savedCurrent)
    }
    if (savedModel) {
      setSelectedModel(savedModel)
    }
  }, [])
  
  // Save to localStorage
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.CONVERSATIONS, JSON.stringify(conversations))
  }, [conversations])
  
  useEffect(() => {
    if (currentConversationId) {
      localStorage.setItem(STORAGE_KEYS.CURRENT_CONVERSATION, currentConversationId)
    }
  }, [currentConversationId])
  
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.SELECTED_MODEL, selectedModel)
  }, [selectedModel])
  
  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [conversations, currentConversationId, isGenerating])
  
  // Initialize WebLLM engine
  const loadModel = useCallback(async () => {
    setLoadingModel(true)
    setLoadProgress({ text: 'Initializing...', percent: 0 })
    setError(null)
    
    try {
      const initProgressCallback = (report) => {
        setLoadProgress({
          text: report.text,
          percent: Math.round(report.progress * 100)
        })
      }
      
      const newEngine = await webllm.CreateMLCEngine(
        selectedModel,
        { initProgressCallback }
      )
      
      setEngine(newEngine)
      setModelLoaded(true)
      setIsModelSelectorOpen(false)
    } catch (err) {
      console.error('Failed to load model:', err)
      setError(err.message || 'Failed to load model. Make sure WebGPU is enabled.')
    } finally {
      setLoadingModel(false)
    }
  }, [selectedModel])
  
  const currentConversation = conversations.find(c => c.id === currentConversationId)
  const selectedModelInfo = AVAILABLE_MODELS.find(m => m.id === selectedModel)
  
  const createNewConversation = () => {
    const newConversation = {
      id: uuidv4(),
      title: 'New Conversation',
      messages: [],
      createdAt: Date.now()
    }
    setConversations([newConversation, ...conversations])
    setCurrentConversationId(newConversation.id)
  }
  
  const deleteConversation = (id, e) => {
    e.stopPropagation()
    setConversations(conversations.filter(c => c.id !== id))
    if (currentConversationId === id) {
      setCurrentConversationId(null)
    }
  }
  
  const handleSend = async () => {
    if (!input.trim() || isGenerating) return
    
    if (!modelLoaded) {
      setIsModelSelectorOpen(true)
      return
    }
    
    const userMessage = {
      id: uuidv4(),
      role: 'user',
      content: input.trim(),
      timestamp: Date.now()
    }
    
    // Create new conversation if none exists
    if (!currentConversation) {
      createNewConversation()
    }
    
    const updatedMessages = [...(currentConversation?.messages || []), userMessage]
    
    setConversations(prev => prev.map(c => 
      c.id === currentConversationId 
        ? { ...c, messages: updatedMessages }
        : c
    ))
    
    setInput('')
    setIsGenerating(true)
    
    try {
      // Generate title on first message
      if (updatedMessages.length === 1) {
        const title = userMessage.content.slice(0, 40) + 
          (userMessage.content.length > 40 ? '...' : '')
        setConversations(prev => prev.map(c => 
          c.id === currentConversationId 
            ? { ...c, title }
            : c
        ))
      }
      
      // Prepare messages for the model
      const messages = [
        { role: "system", content: "You are MHLABA, a helpful AI assistant. Be concise, helpful, and friendly." },
        ...updatedMessages.map(m => ({ role: m.role, content: m.content }))
      ]
      
      // Stream the response
      const completion = await engine.chat.completions.create({
        messages,
        temperature: 0.7,
        max_tokens: 2048,
        stream: true,
      })
      
      let assistantContent = ""
      
      for await (const chunk of completion) {
        const content = chunk.choices[0]?.delta?.content || ""
        assistantContent += content
        
        // Update the conversation with the partial response
        setConversations(prev => {
          const conv = prev.find(c => c.id === currentConversationId)
          if (!conv) return prev
          
          const existingMessages = conv.messages.filter(m => m.id !== 'streaming')
          
          return prev.map(c => 
            c.id === currentConversationId 
              ? { 
                  ...c, 
                  messages: [
                    ...existingMessages,
                    {
                      id: 'streaming',
                      role: 'assistant',
                      content: assistantContent,
                      timestamp: Date.now()
                    }
                  ]
                }
              : c
          )
        })
      }
      
      // Finalize with a proper ID
      setConversations(prev => {
        const conv = prev.find(c => c.id === currentConversationId)
        if (!conv) return prev
        
        const existingMessages = conv.messages.filter(m => m.id !== 'streaming')
        
        return prev.map(c => 
          c.id === currentConversationId 
            ? { 
                ...c, 
                messages: [
                  ...existingMessages,
                  {
                    id: uuidv4(),
                    role: 'assistant',
                    content: assistantContent,
                    timestamp: Date.now()
                  }
                ]
              }
            : c
        )
      })
      
    } catch (err) {
      console.error('Generation error:', err)
      setError(err.message || 'Failed to generate response')
      
      const errorMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: `Error: ${err.message || 'Something went wrong. Please try again.'}`,
        timestamp: Date.now(),
        isError: true
      }
      
      setConversations(prev => prev.map(c => 
        c.id === currentConversationId 
          ? { ...c, messages: [...(c.messages.filter(m => m.id !== 'streaming')), errorMessage] }
          : c
      ))
    } finally {
      setIsGenerating(false)
    }
  }
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }
  
  return (
    <div className="app">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? '' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="logo">M</div>
          <span className="brand">MHLABA</span>
        </div>
        
        <button className="new-chat-btn" onClick={createNewConversation}>
          <Plus size={18} />
          New Chat
        </button>
        
        <div className="conversations-list">
          {conversations.map(conv => (
            <div
              key={conv.id}
              className={`conversation-item ${conv.id === currentConversationId ? 'active' : ''}`}
              onClick={() => setCurrentConversationId(conv.id)}
            >
              <MessageSquare size={16} />
              <span className="conversation-title">{conv.title}</span>
              <button 
                className="icon-btn" 
                style={{ opacity: 0, marginLeft: 'auto' }}
                onClick={(e) => deleteConversation(conv.id, e)}
                onMouseEnter={e => e.currentTarget.style.opacity = 1}
                onMouseLeave={e => e.currentTarget.style.opacity = 0}
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))}
        </div>
        
        <div className="sidebar-footer">
          <button 
            className="icon-btn" 
            onClick={() => setIsModelSelectorOpen(true)}
            title="Change Model"
          >
            <Cpu size={18} />
          </button>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {!sidebarOpen && (
              <button className="icon-btn" onClick={() => setSidebarOpen(true)}>
                <Menu size={18} />
              </button>
            )}
            <span className="header-title">
              {currentConversation?.title || 'MHLABA AI Assistant'}
            </span>
          </div>
          
          <div className="header-actions">
            <button 
              className="model-selector"
              onClick={() => setIsModelSelectorOpen(true)}
              style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
            >
              <Cpu size={14} />
              {selectedModelInfo?.name || 'Select Model'}
              {modelLoaded && <span style={{ color: 'var(--success)' }}>●</span>}
            </button>
          </div>
        </header>
        
        {/* Error Banner */}
        {error && (
          <div className="error-banner">
            <AlertCircle size={16} />
            <span>{error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}
        
        {/* Chat */}
        <div className="chat-container">
          {!currentConversation || currentConversation.messages.length === 0 ? (
            <div className="welcome-screen">
              <div className="welcome-logo">M</div>
              <h1 className="welcome-title">How can I help you today?</h1>
              <p className="welcome-subtitle">
                I'm MHLABA, your personal AI assistant. I run entirely in your browser 
                using WebLLM - no API keys needed!
              </p>
              
              {!modelLoaded && (
                <button 
                  className="load-model-btn"
                  onClick={() => setIsModelSelectorOpen(true)}
                >
                  <Download size={18} />
                  Load AI Model to Start
                </button>
              )}
              
              <div className="suggestion-chips">
                {SUGGESTIONS.map((suggestion, idx) => (
                  <button 
                    key={idx} 
                    className="suggestion-chip"
                    disabled={!modelLoaded}
                    onClick={() => {
                      setInput(suggestion)
                      inputRef.current?.focus()
                    }}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages">
              {currentConversation.messages.map(message => (
                <Message key={message.id} message={message} />
              ))}
              
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
        
        {/* Input */}
        <div className="input-container">
          <div className="input-wrapper">
            <div className="input-box">
              <textarea
                ref={inputRef}
                className="input-field"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={modelLoaded ? "Message MHLABA..." : "Load a model first to start chatting..."}
                rows={1}
                style={{ minHeight: '24px' }}
                disabled={!modelLoaded && !isGenerating}
              />
            </div>
            <button 
              className="send-btn"
              onClick={handleSend}
              disabled={!input.trim() || isGenerating || !modelLoaded}
            >
              <Send size={18} />
            </button>
          </div>
          
          <div className="input-footer">
            <div className="input-tools">
              <button className="tool-btn" onClick={() => setIsModelSelectorOpen(true)}>
                <Cpu size={14} />
                {modelLoaded ? selectedModelInfo?.name : 'Load Model'}
              </button>
            </div>
            <span>
              {modelLoaded 
                ? 'Running locally in your browser with WebLLM'
                : 'No API keys needed - models run locally'
              }
            </span>
          </div>
        </div>
      </main>
      
      {/* Model Selector Modal */}
      <ModelSelector
        isOpen={isModelSelectorOpen}
        onClose={() => setIsModelSelectorOpen(false)}
        selectedModel={selectedModel}
        onSelectModel={setSelectedModel}
        onLoadModel={loadModel}
        loading={loadingModel}
        progress={loadProgress}
      />
    </div>
  )
}

export default App
