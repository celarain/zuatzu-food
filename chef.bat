set CURRENT_DIR=%~dp0
docker stop my_chef_container
docker rm my_chef_container
docker run --name my_chef_container --env-file "%CURRENT_DIR%\.env" -v "%CURRENT_DIR%\logs:/app/logs" -it chef
