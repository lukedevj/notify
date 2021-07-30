import smtplib
import click
import toml
import sys
import ssl
import os

from datetime import datetime, time

class Mail: 

    def __init__(self, 
            smtp_host: str, 
            smtp_port: int,
            smtp_user: str,
            smtp_pass: str
        ):
        self.smtp_host = str(smtp_host)
        self.smtp_port = int(smtp_port)
        self.smtp_user = str(smtp_user)
        self.smtp_pass = str(smtp_pass)
        
        self.smtp_email = (
            self.smtp_user + '@' + self.smtp_host[5:]
        )

    def sender(self, to_email: str, subject: str, body: str):
        message = 'Subject: %s\n' % (subject)
        message+= 'From: <%s>\n' % (self.smtp_email)
        message+= 'To: <%s>\n\n' % (to_email)
        message+= (body)

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            try:
                server.starttls(context=context)
                server.login(self.smtp_user, self.smtp_pass)
            except:
                click.echo('* [ERROR] Invalid username or password.')
                raise click.Abort()

            server.sendmail(
                self.smtp_email, to_email, message.encode('utf-8')
            )
            server.quit()

@click.command()
@click.argument('body')
@click.option('--subject', help='Subject line of message.')
@click.option('--nonzero', is_flag=True, help='Don\'t send notification if input is zero')
@click.option('--exptime', help='Don\'t send notification if the time wit less than expected time. Example: "range 14:46 in 14:50"')
@click.option('--edit-config', is_flag=True, help='Configure notify.')
def main(body: str, subject: str, nonzero: bool, exptime: str, edit_config: bool):
    '''
    Send notifications based on stdin.
    '''

    body = (body if type(body) == str else '')

    if (sys.stdin.isatty() == False):
        stdin = sys.stdin.read()[:-1]
        if (stdin == '0') and (nonzero == True):
            click.echo('* Software aborted on output of stdin is zero.')
            raise click.Abort()
        
        if '%s' in body:
            body = body % (stdin)
        else:
            body+= ' %s' % (stdin)

    subject = ('' if subject == None else subject)

    if isinstance(exptime, str):
        timestamp = datetime.now()
        if ('in' in exptime) and ('range' in exptime):
            exptime = exptime.replace('in', '')
            exptime = exptime.replace('range', '')[1:]
            exptime = exptime.split(' ')
            if len(exptime) == 3:
                exptime.remove('')
        else:
            exptime = [exptime.split(' ')[0]]
        
        if (exptime[0].count(':') == 1):
            exptime[0] = exptime[0].split(':')

        if (len(exptime) == 2) and (exptime[1].count(':') == 1):
            exptime[1] = exptime[1].split(':')

        x = [int(x) for x in exptime[0]]
        x = time(
            hour=x[0], minute=x[1]
        )

        if len(exptime) == 2:
            y = [int(y) for y in exptime[1]]
            y = time(
                hour=y[0], minute=y[1]
            )

            if not (timestamp.hour in list(range(x.hour, y.hour + 1))) or not (timestamp.minute <= y.minute):
                click.echo('* Software aborted because the of time expected is different')
                raise click.Abort()
        else:
            if not (timestamp.hour == x.hour) or not (timestamp.minute == x.minute):
                click.echo('* Software aborted because the of time expected is different')
                raise click.Abort()
    
    path = os.path.expanduser('~/.notify')
    if (os.path.exists(path) == False):
        os.mkdir(path)
    
    file = ('%s/.notify.toml' % (path))
    if (os.path.exists(file) == False):
        data = {
            'email.smtp.host': '', 'email.smtp.port': '', 
            'email.smtp.user': '', 'email.smtp.pass': '',
            'email.list': []
        }
        with open(file, 'w') as f:
            f.write(toml.dumps(data))

    with open(file, 'r') as f:
        conf = toml.loads(f.read())

    if (sys.stdin.isatty() == False) and (edit_config == True):
        click.echo('* [Alert] Please configure the software using only "--edit-config"')
        raise click.Abort()
    
    elif (conf['email.smtp.host'] == '') and (edit_config == False):
        click.echo('* [Alert] Please configure the software using only "--edit-config"')
        raise click.Abort()
    
    elif (sys.stdin.isatty() == True):
        if (edit_config == True):
            os.system('nano ~/.notify/.notify.toml')
            click.echo('* Please restart the software to apply the changes.')
            raise click.Abort()
        
    else:
        mail = Mail(
            smtp_host=conf['email.smtp.host'], 
            smtp_port=conf['email.smtp.port'],
            smtp_user=conf['email.smtp.user'],
            smtp_pass=conf['email.smtp.pass'] 
        )

        for email in conf['email.list']:
            mail.sender(
                to_email=email, subject=subject, body=body
            )
