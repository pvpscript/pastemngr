# pastemngr
A powerful pastebin manager for the command line

# Introduction
Paste manager (pastemngr) is a command line tool for pastebin.com. By consuming
the pastebin service API, this tool has the hability to create and retrieve
pastes from the command line as well as fetching information regarding users
and pastes (locally and online).

## Developer key
Since this application makes use of an API, a developer key is needed. The key
in question is provided by [pastebin.com](pastebin.com).
If the key is not present in the configurations, `pastemngr` won't work
at all.

## User key
This is another key used by the `pastebin` API, but this one is fetched by
the API itself and it's used to execute operations that are related to a
specific pastebin user.

For example, when posting a paste as a given user X, the API has to know its
user key, which will be provided in the **POST** payload.

# Instalation
You can install pastemngr through PyPI: `pip install pastemngr`

## Manual installation
This is the process for installing pastemngr from a clone.
```
git clone https://github.com/pvpscript/pastemngr
cd pastemngr
```

Then run,
`sudo make install`

Which is the same as
```
python setup.py install --record=install_log.txt --prefix=/usr/local
--root=/ --optimize=1
```

The installation log will be saved as `install_log.txt`

# Getting the developer key
There are two ways of getting this key and applying it to this program.
The first one is described below.

## First method (automatically fetching the key)
This method is the easiest, but it can be unreliable in some situations, since
it depends on html crawling, and sometimes the pastebin login page will ask
for a **captcha** resolution, so this might not work everytime.

To fetch the key and save it locally, simply run:
`pastemngr --fetch-dev-key`

## Second method (doing it manually)
This section is a guide through the process of inserting the developer
key manually into pastemngr's configuration. It's important to have this
solution at hand, since the automatic process is highly prone to failure.

1. Login to the [pastebin.com](https://www.pastebin.com) website;
2. Access the [api page](https://pastebin.com/api);
3. Look for a section called "**Your Unique Developer API Key**" as shown
by the image below;
![alt text][api-example]
4. In this section, there will be a text block containing a code
e.g. `b026324c6904b2a9cb4b88d6d61c81d1`. Copy the code found there;
5. Go to the configuration directory, discussed below, create a blank
file called `api_key` and paste the code found at the pastebin site;
6. Save the file.

[api-example]: https://i.imgur.com/ub52AWL.png "API key example"

# Configuration
The configuration directory is located under `$XDG_CONFIG_HOME/pastemngr/`
by default, or `$HOME/.config/pastemngr` if the first is undefined.

### dev\_key file
This file refers to the developer key used for executing operations on the
pastebin API.

### pastemngr.db file
This is an **automatically generated** database file that will keep local
informations, such as pastes info, pastes text and registered accounts with
user info, which includes the user key. 

# Usage
`pastemngr [OPTIONS] [<command>]`

## Options
`--fetch-dev-key`

Request a pastebin login, fetch the account's developer key and save  it
locally, at the config directory. This application needs a developer key to
access the pastebin API, otherwise it won't work.

## Commands
List of accepted commands. For more information about the options, refer to
`pastemngr(1)` manual page.

#### list\_users
`list_users [--raw]`

List registered users in the local database.

#### register
`register [-u USER] [--username USER]`

Register the given user in the local database. This will fetch the user key
associated with the given user name, and store it locally.

#### remove 
`remove [-u USER] [--username USER]`

Remove the given user from the local database.

#### user\_info
` user_info [-u USER] [--username USER] [--local] [--raw]`

Show informations about the given user.

#### new\_paste
`new_paste [--input-file FILE] [-u USER] [--username USER]  [--title TITLE]  [--format FMT] [--visibility N] [--expire TIME]`

Create a new paste and upload it to pastebin.

#### fetch\_paste
`fetch_paste [--paste-key KEY] [--local]`

Fetch the paste identified by the given key.

#### list\_pastes
`list_pastes [-u USER] [--username USER] [--local] [--raw]`

List pastes belonging to the given user.

#### delete\_paste
`delete_paste [-u USER] [--username USER] [--paste-key KEY] [--local]`

Remove the paste identified by the given key.

#### paste\_info
`paste_info [--paste-key KEY]`

Show informations about the paste identified by the given key.

#### remove\_expired
`remove_expired [-u USER] [--username USER]`

Remove  expired  pastes  from the local database for every registered user or
for the given user.

#### update\_db
`update_db [-u USER] [--username USER]`

Update the local database for every registered user or for the given user.
