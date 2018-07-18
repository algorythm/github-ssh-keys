# GitHub SSH Key Fetcher
 This Python program fetches public keys from GitHub and stores them in ~/.ssh/authorized_keys.

## Up and running

I personally always use a virtual environment when executing python programs:

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python github-sshkeys.py
```

or simply

```bash
./run.sh
```