FROM centos:7

WORKDIR /data/

RUN mkdir -p /data/greentea
ADD . /data/greentea/

# install packages
RUN curl https://beaker-project.org/yum/beaker-client-CentOS.repo -o /etc/yum.repos.d/beaker-client-CentOS.repo \
    && cat greentea/requirement/rpms-*.txt | xargs yum install -y \
    && yum clean all \
    && chmod 755 /data/ -R

# create enviroment
RUN useradd -ms /bin/bash greentea \
    && chown greentea:greentea -R greentea

RUN echo "root:GreenTea!" | chpasswd

# TODO: install and enable uwsgi for running project on production
# RUN dnf install uwsgi-plugin-common mod_proxy_uwsgi -y

USER greentea
ENV HOME /data/greentea

RUN virtualenv $HOME/env \
    && cd $HOME \
    && . env/bin/activate \
    && pip install -r $HOME/requirement/requirement.txt

# create default values for running service
RUN sh $HOME/bin/init-secretkey.sh > $HOME/tttt/settings/production.py
ENV DJANGO_SETTINGS_MODULE tttt.settings.production

RUN mkdir -p $HOME/tttt/static $HOME/storage \
    && . $HOME/env/bin/activate \
    && python $HOME/manage.py migrate --noinput \
    && python $HOME/manage.py collectstatic -c --noinput

# create first user
RUN . $HOME/env/bin/activate && \
    echo 'from django.contrib.sites.models import Site; site = Site.objects.create(domain="localhost", name="localhost"); site.save()' | python $HOME/manage.py shell && \
    echo 'from django.contrib.auth.models import User; User.objects.create_superuser("admin", "admin@example.com", "pass")' | python $HOME/manage.py shell

# install cron and enable cron
# it doesn't use for docker, only for real system
# RUN yum install crontabs -y && mv $HOME/tttt/conf/cron/greentea.cron /etc/cron.d/

EXPOSE 8000

CMD sh $HOME/bin/docker-run.sh
