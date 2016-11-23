#!/bin/python
# -*- coding: utf-8 -*-

# Author: Pavel Studenik
# Email: pstudeni@redhat.com
# Date: 24.9.2013

import reversion
from django.contrib import admin
from django.core.urlresolvers import reverse

from models import (Arch, Author, CheckProgress, Distro, DistroTemplate, Event,
                    FileLog, Git, GroupOwner, GroupTaskTemplate, GroupTemplate,
                    GroupTestTemplate, Job, JobTemplate, PhaseLabel,
                    PhaseResult, Recipe, RecipeTemplate, System, Task,
                    TaskRoleEnum, TaskTemplate, Test, TestHistory)


class TemplateTaskInLine(admin.TabularInline):
    model = TaskTemplate
    raw_id_fields = ("test", )
    sortable_field_name = "priority"
    ordering = ["position", "priority"]
    extra = 0


class RecipeInLine(admin.TabularInline):
    model = Recipe
    extra = 0
    fields = ["get_recipe_link", "whiteboard", "status",
              "system", "arch", "distro", "result", "resultrate"]
    readonly_fields = ["get_recipe_link", "status",
                       "system", "arch", "distro", "result", "resultrate"]

    def get_recipe_link(self, obj):
        url = reverse('admin:core_recipe_change', args=(obj.pk,))
        return '<a href="%s">%s</a>' % (url, obj.uid)
    get_recipe_link.allow_tags = True


class RecipeTemplateInLineSmall(admin.TabularInline):
    model = RecipeTemplate
    extra = 0
    fields = ("get_recipe_link", "is_enabled", "name",
              "is_virtualguest", ("role", "arch"), "distro",)
    readonly_fields = ("get_recipe_link", "is_enabled", "arch")

    def is_enabled(self, obj):
        return obj.is_enabled()
    is_enabled.boolean = True

    def get_recipe_link(self, obj):
        url = reverse('admin:core_recipetemplate_change', args=(obj.pk,))
        return '<a href="%s">%s</a>' % (url, obj.id)
    get_recipe_link.allow_tags = True


class RecipeTemplateInLine(RecipeTemplateInLineSmall):
    fields = ("get_recipe_link", "name", "is_virtualguest",
              "role", "arch", "distro", "schedule")
    readonly_fields = ("get_recipe_link", )


class TaskInLine(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("uid", "test", "status",
              "result", "duration", "datestart", "alias")
    readonly_fields = fields


class DistroTemplateAdmin(reversion.VersionAdmin):
    list_display = ("name", "distroname",
                    "variant", "family", "tpljobs_counter")
    ordering = ("name",)
    inlines = [RecipeTemplateInLineSmall]


class JobAdmin(admin.ModelAdmin):
    list_display = ("uid", "template", "date", "is_running", )
    search_fields = ["uid", "template__whiteboard"]
    ordering = ["-date", "-is_running", ]
    inlines = [RecipeInLine]


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("uid", "get_job_link", "whiteboard", "get_template",
                    "get_system_link", "result", "status", "resultrate")
    search_fields = ["uid", "whiteboard"]
    raw_id_fields = ("job", "system", "distro", "parentrecipe")
    # readonly_fields = ("job", "system", "distro")
    inlines = [TaskInLine]

    def get_system_link(self, obj):
        url = reverse('admin:core_system_change', args=(obj.system_id,))
        return '<a href="%s">%s</a>' % (url, obj.system)
    get_system_link.allow_tags = True

    def get_job_link(self, obj):
        url = reverse('admin:core_job_change', args=(obj.job_id,))
        return '<a href="%s">%s</a>' % (url, obj.job)
    get_job_link.allow_tags = True


class TaskAdmin(admin.ModelAdmin):
    list_display = ("uid", "recipe", "test", "status",
                    "duration", "datestart", "result")
    search_fields = ["uid"]
    raw_id_fields = ("recipe", "test")


class TaskTemplateInLine(admin.TabularInline):
    model = TaskTemplate
    extra = 0
    fields = ("get_recipetemplate_link", "jobtemplate")
    readonly_fields = fields

    def get_queryset(self, request):
        qs = super(TaskTemplateInLine, self).get_queryset(request)
        return qs.filter(recipe__jobtemplate__is_enable=True)

    def jobtemplate(self, obj):
        return "%s" % obj.recipe.jobtemplate

    def get_recipetemplate_link(self, obj):
        url = reverse('admin:core_recipetemplate_change',
                      args=(obj.recipe.pk,))
        return '<a href="%s">%s</a>' % (url, obj.recipe.id)
    get_recipetemplate_link.allow_tags = True


class TestAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_enable")
    search_fields = ["name", "owner__email"]
    filter_horizontal = ["dependencies", "groups"]

    def ownerName(self, obj):
        return obj.owner.name

    def ownerEmail(self, obj):
        return obj.owner.email

    inlines = [TaskTemplateInLine]


class TestHistoryAdmin(admin.ModelAdmin):
    list_display = ("test", "author", "commit", "date")


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "is_enabled", "email")


class CheckProgressAdmin(admin.ModelAdmin):
    list_display = ("datestart", "dateend",
                    "percent", "totalsum", "get_duration")


class GitAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "localurl", "get_count")


class JobTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "whiteboard", "is_enable", "schedule", "get_tags", "position")

    def make_enable(modeladmin, request, queryset):
        queryset.update(is_enable=True)
    make_enable.short_description = "Set selected templates to enabled"

    def make_disable(modeladmin, request, queryset):
        queryset.update(is_enable=False)
    make_disable.short_description = "Set selected templates to disabled"

    def make_clone(modeladmin, request, queryset):
        for it in queryset:
            it.clone()
    make_clone.short_description = "Clone selected jobs"

    actions = [make_enable, make_disable, make_clone]

    # 'position' is the name of the model field which holds the position of an element
    list_editable = ('position',)
    list_filter = ["schedule", "is_enable"]
    search_fields = ["whiteboard", ]
    ordering = ["-is_enable", "schedule", "position"]
    inlines = [RecipeTemplateInLine]


class GroupTestInLine(admin.TabularInline):
    model = GroupTestTemplate
    extra = 0
    raw_id_fields = ("test", )
    sortable_field_name = "priority"
    ordering = ["priority"]


class GrupRecipeTemaplate(admin.TabularInline):
    model = GroupTaskTemplate
    fields = ("get_recipe_link", "recipe", "jobtemplate")
    readonly_fields = fields
    extra = 0

    def jobtemplate(self, obj):
        return obj.recipe.jobtemplate

    def get_recipe_link(self, obj):
        url = reverse('admin:core_recipetemplate_change',
                      args=(obj.recipe.pk,))
        return '<a href="%s">%s</a>' % (url, obj.recipe.id)
    get_recipe_link.allow_tags = True


class GroupTaskInLine(admin.TabularInline):
    model = GroupTaskTemplate
    extra = 0
    sortable_field_name = "priority"
    fields = ("get_group_link", "group", "params", "role", "priority",)
    readonly_fields = ("get_group_link", )

    def get_group_link(self, obj):
        url = reverse('admin:core_grouptemplate_change', args=(obj.group.pk,))
        return '<a href="%s">%s</a>' % (url, obj.group.id)
    get_group_link.allow_tags = True


class GroupTemplateAdmin(admin.ModelAdmin):
    search_fields = ["name", ]
    inlines = [GroupTestInLine, GrupRecipeTemaplate]

    def make_clone(modeladmin, request, queryset):
        for it in queryset:
            it.clone()

    make_clone.short_description = "Clone selected groups"
    actions = [make_clone, ]


class GroupOwnerAdmin(admin.ModelAdmin):
    filter_horizontal = ["owners", ]


class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "test", "recipe")


class RecipeTemplateAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "jobtemplate", "distro", "archs", "hvm")
    inlines = [GroupTaskInLine, TemplateTaskInLine]
    search_fields = ["name", "jobtemplate__whiteboard"]
    readonly_fields = ("get_jobtemplate_link", )
    fieldsets = (
        (None, {
            'fields': (('get_jobtemplate_link', 'jobtemplate'), 'name', ('distro', 'arch',), 'hvm', ('is_virtualguest', 'virtualhost'),
                       'role', 'memory', 'disk', 'hostname', 'packages', 'params',)
        }),
        ('Schdule plan', {
            'fields': ('schedule',),
        }),
        ('Kernel options', {
            'fields': ('kernel_options', 'kernel_options_post', 'ks_meta',),
        }),
    )

    def get_jobtemplate_link(self, obj):
        url = reverse('admin:core_jobtemplate_change',
                      args=(obj.jobtemplate.pk,))
        return '<a href="%s">%s</a>' % (url, obj.jobtemplate)
    get_jobtemplate_link.allow_tags = True

    def render_change_form(self, request, context, *args, **kwargs):
        if kwargs.get("obj", None):
            context['adminform'].form.fields['virtualhost'].queryset = RecipeTemplate.objects\
                .filter(jobtemplate=kwargs["obj"].jobtemplate, is_virtualguest=False)\
                .exclude(id=kwargs["obj"].id)
        return super(RecipeTemplateAdmin, self).render_change_form(
            request, context, args, kwargs)


class FileLogAdmin(admin.ModelAdmin):
    list_display = ("recipe", "task", "path", "created",
                    "is_downloaded", "is_indexed", "status_code")
    raw_id_fields = ("recipe", "task")


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "datestart", "dateend", "alert", "is_enabled")


admin.site.register(Job, JobAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(PhaseResult)
admin.site.register(PhaseLabel)
admin.site.register(Test, TestAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(System)
admin.site.register(Arch)
admin.site.register(Event, EventAdmin)
admin.site.register(Distro)
admin.site.register(Git, GitAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(TestHistory, TestHistoryAdmin)
admin.site.register(GroupOwner, GroupOwnerAdmin)
admin.site.register(TaskTemplate, TaskTemplateAdmin)
admin.site.register(TaskRoleEnum)
admin.site.register(FileLog, FileLogAdmin)
admin.site.register(JobTemplate, JobTemplateAdmin)
admin.site.register(GroupTemplate, GroupTemplateAdmin)
admin.site.register(RecipeTemplate, RecipeTemplateAdmin)
admin.site.register(DistroTemplate, DistroTemplateAdmin)
admin.site.register(CheckProgress, CheckProgressAdmin)
