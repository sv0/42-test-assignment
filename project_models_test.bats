#!/usr/bin/env bats
# Bats: the Bash Automated Testing System 
# https://github.com/sstephenson/bats

@test "check if output file was created" {
    run rm -f "20*.dat"
    run sh project_models.sh
    run ls "20*.dat"
    [ "$status" -eq 2 ]
}
