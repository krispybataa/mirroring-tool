#!/usr/bin/env python3
"""
Simple test script for the mirroring tool
Uses only standard library modules - no external dependencies required
"""
import os
import sys
import tempfile
import shutil
import json
import unittest
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions we want to test
from main import count_files, load_config, save_config, sync_folders


class SimpleFileOperationsTest(unittest.TestCase):
    """Simple tests for file operations using only standard library"""
    
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
        print(f"✅ File counting test passed: {count} files found")
    
    def test_count_files_empty_dir(self):
        """Test counting files in empty directory"""
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)
        count = count_files(empty_dir)
        self.assertEqual(count, 0)
        print("✅ Empty directory test passed")
    
    def test_sync_folders_basic(self):
        """Test basic folder synchronization"""
        # Create destination directory
        os.makedirs(self.dest_dir)
        
        # Mock the progress window by creating a simple mock
        class MockProgressWindow:
            def __init__(self):
                pass
            def update(self, file_path, current, total):
                pass
            def close(self):
                pass
        
        # Replace ProgressWindow with our mock
        import main
        original_progress = main.ProgressWindow
        main.ProgressWindow = MockProgressWindow
        
        try:
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
            
            print("✅ Folder sync test passed")
            
        finally:
            # Restore original ProgressWindow
            main.ProgressWindow = original_progress
    
    def test_sync_folders_destination_does_not_exist(self):
        """Test sync when destination directory doesn't exist"""
        # Use a different destination directory that doesn't exist
        non_existent_dest = os.path.join(self.test_dir, "non_existent_dest")
        
        # Mock the progress window
        class MockProgressWindow:
            def __init__(self):
                pass
            def update(self, file_path, current, total):
                pass
            def close(self):
                pass
        
        import main
        original_progress = main.ProgressWindow
        main.ProgressWindow = MockProgressWindow
        
        try:
            # Run sync (destination will be created)
            sync_folders(self.source_dir, non_existent_dest)
            
            # Verify destination was created and files copied
            self.assertTrue(os.path.exists(non_existent_dest))
            for file_path in self.test_files:
                dest_file = os.path.join(non_existent_dest, file_path)
                self.assertTrue(os.path.exists(dest_file))
            
            print("✅ Destination creation test passed")
            
        finally:
            main.ProgressWindow = original_progress
    
    def test_sync_folders_source_not_found(self):
        """Test sync with non-existent source directory"""
        with self.assertRaises(FileNotFoundError):
            sync_folders("/non/existent/path", self.dest_dir)
        print("✅ Source not found error test passed")


class SimpleConfigTest(unittest.TestCase):
    """Simple tests for configuration using only standard library"""
    
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
        print("✅ Config save/load test passed")
    
    def test_load_config_file_not_exists(self):
        """Test loading config when file doesn't exist"""
        # Remove config file if it exists
        if os.path.exists('directory_config.json'):
            os.remove('directory_config.json')
        
        # Load config should return empty dict
        config = load_config()
        self.assertEqual(config, {})
        print("✅ Config file not exists test passed")


def run_simple_tests():
    """Run all simple tests"""
    print("=" * 60)
    print("Running Simple Tests (No External Dependencies)")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        SimpleFileOperationsTest,
        SimpleConfigTest
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All simple tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_simple_tests()
    sys.exit(0 if success else 1) 