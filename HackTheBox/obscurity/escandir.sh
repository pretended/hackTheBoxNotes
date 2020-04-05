 
#/bin/bash path = $1 while ( true ) ; do file = $( ls $path ) if [ " ${file} " == "" ] then continue else mv $path / $file ./ break fi done
 
