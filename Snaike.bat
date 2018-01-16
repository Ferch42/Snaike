@echo off
SET /A "index=1"
SET /A "count=100"
:while
if %index% leq %count% (
   echo ffffffffffffffffffffffffffffff
   echo The run is %index%
   python Snaike.py
   SET /A "index=index + 1"
   goto :while
)
pause