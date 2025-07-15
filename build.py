#!/usr/bin/env python3
"""
Build script for ARMR Mirror Tool
Creates a distribution-ready executable with proper resource handling
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    return True

def check_resources():
    """Check if required resources exist"""
    resources_dir = Path("resoources")
    icon_file = resources_dir / "app_icon_final.ico"
    
    if not resources_dir.exists():
        print("❌ Resources directory not found: resoources/")
        return False
    
    if not icon_file.exists():
        print("❌ Icon file not found: resoources/app_icon_final.ico")
        return False
    
    print("✅ Resources found")
    return True

def clean_build_dirs():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # Clean .spec files except main.spec
    for file in Path('.').glob('*.spec'):
        if file.name != 'main.spec':
            file.unlink()
            print(f"Removed {file.name}")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\n🔨 Building executable...")
    
    try:
        # Run PyInstaller
        cmd = [
            'pyinstaller',
            'main.spec',
            '--clean',
            '--noconfirm'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            return True
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_distribution():
    """Create a clean distribution folder"""
    print("\n📦 Creating distribution...")
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ Dist directory not found. Build failed.")
        return False
    
    # Find the executable
    exe_files = list(dist_dir.glob("*.exe"))
    if not exe_files:
        print("❌ No executable found in dist/")
        return False
    
    exe_file = exe_files[0]
    print(f"✅ Found executable: {exe_file.name}")
    
    # Create distribution folder
    dist_name = "ARMR_Briefcase"
    dist_path = Path(dist_name)
    
    if dist_path.exists():
        shutil.rmtree(dist_path)
    
    dist_path.mkdir()
    
    # Copy executable
    shutil.copy2(exe_file, dist_path / exe_file.name)
    
    # Create README
    readme_content = """ARMR Work-Home Briefcase

This tool helps you sync files between your work computer and external drive.

USAGE:
1. Double-click ARMR_Briefcase.exe to start
2. Choose your sync mode:
   - Work Mode: Copy files FROM work directory TO external drive
   - Home Mode: Copy files FROM external drive TO home directory
3. Select your directories when prompted
4. Confirm the sync operation
5. Wait for the sync to complete

TROUBLESHOOTING:
- Make sure you have write permissions to the directories you're syncing
- Ensure your external drive is connected before starting
- The tool will create the destination directory if it doesn't exist
- If you encounter issues, try running as administrator

Version: 1.0
"""
    
    with open(dist_path / "README.txt", 'w') as f:
        f.write(readme_content)
    
    # Create a simple batch file for easy launching
    batch_content = f"""@echo off
echo Starting ARMR Briefcase...
"{exe_file.name}"
pause
"""
    
    with open(dist_path / "Launch_Tool.bat", 'w') as f:
        f.write(batch_content)
    
    print(f"✅ Distribution created in: {dist_name}/")
    print(f"   - {exe_file.name}")
    print(f"   - README.txt")
    print(f"   - Launch_Tool.bat")
    
    return True

def test_executable():
    """Test the built executable"""
    print("\n🧪 Testing executable...")
    
    dist_dir = Path("dist")
    exe_files = list(dist_dir.glob("*.exe"))
    
    if not exe_files:
        print("❌ No executable to test")
        return False
    
    exe_file = exe_files[0]
    
    try:
        # Try to start the executable (it should show GUI)
        print(f"Starting {exe_file.name}...")
        process = subprocess.Popen([str(exe_file)], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a bit to see if it starts without errors
        import time
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Executable started successfully")
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print("❌ Executable failed to start")
            print("STDOUT:", stdout.decode())
            print("STDERR:", stderr.decode())
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main build process"""
    print("=" * 60)
    print("ARMR Briefcase - Build Script")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check resources
    if not check_resources():
        return False
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if not build_executable():
        return False
    
    # Test executable
    if not test_executable():
        print("⚠️  Executable test failed, but continuing...")
    
    # Create distribution
    if not create_distribution():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 BUILD COMPLETE!")
    print("=" * 60)
    print("Your distribution is ready in: ARMR_Briefcase/")
    print("You can now distribute this folder to your clients.")
    print("\nDistribution includes:")
    print("- Single executable file")
    print("- README with usage instructions")
    print("- Launch script for easy starting")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 