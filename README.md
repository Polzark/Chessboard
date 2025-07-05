# Setup
If you are using `WSL2 on Windows` or are working in a `virtual machine`, you can just

```
$ pip install chess
$ pip install RPi.GPIO
```
and you should be good to go. However, if you are using `macOS` or `Linux`, you will have to install the packages in a virtual machine.
To set it up, you can run these commands.

```
$ python3 -m venv .cheesevenv
$ source .cheesevenv/bin/activate
$ pip install chess
$ pip install RPi.GPIO
```

This should create a `.cheesevenv` folder that should resolve the module import issues.
<br>

To exit the virtual environment, you can use this command.

```
$ deactivate
```

Later on you can enter the virtual environment again by just running this command.

```
$ source .cheesevenv/bin/activate
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
