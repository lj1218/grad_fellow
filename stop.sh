#!/usr/bin/env bash

function not_running()
{
    echo "Not running"
    exit
}

function stop_success()
{
    echo "Stop program success"
    rm -f ${pid_file}
    exit
}

app_name="grad_fellow"
pid_file="my.pid"
pid=$(cat ${pid_file} 2>/dev/null) && {
    grep ${app_name} /proc/${pid}/cmdline >/dev/null 2>&1 && {
        echo "kill ${pid}. You may need to wait for a moment before it exits gracefully."
        kill ${pid}
    } || not_running
} || not_running

while true
do
    grep ${app_name} /proc/${pid}/cmdline >/dev/null 2>&1 || stop_success
    sleep 1
done
