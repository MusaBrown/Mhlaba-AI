"""
Screen Reader Module
Handles screen capture and OCR for reading screen content
"""
import os
from typing import Optional, List
from pathlib import Path


class ScreenReader:
    """Reads and analyzes screen content"""
    
    def __init__(self):
        self.screenshot_dir = Path.home() / "temp"
        self.screenshot_dir.mkdir(exist_ok=True)
        
    def capture_screen(self) -> Optional[str]:
        """Capture screenshot and return the file path"""
        try:
            # Try using PIL/Pillow
            from PIL import ImageGrab
            
            screenshot_path = self.screenshot_dir / "jarvis_screenshot.png"
            screenshot = ImageGrab.grab()
            screenshot.save(screenshot_path)
            return str(screenshot_path)
            
        except ImportError:
            # Fallback: try using mss
            try:
                import mss
                screenshot_path = self.screenshot_dir / "jarvis_screenshot.png"
                
                with mss.mss() as sct:
                    # Capture primary monitor
                    monitor = sct.monitors[1]  # 1 is the primary monitor
                    screenshot = sct.grab(monitor)
                    # Convert to PIL Image and save
                    from PIL import Image
                    img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                    img.save(screenshot_path)
                return str(screenshot_path)
                    
            except ImportError:
                return None
        except Exception as e:
            print(f"[SCREEN] Error capturing screen: {e}")
            return None
            
    def extract_text(self, image_path: str) -> str:
        """Extract text from screenshot using OCR"""
        try:
            import pytesseract
            from PIL import Image
            
            # Configure Tesseract path for Windows if needed
            if os.name == 'nt':
                # Common installation paths for Tesseract on Windows
                possible_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Users\%USERNAME%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                ]
                for tess_path in possible_paths:
                    tess_path = os.path.expandvars(tess_path)
                    if os.path.exists(tess_path):
                        pytesseract.pytesseract.tesseract_cmd = tess_path
                        break
            
            image = Image.open(image_path)
            
            # Configure OCR for better accuracy
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)
            
            return text.strip()
            
        except ImportError:
            return "[OCR not available - install pytesseract and Tesseract-OCR]"
        except Exception as e:
            return f"[Error extracting text: {e}]"
            
    def analyze_screen_content(self, text: str) -> dict:
        """Analyze screen content and provide summary"""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        # Detect content type
        content_type = self._detect_content_type(text)
        
        # Extract key elements
        key_elements = self._extract_key_elements(lines)
        
        return {
            'text': text,
            'content_type': content_type,
            'key_elements': key_elements,
            'line_count': len(lines),
            'word_count': len(text.split())
        }
        
    def _detect_content_type(self, text: str) -> str:
        """Detect what type of content is on screen"""
        text_lower = text.lower()
        
        # Code detection
        code_indicators = ['def ', 'import ', 'class ', 'function', 'var ', 'const ', 'print(', 'if __name__']
        if any(ind in text for ind in code_indicators):
            return "code"
            
        # Web page detection
        web_indicators = ['http', 'www.', '.com', 'login', 'password', 'sign in', 'search']
        if any(ind in text_lower for ind in web_indicators):
            return "webpage"
            
        # Document detection
        if len(text) > 500 and text.count('.') > 20:
            return "document"
            
        # Chat/Conversation detection
        chat_indicators = ['message', 'chat', 'sent', 'received', 'online']
        if any(ind in text_lower for ind in chat_indicators):
            return "chat"
            
        return "general"
        
    def _extract_key_elements(self, lines: List[str]) -> List[str]:
        """Extract key UI elements or important text"""
        elements = []
        
        # Look for headers/titles (short lines, often capitalized)
        for line in lines[:20]:  # Check first 20 lines
            if 3 < len(line) < 60 and line[0].isupper():
                elements.append(line)
                if len(elements) >= 5:
                    break
                    
        # Look for buttons/actions
        action_words = ['button', 'click', 'submit', 'ok', 'cancel', 'save', 'open', 'close']
        for line in lines:
            line_lower = line.lower()
            if any(word in line_lower for word in action_words):
                if line not in elements:
                    elements.append(line)
                    if len(elements) >= 10:
                        break
                        
        return elements
        
    def read_screen(self) -> dict:
        """Complete workflow: capture, extract text, analyze"""
        screenshot_path = self.capture_screen()
        
        if not screenshot_path:
            return {
                'success': False,
                'error': 'Failed to capture screenshot',
                'text': '',
                'analysis': {}
            }
            
        text = self.extract_text(screenshot_path)
        analysis = self.analyze_screen_content(text)
        
        return {
            'success': True,
            'screenshot_path': screenshot_path,
            'text': text,
            'analysis': analysis
        }
        
    def describe_for_ai(self, screen_data: dict) -> str:
        """Create a description suitable for AI analysis"""
        if not screen_data['success']:
            return f"Error reading screen: {screen_data.get('error', 'Unknown error')}"
            
        analysis = screen_data['analysis']
        text = screen_data['text']
        
        description = f"""Content Type: {analysis['content_type']}
Word Count: {analysis['word_count']}
Lines of Text: {analysis['line_count']}

Key Elements Detected:
"""
        for elem in analysis['key_elements'][:5]:
            description += f"- {elem}\n"
            
        description += f"\nExtracted Text:\n{text[:1500]}"
        if len(text) > 1500:
            description += "\n[Content truncated...]"
            
        return description
