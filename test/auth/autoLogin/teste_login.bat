@echo off
setlocal
set URL=http://localhost:8000/api/v1/auth/login

echo Deseja usar as credenciais padrao ou editar manualmente?
echo [1] Usar padrao (admin@npet.org)
echo [2] Inserir manualmente
set /p OPCAO="Escolha uma opcao (1 ou 2): "

if "%OPCAO%"=="2" (
    set /p EMAIL="Digite o email: "
    set /p PASS="Digite a senha: "
) else (
    set EMAIL=admin@npet.org
    set PASS=npet123
)

echo Criando o arquivo JSON puro para o cURL...
(
echo {
echo   "email": "%EMAIL%",
echo   "password": "%PASS%"
echo }
) > "%temp%\payload.json"

echo Enviando requisicao para %URL%...
curl -X POST -H "Content-Type: application/json" -d @"%temp%\payload.json" -c cookies.txt -s -o response.html -w "HTTP Status: %%{http_code}\n" %URL%

echo Exibindo resposta do servidor:
type response.html
echo.

echo Limpando...
del "%temp%\payload.json"
pause
endlocal