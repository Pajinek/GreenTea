#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Pavel Studenik
# email: pstudeni@redhat.com
# created: 24.1.2014

import logging

from django.core.management.base import BaseCommand

from apps.taskomatic.models import Taskomatic


class Command(BaseCommand):
    help = ('Automatization for running task')
    requires_system_checks = True
    can_import_settings = True

    def handle(self, *args, **kwargs):
        taskoMatic = Taskomatic()
        taskoMatic.run()
