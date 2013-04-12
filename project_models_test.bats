#!/usr/bin/env bats
# Bats: the Bash Automated Testing System 
# https://github.com/sstephenson/bats

@test "check if output file was created" {
    rm -f 20*.dat
    sh project_models.sh
    run ls 20*.dat
    [ "$status" -eq 0 ]
}
