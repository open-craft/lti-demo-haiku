from django.views.generic import DetailView, ListView, CreateView, UpdateView, RedirectView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from haiku.models import Haiku, HaikuForm


class HaikuView(object):
    model = Haiku
    form_class = HaikuForm


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
