@echo off
echo ========================================
echo Git Status and Commit Helper
echo ========================================
echo.

cd /d "C:\Users\Omri.Morgan02\Downloads\spammer\Cyber-Security-Education"

echo Checking Git status...
echo.
git status
echo.
echo ========================================
echo.

echo Adding all files...
git add -A
echo.

echo Files staged. Here's what will be committed:
git status --short
echo.
echo ========================================
echo.

set /p continue="Continue with commit? (y/n): "
if /i "%continue%"=="y" (
    echo.
    echo Creating commit...
    git commit -m "Major repository reorganization and new educational platforms - Added Mathematics, Science, and Social Studies platforms with 20,000+ lines of content - Reorganized into Educational_Platforms, Tools_and_Utilities, and Documentation folders - Created comprehensive README, DIRECTORY_MAP, and documentation - Added 15+ interactive Python applications - Added 30+ lesson plans and 25+ student activities - Standards-aligned content (Common Core, NGSS, C3 Framework, NCSS, NCTM)"
    echo.
    echo ========================================
    echo.
    
    echo Commit created. Checking remote status...
    git remote -v
    echo.
    
    set /p push="Push to remote? (y/n): "
    if /i "%push%"=="y" (
        echo.
        echo Pushing to remote...
        git push origin main
        echo.
        if errorlevel 1 (
            echo.
            echo ========================================
            echo Push failed! Common issues:
            echo 1. No remote configured - run: git remote add origin [URL]
            echo 2. Authentication required - may need to set up credentials
            echo 3. Branch mismatch - try: git push origin master
            echo 4. Need to pull first - try: git pull origin main --rebase
            echo ========================================
            echo.
            echo Attempting to get more info...
            git remote show origin
        ) else (
            echo.
            echo ========================================
            echo SUCCESS! Changes pushed to remote repository.
            echo ========================================
        )
    )
) else (
    echo.
    echo Commit cancelled. No changes made.
)

echo.
echo Final status:
git status
echo.
pause
