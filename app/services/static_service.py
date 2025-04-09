from typing import List, Dict, Any
from pathlib import Path
import shutil
import os
import mimetypes
from datetime import datetime

class StaticService:
    """Service for handling static files."""
    
    def __init__(self, config_service):
        """Initialize the static service.
        
        Args:
            config_service: Configuration service instance
        """
        self.config = config_service
        self.static_dir = Path(self.config.static_dir)
        self.cache_timeout = self.config.static_cache_timeout
        
    def copy_static_files(self, output_dir: str) -> None:
        """Copy static files to output directory.
        
        Args:
            output_dir: Output directory path
        """
        output_path = Path(output_dir)
        static_output = output_path / 'static'
        
        # Create output directory if it doesn't exist
        static_output.mkdir(parents=True, exist_ok=True)
        
        # Copy all files from static directory
        for item in self.static_dir.glob('**/*'):
            if item.is_file():
                # Get relative path from static directory
                rel_path = item.relative_to(self.static_dir)
                target_path = static_output / rel_path
                
                # Create parent directories if needed
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(item, target_path)
                
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about a static file.
        
        Args:
            file_path: Path to static file
            
        Returns:
            Dictionary containing file information
        """
        path = self.static_dir / file_path
        if not path.exists():
            return None
            
        stat = path.stat()
        mime_type, _ = mimetypes.guess_type(str(path))
        
        return {
            'path': str(path),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'mime_type': mime_type or 'application/octet-stream'
        }
        
    def list_files(self, directory: str = '') -> List[Dict[str, Any]]:
        """List files in a static directory.
        
        Args:
            directory: Directory path relative to static directory
            
        Returns:
            List of file information dictionaries
        """
        dir_path = self.static_dir / directory
        if not dir_path.exists():
            return []
            
        files = []
        for item in dir_path.glob('**/*'):
            if item.is_file():
                rel_path = item.relative_to(self.static_dir)
                files.append(self.get_file_info(str(rel_path)))
                
        return files
        
    def get_file_url(self, file_path: str) -> str:
        """Get URL for a static file.
        
        Args:
            file_path: Path to static file
            
        Returns:
            URL string
        """
        return f'/static/{file_path}'
        
    def get_cache_headers(self, file_path: str) -> Dict[str, str]:
        """Get cache headers for a static file.
        
        Args:
            file_path: Path to static file
            
        Returns:
            Dictionary of cache headers
        """
        info = self.get_file_info(file_path)
        if not info:
            return {}
            
        return {
            'Cache-Control': f'public, max-age={self.cache_timeout}',
            'Last-Modified': info['modified'].strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Content-Type': info['mime_type']
        }
        
    def ensure_directory(self, directory: str) -> None:
        """Ensure a directory exists in the static directory.
        
        Args:
            directory: Directory path relative to static directory
        """
        dir_path = self.static_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
    def delete_file(self, file_path: str) -> bool:
        """Delete a static file.
        
        Args:
            file_path: Path to static file
            
        Returns:
            True if file was deleted, False otherwise
        """
        path = self.static_dir / file_path
        if not path.exists():
            return False
            
        try:
            path.unlink()
            return True
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False
            
    def move_file(self, source: str, destination: str) -> bool:
        """Move a static file.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if file was moved, False otherwise
        """
        source_path = self.static_dir / source
        dest_path = self.static_dir / destination
        
        if not source_path.exists():
            return False
            
        try:
            # Create parent directories if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.move(str(source_path), str(dest_path))
            return True
        except Exception as e:
            print(f"Error moving file {source} to {destination}: {e}")
            return False 