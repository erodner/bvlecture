REM Hotfix for https://stackoverflow.com/questions/54175042/python-3-7-anaconda-environment-import-ssl-dll-load-fail-error
COPY C:\ProgramData\Anaconda3\pkgs\openssl-1.1.1k-h2bbff1b_0\Library\bin\libcrypto*.dll C:\ProgramData\Anaconda3\envs\bvlecture\DLLs
COPY C:\ProgramData\Anaconda3\pkgs\openssl-1.1.1k-h2bbff1b_0\Library\bin\libssl*.dll C:\ProgramData\Anaconda3\envs\bvlecture\DLLs
