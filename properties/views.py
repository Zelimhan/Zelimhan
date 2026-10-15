from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import SelectionRequestForm
from .models import Property


def _published_queryset():
    return Property.objects.filter(status=Property.Status.PUBLISHED)


def _apply_filters(qs, params):
    q = params.get('q', '').strip()
    deal_type = params.get('deal', '').strip()
    property_type = params.get('type', '').strip()
    city = params.get('city', '').strip()
    rooms = params.get('rooms', '').strip()
    price_min = params.get('price_min', '').strip()
    price_max = params.get('price_max', '').strip()
    area_min = params.get('area_min', '').strip()

    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(address__icontains=q)
            | Q(city__icontains=q)
            | Q(description__icontains=q)
        )
    if deal_type in dict(Property.DealType.choices):
        qs = qs.filter(deal_type=deal_type)
    if property_type in dict(Property.PropertyType.choices):
        qs = qs.filter(property_type=property_type)
    if city:
        qs = qs.filter(city__icontains=city)
    if rooms.isdigit():
        qs = qs.filter(rooms=int(rooms))
    if price_min.isdigit():
        qs = qs.filter(price__gte=int(price_min))
    if price_max.isdigit():
        qs = qs.filter(price__lte=int(price_max))
    if area_min:
        try:
            qs = qs.filter(area__gte=float(area_min.replace(',', '.')))
        except ValueError:
            pass

    return qs, {
        'q': q,
        'deal': deal_type,
        'type': property_type,
        'city': city,
        'rooms': rooms,
        'price_min': price_min,
        'price_max': price_max,
        'area_min': area_min,
    }


@require_GET
def home(request):
    latest = _published_queryset()[:6]
    sale_count = _published_queryset().filter(deal_type=Property.DealType.SALE).count()
    rent_count = _published_queryset().filter(deal_type=Property.DealType.RENT).count()
    return render(request, 'properties/home.html', {
        'latest_properties': latest,
        'property_types': Property.PropertyType.choices,
        'deal_types': Property.DealType.choices,
        'sale_count': sale_count,
        'rent_count': rent_count,
    })


@require_GET
def catalog(request):
    qs, filters = _apply_filters(_published_queryset(), request.GET)
    cities = (
        _published_queryset()
        .values_list('city', flat=True)
        .distinct()
        .order_by('city')
    )
    return render(request, 'properties/catalog.html', {
        'properties': qs,
        'property_types': Property.PropertyType.choices,
        'deal_types': Property.DealType.choices,
        'cities': cities,
        'filters': filters,
        'total': qs.count(),
    })


@require_GET
def property_detail(request, pk):
    prop = get_object_or_404(_published_queryset(), pk=pk)
    similar = (
        _published_queryset()
        .filter(property_type=prop.property_type, deal_type=prop.deal_type)
        .exclude(pk=prop.pk)[:3]
    )
    return render(request, 'properties/detail.html', {
        'property': prop,
        'similar': similar,
    })


@require_GET
def contacts(request):
    return render(request, 'properties/contacts.html')


@require_http_methods(['GET', 'POST'])
def selection(request):
    if request.method == 'POST':
        form = SelectionRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Заявка отправлена. Риелтор свяжется с вами и подготовит подборку.',
            )
            return redirect('selection_thanks')
    else:
        initial = {}
        if request.GET.get('deal') in dict(Property.DealType.choices):
            initial['deal_type'] = request.GET['deal']
        if request.GET.get('type') in dict(Property.PropertyType.choices):
            initial['property_type'] = request.GET['type']
        if request.GET.get('city'):
            initial['city'] = request.GET['city']
        form = SelectionRequestForm(initial=initial)

    return render(request, 'properties/selection.html', {
        'form': form,
    })


@require_GET
def selection_thanks(request):
    return render(request, 'properties/selection_thanks.html')
