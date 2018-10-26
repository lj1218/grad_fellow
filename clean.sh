#!/usr/bin/env bash

[ ! -d build ] && exit
rm -rf build/
rm -rf dist/
rm -rf grad_fellow.egg-info/
echo "cleaned"
