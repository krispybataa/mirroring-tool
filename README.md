# ARMR Work-Home Mirror Tool

A professional file synchronization tool designed to help users sync files between work computers and external drives. Perfect for professionals who need to work on files both at work and at home.

## Features

- **Work Mode**: Sync files FROM work directory TO external drive
- **Home Mode**: Sync files FROM external drive TO home directory
- **Smart File Comparison**: Only copies files that have changed
- **Progress Tracking**: Real-time progress display during sync operations
- **Directory Creation**: Automatically creates destination directories if they don't exist
- **Configuration Persistence**: Remembers your frequently used directories
- **Modern GUI**: Clean, professional interface built with tkinter
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Quick Start

### For End Users
1. Download the `ARMR_Briefcase_Distribution/` folder
2. Double-click `ARMR_Briefcase.exe` to start
3. Choose your sync mode (Work or Home)
4. Select your directories when prompted
5. Confirm the sync operation
6. Wait for completion

### For Developers
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python simple_test.py`
4. Build distribution: `python build.py`

## Usage

### Work Mode
- **Purpose**: Copy files from your work computer to an external drive
- **Use Case**: When leaving work, sync your files to take home
- **Flow**: Work Directory → External Drive

### Home Mode
- **Purpose**: Copy files from external drive to your home computer
- **Use Case**: When arriving home, sync files from your external drive
- **Flow**: External Drive → Home Directory

### Sync Process
1. **Select Mode**: Choose Work Mode or Home Mode
2. **Choose Directories**: Select source and destination folders
3. **Confirm**: Review the sync operation details
4. **Execute**: Watch progress as files are synchronized
5. **Complete**: Receive confirmation when sync is finished

## Technical Details

- **Language**: Python 3.7+
- **GUI Framework**: tkinter (built-in Python GUI)
- **File Operations**: shutil, filecmp, pathlib
- **Build Tool**: PyInstaller for executable creation
- **Testing**: unittest framework with comprehensive test suite
- **Architecture**: Modular design with separate UI and business logic

## Development

### Project Structure
```
mirroring-tool/
├── main.py              # Main application entry point
├── styles.py            # GUI styling and themes
├── main.spec            # PyInstaller configuration
├── build.py             # Build automation script
├── build.bat            # Windows build script
├── requirements.txt     # Python dependencies
├── test_main.py         # Comprehensive test suite
├── test_utils.py        # Testing utilities
├── test_runner.py       # Test execution framework
├── simple_test.py       # Basic tests (no dependencies)
├── resoources/          # Application resources
│   └── app_icon_final.ico
└── README.md           # This file
```

### Building the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python simple_test.py

# Build distribution
python build.py
```

### Testing
```bash
# Run simple tests (no external dependencies)
python simple_test.py

# Run full test suite (requires pytest)
python test_runner.py --all

# Run specific test categories
python test_runner.py --basic
python test_runner.py --gui
python test_runner.py --performance
```

## Distribution

The application is distributed as a single executable file with all dependencies included. The build process creates:

- **ARMR_Briefcase.exe**: Self-contained executable
- **README.txt**: User instructions
- **Launch_Tool.bat**: Easy launch script

### System Requirements
- **OS**: Windows 7/8/10/11 (64-bit recommended)
- **RAM**: 512MB minimum, 2GB recommended
- **Storage**: 100MB free space
- **Permissions**: Write access to source and destination directories

## Troubleshooting

### Common Issues
1. **"Access Denied"**: Run as administrator or check file permissions
2. **"File Not Found"**: Ensure external drive is connected
3. **"Sync Fails"**: Check available disk space
4. **"Application Won't Start"**: Check antivirus exclusions

### Support
For technical support or feature requests, contact your IT department or the development team.

## Version History

- **v1.0**: Initial release with Work/Home sync modes
- **v1.1**: Added progress tracking and configuration persistence
- **v1.2**: Improved error handling and user interface

## License

This software is proprietary and confidential. Unauthorized distribution is prohibited.

---

**Developed by**: Clark Rodriguez  
**Last Updated**: 2024  
**Python Version**: 3.7+ compatible