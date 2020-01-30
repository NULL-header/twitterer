#!/bin/bash
ver='3.8'
assign_ver="Python ${ver}.*"
if [ -n "$1" ]; then
    py=$(python --version 2>&1)
    if [ -e "$1" ] && [[ $py =~ Python.+ ]]; then
        path_py=$1
    else
        echo "the path is not to python."
        path_py='python'
    fi
else
    path_py='python'
fi
{
    py_ver=$($path_py --version 2>&1)
    if [[ $py_ver =~ $assign_ver ]]; then
        echo "ok"
    else
        printf "A version of python is %s and not %s.\nPlease install Python of %s.\n" "${py_ver#Python }" "${ver}" "${ver}"
    fi
 } || echo "Python is not installed."

#now_py=$(${py_ver})
#now_py=${now_py#Python }
#echo "$now_py"
