@echo off

chcp 65001
cls

echo "---------- EXTRACT ----------"
echo "确保你把本VENV_EXTRACT.bat程序，放在和虚拟环境的Scripts文件夹同一个目录下"
echo "准备好了，按任意键开始提取..."
pause > nul

echo "---------- EXTRACT ----------"
echo "正在提取中..."

call .\Scripts\activate.bat

pip freeze > requirements.txt
pip download -r requirements.txt -d ./wheels

echo "---------- FINISHED ----------"
echo "提取产物：requirements.txt清单 + wheels文件夹"
echo "请把这两个东西保存好，可以用来重建venv"
echo "按任意键退出程序..."
pause > nul
exit
