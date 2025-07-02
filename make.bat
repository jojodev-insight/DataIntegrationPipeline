@echo off
REM Windows batch file for Document Parser project commands

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="test" goto test
if "%1"=="test-cov" goto test-cov
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="type-check" goto type-check
if "%1"=="clean" goto clean
if "%1"=="build" goto build
if "%1"=="run-example" goto run-example
if "%1"=="all-checks" goto all-checks
if "%1"=="dev-setup" goto dev-setup

goto help

:help
echo Document Parser - Available commands:
echo.
echo   install      Install the package and dependencies
echo   install-dev  Install development dependencies
echo   test         Run tests
echo   test-cov     Run tests with coverage report
echo   lint         Run linting (flake8)
echo   format       Format code with black
echo   type-check   Run type checking with mypy
echo   clean        Clean build artifacts
echo   build        Build the package
echo   run-example  Run the example script
echo   all-checks   Run all code quality checks
echo   dev-setup    Set up development environment
echo.
echo Usage: make.bat ^<command^>
goto end

:install
pip install -r requirements.txt
pip install -e .
goto end

:install-dev
pip install -r requirements.txt
pip install -e .[dev]
goto end

:test
pytest tests/ -v
goto end

:test-cov
pytest tests/ -v --cov=document_parser --cov-report=html --cov-report=term
goto end

:lint
flake8 document_parser/ tests/
goto end

:format
black document_parser/ tests/ *.py
goto end

:type-check
mypy document_parser/
goto end

:all-checks
call :lint
if errorlevel 1 goto end
call :type-check
if errorlevel 1 goto end
call :test
goto end

:clean
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.egg-info rmdir /s /q *.egg-info
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist .mypy_cache rmdir /s /q .mypy_cache
if exist htmlcov rmdir /s /q htmlcov
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"
goto end

:build
call :clean
python setup.py sdist bdist_wheel
goto end

:run-example
python example_usage.py
goto end

:dev-setup
call :install-dev
echo Development environment setup complete!
echo Run 'make.bat run-example' to test the installation.
goto end

:end
