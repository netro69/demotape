from django.views.generic import ListView, DetailView
from .models import Band


class BandListView(ListView):
    model = Band
    template_name = 'music/band_list.html'
    context_object_name = 'bands'
    paginate_by = 24


class BandDetailView(DetailView):
    model = Band
    template_name = 'music/band_detail.html'
    context_object_name = 'band'
    slug_url_kwarg = 'slug'
