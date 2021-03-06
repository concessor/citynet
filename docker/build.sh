#!/bin/bash

# Base Script File (build.sh)
# Created: Mon 29 Jan 2018 18:50:25 GMT
# Version: 1.0
#
# This Bash script was developped by Cory.
#
# (c) Cory <sgryco@gmail.com>

docker_root=$(dirname $0)
docker image build "$docker_root" --network host -t asegroup11/all_servers:citynet || exit -1

#unit test
./${docker_root}/run_all_tests.sh
