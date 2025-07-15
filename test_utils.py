"""
Utility functions for testing the mirroring tool
"""
import os
import tempfile
import shutil
import random
import string
from pathlib import Path
from unittest.mock import MagicMock, patch


def create_test_directory_structure(base_path, structure):
    """
    Create a test directory structure based on a dictionary specification.
    
    Args:
        base_path (str): Base directory path
        structure (dict): Dictionary defining the structure
            - Keys are file/directory names
            - Values are either strings (file content) or dicts (subdirectories)
    
    Example:
        structure = {
            'file1.txt': 'content1',
            'subdir1': {
                'file2.txt': 'content2',
                'subsubdir': {
                    'file3.txt': 'content3'
                }
            }
        }
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # It's a directory
            os.makedirs(path, exist_ok=True)
            create_test_directory_structure(path, content)
        else:
            # It's a file
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)


def create_random_test_files(base_path, num_files=10, max_depth=3):
    """
    Create random test files in a directory structure.
    
    Args:
        base_path (str): Base directory path
        num_files (int): Number of files to create
        max_depth (int): Maximum directory depth
    """
    file_extensions = ['.txt', '.doc', '.pdf', '.jpg', '.png', '.mp3', '.mp4']
    
    for i in range(num_files):
        # Random depth
        depth = random.randint(0, max_depth)
        
        # Create random path
        path_parts = []
        for _ in range(depth):
            path_parts.append(''.join(random.choices(string.ascii_lowercase, k=8)))
        
        # Add filename
        filename = f'file_{i}_{random.randint(1000, 9999)}'
        filename += random.choice(file_extensions)
        path_parts.append(filename)
        
        # Create full path
        file_path = os.path.join(base_path, *path_parts)
        
        # Create directory if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Create file with random content
        content = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 100)))
        with open(file_path, 'w') as f:
            f.write(content)


def compare_directories(dir1, dir2):
    """
    Compare two directories recursively.
    
    Args:
        dir1 (str): First directory path
        dir2 (str): Second directory path
    
    Returns:
        dict: Comparison results with 'identical', 'missing_files', 'extra_files', 'different_files'
    """
    result = {
        'identical': True,
        'missing_files': [],
        'extra_files': [],
        'different_files': []
    }
    
    def get_file_list(directory):
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, directory)
                files.append(rel_path)
        return set(files)
    
    def get_file_hash(filepath):
        """Get file hash for comparison"""
        import hashlib
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    # Get file lists
    files1 = get_file_list(dir1)
    files2 = get_file_list(dir2)
    
    # Find missing and extra files
    result['missing_files'] = list(files1 - files2)
    result['extra_files'] = list(files2 - files1)
    
    # Check common files
    common_files = files1 & files2
    for file_path in common_files:
        file1_path = os.path.join(dir1, file_path)
        file2_path = os.path.join(dir2, file_path)
        
        if get_file_hash(file1_path) != get_file_hash(file2_path):
            result['different_files'].append(file_path)
    
    # Update identical flag
    if result['missing_files'] or result['extra_files'] or result['different_files']:
        result['identical'] = False
    
    return result


class MockTkinter:
    """Mock Tkinter components for testing"""
    
    @staticmethod
    def mock_toplevel():
        """Create a mock Toplevel window"""
        mock_window = MagicMock()
        mock_window.title = MagicMock()
        mock_window.geometry = MagicMock()
        mock_window.iconbitmap = MagicMock()
        mock_window.transient = MagicMock()
        mock_window.grab_set = MagicMock()
        mock_window.update_idletasks = MagicMock()
        mock_window.winfo_width = MagicMock(return_value=500)
        mock_window.winfo_height = MagicMock(return_value=300)
        mock_window.winfo_screenwidth = MagicMock(return_value=1920)
        mock_window.winfo_screenheight = MagicMock(return_value=1080)
        mock_window.destroy = MagicMock()
        mock_window.deiconify = MagicMock()
        mock_window.withdraw = MagicMock()
        mock_window.quit = MagicMock()
        mock_window.mainloop = MagicMock()
        return mock_window
    
    @staticmethod
    def mock_frame():
        """Create a mock Frame"""
        mock_frame = MagicMock()
        mock_frame.pack = MagicMock()
        return mock_frame
    
    @staticmethod
    def mock_label():
        """Create a mock Label"""
        mock_label = MagicMock()
        mock_label.pack = MagicMock()
        mock_label.config = MagicMock()
        return mock_label
    
    @staticmethod
    def mock_progressbar():
        """Create a mock Progressbar"""
        mock_progress = MagicMock()
        mock_progress.pack = MagicMock()
        mock_progress.__setitem__ = MagicMock()
        return mock_progress
    
    @staticmethod
    def mock_button():
        """Create a mock Button"""
        mock_button = MagicMock()
        mock_button.pack = MagicMock()
        return mock_button
    
    @staticmethod
    def mock_entry():
        """Create a mock Entry"""
        mock_entry = MagicMock()
        mock_entry.pack = MagicMock()
        return mock_entry


class TestDataGenerator:
    """Generate test data for different scenarios"""
    
    @staticmethod
    def create_simple_structure():
        """Create a simple directory structure for basic tests"""
        return {
            'file1.txt': 'Simple test file 1',
            'file2.txt': 'Simple test file 2',
            'subdir1': {
                'file3.txt': 'File in subdirectory 1',
                'file4.txt': 'Another file in subdirectory 1'
            },
            'subdir2': {
                'file5.txt': 'File in subdirectory 2',
                'subsubdir': {
                    'file6.txt': 'File in nested subdirectory'
                }
            }
        }
    
    @staticmethod
    def create_large_structure(num_files=100):
        """Create a large directory structure for performance tests"""
        structure = {}
        for i in range(num_files):
            if i < num_files // 3:
                # Files in root
                structure[f'file_{i}.txt'] = f'Content for file {i}'
            elif i < 2 * num_files // 3:
                # Files in subdir1
                if 'subdir1' not in structure:
                    structure['subdir1'] = {}
                structure['subdir1'][f'file_{i}.txt'] = f'Content for file {i}'
            else:
                # Files in subdir2
                if 'subdir2' not in structure:
                    structure['subdir2'] = {}
                structure['subdir2'][f'file_{i}.txt'] = f'Content for file {i}'
        return structure
    
    @staticmethod
    def create_mixed_content_structure():
        """Create structure with different file types and sizes"""
        return {
            'small.txt': 'Small file',
            'medium.txt': 'Medium file with more content ' * 10,
            'large.txt': 'Large file with lots of content ' * 100,
            'empty.txt': '',
            'binary.bin': b'\x00\x01\x02\x03\x04\x05'.decode('latin-1'),
            'special_chars.txt': 'File with special chars: éñüß©®™',
            'subdir': {
                'nested.txt': 'Nested file content',
                'another.txt': 'Another nested file'
            }
        }


def patch_tkinter_components():
    """Patch Tkinter components for testing"""
    patches = []
    
    # Patch Toplevel
    mock_toplevel = MockTkinter.mock_toplevel()
    patches.append(patch('tkinter.Toplevel', return_value=mock_toplevel))
    
    # Patch Frame
    mock_frame = MockTkinter.mock_frame()
    patches.append(patch('tkinter.ttk.Frame', return_value=mock_frame))
    
    # Patch Label
    mock_label = MockTkinter.mock_label()
    patches.append(patch('tkinter.ttk.Label', return_value=mock_label))
    
    # Patch Progressbar
    mock_progress = MockTkinter.mock_progressbar()
    patches.append(patch('tkinter.ttk.Progressbar', return_value=mock_progress))
    
    # Patch Button
    mock_button = MockTkinter.mock_button()
    patches.append(patch('tkinter.Button', return_value=mock_button))
    
    # Patch Entry
    mock_entry = MockTkinter.mock_entry()
    patches.append(patch('tkinter.ttk.Entry', return_value=mock_entry))
    
    return patches


class TemporaryDirectory:
    """Context manager for temporary directories"""
    
    def __init__(self, suffix='', prefix='tmp', dir=None):
        self.suffix = suffix
        self.prefix = prefix
        self.dir = dir
        self.path = None
    
    def __enter__(self):
        self.path = tempfile.mkdtemp(suffix=self.suffix, prefix=self.prefix, dir=self.dir)
        return self.path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path and os.path.exists(self.path):
            shutil.rmtree(self.path, ignore_errors=True)


def run_tests_with_coverage():
    """Run tests with coverage reporting"""
    try:
        import coverage
        
        # Start coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Import and run tests
        import test_main
        unittest.main(module=test_main, exit=False)
        
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        
        # Generate HTML report
        cov.html_report(directory='htmlcov')
        
        # Print summary
        cov.report()
        
        return True
    except ImportError:
        print("Coverage not installed. Install with: pip install coverage")
        return False


if __name__ == '__main__':
    # Example usage
    with TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory: {temp_dir}")
        
        # Create test structure
        structure = TestDataGenerator.create_simple_structure()
        create_test_directory_structure(temp_dir, structure)
        
        print("Test structure created successfully!")
        print("Files created:")
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}") 