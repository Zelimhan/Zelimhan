from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from properties.models import GROZNY, Property


DEMO_PROPERTIES = [
    {
        'title': '2-комн. у Мечети «Сердце Чечни»',
        'deal_type': Property.DealType.SALE,
        'property_type': Property.PropertyType.APARTMENT,
        'price': Decimal('6200000'),
        'area': Decimal('58.0'),
        'rooms': 2,
        'floor': 7,
        'floors_total': 12,
        'district': 'Ахматовский',
        'address': 'пр. А.А. Кадырова, 18',
        'description': 'Светлая квартира в Грозном, рядом парк и инфраструктура района.',
    },
    {
        'title': 'Студия в центре Грозного',
        'deal_type': Property.DealType.RENT,
        'property_type': Property.PropertyType.APARTMENT,
        'price': Decimal('35000'),
        'area': Decimal('32.0'),
        'rooms': 1,
        'floor': 4,
        'floors_total': 9,
        'district': 'Центр',
        'address': 'ул. Мира, 7',
        'description': 'Сдаётся на длительный срок, мебель и техника включены.',
    },
    {
        'title': 'Дом с участком в Новых Алдах',
        'deal_type': Property.DealType.SALE,
        'property_type': Property.PropertyType.HOUSE,
        'price': Decimal('14500000'),
        'area': Decimal('140.0'),
        'rooms': 4,
        'floor': 2,
        'floors_total': 2,
        'district': 'Новые Алды',
        'address': 'ул. Мамсурова, 24',
        'description': 'Семейный дом с двором, удобный выезд в центр города.',
    },
    {
        'title': 'Офис у пр. Путина',
        'deal_type': Property.DealType.RENT,
        'property_type': Property.PropertyType.COMMERCIAL,
        'price': Decimal('95000'),
        'area': Decimal('72.0'),
        'rooms': None,
        'floor': 2,
        'floors_total': 6,
        'district': 'Центр',
        'address': 'пр. В.В. Путина, 15',
        'description': 'Коммерческое помещение для офиса или шоурума в Грозном.',
    },
    {
        'title': '3-комн. в ЖК «Первый»',
        'deal_type': Property.DealType.SALE,
        'property_type': Property.PropertyType.APARTMENT,
        'price': Decimal('7355250'),
        'area': Decimal('70.1'),
        'rooms': 3,
        'floor': 5,
        'floors_total': 12,
        'district': 'Шейх-Мансуровский',
        'address': 'ул. Фасадная, 5',
        'description': 'Просторная квартира в современном жилом комплексе Грозного.',
    },
    {
        'title': 'Таунхаус у Грозного моря',
        'deal_type': Property.DealType.SALE,
        'property_type': Property.PropertyType.TOWNHOUSE,
        'price': Decimal('9800000'),
        'area': Decimal('110.0'),
        'rooms': 3,
        'floor': 2,
        'floors_total': 2,
        'district': 'Грозненский район',
        'address': 'пос. Пригородный, ул. Озёрная, 3',
        'description': 'Таунхаус рядом с зоной отдыха, для семьи или сдачи.',
    },
]


class Command(BaseCommand):
    help = 'Демо-риелтор и объекты только по Грозному'

    @transaction.atomic
    def handle(self, *args, **options):
        realtor, created = User.objects.get_or_create(
            username='realtor',
            defaults={
                'first_name': 'Зарема',
                'last_name': 'Алиева',
                'email': 'realtor@reeltor.example',
                'role': User.Role.REALTOR,
                'phone': '+7 (8712) 22-33-44',
            },
        )
        if created:
            realtor.set_password('realtor123')
            realtor.save()
            self.stdout.write(self.style.SUCCESS('Создан риелтор: realtor / realtor123'))
        else:
            self.stdout.write('Риелтор realtor уже есть')

        # Убираем старые демо-объекты других городов
        removed, _ = Property.objects.exclude(city=GROZNY).delete()
        if removed:
            self.stdout.write(f'Удалено объектов вне Грозного: {removed}')

        Property.objects.filter(city=GROZNY).update(city=GROZNY)

        created_count = 0
        for data in DEMO_PROPERTIES:
            obj, was_created = Property.objects.update_or_create(
                title=data['title'],
                address=data['address'],
                defaults={
                    **data,
                    'city': GROZNY,
                    'status': Property.Status.PUBLISHED,
                    'realtor': realtor,
                },
            )
            if was_created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Объектов в Грозном: {Property.objects.filter(city=GROZNY).count()} '
            f'(новых: {created_count})'
        ))
