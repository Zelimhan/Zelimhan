from django.conf import settings
from django.db import models
from django.urls import reverse


GROZNY = 'Грозный'


class Property(models.Model):
    class DealType(models.TextChoices):
        SALE = 'sale', 'Продажа'
        RENT = 'rent', 'Аренда'

    class PropertyType(models.TextChoices):
        APARTMENT = 'apartment', 'Квартира'
        HOUSE = 'house', 'Дом'
        TOWNHOUSE = 'townhouse', 'Таунхаус'
        COMMERCIAL = 'commercial', 'Коммерческая'
        LAND = 'land', 'Участок'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликован'
        RESERVED = 'reserved', 'Забронирован'
        SOLD = 'sold', 'Продан'
        ARCHIVED = 'archived', 'В архиве'

    title = models.CharField('Название', max_length=200)
    deal_type = models.CharField(
        'Тип сделки',
        max_length=10,
        choices=DealType.choices,
        default=DealType.SALE,
        db_index=True,
    )
    property_type = models.CharField(
        'Тип объекта',
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    price = models.DecimalField('Цена, ₽', max_digits=14, decimal_places=0)
    area = models.DecimalField('Площадь, м²', max_digits=10, decimal_places=1)
    rooms = models.PositiveSmallIntegerField('Комнат', null=True, blank=True)
    floor = models.PositiveSmallIntegerField('Этаж', null=True, blank=True)
    floors_total = models.PositiveSmallIntegerField('Этажей в доме', null=True, blank=True)
    city = models.CharField('Город', max_length=100, default=GROZNY, editable=False)
    district = models.CharField('Район', max_length=100, blank=True)
    address = models.CharField('Адрес', max_length=255)
    description = models.TextField('Описание', blank=True)
    photo = models.ImageField('Фото', upload_to='properties/%Y/%m/', blank=True)
    realtor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties',
        verbose_name='Риелтор',
        limit_choices_to={'role': 'realtor'},
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Объект недвижимости'
        verbose_name_plural = 'Объекты недвижимости'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.city = GROZNY
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})

    @property
    def price_label(self):
        if self.deal_type == self.DealType.RENT:
            return '₽/мес.'
        return '₽'


class SelectionRequest(models.Model):
    """Заявка на персональный подбор по Грозному."""

    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE = 'done', 'Закрыта'

    name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=32)
    email = models.EmailField('Email', blank=True)
    deal_type = models.CharField(
        'Тип сделки',
        max_length=10,
        choices=Property.DealType.choices,
        default=Property.DealType.SALE,
    )
    property_type = models.CharField(
        'Тип объекта',
        max_length=20,
        choices=Property.PropertyType.choices,
        blank=True,
    )
    city = models.CharField('Город', max_length=100, default=GROZNY, editable=False)
    district = models.CharField('Район Грозного', max_length=100, blank=True)
    budget_min = models.PositiveIntegerField('Бюджет от, ₽', null=True, blank=True)
    budget_max = models.PositiveIntegerField('Бюджет до, ₽', null=True, blank=True)
    rooms = models.PositiveSmallIntegerField('Комнат', null=True, blank=True)
    comment = models.TextField('Пожелания', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='selection_requests',
        verbose_name='Риелтор',
        limit_choices_to={'role': 'realtor'},
    )
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка на подбор'
        verbose_name_plural = 'Заявки на подбор'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.city = GROZNY
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} — {self.phone}'
