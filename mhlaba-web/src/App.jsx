import React, { useState, useEffect, useRef } from 'react'
import { 
  Plus, MessageSquare, Settings, Trash2, 
  Send, Copy, Check, MoreHorizontal, X,
  Menu, Moon, Sun, FileText, Sparkles
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { v4 as uuidv4 } from 'uuid'

// Storage keys
const STORAGE_KEYS = {
  CONVERSATIONS: 'mhlaba_conversations',
  CURRENT_CONVERSATION: 'mhlaba_current_conversation',
  SETTINGS: 'mhlaba_settings'
}

// Default settings
const DEFAULT_SETTINGS = {
  provider: 'openai',
  openaiKey: '',
  openaiModel: 'gpt-3.5-turbo',
  anthropicKey: '',
  anthropicModel: 'claude-instant-1'
}

// Suggestion chips
const SUGGESTIONS = [
  "Explain quantum computing in simple terms",
  "Help me write a Python function to sort a list",
  "What are the best practices for React hooks?",
  "Create a workout plan for beginners"
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
function Message({ message, onCopy }) {
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

// Settings Modal
function SettingsModal({ isOpen, onClose, settings, onSave }) {
  const [localSettings, setLocalSettings] = useState(settings)
  
  if (!isOpen) return null
  
  const handleSave = () => {
    onSave(localSettings)
    onClose()
  }
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Settings</h2>
          <button className="modal-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>
        
        <div className="modal-body">
          <div className="provider-tabs">
            <button 
              className={`provider-tab ${localSettings.provider === 'openai' ? 'active' : ''}`}
              onClick={() => setLocalSettings({ ...localSettings, provider: 'openai' })}
            >
              OpenAI
            </button>
            <button 
              className={`provider-tab ${localSettings.provider === 'anthropic' ? 'active' : ''}`}
              onClick={() => setLocalSettings({ ...localSettings, provider: 'anthropic' })}
            >
              Anthropic
            </button>
          </div>
          
          {localSettings.provider === 'openai' ? (
            <>
              <div className="form-group">
                <label className="form-label">OpenAI API Key</label>
                <input
                  type="password"
                  className="form-input"
                  value={localSettings.openaiKey}
                  onChange={e => setLocalSettings({ ...localSettings, openaiKey: e.target.value })}
                  placeholder="sk-..."
                />
                <p className="form-hint">Your API key is stored locally in your browser.</p>
              </div>
              
              <div className="form-group">
                <label className="form-label">Model</label>
                <select 
                  className="form-select"
                  value={localSettings.openaiModel}
                  onChange={e => setLocalSettings({ ...localSettings, openaiModel: e.target.value })}
                >
                  <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                  <option value="gpt-4">GPT-4</option>
                  <option value="gpt-4-turbo">GPT-4 Turbo</option>
                </select>
              </div>
            </>
          ) : (
            <>
              <div className="form-group">
                <label className="form-label">Anthropic API Key</label>
                <input
                  type="password"
                  className="form-input"
                  value={localSettings.anthropicKey}
                  onChange={e => setLocalSettings({ ...localSettings, anthropicKey: e.target.value })}
                  placeholder="sk-ant-..."
                />
                <p className="form-hint">Your API key is stored locally in your browser.</p>
              </div>
              
              <div className="form-group">
                <label className="form-label">Model</label>
                <select 
                  className="form-select"
                  value={localSettings.anthropicModel}
                  onChange={e => setLocalSettings({ ...localSettings, anthropicModel: e.target.value })}
                >
                  <option value="claude-instant-1">Claude Instant</option>
                  <option value="claude-2">Claude 2</option>
                  <option value="claude-3-sonnet-20240229">Claude 3 Sonnet</option>
                  <option value="claude-3-opus-20240229">Claude 3 Opus</option>
                </select>
              </div>
            </>
          )}
        </div>
        
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" onClick={handleSave}>Save Settings</button>
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
  const [isLoading, setIsLoading] = useState(false)
  const [settings, setSettings] = useState(DEFAULT_SETTINGS)
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  
  // Load data from localStorage on mount
  useEffect(() => {
    const savedConversations = localStorage.getItem(STORAGE_KEYS.CONVERSATIONS)
    const savedCurrent = localStorage.getItem(STORAGE_KEYS.CURRENT_CONVERSATION)
    const savedSettings = localStorage.getItem(STORAGE_KEYS.SETTINGS)
    
    if (savedConversations) {
      setConversations(JSON.parse(savedConversations))
    }
    if (savedCurrent) {
      setCurrentConversationId(savedCurrent)
    }
    if (savedSettings) {
      setSettings({ ...DEFAULT_SETTINGS, ...JSON.parse(savedSettings) })
    }
  }, [])
  
  // Save conversations to localStorage
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.CONVERSATIONS, JSON.stringify(conversations))
  }, [conversations])
  
  // Save current conversation to localStorage
  useEffect(() => {
    if (currentConversationId) {
      localStorage.setItem(STORAGE_KEYS.CURRENT_CONVERSATION, currentConversationId)
    }
  }, [currentConversationId])
  
  // Save settings to localStorage
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings))
  }, [settings])
  
  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [conversations, currentConversationId])
  
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
  
  const generateTitle = async (messages) => {
    if (messages.length < 2) return
    
    const firstUserMessage = messages.find(m => m.role === 'user')
    if (!firstUserMessage) return
    
    const title = firstUserMessage.content.slice(0, 40) + 
      (firstUserMessage.content.length > 40 ? '...' : '')
    
    setConversations(prev => prev.map(c => 
      c.id === currentConversationId 
        ? { ...c, title }
        : c
    ))
  }
  
  const callOpenAI = async (messages) => {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${settings.openaiKey}`
      },
      body: JSON.stringify({
        model: settings.openaiModel,
        messages: [
          { role: 'system', content: 'You are MHLABA, a helpful AI assistant. Be concise and helpful.' },
          ...messages.map(m => ({ role: m.role, content: m.content }))
        ],
        temperature: 0.7,
        max_tokens: 2000
      })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error?.message || 'Failed to get response from OpenAI')
    }
    
    const data = await response.json()
    return data.choices[0].message.content
  }
  
  const callAnthropic = async (messages) => {
    const conversation = messages.map(m => 
      m.role === 'user' ? `Human: ${m.content}` : `Assistant: ${m.content}`
    ).join('\n\n')
    
    const response = await fetch('https://api.anthropic.com/v1/complete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': settings.anthropicKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: settings.anthropicModel,
        prompt: `${conversation}\n\nAssistant:`,
        max_tokens_to_sample: 2000,
        temperature: 0.7
      })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error?.message || 'Failed to get response from Anthropic')
    }
    
    const data = await response.json()
    return data.completion
  }
  
  const handleSend = async () => {
    if (!input.trim() || isLoading) return
    
    // Check if API key is set
    const apiKey = settings.provider === 'openai' ? settings.openaiKey : settings.anthropicKey
    if (!apiKey) {
      alert(`Please set your ${settings.provider === 'openai' ? 'OpenAI' : 'Anthropic'} API key in settings.`)
      setIsSettingsOpen(true)
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
    setIsLoading(true)
    
    try {
      let responseContent
      
      if (settings.provider === 'openai') {
        responseContent = await callOpenAI(updatedMessages)
      } else {
        responseContent = await callAnthropic(updatedMessages)
      }
      
      const assistantMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: responseContent,
        timestamp: Date.now()
      }
      
      const finalMessages = [...updatedMessages, assistantMessage]
      
      setConversations(prev => prev.map(c => 
        c.id === currentConversationId 
          ? { ...c, messages: finalMessages }
          : c
      ))
      
      // Generate title after first exchange
      if (updatedMessages.length === 1) {
        generateTitle(finalMessages)
      }
      
    } catch (error) {
      console.error('Error:', error)
      
      const errorMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: `Error: ${error.message}. Please check your API key and try again.`,
        timestamp: Date.now(),
        isError: true
      }
      
      setConversations(prev => prev.map(c => 
        c.id === currentConversationId 
          ? { ...c, messages: [...updatedMessages, errorMessage] }
          : c
      ))
    } finally {
      setIsLoading(false)
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
          <button className="icon-btn" onClick={() => setIsSettingsOpen(true)}>
            <Settings size={18} />
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
            <select 
              className="model-selector"
              value={settings.provider === 'openai' ? settings.openaiModel : settings.anthropicModel}
              onChange={(e) => {
                if (settings.provider === 'openai') {
                  setSettings({ ...settings, openaiModel: e.target.value })
                } else {
                  setSettings({ ...settings, anthropicModel: e.target.value })
                }
              }}
            >
              {settings.provider === 'openai' ? (
                <>
                  <option value="gpt-3.5-turbo">GPT-3.5</option>
                  <option value="gpt-4">GPT-4</option>
                  <option value="gpt-4-turbo">GPT-4 Turbo</option>
                </>
              ) : (
                <>
                  <option value="claude-instant-1">Claude Instant</option>
                  <option value="claude-2">Claude 2</option>
                  <option value="claude-3-sonnet-20240229">Claude 3 Sonnet</option>
                </>
              )}
            </select>
          </div>
        </header>
        
        {/* Chat */}
        <div className="chat-container">
          {!currentConversation || currentConversation.messages.length === 0 ? (
            <div className="welcome-screen">
              <div className="welcome-logo">M</div>
              <h1 className="welcome-title">How can I help you today?</h1>
              <p className="welcome-subtitle">
                I'm MHLABA, your personal AI assistant. I can help you with writing, 
                coding, analysis, and much more.
              </p>
              
              <div className="suggestion-chips">
                {SUGGESTIONS.map((suggestion, idx) => (
                  <button 
                    key={idx} 
                    className="suggestion-chip"
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
              
              {isLoading && (
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
                placeholder="Message MHLABA..."
                rows={1}
                style={{ minHeight: '24px' }}
              />
            </div>
            <button 
              className="send-btn"
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
            >
              <Send size={18} />
            </button>
          </div>
          
          <div className="input-footer">
            <div className="input-tools">
              <button className="tool-btn" onClick={() => setIsSettingsOpen(true)}>
                <Settings size={14} />
                Settings
              </button>
            </div>
            <span>
              {settings.provider === 'openai' ? 'OpenAI' : 'Anthropic'} · 
              Press Enter to send, Shift+Enter for new line
            </span>
          </div>
        </div>
      </main>
      
      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        settings={settings}
        onSave={setSettings}
      />
    </div>
  )
}

export default App
