from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from properties.models import Property


DEMO_PROPERTIES = [
    {
        'title': '2-комн. у парка',
        'deal_type': Property.DealType.SALE,
        'property_type': Property.PropertyType.APARTMENT,
        'price': Decimal('12500000'),
        'area': Decimal('58.0'),
        'rooms': 2,
        'floor': 7,
        'floors_total': 16,
        'city': 'Москва',
        'address': 'ул. Садовая, 12',
        'description': 'Светлая квартира с видом во двор, рядом парк и школа.',
    },
    {
        'title': 'Студия в центре',
        'deal_type': Property.DealType.RENT,
        'property_type': Property.PropertyType.APARTMENT,
        'price': Decimal('65000'),
        'area': Decimal('28.5'),
        'rooms': 1,
        'floor': 4,
        'floors_total': 9,
        'city': 'Москва',
        'address': 'пер. Камергерский, 3',
        'description': 'Сдаётся на длительный срок, мебель и техника включены.',
    },
    {
        'title': 'Дом с участком',
        'deal_type': Property.DealType.SALE,
        'property_type': Property.PropertyType.HOUSE,
        'price': Decimal('28900000'),
        'area': Decimal('160.0'),
        'rooms': 4,
        'floor': 2,
        'floors_total': 2,
        'city': 'Химки',
        'address': 'пос. Новогорск, ул. Лесная, 8',
        'description': 'Коттедж для семьи, участок 6 соток, гараж.',
    },
    {
        'title': 'Офис у метро',
        'deal_type': Property.DealType.RENT,
        'property_type': Property.PropertyType.COMMERCIAL,
        'price': Decimal('180000'),
        'area': Decimal('95.0'),
        'rooms': None,
        'floor': 3,
        'floors_total': 8,
        'city': 'Санкт-Петербург',
        'address': 'Невский пр., 100',
        'description': 'Открытое пространство, отдельный вход со двора.',
    },
    {
        'title': '3-комн. в Грозном',
        'deal_type': Property.DealType.SALE,
        'property_type': Property.PropertyType.APARTMENT,
        'price': Decimal('7355250'),
        'area': Decimal('70.1'),
        'rooms': 3,
        'floor': 5,
        'floors_total': 12,
        'city': 'Грозный',
        'address': 'пр. В.В. Путина, 15',
        'description': 'Пример объекта по региону — удобно проверить фильтр города.',
    },
]


class Command(BaseCommand):
    help = 'Создаёт демо-риелтора и опубликованные объекты для локального MVP'

    @transaction.atomic
    def handle(self, *args, **options):
        realtor, created = User.objects.get_or_create(
            username='realtor',
            defaults={
                'first_name': 'Анна',
                'last_name': 'Риелторова',
                'email': 'realtor@reeltor.example',
                'role': User.Role.REALTOR,
                'phone': '+7 (495) 111-22-33',
            },
        )
        if created:
            realtor.set_password('realtor123')
            realtor.save()
            self.stdout.write(self.style.SUCCESS('Создан риелтор: realtor / realtor123'))
        else:
            self.stdout.write('Риелтор realtor уже есть')

        created_count = 0
        for data in DEMO_PROPERTIES:
            obj, was_created = Property.objects.get_or_create(
                title=data['title'],
                city=data['city'],
                defaults={
                    **data,
                    'status': Property.Status.PUBLISHED,
                    'realtor': realtor,
                },
            )
            if was_created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Добавлено объектов: {created_count}'))
