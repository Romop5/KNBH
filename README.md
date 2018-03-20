# Dormitory Girl Hunter

## © tammar96 & europ & xbolva00

## Description

Define woman as a person with surname ending with `á`. The script searches persons on the specified floor and block defined by user via parameters. Women are displayed with red bold color.

## Usage

1. Install python3.6

    ```sh
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt update
    sudo apt install python3.6
    ```

2. Run

    ```sh
    python3.6 main.py [OPTIONS]
    ```

    OPTIONS:

        Help:
            -h
            --help

        Floor:
            -f=NUMBER
            --floor=NUMBER

        Block:
            -b=BLOCK
            --block=BLOCK

        Ping room:
            -p
            --ping

        Room:
            -r
            --room=ROOM

        Girls only:
            -g
            --girls
