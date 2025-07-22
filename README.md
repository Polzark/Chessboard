Hello hello helloo
gonna be writing about the Game class and Game_state stuff

The Game will store two different chessboards:

1. the one that is the same as the python-chess chessboard
   (the normal chessboard)

2. the one that updates after every VALID piece pick-up and put-down
   (now dubbed as the interim chessboard)

The game will also store all the lights attached to the chessboard and which ones
currently on.

Game State Stuff

there are three different game_states:

1. Pickup_state
   The player needs to pick up a piece of the same colour and all the possible
   moves for that piece is lit up on the chessboard. The game_state will then
   transition to putdown_state for the same colour. If a different coloured piece
   or a piece is put down, we transition to the error state (cuz that should not be happening)

   TLDR:

   1. pick up correct colour piece -> display legal moves -> putdown_state and update interim board
   2. do anything else -> error_state

2. Putdown_state
   The player needs to put down the same piece onto a different square that is
   included in the legal moves. Another piece of the opposite colour maybe picked up
   in the interim for piece capture. ONLY for castling can another piece of the
   same colour be picked up. After valid moves, turn off all the lights and transition
   to pickup_state for the opposite colour (maybe do some fancy shmancy stuff with
   the lights idk). Also, update the python-chess library and game chessboard.
   If ANY of the interim moves are invalid (i.e. piece placed on wrong tile, the
   captured piece is not a legal move) transition to the error_state.

   TLDR:

   1. Make valid moves to put down piece -> turn off lights -> pickup_state for
      opposite colour and update chessboard and interim board

   2. Make a mistake -> error_state

3. Error_state
   All lights go red (oh no). Only transition out of this state once the board
   returns to previous interim board. Go back to previous game_state and keep
   trucking along.

   TLDR: do you really need one

   blare red -> fix board -> go to prev state



# Setup
For best practices, you will have to install the packages in a virtual machine.
To set it up, you can run these commands.

```
$ cd ChessBoard/
$ python3 -m venv .cheesevirtualenv --system-site-packages
$ source .cheesevirtualenv/bin/activate
$ pip install chess
$ pip install RPi.GPIO
$ pip3 install rpi_ws281x adafruit-circuitpython-neopixel
$ pip install numpy
```

If you are on the Raspberry Pi 3 Model B V1.2, continue with:

```
$ pip3 install --upgrade adafruit-python-shell
$ wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
$ sudo -E env "PATH=$VIRTUAL_ENV/bin:$PATH" python3 raspi-blinka.py
```

If you are setting up just for the packages (not on a Raspberry Pi):

```
$ sudo apt-get install -y i2c-tools libgpiod-dev python3-libgpiod
$ pip install --upgrade adafruit-blinka
```

This should create a `.cheesevirtualenv` folder that should resolve the module import issues.
<br>

To exit the virtual environment, you can use this command.

```
$ deactivate
```

Later on you can enter the virtual environment again by just running this command.

```
$ source .cheesevirtualenv/bin/activate
```

## Why is this required?
This is to tackle the “Externally Managed Environment” error while using Pip3.

```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.12/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

For furthur reading, you can refer to: https://medium.com/@Po1s1n/tackling-the-externally-managed-environment-error-while-using-pip3-6d45b367c561

## Still have problems with your Python interpreter?
Select the correct interpreter:

- Type Ctrl+P (Quick Open)
- In there, select `> Python: Select Interpreter`
- Choose `Python 3.10.12 (.cheesevirtualenv) ./.cheesevirtualenv/bin/python`
