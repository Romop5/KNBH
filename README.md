# Dormitory Girl Hunter

## © tammar96 & europ

## Description

Define woman as a person with surname ending with "á" or "ová". The script searches throught the rooms defined by user via parameters. Women are displayed with bold red color.

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

        [
          [
            [-rf=A] Rooms from number A
            [-rf=B] Rooms to   number B
          ]
          or
          [
            [-fl=N] Rooms from floor N
          ]
        ]
        [-bl=X] Rooms from block X
        [-h]    Help

