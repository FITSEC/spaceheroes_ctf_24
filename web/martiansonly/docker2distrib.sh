#!/bin/sh
rm -rf distrib/*
cp -pr docker/* distrib/
rm -r distrib/src/target
rm distrib/src/Cargo.lock
printf '%s' 'shctf{this_is_not_a_real_flag_please_do_not_submit_this}' > distrib/flag.txt
tar czf distrib/martiansonly.tar.gz distrib/* --numeric-owner
