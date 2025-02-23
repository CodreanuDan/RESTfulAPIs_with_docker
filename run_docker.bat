@echo off
echo ==============================
echo INFO: Running run_docker.bat...
echo ==============================

docker --version

:: Go in specified directory
cd /d D:\FACULTATE\AN_1_MASTER\Semestrul_2\Damian\T1\

:: Check if env_data.env file exists
if not exist env_data.env (
    echo ERROR: No env_data.env file in current dir!
    pause
    exit /b
)

:: Show the list of Docker images before checking
echo ==============================
echo INFO: Showing Docker images...
docker images

:: Show Dockerfile location
echo ==============================
echo INFO: Dockerfile path: Dockerfile

:: Check if Dockerfile exists
if not exist Dockerfile (
    echo ERROR: Dockerfile not found!
    pause
    exit /b
)

:: Check if image exists
docker inspect myapp >nul 2>&1
if %errorLevel% neq 0 (
    echo INFO: Docker image not found, building image...
    docker build --no-cache -t myapp .
) else (
    echo INFO: Docker image exists!
)

:: Cleanup old containers and images
echo ==============================
echo INFO: Deleting old containers...
docker container prune -f
echo INFO: Deleting old images... 
docker image prune -f

:: Check if WEATHER_API_KEY_1 exists in env_data.env
findstr /R "^WEATHER_API_KEY_1=" env_data.env >nul
if %errorLevel% neq 0 (
    echo ERROR: WEATHER_API_KEY_1 not found in env_data.env!
    pause
    exit /b
) else (
    echo INFO: WEATHER_API_KEY_1 found!
)

:: Check if WEATHER_API_KEY_2 exists in env_data.env
findstr /R "^WEATHER_API_KEY_2=" env_data.env >nul
if %errorLevel% neq 0 (
    echo ERROR: WEATHER_API_KEY_2 not found in env_data.env!
    pause
    exit /b
) else (
    echo INFO: WEATHER_API_KEY_2 found!
)

:: Run the container, added -it tu run interactively
echo ==============================
echo INFO: Running container...
docker run -it --env-file env_data.env -p 8080:8080 myapp

:: Copy json data
echo ==============================
echo INFO: Copy data into machine...
docker cp <container_id>:/app/inputs.json .

echo ==============================
echo INFO: Container exited. Press any key to close.
@REM pause
exit /b