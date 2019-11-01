# MultiExploit

useful under circumstances where exploits are repeatedly executed

* RHG (robot hacking game) hands-free contests
* AD (Attack/Defense) submit flags in rounds

> rules can be found  [here(RHG)](https://ctf-wiki.github.io/ctf-wiki/introduction/cgc-zh/) and [here(AD)](https://ctf-wiki.github.io/ctf-wiki/introduction/experience-zh/)

### Usage

#### 1. Configure `config.yml`

the default configuration is located at ./config.yml  
file structure:

```yaml
exploits:
  [script name]:
    target:
      - [group name]
target_groups:
  [group name]:
    - [target string passed to the script]
```

#### 2. Place the exploits under `./exp/`

the name of the exploits must be identical to the `[script name]` in your config file  
exploits must implement a function `attack(target)`  
for each appliable `[target string]`, the function will be receiving it unchanged

#### 3. Fire it up

`python[2/3] main.py`

TODO: cli arguments