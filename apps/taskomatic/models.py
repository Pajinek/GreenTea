# -*- coding: utf-8 -*-
# author: Pavel Studenik
# email: pstudeni@redhat.com
# created: 24.1.2014

# Author: Martin Korbel
# Email: mkorbel@redhat.com
# Date: 20.07.2014

import logging
import shlex
import sys
import time
import traceback
from cStringIO import StringIO
from datetime import datetime, timedelta

from croniter import croniter
from django.conf import settings
from django.core import management
from django.db import models
from django.db.models import Count, Max
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.core.utils.date_helpers import toLocalZone

# from single_process import single_process


logger = logging.getLogger(__name__)


class TaskPeriodList:

    @staticmethod
    def last_runs(history=0):
        filters = {}
        if history > 0:
            filters["date_create__lt"] = datetime.now() - timedelta(history)
        data = TaskPeriodSchedule.objects.values("period_id")\
            .filter(**filters)\
            .annotate(max_id=Max("id")).order_by("period")
        return data


class TaskPeriodSchedule(models.Model):
    title = models.CharField(max_length=64)
    period = models.ForeignKey("TaskPeriod", blank=True, null=True)
    date_create = models.DateTimeField(
        _('Date of create'),
        default=timezone.now)
    counter = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["period_id", "counter"]

    def __unicode__(self):
        return "[%d] %s" % (self.counter, self.title)

    def recount(self):
        self.counter = TaskPeriodSchedule.object.filter(
            period=self.period).count()
        self.save()

    def delete(self, *args, **kwargs):
        super(TaskPeriodSchedule, self).delete(*args, **kwargs)
        self.period.recount_all()


class TaskPeriod(models.Model):
    title = models.CharField(max_length=64)
    label = models.SlugField(max_length=64, unique=True,
                             help_text="Label must be same for command 'schedule --schedule-label [label]'")
    common = models.CharField(_("Command"), max_length=128,
                              help_text="All allowed <a href=\"https://github.com/SatelliteQE/GreenTea/wiki/Commands\">commands</a>. Example: \'beaker schedule --schedule-label daily\'")
    date_last = models.DateTimeField(
        _('Date of last run'),
        null=True,
        blank=True)
    is_enable = models.BooleanField(default=False)
    cron = models.CharField(max_length=64, default="*  *  *  *  *")
    position = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "title"]

    def get_previous_run(self):
        tasks = Task.objects.filter(period=self).order_by("-date_run")
        if len(tasks) > 0:
            return tasks[0].date_run
        return None

    def __unicode__(self):
        return self.title

    def createTask(self):
        res = self.common.split(' ', 1)
        command = res.pop(0)
        params = "" if len(res) == 0 else res.pop()
        task = Task.objects.create(title=self.title,
                                   common=command,
                                   common_params=params,
                                   status=Task.STATUS_ENUM_WAIT,
                                   period=self)
        return task

    def recount_all(self):
        tps = TaskPeriodSchedule.objects.filter(
            period=self).order_by("date_create")
        for key, it in enumerate(tps):
            it.counter = key
            it.save()

    def clean_empty(self):
        tps = TaskPeriodSchedule.objects.filter(
            period=self).order_by("date_create")
        for it in tps:
            count = it.job_set.all().count()
            if count == 0:
                it.delete()


class Task(models.Model):
    STATUS_ENUM_WAIT = 0
    STATUS_ENUM_INPROGRESS = 1
    STATUS_ENUM_DONE = 2
    STATUS_ENUM_ERROR = 3
    STATUS_ENUM = (
        (STATUS_ENUM_WAIT, "Waiting"),
        (STATUS_ENUM_INPROGRESS, "In progress"),
        (STATUS_ENUM_DONE, "Done"),
        (STATUS_ENUM_ERROR, "Error"),
    )
    # user = models.ForeignKey(User)
    title = models.CharField(max_length=64)
    common = models.CharField(max_length=128)
    common_params = models.TextField(_('Parameters'), blank=True)
    status = models.IntegerField(default=0, choices=STATUS_ENUM)
    exit_result = models.TextField(_('Result log'), blank=True)
    date_create = models.DateTimeField(
        _('Date of create'),
        default=timezone.now)
    date_run = models.DateTimeField(
        _('Date of pick up'),
        blank=True,
        null=True)
    time_long = models.FloatField(default=0.0)  # better set to NULL
    period = models.ForeignKey(TaskPeriod, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def get_time_long(self):
        t = timedelta(seconds=self.time_long)
        return str(t)

    def get_params(self):
        data = {}
        for it in self.common_params.split():
            key, value = it.strip().split("=")
            data[key] = value
        return data

    def run(self, errorHandler=None):
        t1 = timezone.now()
        self.status = self.STATUS_ENUM_INPROGRESS  # set status "in progress"
        self.date_run = t1
        self.save()
        params = [it.strip() for it in self.common_params.split()]

        # --- RUN --- #
        if errorHandler:
            errorHandler.flush()

        out = StringIO()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler = logging.StreamHandler(stream=out)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(handler)
        old = (sys.stdout, sys.stderr)
        sys.stdout = out
        sys.stderr = out
        try:
            params = shlex.split(self.common_params)
            management.call_command(
                self.common, *params, verbosity=3, stdout=out,
                interactive=False)
            self.exit_result += out.getvalue() + "\n"
            self.status = self.STATUS_ENUM_DONE  # set status "done"
            sys.stdout, sys.stderr = old
        except Exception as e:
            self.exit_result = traceback.format_exc()
            self.status = self.STATUS_ENUM_ERROR  # set status "error"
            logger.exception(e)
        finally:
            sys.stdout, sys.stderr = old
            logging.getLogger('').removeHandler(handler)
            out.close()
        # Get all errors from logger
        if errorHandler:
            for er in errorHandler.flush():
                self.exit_result += er.getMessage() + "\n"
        # --- END RUN --- #

        t0 = timezone.now()
        t2 = t0 - t1
        self.time_long = t2.seconds + t2.microseconds / 1000000.0
        self.save()


class Taskomatic:
    logHandler = None

    class ListBufferingHandler(logging.handlers.BufferingHandler):

        def shouldFlush(self, record):
            return False

        def flush(self):
            old = self.buffer
            self.buffer = list()
            return old

    def checkTaskPeriods(self):
        tPeriods = TaskPeriod.objects.filter(is_enable=True)
        for period in tPeriods:
            if not period.date_last:
                period.date_last = timezone.now()
                period.save()
            last_check = toLocalZone(period.date_last)
            citer = croniter(period.cron, last_check)
            next_date = citer.get_next()
            if next_date < time.time():
                period.createTask()
                period.date_last = timezone.now()
                period.save()

    def checkTasks(self):
        tasks = Task.objects.filter(status=Task.STATUS_ENUM_WAIT)
        self.logHandler = Taskomatic.ListBufferingHandler(0)
        self.logHandler.setLevel(logging.INFO)
        logger.addHandler(self.logHandler)

        for task in tasks:
            task.run(self.logHandler)

    def cleanOldTasks(self):
        # delete old tasks with status DONE, keep only last 300 tasks
        [it.delete() for it in Task.objects
            .filter(status=Task.STATUS_ENUM_DONE)
            .order_by("-date_run")[settings.MAX_TASKOMATIC_HISTORY:]]

    # @single_process
    def run(self):
        self.checkTaskPeriods()
        self.checkTasks()
        self.cleanOldTasks()
