# Time 2 Study
A simple timer to track your learning time.

## Features
Turn tracking on:
```bash
t2s --on
```
Turn tracking off:
```bash
t2s --off
```
Stop the timer:
```bash
t2s --stop
```
Start the timer:
```bash
t2s --start
```
Turn off the timer and save notes about what you learned:
```bash
t2s --off --notes "I learned pointers in C"
```
Show your last recorded learning data:
```bash
t2s --last
```
Show your first recorded learning data:
```bash
t2s --first
```
Delete the stored learning data:
```bash
t2s --delete-all
```
Delete the last stored learning data:
```bash
t2s --delete-last
```
Show help and available shortcuts:
```bash
t2s --help
```

## Installation
Clone the repository and install the package:

```bash
git clone https://github.com/mknnnnnnn/time-2-study.git
cd time-2-study
python3 -m venv .venv
source .venv/bin/activate
pip3 install .
```

## Usage

Start the timer:
```bash
t2s --on
```