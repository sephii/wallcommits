import os

from fabric.api import (local, cd, get, lcd, sudo, env, prefix, execute,
        put)

env.hosts = ['wallcommits.fankhauser.name']
env.site_user = 'wallcommits'
env.site_group = 'wwwcln'
env.install_dir = "/home/www/fankhauser.name/subdomains/wallcommits"

def push_tag(tag):
    local("git push -f origin %s" % tag)

def checkout_tag(tag):
    local("git checkout %s" % tag)

def update_remote_git(tag):
    with cd(os.path.join(env.install_dir, "wallcommits")):
        sudo("git fetch -t -p", user=env.site_user)
        sudo("git checkout %s" % tag, user=env.site_user)

def install_requirements():
    with cd(os.path.join(env.install_dir, "wallcommits")):
        with prefix("source bin/activate"):
            sudo("pip install -r requirements.txt", user=env.site_user)

def migrate_database():
    with cd(os.path.join(env.install_dir, "wallcommits")):
        with prefix("source bin/activate"):
            sudo("python manage.py syncdb", user=env.site_user)
            sudo("python manage.py migrate", user=env.site_user)

def install_static():
    with cd(os.path.join(env.install_dir, "wallcommits")):
        with prefix("source bin/activate"):
            sudo("python manage.py collectstatic --noinput", user=env.site_user)

def restart_apache():
    sudo("apache2ctl graceful")

def deploy(tag):
    push_tag(tag)
    update_remote_git(tag)
    install_requirements()
    install_static()
    migrate_database()
    restart_apache()
