@echo off
set WATERMARK=true
set PASSWORD=true
set PAGENUMBER=false
set PREFIX=
set SUFFIX=(draft)

echo.
echo ===== PDF 加工ツール 実行開始 =====
if "%WATERMARK%"=="true" ( echo 透かし追加: 有効 ) else ( echo 透かし追加: 無効 )
if "%PASSWORD%"=="true" ( echo パスワード追加: 有効 ) else ( echo パスワード追加: 無効 )
if "%PAGENUMBER%"=="true" ( echo ページ番号追加: 有効 ) else ( echo ページ番号追加: 無効 )
echo ファイル名接頭辞（prefix）: "%PREFIX%"
echo ファイル名接尾辞（suffix）: "%SUFFIX%"
echo.

poetry run python main.py ^
    %WATERMARK:~-4%==true --watermark ^
    %PASSWORD:~-4%==true --password ^
    %PAGENUMBER:~-4%==true --pagenumber ^
    --prefix "%PREFIX%" --suffix "%SUFFIX%"

pause
