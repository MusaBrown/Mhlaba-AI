"""
System Executor Module
Handles system-level commands and operations
"""
import os
import sys
import subprocess
import webbrowser
import psutil
from pathlib import Path
from typing import Optional
import platform


class SystemExecutor:
    """Executes system commands"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.common_apps = {
            'chrome': ['chrome', 'google-chrome', 'chromium'],
            'firefox': ['firefox'],
            'edge': ['msedge', 'microsoft-edge'],
            'notepad': ['notepad'],
            'word': ['winword'],
            'excel': ['excel'],
            'powerpoint': ['powerpnt'],
            'calculator': ['calc'],
            'explorer': ['explorer'],
            'cmd': ['cmd'],
            'powershell': ['powershell'],
            'terminal': ['wt', 'windows-terminal'],
            'vscode': ['code'],
            'spotify': ['spotify'],
            'steam': ['steam']
        }
        
    def open_application(self, app_name: str) -> str:
        """Open an application by name"""
        app_name = app_name.lower().strip()
        
        # Check if it's a known app
        for known_name, commands in self.common_apps.items():
            if known_name in app_name or app_name in known_name:
                for cmd in commands:
                    try:
                        subprocess.Popen(cmd, shell=True)
                        return f"Opening {known_name.title()}"
                    except:
                        continue
                        
        # Try to open as-is
        try:
            subprocess.Popen(app_name, shell=True)
            return f"Opening {app_name}"
        except Exception as e:
            return f"Unable to open {app_name}. Error: {e}"
            
    def open_file_explorer(self, path: str = None) -> str:
        """Open Windows File Explorer"""
        try:
            if path and Path(path).exists():
                subprocess.Popen(f'explorer "{path}"', shell=True)
            else:
                subprocess.Popen('explorer', shell=True)
            return "Opening File Explorer"
        except Exception as e:
            return f"Error opening File Explorer: {e}"
            
    def web_search(self, query: str) -> str:
        """Perform a web search"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"Searching for: {query}"
        
    def open_website(self, url: str) -> str:
        """Open a website"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open(url)
        return f"Opening {url}"
        
    def get_system_info(self) -> str:
        """Get system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = (
                f"System Information:\n"
                f"Platform: {platform.platform()}\n"
                f"Processor: {platform.processor()}\n"
                f"CPU Usage: {cpu_percent}%\n"
                f"Memory: {memory.percent}% used ({memory.used // (1024**3)} GB / {memory.total // (1024**3)} GB)\n"
                f"Disk: {disk.percent}% used ({disk.used // (1024**3)} GB / {disk.total // (1024**3)} GB)\n"
                f"Boot Time: {psutil.boot_time()}"
            )
            
            return info
        except Exception as e:
            return f"Error getting system info: {e}"
            
    def list_processes(self, limit: int = 10) -> str:
        """List running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except:
                    pass
                    
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            result = "Top processes by CPU usage:\n"
            for p in processes[:limit]:
                result += f"  {p['pid']}: {p['name']} ({p.get('cpu_percent', 0)}%)\n"
                
            return result
        except Exception as e:
            return f"Error listing processes: {e}"
            
    def kill_process(self, process_name: str) -> str:
        """Kill a process by name"""
        try:
            killed = []
            for proc in psutil.process_iter(['pid', 'name']):
                if process_name.lower() in proc.info['name'].lower():
                    try:
                        p = psutil.Process(proc.info['pid'])
                        p.terminate()
                        killed.append(proc.info['name'])
                    except:
                        pass
                        
            if killed:
                return f"Terminated processes: {', '.join(killed)}"
            else:
                return f"No process found matching '{process_name}'"
        except Exception as e:
            return f"Error killing process: {e}"
            
    def take_screenshot(self, filename: str = "screenshot.png") -> str:
        """Take a screenshot"""
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            screenshot_path = Path.home() / "Pictures" / filename
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            screenshot.save(screenshot_path)
            return f"Screenshot saved to {screenshot_path}"
        except ImportError:
            return "Screenshot requires PIL (Pillow). Install with: pip install Pillow"
        except Exception as e:
            return f"Error taking screenshot: {e}"
            
    def create_folder(self, folder_name: str, location: str = None) -> str:
        """Create a new folder"""
        try:
            if location:
                path = Path(location) / folder_name
            else:
                path = Path.cwd() / folder_name
                
            path.mkdir(parents=True, exist_ok=True)
            return f"Created folder: {path}"
        except Exception as e:
            return f"Error creating folder: {e}"
            
    def get_current_directory(self) -> str:
        """Get current working directory"""
        return str(Path.cwd())
        
    def change_directory(self, path: str) -> str:
        """Change working directory"""
        try:
            new_path = Path(path)
            if new_path.exists() and new_path.is_dir():
                os.chdir(new_path)
                return f"Changed directory to: {new_path}"
            else:
                return f"Directory not found: {path}"
        except Exception as e:
            return f"Error changing directory: {e}"
