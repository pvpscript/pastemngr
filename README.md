# pastemngr
A powerful pastebin manager for the command line

TODO:
Revise developer key explanation; Revise devkey vs userkey explanation; Add prints to this readme.

Create setup.py [DONE]; Make it install dependencies automatically [DONE];

Finish the argparse help [DONE]; Use os.path to build paths in the config.py file [DONE];


# Introduction
Paste manager (pastemngr) is a command line tool for pastebin.com. By consuming
the pastebin service API, this tool has the hability to create and retrieve
pastes from the command line as well as fetching information regarding users
and pastes (locally and online).

# Developer key
It's very relevant to emphasize the importance of the developer key, since this
application uses the API provided by pastebin.com.

Their API requires a developer key, therefore, every operation that is
executed by it needs this key as a parameter, or it won't work at all.

## Developer Key vs User Key
The API provided by pastebin make use of two types of keys, the **developer key**
and the **user key**.

The first will be the _master key_, the one that will allow this application to
execute any of the possible operations provided by the API, meaning that
this key is only responsible for providing access. That's all.

The latter, is the key that will be used for user specific operations, such
as posting pastes associated with an account or fetching user informations,
such as account details or pastes owned by an account. For example, when a
paste is associated with a user, this key comes into place making it's
owner the author of the posted paste. Also, when running an operation to fetch
data from a user, this key tells the API which user the application is
fetching information from.

## Getting the developer key
There are two ways of getting this key and applying it to this program.
The first one is described below.

### First method (automatically fetching the key)
This method is the easiest, but it can be unreliable in some situations, since
it depends on html crawling, if the pastebin site's is changed, this might
not work.

To fetch the key and save it locally, simply run:
`pastemngr --fetch-dev-key`

### Second method (doing it manually)
This section is a guide through the process of inserting the developer
key meanually into this app's configuration. It's important to have this
solution at hand, since the first one is prone to failure.

1. Login to the [pastebin.com](https://www.pastebin.com) website;
2. Access the [api page](https://pastebin.com/api);
3. Look for a section called "**Your Unique Developer API Key**";
4. In this section, there will be a text block containing a code
such as `b026324c6904b2a9cb4b88d6d61c81d1`. Copy the code found there;
5. Go to the configuration folder, discussed below, and create a blank
file called `api_key` and paste the code found at the pastebin site;
6. Save the file.

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

## Usage
`pastemngr [OPTIONS] [<command>]`

## Options
`--list-users`

List registered users in the local database.

`--fetch-dev-key`

Request a pastebin login, fetch the account's developer key and save  it
locally, at the config folder. This application needs a developer key to
access the pastebin API, otherwise it won't work.

## Commands
List of accepted commands. To information about the options, refer to
`pastemngr(1)` manual page.

#### register
`register [-u USER] [--username USER]`

Register the given user in the local database.

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

# Instalation
How to install this application
