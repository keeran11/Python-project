from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django.forms import modelformset_factory


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    # profile_picture = models.ImageField(upload_to="staff_img/%Y/%m/%d",
    #                           default='image/staff.png', verbose_name='Own Picture',
    #                           null=True, blank=True,
    #                           width_field="width_field",
    #                           height_field='height_field')
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to="staff_img", default='image/staff.png', verbose_name='Own Picture')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=False, blank=True)
    last_name = models.CharField(max_length=50)
    contact_number = models.IntegerField()
    address = models.CharField(max_length=200)
    email_address = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, editable=False)

    class Meta:
        ordering = ["-staff_id"]
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff Information'
        ordering = ['first_name', 'middle_name', 'last_name']
        permissions = (('can_view_staff', "Can view staff"), ('can_view_staff_details', 'Can view staff detail'))

    def __str__(self):
        return '({0}) {1} {2}'.format(self.staff_id, self.first_name, self.last_name)

    def get_absulate_url(self):
        return reverse('myapp:StaffEdit', args=[self.staff_id])


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    slug = models.SlugField()
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    middle_name = models.CharField(max_length=50, verbose_name="Middle Name", null=False, blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    contact_number = models.IntegerField(verbose_name="Contact Number")
    address = models.CharField(max_length=200, verbose_name="Address")
    email_address = models.EmailField(null=True, blank=True, verbose_name="Email Address")

    class Meta:
        ordering = ['-customer_id']
        verbose_name = "Customer"
        verbose_name_plural = "Customer Information"
        permissions = (('can_view_customer', 'Can view customer'),)

    # def get_absulate_url(self):
    #     return reverse("myapp:post_details", kwargs={"slug": self.slug})

    def __str__(self):
        return '({0} {1} {2})'.format(self.customer_id, self.first_name, self.last_name)

    def my_property(self):
        return self.first_name + ' ' + self.last_name

    my_property.short_description = "Full name of the Person"
    my_property.admin_order_field = 'last_name'
    full_name = property(my_property)


# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.customer_id)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Customer.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug
#
#
# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)
#
#
# pre_save.connect(pre_save_post_receiver, sender=Customer)


############ This is models for reservations ##################
class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    # slug = models.SlugField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Customer Name')
    staff = models.ForeignKey(Staff, on_delete=models.CharField, editable=False, verbose_name='Staff Name', null=True)
    no_of_adults = models.PositiveIntegerField(default=1, verbose_name='Number of Adult Member')
    no_of_childrens = models.PositiveIntegerField(default=0, verbose_name='Number of Children')
    reservation_date_time = models.DateTimeField(default=timezone.now, verbose_name='Reservation Date Time')
    expected_arrival_date_time = models.DateTimeField(default=timezone.now, verbose_name='Expected Arrival Date Time')
    expected_departure_date_time = models.DateTimeField(default=timezone.now, verbose_name='Expected Departure Date '
                                                                                           'Time')

    class Meta:
        ordering = ["-reservation_id"]
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservation Information'
        permissions = (('can_view_reservation', 'Can View Reservation'),
                       ('can_view_reservations_default', 'Can view reservation default'),
                       )

    def __str__(self):
        return '({0}) {1}'.format(self.reservation_id, self.customer)

    def colored_name(self):
        return format_html(
            '<span style= "color: #{};"{} {}</span>>',
            self.customer,
            self.no_of_adults,
            self.no_of_childrens,

        )

    def customer_first_name(self, obj):
        return obj.customer.first_name


# def create_slug_for_reservation(instance, new_slug=None):
#     slug = slugify(instance.customer_first_name)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Reservation.objects.filter(slug=slug)
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug_for_reservation(instance, new_slug=new_slug)
#     return slug
#
#
# def pre_save_post_receiver_for_reservation(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug_for_reservation(instance)
#
#
# pre_save.connect(pre_save_post_receiver_for_reservation, sender=Reservation)


class Facility(models.Model):
    name = models.CharField(max_length=12, verbose_name='Facility Name')
    price = models.PositiveIntegerField(verbose_name='Facility Price')

    def __str__(self):
        return '({0}) {1}'.format(self.name, self.price)

    class Meta:
        ordering = ['-id', '-price']
        verbose_name = 'Facility'
        verbose_name_plural = 'All Facility Information'

################## Room Details Informations ########################
class RoomTypeName(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RoomCatagory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RoomType(models.Model):
    PetType = (
        ('true', 'true'),
        ('false', 'false'),
        )
    
    room_type_id = models.AutoField(primary_key=True) 
    name = models.ForeignKey(RoomTypeName, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(RoomCatagory, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField()
    price = models.PositiveIntegerField(verbose_name='Room Price')
    size = models.CharField(max_length=1000, verbose_name='Room Size')
    capacity = models.IntegerField(verbose_name='Capacity')
    pets = models.CharField(max_length=10, choices=PetType, blank=True, default='false')
    breakfast = models.CharField(blank=True, choices=PetType, max_length=10, default='false')
    features = models.CharField(blank=True, choices=PetType, max_length=10, default='false')
    description = models.TextField()
    extras = models.ManyToManyField(Facility)

    def __str__(self):
        return '({0}) {1}'.format(self.name.name, self.category.name)

    class Meta:
        ordering = ['name']
        verbose_name = "RoomType"
        verbose_name_plural = 'All Room Information'

    def my_property(self):
        return self.name.name + ' ' + self.category.name

    my_property.short_description = "Full Slug"
    my_property.admin_order_field = 'category'
    full_slug = property(my_property)

    def display_for_room_facility(self):
        return ', '.join([extras.name for extras in self.extras.all()])

    display_for_room_facility.short_description = 'All Room Facilities'


# def create_slug_for_roomtype(instance, new_slug=None):
#     slug = slugify(instance.name)
#     if new_slug is not None:
#         slug = new_slug
#         qs = RoomType.objects.filter(slug=slug)
#         exists = qs.exists()
#         if exists:
#             new_slug = "%s-%s" % (slug, qs.first().id)
#             return instance.create_slug_for_roomtype(instance, new_slug=new_slug)
#         return slug


# def pre_save_post_receiver_for_roomtypen(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = sender.create_slug_for_roomtype(instance)


# pre_save.connect(pre_save_post_receiver_for_roomtypen, sender=RoomType)


class RoomImage(models.Model):
    room = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room_img/%Y/%m/%d",
                              verbose_name='Room Picture',
                              null=True, blank=True,
                              width_field="width_field",
                              height_field='height_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)


#################################################################################


class Room(models.Model):
    room_no = models.CharField(max_length=10, unique=True, verbose_name='Room Number')
    # slug = models.SlugField()
    room_type = models.ForeignKey(RoomType, null=False, blank=True, on_delete=models.CASCADE, verbose_name='Room Type')
    availability = models.BooleanField(default=0)
    reservation = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.SET_NULL,
                                    verbose_name='Reservation Information')
    facility = models.ManyToManyField(Facility)

    class Meta:
        ordering = ['room_no']
        verbose_name = 'Room'
        verbose_name_plural = 'Room'
        permissions = (('can_view_room', 'Can View Room'),)

    def __str__(self):
        return "%s - %s - Rs. %i - %s" % (self.room_no, self.room_type.name, self.room_type.price, self.facility.name)

    def display_for_facility(self):
        return ', '.join([facility.name for facility in self.facility.all()])

    display_for_facility.short_description = 'All Facilities'

    def get_absulate_url(self):
        return reverse('myapp:RoomDetailView', args=[self.room_no])

    def save(self, *args, **kwargs):
        if self.reservation:
            self.availability = 0

        else:
            self.availability = 1

        super().save(*args, **kwargs)


# ###### slug create for room #####
# def create_slug_for_room(instance, new_slug=None):
#     slug = slugify(instance.room_no)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Room.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug_for_room(instance, new_slug=new_slug)
#     return slug
#
#
# def pre_save_post_receiver_for_room(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug_for_room(instance)
#
#
# pre_save.connect(pre_save_post_receiver_for_room, sender=Room)
