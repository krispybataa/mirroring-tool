# Testing Guide for ARMR Work-Home Mirror Tool

This guide explains how to use the comprehensive test suite for the mirroring tool.

## Overview

The test suite is designed to test all aspects of the mirroring tool without requiring manual GUI interaction. It includes:

- **Unit tests** for core functionality
- **Integration tests** for complete workflows
- **GUI tests** with mocked Tkinter components
- **Performance tests** with large datasets
- **Coverage reporting** to identify untested code

## Quick Start

### 1. Install Testing Dependencies

```bash
pip install -r requirements.txt
```

**Note:** The testing dependencies are now included in the main requirements.txt file. If you only want to install the core dependencies without testing tools, you can install them individually:

```bash
# Core dependencies only
pip install pyinstaller

# With testing dependencies
pip install -r requirements.txt
```

### 2. Run Simple Tests (No External Dependencies)

```bash
python simple_test.py
```

### 3. Run Basic Tests (Requires pytest)

```bash
python test_runner.py --basic
```

### 4. Run All Tests

```bash
python test_runner.py --all
```

### 5. Generate Test Report

```bash
python test_runner.py --report
```

## Test Files Structure

```
mirroring-tool/
├── test_main.py          # Main test suite (requires pytest)
├── test_utils.py         # Testing utilities and helpers
├── test_runner.py        # Test runner with CLI
├── simple_test.py        # Simple tests (no external dependencies)
├── requirements.txt      # All dependencies including testing
└── README_TESTING.md     # This file
```

## Available Test Commands

### Simple Tests (No Dependencies)
Tests core functionality using only standard library:
```bash
python simple_test.py
```

### Basic Functionality Tests
Tests core file operations, configuration, and integration (requires pytest):
```bash
python test_runner.py --basic
```

### GUI Tests
Tests GUI components with mocked Tkinter:
```bash
python test_runner.py --gui
```

### Performance Tests
Tests with large datasets to measure performance:
```bash
python test_runner.py --performance
```

### Coverage Tests
Runs all tests with coverage reporting:
```bash
python test_runner.py --coverage
```

### All Tests
Runs the complete test suite:
```bash
python test_runner.py --all
```

### Specific Test
Run a specific test by name:
```bash
python test_runner.py --test test_count_files
```

### Generate Report
Creates a comprehensive test report:
```bash
python test_runner.py --report
```

## Test Categories

### 1. Simple Tests (`simple_test.py`)
**No external dependencies required** - uses only Python standard library:
- File counting functionality
- Directory synchronization
- Configuration loading/saving
- Error handling for missing directories
- File content verification

### 2. File Operations (`TestFileOperations`)
- File counting functionality
- Directory synchronization
- Error handling for missing directories
- File content verification

### 2. Configuration (`TestConfiguration`)
- Loading and saving configuration files
- Handling missing configuration files
- JSON serialization/deserialization

### 3. GUI Components
- **Progress Window** (`TestProgressWindow`): Tests progress display and updates
- **Directory Selection Dialog** (`TestDirectorySelectionDialog`): Tests directory selection logic
- **Confirmation Dialog** (`TestConfirmationDialog`): Tests confirmation workflows

### 4. Mode Functions (`TestModeFunctions`)
- Work mode workflow testing
- Home mode workflow testing
- Error handling and cancellation scenarios

### 5. Integration (`TestIntegration`)
- Complete sync workflows
- End-to-end functionality testing

## Testing Utilities

### `test_utils.py`

This file provides utilities for testing:

#### Directory Creation
```python
from test_utils import create_test_directory_structure

structure = {
    'file1.txt': 'content1',
    'subdir': {
        'file2.txt': 'content2'
    }
}
create_test_directory_structure('/path/to/test', structure)
```

#### Random Test Data
```python
from test_utils import create_random_test_files

# Create 100 random files in a directory
create_random_test_files('/path/to/test', num_files=100, max_depth=3)
```

#### Directory Comparison
```python
from test_utils import compare_directories

result = compare_directories('/source', '/destination')
print(f"Identical: {result['identical']}")
print(f"Missing files: {result['missing_files']}")
```

#### Mock Tkinter Components
```python
from test_utils import MockTkinter

# Create mock window
mock_window = MockTkinter.mock_toplevel()

# Create mock frame
mock_frame = MockTkinter.mock_frame()
```

## Running Tests with Coverage

### Install Coverage
```bash
pip install coverage
```

### Run with Coverage
```bash
python test_runner.py --coverage
```

This will:
1. Run all tests
2. Generate a coverage report in the terminal
3. Create an HTML coverage report in `htmlcov/` directory

### View HTML Coverage Report
Open `htmlcov/index.html` in your web browser to see detailed coverage information.

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    - name: Run tests
      run: python test_runner.py --all
    - name: Generate coverage report
      run: python test_runner.py --coverage
```

## Best Practices

### 1. Test Isolation
- Each test should be independent
- Use temporary directories for file operations
- Clean up after tests

### 2. Mocking
- Mock GUI components to avoid requiring display
- Mock file system operations when testing logic
- Use `unittest.mock` for complex mocking scenarios

### 3. Test Data
- Use realistic test data
- Test edge cases (empty files, large files, special characters)
- Test error conditions

### 4. Performance Testing
- Test with realistic file sizes and counts
- Measure and track performance metrics
- Set performance benchmarks

## Troubleshooting

### Common Issues

#### 1. Import Errors
If you get import errors, make sure you're running tests from the project root:
```bash
cd /path/to/mirroring-tool
python test_runner.py --basic
```

#### 2. Tkinter Issues
The tests use mocked Tkinter components, so you shouldn't need a display. If you get Tkinter errors, check that the mocking is working correctly.

#### 3. File Permission Issues
Tests create temporary files and directories. Make sure you have write permissions in the test directory.

#### 4. Coverage Not Working
Make sure coverage is installed:
```bash
pip install coverage
```

### Debugging Tests

#### Run Single Test with Verbose Output
```bash
python -m unittest test_main.TestFileOperations.test_count_files -v
```

#### Run Tests with Debug Output
```bash
python test_runner.py --all 2>&1 | tee test_output.log
```

## Adding New Tests

### 1. Add to Existing Test Class
```python
def test_new_functionality(self):
    """Test description"""
    # Test setup
    # Test execution
    # Assertions
    self.assertEqual(expected, actual)
```

### 2. Create New Test Class
```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        pass
    
    def tearDown(self):
        """Clean up after tests"""
        pass
    
    def test_feature(self):
        """Test the new feature"""
        pass
```

### 3. Update Test Runner
Add the new test class to the appropriate function in `test_runner.py`.

## Performance Benchmarks

The test suite includes performance testing that creates large datasets and measures sync times. Use this to:

- Track performance regressions
- Optimize sync algorithms
- Set performance expectations

Run performance tests:
```bash
python test_runner.py --performance
```

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain good test coverage
4. Update this documentation if needed

## Support

If you encounter issues with the test suite:

1. Check the troubleshooting section
2. Run tests with verbose output
3. Check that all dependencies are installed
4. Verify you're running from the correct directory 