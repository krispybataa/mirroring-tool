import unittest
import os
import shutil
import tempfile
import json
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import sys

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions we want to test
from main import (
    count_files, 
    load_config, 
    save_config, 
    sync_folders,
    work_mode,
    home_mode,
    DirectorySelectionDialog,
    ConfirmationDialog,
    ProgressWindow
)


class TestFileOperations(unittest.TestCase):
    """Test file and directory operations"""
    
    def setUp(self):
        """Set up temporary directories for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "destination")
        
        # Create source directory structure
        os.makedirs(self.source_dir)
        os.makedirs(os.path.join(self.source_dir, "subdir1"))
        os.makedirs(os.path.join(self.source_dir, "subdir2"))
        
        # Create test files
        self.test_files = [
            "file1.txt",
            "file2.txt", 
            "subdir1/file3.txt",
            "subdir2/file4.txt",
            "subdir2/file5.txt"
        ]
        
        for file_path in self.test_files:
            full_path = os.path.join(self.source_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(f"Content for {file_path}")
    
    def tearDown(self):
        """Clean up temporary directories"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_count_files(self):
        """Test counting files in directory"""
        count = count_files(self.source_dir)
        self.assertEqual(count, 5)  # 5 test files created
    
    def test_count_files_empty_dir(self):
        """Test counting files in empty directory"""
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)
        count = count_files(empty_dir)
        self.assertEqual(count, 0)
    
    def test_sync_folders_basic(self):
        """Test basic folder synchronization"""
        # Create destination directory
        os.makedirs(self.dest_dir)
        
        # Mock the progress window
        with patch('main.ProgressWindow') as mock_progress:
            mock_progress_instance = MagicMock()
            mock_progress.return_value = mock_progress_instance
            
            # Run sync
            sync_folders(self.source_dir, self.dest_dir)
            
            # Verify all files were copied
            for file_path in self.test_files:
                source_file = os.path.join(self.source_dir, file_path)
                dest_file = os.path.join(self.dest_dir, file_path)
                self.assertTrue(os.path.exists(dest_file))
                
                # Verify file contents are identical
                with open(source_file, 'rb') as f1, open(dest_file, 'rb') as f2:
                    self.assertEqual(f1.read(), f2.read())
    
    def test_sync_folders_destination_does_not_exist(self):
        """Test sync when destination directory doesn't exist"""
        # Mock the progress window
        with patch('main.ProgressWindow') as mock_progress:
            mock_progress_instance = MagicMock()
            mock_progress.return_value = mock_progress_instance
            
            # Run sync (destination will be created)
            sync_folders(self.source_dir, self.dest_dir)
            
            # Verify destination was created and files copied
            self.assertTrue(os.path.exists(self.dest_dir))
            for file_path in self.test_files:
                dest_file = os.path.join(self.dest_dir, file_path)
                self.assertTrue(os.path.exists(dest_file))
    
    def test_sync_folders_source_not_found(self):
        """Test sync with non-existent source directory"""
        with self.assertRaises(FileNotFoundError):
            sync_folders("/non/existent/path", self.dest_dir)
    
    def test_sync_folders_destination_not_found(self):
        """Test sync with non-existent destination directory"""
        # This should work as the destination will be created
        with patch('main.ProgressWindow') as mock_progress:
            mock_progress_instance = MagicMock()
            mock_progress.return_value = mock_progress_instance
            
            sync_folders(self.source_dir, "/non/existent/dest")
            # Should not raise an exception as destination is created


class TestConfiguration(unittest.TestCase):
    """Test configuration loading and saving"""
    
    def setUp(self):
        """Set up temporary config file"""
        self.test_config_file = tempfile.mktemp(suffix='.json')
        self.test_config = {
            'work_dir': '/path/to/work',
            'home_dir': '/path/to/home'
        }
    
    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        # Save config
        save_config(self.test_config)
        
        # Load config
        loaded_config = load_config()
        
        # Verify config was saved and loaded correctly
        self.assertEqual(loaded_config, self.test_config)
    
    def test_load_config_file_not_exists(self):
        """Test loading config when file doesn't exist"""
        # Remove config file if it exists
        if os.path.exists('directory_config.json'):
            os.remove('directory_config.json')
        
        # Load config should return empty dict
        config = load_config()
        self.assertEqual(config, {})
    
    def test_save_config_creates_file(self):
        """Test that save_config creates the file"""
        # Remove config file if it exists
        if os.path.exists('directory_config.json'):
            os.remove('directory_config.json')
        
        # Save config
        save_config(self.test_config)
        
        # Verify file was created
        self.assertTrue(os.path.exists('directory_config.json'))
        
        # Verify content
        with open('directory_config.json', 'r') as f:
            saved_config = json.load(f)
        self.assertEqual(saved_config, self.test_config)


class TestProgressWindow(unittest.TestCase):
    """Test progress window functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.root = MagicMock()
    
    @patch('tkinter.Toplevel')
    @patch('os.path.exists')
    def test_progress_window_creation(self, mock_exists, mock_toplevel):
        """Test progress window creation"""
        mock_exists.return_value = False  # No icon file
        mock_window = MagicMock()
        mock_toplevel.return_value = mock_window
        
        progress = ProgressWindow("Test Progress")
        
        # Verify window was created
        mock_toplevel.assert_called_once()
        self.assertEqual(progress.window, mock_window)
    
    @patch('tkinter.Toplevel')
    @patch('os.path.exists')
    def test_progress_window_update(self, mock_exists, mock_toplevel):
        """Test progress window update"""
        mock_exists.return_value = False
        mock_window = MagicMock()
        mock_toplevel.return_value = mock_window
        
        progress = ProgressWindow("Test Progress")
        
        # Mock the labels and progress bar
        progress.file_label = MagicMock()
        progress.progress = MagicMock()
        progress.stats_label = MagicMock()
        
        # Test update
        progress.update("/path/to/file.txt", 5, 10)
        
        # Verify updates were called
        progress.file_label.config.assert_called_with(text="Copying: file.txt")
        progress.progress.__setitem__.assert_called_with('value', 50.0)
        progress.stats_label.config.assert_called_with(
            text="Progress: 5 of 10 files (50.0%)"
        )


class TestDirectorySelectionDialog(unittest.TestCase):
    """Test directory selection dialog"""
    
    def setUp(self):
        """Set up test environment"""
        self.root = MagicMock()
        self.config = {'work_dir': '/test/work', 'home_dir': '/test/home'}
    
    @patch('tkinter.StringVar')
    @patch('tkinter.Toplevel')
    @patch('os.path.exists')
    def test_work_mode_dialog_creation(self, mock_exists, mock_toplevel, mock_stringvar):
        """Test work mode dialog creation"""
        mock_exists.return_value = False
        mock_dialog = MagicMock()
        mock_toplevel.return_value = mock_dialog
        
        dialog = DirectorySelectionDialog("Work Mode", self.config)
        
        # Verify dialog was created
        mock_toplevel.assert_called_once()
        self.assertEqual(dialog.mode, "Work Mode")
        self.assertEqual(dialog.config, self.config)
    
    @patch('tkinter.StringVar')
    @patch('tkinter.Toplevel')
    @patch('os.path.exists')
    def test_home_mode_dialog_creation(self, mock_exists, mock_toplevel, mock_stringvar):
        """Test home mode dialog creation"""
        mock_exists.return_value = False
        mock_dialog = MagicMock()
        mock_toplevel.return_value = mock_dialog
        
        dialog = DirectorySelectionDialog("Home Mode", self.config)
        
        # Verify dialog was created
        mock_toplevel.assert_called_once()
        self.assertEqual(dialog.mode, "Home Mode")
        self.assertEqual(dialog.config, self.config)


class TestConfirmationDialog(unittest.TestCase):
    """Test confirmation dialog"""
    
    def setUp(self):
        """Set up test environment"""
        self.root = MagicMock()
    
    @patch('tkinter.Toplevel')
    @patch('os.path.exists')
    def test_confirmation_dialog_creation(self, mock_exists, mock_toplevel):
        """Test confirmation dialog creation"""
        mock_exists.return_value = False
        mock_dialog = MagicMock()
        mock_toplevel.return_value = mock_dialog
        
        dialog = ConfirmationDialog("/source", "/destination", "work")
        
        # Verify dialog was created
        mock_toplevel.assert_called_once()
        self.assertEqual(dialog.mode, "work")
        self.assertFalse(dialog.result)


class TestModeFunctions(unittest.TestCase):
    """Test work_mode and home_mode functions"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = {'work_dir': '/test/work', 'home_dir': '/test/home'}
    
    @patch('main.DirectorySelectionDialog')
    @patch('main.ConfirmationDialog')
    @patch('main.sync_folders')
    @patch('main.messagebox')
    def test_work_mode_success(self, mock_messagebox, mock_sync, mock_confirm, mock_dir):
        """Test successful work mode execution"""
        # Mock directory selection
        mock_dir_instance = MagicMock()
        mock_dir_instance.result = {'source': '/source', 'destination': '/dest'}
        mock_dir.return_value = mock_dir_instance
        
        # Mock confirmation
        mock_confirm_instance = MagicMock()
        mock_confirm_instance.result = True
        mock_confirm.return_value = mock_confirm_instance
        
        # Mock sync (no exception)
        mock_sync.return_value = None
        
        # Test work mode
        result = work_mode(self.config)
        
        # Verify success
        self.assertTrue(result)
        mock_sync.assert_called_once_with('/source', '/dest')
        mock_messagebox.showinfo.assert_called_once()
    
    @patch('main.DirectorySelectionDialog')
    @patch('main.messagebox')
    def test_work_mode_cancelled_at_directory_selection(self, mock_messagebox, mock_dir):
        """Test work mode cancelled at directory selection"""
        # Mock directory selection cancelled
        mock_dir_instance = MagicMock()
        mock_dir_instance.result = None
        mock_dir.return_value = mock_dir_instance
        
        # Test work mode
        result = work_mode(self.config)
        
        # Verify cancelled
        self.assertFalse(result)
    
    @patch('main.DirectorySelectionDialog')
    @patch('main.ConfirmationDialog')
    @patch('main.messagebox')
    def test_work_mode_cancelled_at_confirmation(self, mock_messagebox, mock_confirm, mock_dir):
        """Test work mode cancelled at confirmation"""
        # Mock directory selection
        mock_dir_instance = MagicMock()
        mock_dir_instance.result = {'source': '/source', 'destination': '/dest'}
        mock_dir.return_value = mock_dir_instance
        
        # Mock confirmation cancelled
        mock_confirm_instance = MagicMock()
        mock_confirm_instance.result = False
        mock_confirm.return_value = mock_confirm_instance
        
        # Test work mode
        result = work_mode(self.config)
        
        # Verify cancelled
        self.assertFalse(result)
    
    @patch('main.DirectorySelectionDialog')
    @patch('main.ConfirmationDialog')
    @patch('main.sync_folders')
    @patch('main.messagebox')
    def test_work_mode_sync_error(self, mock_messagebox, mock_sync, mock_confirm, mock_dir):
        """Test work mode with sync error"""
        # Mock directory selection
        mock_dir_instance = MagicMock()
        mock_dir_instance.result = {'source': '/source', 'destination': '/dest'}
        mock_dir.return_value = mock_dir_instance
        
        # Mock confirmation
        mock_confirm_instance = MagicMock()
        mock_confirm_instance.result = True
        mock_confirm.return_value = mock_confirm_instance
        
        # Mock sync error
        mock_sync.side_effect = Exception("Sync failed")
        
        # Test work mode
        result = work_mode(self.config)
        
        # Verify error handling
        self.assertFalse(result)
        mock_messagebox.showerror.assert_called_once()
    
    @patch('main.DirectorySelectionDialog')
    @patch('main.ConfirmationDialog')
    @patch('main.sync_folders')
    @patch('main.messagebox')
    def test_home_mode_success(self, mock_messagebox, mock_sync, mock_confirm, mock_dir):
        """Test successful home mode execution"""
        # Mock directory selection
        mock_dir_instance = MagicMock()
        mock_dir_instance.result = {'source': '/source', 'destination': '/dest'}
        mock_dir.return_value = mock_dir_instance
        
        # Mock confirmation
        mock_confirm_instance = MagicMock()
        mock_confirm_instance.result = True
        mock_confirm.return_value = mock_confirm_instance
        
        # Mock sync (no exception)
        mock_sync.return_value = None
        
        # Test home mode
        result = home_mode(self.config)
        
        # Verify success
        self.assertTrue(result)
        mock_sync.assert_called_once_with('/source', '/dest')
        mock_messagebox.showinfo.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "destination")
        
        # Create test files
        os.makedirs(self.source_dir)
        with open(os.path.join(self.source_dir, "test.txt"), 'w') as f:
            f.write("Test content")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @patch('main.ProgressWindow')
    def test_complete_sync_workflow(self, mock_progress):
        """Test complete sync workflow"""
        mock_progress_instance = MagicMock()
        mock_progress.return_value = mock_progress_instance
        
        # Test the complete sync process
        sync_folders(self.source_dir, self.dest_dir)
        
        # Verify files were copied
        self.assertTrue(os.path.exists(self.dest_dir))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "test.txt")))
        
        # Verify file content
        with open(os.path.join(self.dest_dir, "test.txt"), 'r') as f:
            content = f.read()
        self.assertEqual(content, "Test content")


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestFileOperations,
        TestConfiguration,
        TestProgressWindow,
        TestDirectorySelectionDialog,
        TestConfirmationDialog,
        TestModeFunctions,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful()) 