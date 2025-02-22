@echo off

timeout /t 1 /nobreak

:: Go in specified directory
cd /d C:\Users\uig37216\Desktop\SCOALA\RESTful\Tema_1_3ApiApelate

timeout /t 1 /nobreak

:: Check if env_data.env file exists
if not exist env_data.env (
    echo ERROR: No env_data.env file in current dir !
    pause
    exit /b
)

timeout /t 1 /nobreak

:: Show the list of Docker images before checking
echo INFO: Showing Docker images...
docker images

timeout /t 1 /nobreak

:: Show Dockerfile location
echo INFO: Dockerfile path: Dockerfile

timeout /t 1 /nobreak

:: Check if Dockerfile exists
if not exist Dockerfile (
    echo ERROR: Dockerfile not found at the specified location!
    pause
    exit /b
)

:: Build image if it's not built
docker images | findstr /i "myapp"
if %errorLevel% neq 0 (
    echo INFO: Docker image not found, building image...
    docker build -t myapp -f Dockerfile .
)

:: Add a small delay before running the container to ensure image is built
timeout /t 5 /nobreak

:: Run the container with variables from env_data.env file with port 8080
echo INFO: Run container...
docker run --env-file env_data.env -p 8080:8080 myapp

timeout /t 1 /nobreak

pause

