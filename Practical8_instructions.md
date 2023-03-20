# Neural Networks in Scikit-Learn and NumPy

__Setup__

Practical 8 runs on EIDF, and uses two IPython Notebooks - `Practical8a.ipynb` and `Practical8b.ipynb`.

You will need:

Your EIDF login from [EIDF Portal](https://portal.eidf.ac.uk/), and a port forward for Jupyter Lab, e.g.:

On Mac/Linux, Windows (with WSL or cygwin):

`ssh -J <username>@eidf-gateway.epcc.ed.ac.uk -L 8000:10.1.0.221:80 <username>@10.24.2.245`

Open browser and go to `127.0.0.1:8000`

On Windows (with MobaXTerm):

SSH Tunnel:
```
<Forwarded port> = 2222
<SSH server> = eidf-gateway.epcc.ed.ac.uk
<Username> = <USERNAME>
<SSH port> = 22
<Remote server> = 10.24.2.245
<Remote port> = 22
```

Port Forward:
```
<Forwarded port> = 8000
<SSH server> = 127.0.0.1
<Username> = <USERNAME>
<SSH port> = 2222
<Remote server> = 10.1.0.221
<Remote port> = 80
```
