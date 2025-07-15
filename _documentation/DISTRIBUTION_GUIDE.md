# Distribution Guide for ARMR Mirror Tool

This guide explains how to build and distribute the ARMR Mirror Tool to clients in a robust, professional manner.

## Quick Start

### 1. Build the Distribution
```bash
python build.py
```

This will create a `ARMR_Mirror_Tool_Distribution/` folder containing everything needed for client distribution.

### 2. Test the Distribution
1. Copy the distribution folder to a clean machine (or VM)
2. Run the executable to ensure it works
3. Test both sync modes with sample data

### 3. Distribute to Clients
Send the entire `ARMR_Mirror_Tool_Distribution/` folder to your clients.

## What's Included in the Distribution

```
ARMR_Mirror_Tool_Distribution/
├── ARMR_Mirror_Tool.exe      # Main executable (self-contained)
├── README.txt                # User instructions
└── Launch_Tool.bat          # Easy launch script
```

## Build Process Details

### Prerequisites
- Python 3.7+ installed
- PyInstaller installed: `pip install pyinstaller`
- All project dependencies: `pip install -r requirements.txt`

### Build Steps
1. **Check Resources**: Ensures icon and other resources exist
2. **Clean Build**: Removes previous build artifacts
3. **Compile**: Creates single-file executable with PyInstaller
4. **Test**: Verifies executable starts without errors
5. **Package**: Creates clean distribution folder

### Key Improvements Made

#### 1. Resource Path Handling
```python
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
```

#### 2. PyInstaller Configuration
- **Single-file executable**: Everything bundled into one .exe
- **Resources included**: Icon and other assets properly bundled
- **Hidden imports**: All required modules explicitly included
- **Exclusions**: Unnecessary libraries excluded to reduce size
- **Application icon**: Professional icon set for the executable

#### 3. Error Handling
- Graceful fallbacks when resources are missing
- Better error messages for common issues
- Robust path handling for different environments

## Common Distribution Issues and Solutions

### Issue 1: "Missing DLL" or "Application Error"
**Cause**: Missing Visual C++ Redistributable or other system dependencies
**Solution**: 
- Include Visual C++ Redistributable in distribution
- Or create a "portable" version that includes all dependencies

### Issue 2: "Access Denied" Errors
**Cause**: Insufficient permissions for file operations
**Solution**:
- Run as administrator
- Ensure proper file permissions
- Add UAC manifest to executable

### Issue 3: "File Not Found" Errors
**Cause**: Resources not properly bundled
**Solution**:
- Verify resources are included in PyInstaller spec
- Use `get_resource_path()` function for all file access

### Issue 4: Antivirus False Positives
**Cause**: PyInstaller executables often trigger antivirus software
**Solution**:
- Sign the executable with a code signing certificate
- Submit to antivirus vendors for whitelisting
- Use a trusted build environment

## Advanced Distribution Options

### Option 1: Installer Package
Create a proper Windows installer using tools like:
- Inno Setup
- NSIS (Nullsoft Scriptable Install System)
- WiX Toolset

### Option 2: Portable Distribution
For maximum compatibility, create a portable version:
```bash
# Build with --onedir instead of --onefile
pyinstaller --onedir main.spec
```

### Option 3: Code Signing
For enterprise distribution, sign your executable:
```bash
# Using a code signing certificate
signtool sign /f certificate.pfx /p password ARMR_Mirror_Tool.exe
```

## Testing Checklist

Before distributing to clients, test:

### Basic Functionality
- [ ] Application starts without errors
- [ ] GUI displays correctly
- [ ] Both sync modes work
- [ ] Directory selection works
- [ ] Progress window displays
- [ ] Configuration saves/loads

### File Operations
- [ ] Can sync files between directories
- [ ] Handles large files correctly
- [ ] Preserves file attributes
- [ ] Creates destination directories
- [ ] Handles permission errors gracefully

### Error Scenarios
- [ ] Missing source directory
- [ ] Insufficient disk space
- [ ] Network drive disconnection
- [ ] File in use by another process
- [ ] Invalid file paths

### Cross-Platform Testing
- [ ] Windows 10 (64-bit)
- [ ] Windows 11 (64-bit)
- [ ] Windows Server 2019/2022
- [ ] Different user permission levels

## Client Deployment Instructions

### For IT Administrators

1. **Extract the distribution** to a network share or local directory
2. **Deploy to client machines** using your preferred method:
   - Group Policy
   - SCCM
   - Manual installation
   - USB drive distribution

3. **Set up shortcuts** on client desktops or start menus
4. **Configure permissions** if needed for specific directories

### For End Users

1. **Download and extract** the distribution folder
2. **Run ARMR_Mirror_Tool.exe** or double-click Launch_Tool.bat
3. **Follow the on-screen instructions** to sync files
4. **Contact IT support** if issues arise

## Troubleshooting Guide

### For Build Issues
```bash
# Clean everything and rebuild
python build.py --clean
pyinstaller --clean main.spec
```

### For Runtime Issues
1. Check Windows Event Viewer for error details
2. Run executable from command line to see error messages
3. Verify all dependencies are included in the build
4. Test on a clean virtual machine

### For Client Issues
1. **"Application won't start"**: Check antivirus exclusions
2. **"Permission denied"**: Run as administrator
3. **"File not found"**: Verify external drive is connected
4. **"Sync fails"**: Check available disk space

## Version Management

### Versioning Strategy
- Use semantic versioning (e.g., 1.0.0, 1.0.1, 1.1.0)
- Include version in executable properties
- Maintain changelog for each release

### Update Distribution
1. Update version number in code
2. Rebuild using `python build.py`
3. Test thoroughly
4. Distribute new version to clients

## Security Considerations

### Code Signing
- Sign executables with trusted certificate
- Include digital signature verification
- Maintain certificate validity

### Antivirus Compatibility
- Test with major antivirus software
- Submit for whitelisting if needed
- Use clean build environments

### File Permissions
- Respect user file permissions
- Don't require unnecessary admin rights
- Handle permission errors gracefully

## Support and Maintenance

### Documentation
- Maintain user documentation
- Create troubleshooting guides
- Document known issues and workarounds

### Update Process
- Establish update distribution method
- Test updates thoroughly
- Provide rollback procedures

### Client Support
- Set up support contact information
- Create FAQ for common issues
- Establish escalation procedures

## Conclusion

Following this guide will ensure your ARMR Mirror Tool distribution is robust, professional, and reliable for client use. The key is thorough testing and proper packaging to avoid common distribution issues. 