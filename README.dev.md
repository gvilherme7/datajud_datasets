# Python Environment Setup with Makefile

This repository contains a Makefile to facilitate Python virtual environment setup and management across multiple platforms (Windows and Unix-like systems).

### Method 1: Using Makefile

## Prerequisites

- Python (recommended version: 3.11.0)
- Make (optional)
- Operating System: Windows or Linux/MacOS

## Virtual Environment Setup Methods

### Method 1: Using Makefile (Cross-Platform)

## Prerequisites

- Python (recommended version: 3.11.0)
- Make
- Operating System: Windows or Linux/MacOS

## Environment Setup

### Main Commands

| Command | Description |
|---------|-----------|
| `make setup` | Checks Python installation, creates virtual environment, and installs dependencies |
| `make run` | Executes the main script (`main.py`) after setting up the environment |
| `make clean` | Removes the virtual environment |

### Makefile Details

#### Key Variables
- `PYTHON_VERSION`: Defines Python version (3.11.0)
- `VENV`: Virtual environment directory (`.venv`)

#### Features

1. **Python Installation Check**
   - On Windows: Automatically downloads and installs if not found
   - On Unix-like systems: Provides manual installation instructions

2. **Virtual Environment Creation**
   - Creates an isolated virtual environment
   - Updates pip
   - Supports Windows and Unix systems

3. **Dependency Installation**
   - Uses `requirements.txt` to install packages

### Installation and Usage

#### First-Time Setup

1. Clone the repository
2. Install Python (3.11.0 recommended)
3. Run `make setup`

#### Running the Project

- To setup and run: `make run`
- To clean the environment: `make clean`

### Additional Requirements

- Create a `requirements.txt` file with your dependencies
- Have a main `main.py` script

### Notes

- Windows requires administrator permissions for installation
- On Unix systems, use package managers to install Python

---

### Method 2: Standard Virtual Environment Setup

#### Using `venv` (Recommended)

1. **Create Virtual Environment**
```bash
# On Windows
python -m venv .venv

# On macOS/Linux
python3 -m venv .venv
```

2. **Activate Virtual Environment**
```bash
# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
# With virtual environment activated
pip install -r requirements.default.txt
```

4. **Deactivate Virtual Environment**
```bash
deactivate
```

## Project Structure

```
project-root/
│
├── .venv/               # Virtual environment directory
├── src/                 # Source code directory
│   └── main.py          # Main application script
├── tests/               # Test files directory
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignore file
```

## Contributing Guidelines

### Getting Started

1. **Fork the Repository**
   - Click "Fork" on the top right of the GitHub repository
   - Clone your forked repository
   ```bash
   git clone https://github.com/YOUR-USERNAME/repository-name.git
   cd repository-name
   ```

2. **Setup Development Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Unix
   .venv\Scripts\activate     # On Windows

   # Install dependencies
   pip install -r requirements.default.txt
   
   # Install development dependencies
   pip install -r requirements-dev.txt  # If you have a separate dev requirements file
   ```

### Contribution Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clean, documented code
   - Follow project's coding standards
   - Add/update tests for new functionality

3. **Run Tests**
   ```bash
   # Run all tests
   pytest tests/

   # Run linters (if configured)
   flake8 src/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: Describe your changes clearly and concisely"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Open a Pull Request from your fork to the main repository
   - Describe changes in the PR description
   - Link any related issues

### Best Practices

- Write clear, concise commit messages
- Keep pull requests focused and small
- Add tests for new functionality
- Update documentation as needed
- Follow PEP 8 style guidelines
- Use type hints and docstrings

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Collaborate openly and kindly

---

### Recommended Tools

- **Virtual Environment**: `venv`
- **Dependency Management**: `uv`
- **Testing**: `pytest`
- **Linting**: `flake8`, `pylint`
- **Type Checking**: `mypy`