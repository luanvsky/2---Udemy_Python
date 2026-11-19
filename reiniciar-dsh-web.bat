@echo off
setlocal enabledelayedexpansion
title DSH Web - NAO FECHE ESTA JANELA

echo ============================================================
echo   Reiniciar o DSH Web
echo   (ativa nucleo 0.1.7-rc.2, microfone e painel JIRA)
echo ============================================================
echo.

echo [1/4] Encerrando o servidor antigo na porta 3080...
set "FOUND="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3080" ^| findstr "LISTENING"') do (
    set "FOUND=1"
    echo       encontrado PID %%a - encerrando...
    taskkill /F /PID %%a >nul 2>&1
)
if not defined FOUND (
    echo       nada escutando na 3080 - seguindo.
) else (
    echo       aguardando a porta liberar...
    timeout /t 3 /nobreak >nul
)

echo.
echo [2/4] Conferindo o token do JIRA (arquivo .jira-token)...
set "JIRA_TOKEN_VALUE="
set "TOKENFILE=%USERPROFILE%\.dsh\.jira-token"
if not exist "%TOKENFILE%" goto notoken
findstr /C:"COLE-AQUI" "%TOKENFILE%" >nul 2>&1
if not errorlevel 1 goto placeholder
for /f "usebackq delims=" %%t in ("%TOKENFILE%") do if not defined JIRA_TOKEN_VALUE set "JIRA_TOKEN_VALUE=%%t"
if not defined JIRA_TOKEN_VALUE goto notoken
echo       OK - arquivo presente. O servidor do Kanban le ele direto.
echo       O painel JIRA do chat NAO usa mais esta variavel: ele le o
echo       cofre de credenciais (ref JIRA_TASKS_TOKEN em
echo       %USERPROFILE%\.dsh\.credentials.yaml). Por isso o token
echo       nao e mais exportado como JIRA_API_TOKEN.
goto aftertoken

:placeholder
echo       AVISO: o .jira-token ainda contem o placeholder.
echo              O servidor do Kanban JIRA NAO vai autenticar.
goto aftertoken

:notoken
echo       AVISO: .jira-token ausente ou vazio.
echo              O servidor do Kanban JIRA NAO vai autenticar.

:aftertoken

echo.
echo [3/4] Verificando o servidor do Kanban do Jira (porta 8099)...
netstat -ano | findstr ":8099" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
    echo       nao esta rodando - subindo em segundo plano...
    start "Servidor Kanban Jira" /min cmd /c "cd /d D:\dsh-vsky && node kanban-servidor.mjs"
    timeout /t 2 /nobreak >nul
) else (
    echo       ja esta rodando - mantido.
)

echo.
echo [4/4] Subindo o dsh web...
echo.
echo       ****************************************************
echo       *  NAO FECHE ESTA JANELA enquanto usar o chat.     *
echo       *  Fechar a janela derruba o chat.                 *
echo       ****************************************************
echo.
echo       O navegador deve abrir sozinho. Se nao abrir,
echo       copie a linha "dsh web: http://..." abaixo.
echo.
cd /d "D:\dsh-vsky"
call "%APPDATA%\npm\dsh.cmd" web

echo.
echo [fim] O dsh web foi encerrado.
echo       Pressione qualquer tecla para fechar esta janela.
pause >nul
