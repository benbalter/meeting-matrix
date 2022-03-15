# Meeting Matrix

*Visually counts down the time remaining in a meeting on an RGB LED Matrix using a Raspberry Pi.*

## What it does

A Raspberry Pi powered RGB LED Matrix to sit over your shoulder during virtual meetings and subtly count down the time remaining in a meeting to keep things on track. Specifically, it displays the number of minutes remaining (e.g., `5 minutes`) when:

* Half of the meeting has elapsed (for example, 30 minutes for an hour meeting, 15 minutes for a 30 minute meeting)
* Every 10 minutes when 50% of the meeting to 20 minutes are remaining
* Every 5 minutes when 20 minutes to 5 minutes are remaining
* Every minute for the last 5 minutes

## How it works

The Raspberry Pi connects to your Google Calendar to know when you're in a meeting and how much time is remaining. After that, the hardware/software interface consists of:

* Raspberry Pi (any 32 pin model would work)
* [Adafruit RGB Matrix Bonnet for Raspberry Pi](https://www.adafruit.com/product/3211)
* [RGB Matrix](https://www.adafruit.com/category/327) (any size)
* [Controlling RGB LED display with Raspberry Pi GPIO](https://github.com/hzeller/rpi-rgb-led-matrix)

This is my first Python project, so please be kind!
## Setup 

This repository contains an [Ansible Playbook](playbook.yml) which will build/install the necessary dependencies configure the Raspberry Pi with a single command:

1. Flash the 64 bit Raspian lite image to the Micro SD card, configuring wifi and your SSH key
2. Customize [`playbook.yml`](playbook.yml) and [`hosts.example.yml`](hosts.example.yml) (as `hosts.yml`)
3. Run `ansible-playbook playbook.yml --inventory hosts.yml`

## Authentication

You'll need to add a `credentials.json` file to the project directory, which contains your Google OAuth credentials as downloaded from the Cloud Console. 

You'll also need to authorize the app on device with a browser, and then copy the resulting `token.json` file to the project directory on your Raspberry Pi.

## Running

SSH into the device and run `python meeting_matrix.py`.

## License

The project is licensed under the GPLv2 license based on its dependency on [`hzeller/rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix).