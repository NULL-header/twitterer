#!/bin/bash

pushd "$(dirname "${0}")" >/dev/null || {
    echo "Can not move the work directory."
    exit 1
}

ver='3.8'
assign_ver="Python ${ver}.*"
path_venv=".data/.venv"
path_src="src/HelloVenv.py"

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
        :
    else
        printf "A version of python is %s and not %s.\nPlease install Python of %s.\n" "${py_ver#Python }" "${ver}" "${ver}"
        popd
        exit 1
    fi
 } || {
     echo "Python is not installed."
     exit 1
 }

if [ -e $path_venv ]; then
    :
else
    $path_py -m venv "$path_venv"
fi

{
    source $path_venv/bin/activate
} || {
    echo "A error occured in probrem such as venv."
}

$path_py $path_src

popd > /dev/null || {
    echo "Error is occured in end process."
}
