@echo off

del Updated_Job_List.csv >nul

echo Will take information from "CS_LOAD.csv" and modify it
echo Will also compare jobs from "outdated.csv" and make sure "Updated_Job_List.csv" has the current jobs
python csvConverter.py
echo Should have output to "Updated_Job_List.csv"

del new_CS_LOAD.csv >nul
del new_outdated.csv >nul
copy Updated_Job_List.csv outdated.csv >nul

pause