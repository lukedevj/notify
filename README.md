# Notify

Receive daily reports.

[Buy me a coffee ☕︎](https://coinos.io/lukedev)

## Install
```shell
cd ~/ && git clone https://github.com/lukedevj/notify
python3 notify/setup.py install
```

## Configuration

```shell
notify --edit-config
```

open ~/.notify/.notify.toml
```toml
"email.smtp.host" = "smtp.mailtrap.io"
"email.smtp.port" = "2525"
"email.smtp.user" = "example"
"email.smtp.pass" = "example"
"email.list" = ["to@example.com"]
```

## Sending E-MAIL
Send a "Good morning!" email if the time is in the range of **06:00** to **06:50**
```shell
whoami | notify "Good Morning, %s!" --subject "Let's wake up?" --exptime "range 06:00 in 06:50"
```

## Crontab

Setting up crontab so that the software runs at a certain time.

```shell
sudo crontab -e
```

Running notification every 1 hour.
```shell
00 1   * * *   root    whoami | notify "Good Morning, %s!" --subject "Let's wake up?" --exptime "range 06:00 in 06:50"
```

