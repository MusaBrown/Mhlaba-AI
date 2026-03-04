"""
Document Handler Module
Handles reading and processing various document types
"""
import os
from pathlib import Path
from typing import List, Optional
import subprocess


class DocumentHandler:
    """Handles document operations"""
    
    def __init__(self):
        self.supported_extensions = {
            '.txt', '.md', '.py', '.js', '.html', '.css', '.json', 
            '.xml', '.csv', '.log', '.ini', '.cfg', '.yaml', '.yml',
            '.docx', '.pdf', '.rtf'
        }
        
    def read_document(self, filepath: str) -> Optional[str]:
        """Read a document and return its content"""
        # Try to resolve the path
        path = self._resolve_path(filepath)
        
        if not path or not path.exists():
            return None
            
        extension = path.suffix.lower()
        
        try:
            # Text-based files
            if extension in ['.txt', '.md', '.py', '.js', '.html', '.css', 
                            '.json', '.xml', '.csv', '.log', '.ini', 
                            '.cfg', '.yaml', '.yml']:
                return self._read_text_file(path)
                
            # Word documents
            elif extension == '.docx':
                return self._read_docx(path)
                
            # PDF files
            elif extension == '.pdf':
                return self._read_pdf(path)
                
            # RTF files
            elif extension == '.rtf':
                return self._read_rtf(path)
                
            else:
                # Try to read as text anyway
                return self._read_text_file(path)
                
        except Exception as e:
            print(f"Error reading document: {e}")
            return None
            
    def _resolve_path(self, filepath: str) -> Optional[Path]:
        """Resolve a file path from various inputs"""
        # Direct path
        path = Path(filepath)
        if path.exists():
            return path.resolve()
            
        # In current directory
        path = Path.cwd() / filepath
        if path.exists():
            return path.resolve()
            
        # In Documents folder
        docs_path = Path.home() / "Documents" / filepath
        if docs_path.exists():
            return docs_path.resolve()
            
        # In Downloads folder
        downloads_path = Path.home() / "Downloads" / filepath
        if downloads_path.exists():
            return downloads_path.resolve()
            
        # Desktop
        desktop_path = Path.home() / "Desktop" / filepath
        if desktop_path.exists():
            return desktop_path.resolve()
            
        return None
        
    def _read_text_file(self, path: Path) -> str:
        """Read a text file"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
                
        # If all encodings fail, read as binary and decode with errors ignored
        with open(path, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
            
    def _read_docx(self, path: Path) -> str:
        """Read a Word document"""
        try:
            from docx import Document
            doc = Document(path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        except ImportError:
            return "[Word document - install python-docx to read content]"
        except Exception as e:
            return f"[Error reading Word document: {e}]"
            
    def _read_pdf(self, path: Path) -> str:
        """Read a PDF file"""
        try:
            import PyPDF2
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            return "[PDF document - install PyPDF2 to read content]"
        except Exception as e:
            return f"[Error reading PDF: {e}]"
            
    def _read_rtf(self, path: Path) -> str:
        """Read an RTF file"""
        try:
            from striprtf.striprtf import rtf_to_text
            with open(path, 'r') as f:
                rtf_content = f.read()
            return rtf_to_text(rtf_content)
        except ImportError:
            return "[RTF document - install striprtf to read content]"
        except Exception as e:
            return f"[Error reading RTF: {e}]"
            
    def list_files(self, directory: str = None, pattern: str = "*") -> List[str]:
        """List files in a directory"""
        if directory is None:
            directory = Path.cwd()
        else:
            directory = self._resolve_path(directory) or Path.cwd()
            
        try:
            files = list(directory.glob(pattern))
            return [f.name for f in files if f.is_file()]
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
            
    def get_file_info(self, filepath: str) -> dict:
        """Get information about a file"""
        path = self._resolve_path(filepath)
        
        if not path or not path.exists():
            return None
            
        stat = path.stat()
        return {
            'name': path.name,
            'path': str(path),
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'extension': path.suffix
        }
        
    def open_document(self, filepath: str) -> bool:
        """Open a document with the default application"""
        path = self._resolve_path(filepath)
        
        if not path or not path.exists():
            return False
            
        try:
            os.startfile(str(path))
            return True
        except Exception as e:
            print(f"Error opening document: {e}")
            return False
