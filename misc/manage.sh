#!/bin/bash

function start() {
    systemctl start mongod
    systemctl start rabbitmq-server
    systemctl start casm-web
    systemctl start casm-worker
    systemctl start casm-worker-github
    systemctl start casm-scheduler
    systemctl start nginx
}

function stop() {
    systemctl stop casm-web
    systemctl stop casm-worker
    systemctl stop casm-worker-github
    systemctl stop casm-scheduler
    systemctl stop nginx
    systemctl stop mongod
    systemctl stop rabbitmq-server
}


function status() {
    systemctl status casm-web
    systemctl status casm-worker
    systemctl status casm-worker-github
    systemctl status casm-scheduler
    systemctl status nginx
    systemctl status mongod
    systemctl status rabbitmq-server
}

function disable() {
    systemctl disable mongod
    systemctl disable rabbitmq-server
    systemctl disable casm-web
    systemctl disable casm-worker
    systemctl disable casm-worker-github
    systemctl disable casm-scheduler
    systemctl disable nginx
}

function enable() {
    systemctl enable mongod
    systemctl enable rabbitmq-server
    systemctl enable casm-web
    systemctl enable casm-worker
    systemctl enable casm-worker-github
    systemctl enable casm-scheduler
    systemctl enable nginx
}

function showLog() {
    echo "------ nginx server log ------"
    journalctl -n 15 --no-pager -u nginx
    echo "------ mongod server log ------"
    journalctl -n 15 --no-pager -u mongod
    echo "------ rabbitmq-server server log ------"
    journalctl -n 15 --no-pager -u rabbitmq-server
    echo "------ casm-scheduler server log ------"
    journalctl -n 15 --no-pager -u casm-scheduler
    echo "------ casm-web server log ------"
    journalctl -n 15 --no-pager -u casm-web
    echo "------ casm-worker server log ------"
    journalctl -n 15 --no-pager -u casm-worker
    echo "------ casm-worker github server log ------"
    journalctl -n 15 --no-pager -u casm-worker-github
}

function help() {
    echo "CASM 服务管理"
    echo "Usage: manage.sh [ stop | start | status | restart | disable | enable | log ]"
}

function restart() {
    stop
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    disable)
        disable
        ;;
    enable)
        enable
        ;;
    log)
        showLog
        ;;
    help)
        help
        ;;
    *)
        help
        ;;
esac
exit 0