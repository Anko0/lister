""" Sorting module 

Contains class Sort that contains following functions:
- sort_items_default: returns sorted user's not executed items by executed time
- sort_items_today: returns sorted user's items by today date
- sort_items_by_param: returns sorted user's items by parameter
- sort_types_popular: returns user's most popular types of items
- search_item: returns user's items that contains searched substring

"""


from datetime import datetime, timedelta

from django.db.models import Count

from .models import Item


types = dict(Item.TYPE)


class Sort():

    @staticmethod
    def sort_items_default(current_user):
        items = (Item.objects.filter(item_author = current_user, 
                                    item_isdone = "no")
                                    .order_by('item_executed'))
        return items
    
    @staticmethod
    def sort_items_today(current_user):
        now = datetime.now()
        items = (Item.objects.filter(item_author = current_user, 
                                    item_executed = now)
                                    .order_by('item_executed'))
        return items

    @staticmethod
    def sort_items_by_param(key, current_user):
        items_presort = (Item.objects.filter(item_author = current_user)
                                            .order_by('item_executed'))
        """ sort by types """
        if key in types:
            items = items_presort.filter(item_type = key)
        if key == 'title':
            items = items_presort.order_by('item_type')
        """ sort by dates """
        now = datetime.now()
        endm = now.replace(month = (int(now.month + 1) % 12))
        startnm = now.replace(day=1, month = (int(now.month + 1) % 12))
        endnm = now.replace(day=1, month = (int(now.month + 2) % 12))
        if key == 'before':
            items = items_presort.filter(item_executed__lt=(now))
        if key == 'after':
            items = items_presort.filter(item_executed__gte=(now))
        if key == 'month':
            items = items_presort.filter(item_executed__range=(now, endm))
        if key == 'nmonth':
            items = items_presort.filter(item_executed__range=(startnm, endnm))
        if key == 'week':
            endw = now + timedelta(days=6)
            items = items_presort.filter(item_executed__range=(now, endw))
        if key == 'nweek':
            today_iter = datetime.weekday(now)
            startnw = now + timedelta(days=(7 - today_iter))
            endnw = startnw  + timedelta(days=6)
            items = items_presort.filter(item_executed__range=(startnw, endnw))
        if key == 'bydate':
            items = items_presort
        if key == 'today':
            items = Sort.sort_items_today(current_user)
        """ sort by executing """
        if key == 'all':
            items = items_presort
        if key == 'done':
            items = items_presort.filter(item_isdone = "yes")
        
        return items

    @staticmethod
    def sort_types_popular(current_user):
        """ Most popular types of items for current user.

        Return most popular types with separator " - " between type and count
        and separator "; " between type and type 
        
        """
        popular_types_collector = []
        items = (Item.objects.filter(item_author = current_user).all()
                                    .values('item_type').annotate(total=
                                    Count('item_type')).order_by('-total'))
        for i in range(0, items.count()):
            if items[i].get('total') == items[0].get('total'):
                popular_types_collector.append("{} - {}".format(
                                                items[i].get('item_type'), 
                                                items[i].get('total')))
        return popular_types_collector

    @staticmethod
    def search_item(key, current_user):
        items_presort = (Item.objects.filter(item_author = current_user)
                                            .order_by('item_executed'))
        items = items_presort.filter(item_name__contains = key)
        return items
