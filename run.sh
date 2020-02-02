#!/bin/bash

pushd "$(dirname "${0}")" >/dev/null || {
    echo "Can not move the work directory."
    exit 1
}


#property of env
ver='3.8'
assign_ver="Python ${ver}.*"
path_venv=".data/.venv"
path_src="src/HelloVenv.py"

#initialize
declare -A args
declare -A options_to_short
declare -a options_nonarg
declare -a array_options
path_py='python'

endprocess(){
    echo -e "$1"
    popd > /dev/null || {
        echo "Error is occured in end process."
    }
    exit 1
}

#property of methods long name
options_to_short=(
    ['python-path']='p'
    ['help']='h'
)

#property of methods short name
options_nonarg=( 'h' )

#common process in options
pros(){
    #help
    func_h(){
        echo "Usage:"
        echo "    -h   --help          option -> show usage"
        echo "    -p   --python-path   option -> set path of python"
        exit 1
    }
    #python-path
    func_p(){
        if [ -n "$1" ]; then
            args['add_path']="$1"
        else
            endprocess "-p or --python-path option need a argment."
        fi
    }
    #replaced long option to short
    op="$1"
    for option in "${!options_to_short[@]}"; do
        if [ "$1" == "$option" ]; then
            op=${options_to_short[$option]}
        fi
    done
    #method calling
    if [ -z "$2" ]; then
        "func_$op" 2> /dev/null || endprocess "A error occured in a calling of no-argumential option."
    else
        "func_$op" "$2" 2> /dev/null || endprocess "A error occured in a calling of argumntial option."
    fi
}
#option checking
while (( $# > 0 )); do
    array_options=()
    non_need_arg=''
    case "$1" in
        --*)
            hyphen='--'
            ;;
        -*)
            hyphen='-'
            for option in "${options_nonarg[@]}"; do
                if [[ $1 =~ $option ]]; then
                    array_options+=( "$option" )
                    non_need_arg='n'
                fi
            done
            ;;
        *)
            endprocess 'run.sh needs such as -e or --example.'
            hyphen=''
            ;;
    esac
    if [ -n "$hyphen" ]; then
        if [ -z "$non_need_arg" ]; then
            pros "${1#${hyphen}}" "$2"
            shift
        else
            for option in "${array_options[@]}"; do
                pros "$option"
            done
        fi
    fi
    shift
done

#-p option
add_path(){
    if [ -e "$1" ] && [[ $($1 --version 2> /dev/null) =~ Python.+ ]]; then
        path_py="$1"
    else
        endprocess "Python is not forward on the path."
    fi
}

for option in "${!args[@]}"; do
    $option "${args[$option]}"
done



{
    ver_py=$($path_py --version 2>&1)
    if [[ ! $ver_py =~ $assign_ver ]]; then
        endprocess "A version of python is ${ver_py#Python } and not ${ver}.\nPlease install Python of ${ver}."
    fi
} || endprocess "Python is not installed or seted path."

if [ ! -e $path_venv ]; then
    $path_py -m venv "$path_venv"
fi

source $path_venv/bin/activate || endprocess "A error occured in probrem such as venv."

$path_py $path_src

endprocess "done Successfully."
