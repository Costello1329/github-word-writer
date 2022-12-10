# Github word writer
Writes funny words straight inside your Github contribution chart table.


### Example:
![Funy word](demo.png)

### How to use:
+ Generate **empty** repository, copy it's url (use ssh or access token)
    + If you use ssh, then just paste ssh address as origin
    + If you use token, then use http auth: `https://login:token@github.com/login/repo.git`
+ Run script: `pip install -r src/requirements.txt && python3 src/main.py`
+ Paste word (you can check the list of allowed symbols in `src/alphabet.txt` folder)
+ Paste origin
+ Paste username and email (will be used to set up git config and apply commits, so you should make sure that login and email the same as your github account name and email address, otherwise contributions won't be counted)
