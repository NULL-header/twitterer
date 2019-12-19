@echo off

pushd %~dp0

setlocal
set fold=test
set file=test1.py

call :Generater
call :MDChecker
call :VEMaker

echo all green.

call .data\.venv\Scripts\activate

pushd %fold%
python %file%

popd
popd
pause >nul
deactivate
exit


rem ===subroutine===

:Generater
if exist .data (
	echo the .data folder exists.
) else (
	echo the .data folder does not exist.
	echo make this.
	md .data
)
if exist doc (
	echo the doc folder exists.
) else (
	echo the doc folder does not exist.
	echo make this.
	md doc
)
if exist test (
	echo the test folder exists.
) else (
	echo the test folder does not exist.
	echo make this.
	md test
	echo #encoding:utf-8>test\test1.py
	echo.>>test\test1.py
	echo print^(^"hello venv and you!^"^)>>test\test1.py
)
if exist requirements.txt (
	echo requirements.txt exists.
) else (
	type nul >requirements.txt
	echo requirements.txt does not exist.
	echo made this.
)
if exist ac_venv.bat (
	echo ac_venv.bat exists.
) else (
	echo cmd ^/k .data\.venv\Scripts\activate >ac_venv.bat
	echo ac_venv.bat does not exist.
	echo made this.
)
if exist ac_atom.bat (
	echo ac_atom.bat exists.
) else (
	echo atom . >ac_atom.bat
	echo ac_atom.bat does not exist.
	echo made this.
)
if exist ac_bash.bat (
	echo ac_bash.bat exists.
) else (
	echo git-bash >ac_bash.bat
	echo ac_atom.bat does not exist.
	echo made this.
)
if exist .gitignore (
	echo .gitignore exists.
) else (
	type nul >.gitignore
	echo /*.bat >.gitignore
	echo /.data/ >>.gitignore
	echo .gitignore does not exist.
	echo made this.
)
if exist .data\.venv (
	echo venv exists.
) else (
	echo venv does not exist.
	echo made this.
	python -m venv .data\.venv
	pushd .data\.venv\Lib\site-packages
	echo import builtins>usercustomize.py
	echo.>>usercustomize.py
	echo __original = open>>usercustomize.py
	echo def __open^(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None^):>>usercustomize.py
	echo     if 'b' not in mode and not encoding:>>usercustomize.py
	echo         encoding = 'utf-8'>>usercustomize.py
	echo     return __original^(file, mode, buffering, encoding, errors, newline, closefd, opener^)>>usercustomize.py
	echo.>>usercustomize.py
	echo builtins.open = __open>>usercustomize.py
	popd
)
exit /b



:MDChecker
for /f "usebackq delims=" %%i in (`certutil -hashfile requirements.txt MD5 ^| find /v "CertUtil" ^| find /v "MD5"`) do set Hash=%%i
if "%Hash%" == "" (
	set Hash=d41d8cd98f00b204e9800998ecf8427e
)
exit /b



:VEMaker
pushd .data
if exist "ram-%Hash%.txt" (
	echo requirements.txt is not changed.
) else (
	echo requirements.txt is changed.
	del /q ram-*.txt
	type nul >"ram-%Hash%.txt"
	call .venv\Scripts\activate
	python -m pip freeze|xargs python -m pip uninstall -y
	if "%Hash%" == "d41d8cd98f00b204e9800998ecf8427e" (
		echo there is nothing in requirements.txt.
	) else (
		which python
		echo there are something package in requirements.txt
		python -m pip install --upgrade pip
		python -m pip install -r ..\requirements.txt
	)
	deactivate
	echo all green.
	pause >nul
	exit
)
popd
exit /b
