import React, { useState, useEffect, useRef } from 'react'
import { 
  Plus, MessageSquare, Settings, Trash2, 
  Send, Copy, Check, X, Menu, Sparkles, 
  AlertCircle, Loader2
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { v4 as uuidv4 } from 'uuid'
import { API_URL, DEFAULT_MODEL } from './config'

// Storage keys
const STORAGE_KEYS = {
  CONVERSATIONS: 'mhlaba_conversations',
  CURRENT_CONVERSATION: 'mhlaba_current_conversation'
}

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
    setTimeout(() => setCopied(false), 2002)
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

// Main App
function App() {
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [input, setInput] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [apiStatus, setApiStatus] = useState('checking') // 'checking', 'connected', 'error'
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [error, setError] = useState(null)
  
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  
  // Load data from localStorage on mount
  useEffect(() => {
    const savedConversations = localStorage.getItem(STORAGE_KEYS.CONVERSATIONS)
    const savedCurrent = localStorage.getItem(STORAGE_KEYS.CURRENT_CONVERSATION)
    
    if (savedConversations) {
      setConversations(JSON.parse(savedConversations))
    }
    if (savedCurrent) {
      setCurrentConversationId(savedCurrent)
    }
  }, [])
  
  // Check API health on mount
  useEffect(() => {
    checkApiHealth()
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
  
  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [conversations, currentConversationId, isGenerating])
  
  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/api/health`)
      if (response.ok) {
        setApiStatus('connected')
        setError(null)
      } else {
        setApiStatus('error')
        setError('API server is not responding. Please check if the backend is running.')
      }
    } catch (err) {
      console.error('API health check failed:', err)
      setApiStatus('error')
      setError('Cannot connect to API server. Please check your backend deployment.')
    }
  }
  
  const currentConversation = conversations.find(c => c.id === currentConversationId)
  
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
    if (!input.trim() || isGenerating || apiStatus !== 'connected') return
    
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
    setError(null)
    
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
      
      // Prepare messages for API
      const messages = [
        { role: "system", content: "You are MHLABA, a helpful AI assistant. Be concise, helpful, and friendly." },
        ...updatedMessages.map(m => ({ role: m.role, content: m.content }))
      ]
      
      // Call API
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: DEFAULT_MODEL,
          messages,
          stream: false
        })
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `HTTP ${response.status}`)
      }
      
      const data = await response.json()
      const assistantContent = data.message?.content || data.response || 'No response'
      
      const assistantMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: assistantContent,
        timestamp: Date.now()
      }
      
      setConversations(prev => prev.map(c => 
        c.id === currentConversationId 
          ? { ...c, messages: [...updatedMessages, assistantMessage] }
          : c
      ))
      
    } catch (err) {
      console.error('Generation error:', err)
      setError(`Error: ${err.message}. Please try again.`)
      
      const errorMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: `Error: ${err.message}. Please check if the API server is running.`,
        timestamp: Date.now(),
        isError: true
      }
      
      setConversations(prev => prev.map(c => 
        c.id === currentConversationId 
          ? { ...c, messages: [...updatedMessages, errorMessage] }
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
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px',
            fontSize: '12px',
            color: apiStatus === 'connected' ? 'var(--success)' : 'var(--error)'
          }}>
            <span style={{ 
              width: '8px', 
              height: '8px', 
              borderRadius: '50%', 
              background: apiStatus === 'connected' ? 'var(--success)' : 'var(--error)',
              display: 'inline-block'
            }} />
            {apiStatus === 'connected' ? 'API Connected' : 'API Disconnected'}
          </div>
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
            <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              Model: {DEFAULT_MODEL}
            </span>
          </div>
        </header>
        
        {/* Error Banner */}
        {(error || apiStatus === 'error') && (
          <div className="error-banner">
            <AlertCircle size={16} />
            <span>{error || 'Cannot connect to API server'}</span>
            <button onClick={() => { setError(null); checkApiHealth(); }}>
              <Loader2 size={14} style={{ animation: 'spin 1s linear infinite' }} />
            </button>
          </div>
        )}
        
        {/* Chat */}
        <div className="chat-container">
          {!currentConversation || currentConversation.messages.length === 0 ? (
            <div className="welcome-screen">
              <div className="welcome-logo">M</div>
              <h1 className="welcome-title">How can I help you today?</h1>
              <p className="welcome-subtitle">
                I'm MHLABA, your personal AI assistant powered by Ollama.
                {apiStatus !== 'connected' && ' Please wait while we connect to the API...'}
              </p>
              
              {apiStatus === 'checking' && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--text-muted)' }}>
                  <Loader2 size={20} style={{ animation: 'spin 1s linear infinite' }} />
                  Connecting to API...
                </div>
              )}
              
              <div className="suggestion-chips">
                {SUGGESTIONS.map((suggestion, idx) => (
                  <button 
                    key={idx} 
                    className="suggestion-chip"
                    disabled={apiStatus !== 'connected'}
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
              
              {isGenerating && (
                <div className="message assistant">
                  <div className="message-avatar assistant">M</div>
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              
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
                placeholder={
                  apiStatus === 'connected' 
                    ? "Message MHLABA..." 
                    : apiStatus === 'checking'
                    ? "Connecting to API..."
                    : "API unavailable. Check backend..."
                }
                rows={1}
                style={{ minHeight: '24px' }}
                disabled={apiStatus !== 'connected' && apiStatus !== 'checking'}
              />
            </div>
            <button 
              className="send-btn"
              onClick={handleSend}
              disabled={!input.trim() || isGenerating || apiStatus !== 'connected'}
            >
              <Send size={18} />
            </button>
          </div>
          
          <div className="input-footer">
            <span>
              {apiStatus === 'connected' 
                ? `Connected to Ollama · Model: ${DEFAULT_MODEL}`
                : apiStatus === 'checking'
                ? 'Checking API connection...'
                : 'API disconnected. Check backend.'
              }
            </span>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
