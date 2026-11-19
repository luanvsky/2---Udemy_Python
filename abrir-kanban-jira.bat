@echo off
setlocal
title Kanban do Jira
set "PORTA=8099"
set "PASTA=D:\dsh-vsky"
set "URL=http://127.0.0.1:%PORTA%"

rem App de conformidade (http://127.0.0.1:3000). O quadro usa esta variavel
rem para o botao "App de conformidade" e para o deep link ?processo=...
rem Sem ela o servidor cai no preview do Cloud Run.
set "PORTA_APP=3000"
set "PASTA_APP=D:\conformidade-ifs"
set "KANBAN_APP_URL=http://127.0.0.1:%PORTA_APP%"

echo ============================================================
echo   Kanban do Jira  +  App de Conformidade
echo ============================================================
echo.

rem --- 1) sobe o app de conformidade, se ainda nao estiver no ar --------
netstat -ano | findstr ":%PORTA_APP%" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo   App de conformidade: ja esta rodando.
) else (
    echo   App de conformidade: subindo em segundo plano ^(leva ~10s^)...
    start "App Conformidade IFS" /min cmd /c "cd /d %PASTA_APP% && npm run dev"
)

rem --- 2) sobe o quadro, se ainda nao estiver no ar ---------------------
echo.
netstat -ano | findstr ":%PORTA%" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 goto abrir

echo   Quadro: subindo em segundo plano...
start "Servidor Kanban Jira" /min cmd /c "cd /d %PASTA% && node kanban-servidor.mjs"

set /a tentativas=0
:esperar
timeout /t 1 /nobreak >nul
netstat -ano | findstr ":%PORTA%" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 goto abrir
set /a tentativas+=1
if %tentativas% lss 20 goto esperar

echo.
echo   AVISO: o quadro nao respondeu na porta %PORTA% em 20 segundos.
echo          Para ver o erro real, abra um terminal e rode:
echo              cd /d %PASTA%
echo              node kanban-servidor.mjs
echo.
pause
exit /b 1

rem --- 3) abre o navegador ---------------------------------------------
:abrir
echo   Abrindo %URL% ...
start "" "%URL%"
echo.
echo   Pronto. Esta janela pode ser fechada.
timeout /t 4 /nobreak >nul
exit /b 0
