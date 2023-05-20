### ssh-switch
This tools switches ssh profiles

### examples of usage

Create profile "my_profile_name" based on current `id_rsa` and `id_rsa.pub` and switch to it:
```shell
./ssh-switch.py my_profile_name  --create 
```

Switch to profile "job"
```shell
./ssh-switch.py job
```

Show a current profile
```shell
./ssh-switch.py --current
```

Show a list of profiles
```shell
./ssh-switch.py --list
```

### usage:
ssh-switch \[-h\] \[--create\] \[--current\] \[--list\] **\[profile\]**  
  
switches system ssh profiles  
  
positional arguments:  
  **profile**     profile alias to switch  
  
optional arguments:  
  -**h**, --**help**  show this help message and exit  
  --**create**    creates profile based on current system id\_rsa and id\_rsa.pub and switches to it  
  --**current**   prints current profile  
  --**list**      prints list of profiles


### installation

```shell
chmod +x ssh-switch.py
sudo cp ssh-switch.py /usr/local/bin/ssh-switch
```