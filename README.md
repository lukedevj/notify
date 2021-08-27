# Notify

Receive daily reports about your node directly from your email.

[![Donate](https://img.shields.io/badge/Donate-Bitcoin-green.svg)](https://coinos.io/lukedevj)

## Install

* Require `Python >= 3.6`
* Clone Repository 

```bash
$ cd notify/
$ python3 setup.py install --user
```

Verify it's installed:

```bash
$ notify --help
```

## Configuration

Configuring SMTP Client. 

```
$ notify "" --edit-config
```

Follow the tutorials if you use these E-MAIL providers [Gmail](https://support.google.com/mail/answer/7126229) or [Outlook](https://support.microsoft.com/en-us/office/pop-imap-and-smtp-settings-for-outlook-com-d088b986-291d-42b8-9564-9c414e2aa040). 

```bash
"email.smtp.host" = "smtp.gmail.com"
"email.smtp.port" = "465"
"email.smtp.user" = "user@gmail.com"
"email.smtp.pass" = "password"
"email.list" = ["to@gmail.com"]
```

> :warning: Not use an email and password that you use on a daily basis on the computer that this software can be hacked and the configuration file is in plain text, preferably create a new email.

## Testing Email Delivery

This command will take the result of the "whoami" command and send it as a message to the emails specified in the configuration file.

```bash
$ whoami | notify "Hello, %s" --subject="Hello?"
```

Check your email now.

Send a *"Good morning"* email if the time is in the range of **06:00** to **06:50**.

```bash
$ whoami | notify "Good Morning, %s" --subject "Let's wake up?" --exptime "range 06:00 in 06:50"
```

Send a email if the output of a command is non-zero.

```bash
$ python3 -c "print(5-5)" | notify "The Result is non-zero." --nonzero
```

## Using Crontab 

First let's create a bash script, so that crontab can run at a certain time.

```bash
$ which bos
$ which notify
$ nano ~/notify/report.sh
```
Let's use [BOS](https://github.com/alexbosworth/balanceofsatoshis) to generate a report about the node replace /path/bos and /path/notify with the path shown with the which command.

```bash
#!/bin/bash
/path/bos report --styled | /path/notify "%s" --subject="Daily node update"
```

Now we are going to configure crontab but before that you should be familiar with it, [Google](https://www.google.com/search?q=using+crontab+on+linux) it to be more familiar.

```bash
$ crontab -e
```
We are configuring the crontab so that when the time comes to **23:59** it executes the script in bash specified.
```bash
# m h  dom mon dow   command
59 23 * * * /bin/bash ~/notify/report.sh
```
Thanks for this tool your contribution will be welcome :)
