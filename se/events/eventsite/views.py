from django.shortcuts import render, redirect
from .models import Event
from django.http import JsonResponse
from django.db.models import Q
from .constants import CATEGORY_TAGS, NEIGHBORHOOD_TAGS
from collections import defaultdict
from .forms import EventForm

import datetime

def home(request):
    return render(request, 'eventsite/home.html')


def multi(request):
    return render(request, 'eventsite/multi.html')

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newmulti')  # Redirect to a success page or another view
    else:
        form = EventForm()

    return render(request, 'eventsite/add_event.html', {'form': form})


def newmulti(request):
    tag_fields = ['tag1', 'tag2', 'tag3']
    # categoryChoices = set()
    # for field_name in tag_fields:
    #     values = Event.objects.filter(**{field_name + '__isnull': False}).values_list(field_name, flat=True).distinct()
    #     display_names = [Event._meta.get_field(field_name)]
    #                      #.choices_dict.get(value) for value in values]
    #     print(display_names)
    #     categoryChoices.update(values)

    # field_name = 'neighborhood'
    # neighborhoodValues = Event.objects.filter(**{field_name + '__isnull': False}).values_list(field_name, flat=True).distinct()
    
    categoryChoices = [human for comp, human in CATEGORY_TAGS]
    neighborhoodValues = [human for comp, human in NEIGHBORHOOD_TAGS]

    
    return render(request, 'eventsite/newmulti.html', 
                  {'catetory_choices': CATEGORY_TAGS,
                   'neighborhood_choices': NEIGHBORHOOD_TAGS})


def update_data(request):

    # setup dicts based on constants
    neighborhood_dict = {k:v for k,v in NEIGHBORHOOD_TAGS}
    category_dict = {k:v for k,v in CATEGORY_TAGS}

    selected_choices = request.GET.getlist('selected_choices[]')
    neighborhood_choices = request.GET.getlist('neighborhood_choices[]')

    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    this_week = request.GET.get('this_week')
    this_weekend = request.GET.get('this_weekend')

    # Convert strings to boolean
    this_week = this_week.lower().strip() == "true"
    this_weekend = this_weekend.lower().strip() == "true"

    # get the dates of upcoming weekend and week
    current_date = datetime.date.today()
    current_day_of_week = current_date.weekday()
    if current_day_of_week in [4, 5, 6]:  # 4 = Friday, 5 = Saturday, 6 = Sunday
        friday_date = current_date - datetime.timedelta(days=current_day_of_week - 4)
    else:
        days_until_friday = 4 - current_day_of_week
        friday_date = current_date + datetime.timedelta(days=days_until_friday)

    sunday_date = friday_date + datetime.timedelta(days=2)
    last_day_of_week = current_date + datetime.timedelta(days=7)

    print(friday_date)
    print(sunday_date)
    print(last_day_of_week)

    # week 

    # convert dates 
    if fromDate: 
        from_date = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
    if toDate:
        to_date = datetime.datetime.strptime(toDate, '%Y-%m-%d')

    # Ensure selected_choices and neighborhood_choices are a list, not a string
    if not isinstance(selected_choices, list):
        selected_choices = [selected_choices]

    if not isinstance(neighborhood_choices, list):
        neighborhood_choices = [neighborhood_choices]

    items = Event.objects.all()

    # Filter data based on selected choices
    if selected_choices: 
        items = items.filter(Q(tag1__in=selected_choices) | 
                             Q(tag2__in=selected_choices) | 
                             Q(tag3__in=selected_choices))

    if neighborhood_choices: 
        items = items.filter(Q(neighborhood__in=neighborhood_choices))

    # Filter the events based on the date range filter
    if this_weekend: 
        date_range_filter = {}
        date_range_filter['start_day__gte'] = friday_date
        date_range_filter['end_day__lte'] = sunday_date
        items = items.filter(**date_range_filter)

    elif this_week: 
        date_range_filter = {}
        date_range_filter['start_day__gte'] = current_date
        date_range_filter['end_day__lte'] = last_day_of_week
        items = items.filter(**date_range_filter)

    elif fromDate or toDate: 
        date_range_filter = {}
        if fromDate:
            date_range_filter['start_day__gte'] = from_date
        if toDate:
            date_range_filter['end_day__lte'] = to_date
        items = items.filter(**date_range_filter)

    # Create HTML content to be returned to the client
    data_html = '<br>'

    for item in items:

        data_html += f"""
        <div class="styled-box">
        <h1>{item.name}</h1>
        <ul>
            <li><strong>Neighboorhood: </strong> {neighborhood_dict.get(item.neighborhood, 'None')}</li>
            <li><strong>Start Date:</strong> {item.start_day}</li>
            <li><strong>End Date:</strong> {item.end_day}</li>
            <li><strong>Start Time:</strong> {item.start_time}</li>
            <li><strong>End Time:</strong> {item.end_time}</li>
            <li><strong>Additional Info:</strong> {item.additional_info}</li>
            <li><strong>Event Categories:</strong>"""
        
        for tag in [{item.tag1}, {item.tag2}, {item.tag3}]:
            tag = next(iter(tag))
            if tag is not None and tag != "{None}": 
                data_html += "<li>" + category_dict.get(tag, "None") + "</li> "
        data_html += """</ul></div>"""
    
    if not items: 
        return JsonResponse({'data': "<h2> No Events Found </h2>"})

    return JsonResponse({'data': data_html})