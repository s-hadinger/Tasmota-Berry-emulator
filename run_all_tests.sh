#!/bin/bash
echo "Running all Berry Animation Framework tests..."
./berry -s -g -m lib/libesp32/berry_animation/src/ lib/libesp32/berry_animation/src/tests/test_all.be
echo "Done!"