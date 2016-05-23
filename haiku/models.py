from django.db import models
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class Haiku(models.Model):
    class Meta:
        verbose_name_plural = "haiku"

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    poem = models.TextField(help_text=mark_safe(_("""Haiku have three lines
defined by syllable counts
of five, seven, five.""")))

    def __unicode__(self):
        return self.poem

    def __str__(self):
        return unicode(self).encode('utf-8')

    def get_absolute_url(self):
        return reverse('haiku:view', kwargs=dict(pk=self.id))

    def get_grade_percent(self):
        grade = self.get_grade()
        return '{}%'.format(int(grade * 100))

    def get_grade(self):
        '''Give 33% for each non-empty line up to 3 lines, 0 points for over 3'''
        lines = filter(len, [line.strip() for line in self.poem.splitlines()])
        score = 1.0/3 * len(lines)
        if score > 1:
            score = 0.0
        return score


class HaikuForm(forms.ModelForm):
    class Meta:
        model = Haiku
        fields = ['poem']
