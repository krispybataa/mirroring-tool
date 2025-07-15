#!/usr/bin/env python3
"""
Test runner for the mirroring tool
Provides easy ways to run tests and generate reports
"""
import os
import sys
import unittest
import argparse
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_basic_tests():
    """Run basic functionality tests"""
    print("Running basic functionality tests...")
    
    # Import test modules
    from test_main import (
        TestFileOperations,
        TestConfiguration,
        TestIntegration
    )
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestFileOperations,
        TestConfiguration,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


def run_gui_tests():
    """Run GUI-related tests (with mocked Tkinter)"""
    print("Running GUI tests (with mocked components)...")
    
    # Import test modules
    from test_main import (
        TestProgressWindow,
        TestDirectorySelectionDialog,
        TestConfirmationDialog,
        TestModeFunctions
    )
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestProgressWindow,
        TestDirectorySelectionDialog,
        TestConfirmationDialog,
        TestModeFunctions
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


def run_all_tests():
    """Run all tests"""
    print("Running all tests...")
    
    # Import all test modules
    from test_main import (
        TestFileOperations,
        TestConfiguration,
        TestProgressWindow,
        TestDirectorySelectionDialog,
        TestConfirmationDialog,
        TestModeFunctions,
        TestIntegration
    )
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
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
    
    return result.wasSuccessful()


def run_performance_tests():
    """Run performance tests with large datasets"""
    print("Running performance tests...")
    
    try:
        import tempfile
        import shutil
        from test_utils import create_random_test_files, compare_directories
        
        # Create temporary directories
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = os.path.join(temp_dir, "source")
            dest_dir = os.path.join(temp_dir, "destination")
            
            os.makedirs(source_dir)
            os.makedirs(dest_dir)
            
            # Create large test dataset
            print("Creating test dataset...")
            create_random_test_files(source_dir, num_files=500, max_depth=5)
            
            # Test sync performance
            print("Testing sync performance...")
            start_time = time.time()
            
            from main import sync_folders
            from unittest.mock import patch
            
            with patch('main.ProgressWindow') as mock_progress:
                mock_progress_instance = unittest.mock.MagicMock()
                mock_progress.return_value = mock_progress_instance
                
                sync_folders(source_dir, dest_dir)
            
            end_time = time.time()
            sync_time = end_time - start_time
            
            # Verify sync
            print("Verifying sync results...")
            comparison = compare_directories(source_dir, dest_dir)
            
            print(f"Sync completed in {sync_time:.2f} seconds")
            print(f"Files synced: {len([f for f in os.listdir(dest_dir) if os.path.isfile(os.path.join(dest_dir, f))])}")
            print(f"Sync successful: {comparison['identical']}")
            
            if not comparison['identical']:
                print(f"Missing files: {len(comparison['missing_files'])}")
                print(f"Extra files: {len(comparison['extra_files'])}")
                print(f"Different files: {len(comparison['different_files'])}")
            
            return comparison['identical']
    except ImportError as e:
        print(f"Performance tests require additional dependencies: {e}")
        print("Install with: pip install pytest-benchmark")
        return False


def run_coverage_tests():
    """Run tests with coverage reporting"""
    print("Running tests with coverage...")
    
    try:
        import coverage
        
        # Start coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Run all tests
        success = run_all_tests()
        
        # Stop coverage
        cov.stop()
        cov.save()
        
        # Generate reports
        print("\nGenerating coverage report...")
        cov.report()
        
        # Generate HTML report
        html_dir = "htmlcov"
        cov.html_report(directory=html_dir)
        print(f"HTML coverage report generated in: {html_dir}")
        
        return success
        
    except ImportError:
        print("Coverage not installed. Install with: pip install coverage")
        return run_all_tests()


def run_specific_test(test_name):
    """Run a specific test by name"""
    print(f"Running specific test: {test_name}")
    
    # Import all test modules
    from test_main import (
        TestFileOperations,
        TestConfiguration,
        TestProgressWindow,
        TestDirectorySelectionDialog,
        TestConfirmationDialog,
        TestModeFunctions,
        TestIntegration
    )
    
    # Create test suite with specific test
    test_suite = unittest.TestSuite()
    
    # Find the test
    test_loader = unittest.TestLoader()
    
    # Try to find the test in each test class
    test_classes = [
        TestFileOperations,
        TestConfiguration,
        TestProgressWindow,
        TestDirectorySelectionDialog,
        TestConfirmationDialog,
        TestModeFunctions,
        TestIntegration
    ]
    
    test_found = False
    for test_class in test_classes:
        try:
            test = test_loader.loadTestsFromName(test_name, test_class)
            if test.countTestCases() > 0:
                test_suite.addTest(test)
                test_found = True
                break
        except:
            continue
    
    if not test_found:
        print(f"Test '{test_name}' not found!")
        return False
    
    # Run the test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


def generate_test_report():
    """Generate a comprehensive test report"""
    print("Generating test report...")
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'tests': {}
    }
    
    # Run different test categories
    test_categories = [
        ('Basic Functionality', run_basic_tests),
        ('GUI Components', run_gui_tests),
        ('Performance', run_performance_tests)
    ]
    
    for category, test_func in test_categories:
        print(f"\n{'='*50}")
        print(f"Running {category} tests...")
        print('='*50)
        
        try:
            success = test_func()
            report['tests'][category] = {
                'status': 'PASSED' if success else 'FAILED',
                'success': success
            }
        except Exception as e:
            report['tests'][category] = {
                'status': 'ERROR',
                'success': False,
                'error': str(e)
            }
    
    # Print summary
    print("\n" + "="*60)
    print("TEST REPORT SUMMARY")
    print("="*60)
    print(f"Timestamp: {report['timestamp']}")
    print()
    
    total_tests = len(report['tests'])
    passed_tests = sum(1 for test in report['tests'].values() if test['success'])
    
    for category, result in report['tests'].items():
        status_icon = "✅" if result['success'] else "❌"
        print(f"{status_icon} {category}: {result['status']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
    
    print()
    print(f"Overall: {passed_tests}/{total_tests} test categories passed")
    
    # Save report to file
    import json
    report_file = f"test_report_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Detailed report saved to: {report_file}")
    
    return passed_tests == total_tests


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Test runner for mirroring tool')
    parser.add_argument('--basic', action='store_true', 
                       help='Run basic functionality tests')
    parser.add_argument('--gui', action='store_true', 
                       help='Run GUI tests (with mocked components)')
    parser.add_argument('--performance', action='store_true', 
                       help='Run performance tests')
    parser.add_argument('--coverage', action='store_true', 
                       help='Run tests with coverage reporting')
    parser.add_argument('--all', action='store_true', 
                       help='Run all tests')
    parser.add_argument('--report', action='store_true', 
                       help='Generate comprehensive test report')
    parser.add_argument('--test', type=str, 
                       help='Run a specific test by name')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    success = True
    
    try:
        if args.basic:
            success = run_basic_tests()
        elif args.gui:
            success = run_gui_tests()
        elif args.performance:
            success = run_performance_tests()
        elif args.coverage:
            success = run_coverage_tests()
        elif args.all:
            success = run_all_tests()
        elif args.report:
            success = generate_test_report()
        elif args.test:
            success = run_specific_test(args.test)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 