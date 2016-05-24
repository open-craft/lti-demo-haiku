from django.views.generic import DetailView, ListView, CreateView, UpdateView, RedirectView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from django_lti_tool_provider.signals import Signals
from django_lti_tool_provider.models import LtiUserData
from haiku.models import Haiku, HaikuForm


class HaikuView(object):
    model = Haiku
    form_class = HaikuForm
    custom_key = ''

    '''Send grade to LTI Consumer'''
    def send_grade(self, haiku):
        try:
            lti_data = LtiUserData.objects.get(user=self.request.user, custom_key=self.custom_key)
        except LtiUserData.DoesNotExist:
            lti_data = None

        if not lti_data:
            # We are running outside of an LTI context, so we don't need to send a grade.
            return
        if not lti_data.edx_lti_parameters.get('lis_outcome_service_url'):
            # edX didn't provide a callback URL for grading, so this is an unscored problem.
            return

        Signals.Grade.updated.send(
            __name__,
            user=self.request.user,
            custom_key=self.custom_key,
            grade=haiku.get_grade(),
        )


class ShowOrCreateHaikuView(HaikuView, RedirectView):
    permanent = False

    def get_redirect_url(self):
        haiku = Haiku.objects.filter(author_id=self.request.user.id).values_list('id', flat=True)
        if len(haiku) > 1:
            return reverse('haiku:list')
        if len(haiku) > 0:
            return reverse('haiku:view', kwargs=dict(pk=haiku[0]))
        else:
            return reverse('haiku:add')


class ShowHaikuView(HaikuView, DetailView):
    template_name = 'view.html'


class ListHaikuView(HaikuView, ListView):
    template_name = 'list.html'
    paginate_by = 12
    paginate_orphans = 2


class CreateHaikuView(HaikuView, CreateView):
    template_name = 'edit.html'

    '''Login required for all posts'''
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        return super(CreateHaikuView, self).post(*args, **kwargs)

    '''Set haiku.author to current user, and send grade'''
    def form_valid(self, form):
        form.instance.author = self.request.user
        self.send_grade(form.instance)
        return super(CreateHaikuView, self).form_valid(form)


class UpdateHaikuView(HaikuView, UpdateView):
    template_name = 'edit.html'

    '''Haiku may be edited only by the author'''
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        haiku = self.get_object()
        if not self.request.user == haiku.author:
            raise PermissionDenied
        return super(UpdateHaikuView, self).post(*args, **kwargs)

    '''Send updated grade'''
    def form_valid(self, form):
        self.send_grade(form.instance)
        return super(UpdateHaikuView, self).form_valid(form)
