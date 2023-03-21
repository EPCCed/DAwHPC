# Practical 9 - Deep Learning with PyTorch

__Setup__

Practical 9 runs on Cirrus, and uses two IPython Notebooks - `Practical9a.ipynb` and `Practical9b.ipynb`.

Please refer to the previous instructions for running practicals on Cirrus.

___Note to m22ext users:___
- _change any `m22oc` references to `m22ext` in the following_
- _where m22oc requires "-\<username\>" delete this: `m22oc-<username>` -> `m22ext`_

_Connection_
- Connect to Cirrus (Mac/Linux/Windows(with WSL)):

`ssh <username>@login.cirrus.ac.uk`

- Connect to Cirrus (Windows (with MobaXTerm)):

```
<SSH server> = login.cirrus.ac.uk
<Username> = <USERNAME>
<SSH port> = 22
```

_Port Forward_ - AFTER starting Jupyter Lab Sessions - see below
- Port forward from Cirrus (Mac/Linux/Windows(with WSL)):

`ssh <username>@login.cirrus.ac.uk -L 8991:<node>:8991`

- port forward from CIrrus (Windows (with MobaXTerm)):

```
<Forwarded port> = 8991
<SSH server> = login.cirrus.ac.uk
<Username> = <USERNAME>
<SSH port> = 22
<Remote server> = <node> e.g., r1i1n0
<Remote port> = 8991
```

__For Practical 9a__
- copy Practical9a.ipynb to your work folder:
    - `cp $WORK/../shared/DAwHPC/practicals/Practical9a.ipynb $WORK`
- use `srun` to request an interactive session on a __CPU__ node:
    - `srun --exclusive --nodes=1 --time=01:00:00 --partition=standard --qos=standard --account=m22oc-<username> --pty /usr/bin/bash`
- source bashrc_pytorch:
    - `source /work/m22oc/m22oc/shared/DAwHPC/bashrc_pytorch`
- load PyTorch __CPU__ module:
    - `module load module load pytorch/1.12.1`
- start Jupyter Lab session:
    - `jupyter lab --ip=0.0.0.0 --no-browser --port=8991`
- set up your port forwarding (see above):
    - to find your node, use `uname -n`
- open a browser and go to:
    - `127.0.0.1:8991`

__After completing Practical 9a__
- close your Jupyter Labs browser tab
- close your port forward
- in the terminal hit <kbd>Ctrl</kbd> + <kbd>C</kbd> then <kbd>Y</kbd> to end the Jupyter Labs session
- type `exit` to leave the __CPU__ node

__For Practical 9b__
- copy Practical9b.ipynb to your work folder:
    - `cp $WORK/../shared/DAwHPC/practicals/Practical9b.ipynb $WORK`
- use `srun` to request an interactive session on a __GPU__ node:
    - `srun --nodes=1 --partition=gpu --qos=gpu --gres=gpu:1 --time=01:00:00 --account=m22oc-<username> --pty /bin/bash`
- source bashrc_pytorch:
    - `source /work/m22oc/m22oc/shared/DAwHPC/bashrc_pytorch`
- load PyTorch __GPU__ module:
    - `module load module load pytorch/1.12.1-gpu`
- start Jupyter Lab session:
    - `jupyter lab --ip=0.0.0.0 --no-browser --port=8991`
- set up your port forwarding (see above):
    - to find your node, use `uname -n`
- open a browser and go to:
    - `127.0.0.1:8991`