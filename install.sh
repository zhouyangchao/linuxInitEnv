#!/bin/sh

install_dir=${1:-$(echo ~)}

cp config/* ${install_dir}

mkdir -p ${install_dir}/.vim_swap/

sed -i "s#/root/#"$install_dir"#g" ${install_dir}/.gdbinit

