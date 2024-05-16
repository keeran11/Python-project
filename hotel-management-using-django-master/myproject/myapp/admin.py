from django.contrib import admin
from .models import *
from pagedown.widgets import AdminPagedownWidget

# Register your models here.

#### for staff #####
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'staff_id',
        'user',
        'first_name',
        'middle_name',
        'last_name',
        'contact_number',
        'address',
        'email_address',
    )

    search_fields = [
        'staff_id',
        'user',
        'first_name',
        'middle_name',
        'last_name',
        'contact_number',
        'address',
        'email_address',
    ]

    fieldsets = (
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
        ('Full Name', {
            'fields': ('first_name', 'middle_name', 'last_name')
        }),
        ('Contact Information', {
            'fields': (('contact_number', 'email_address'), 'address')
        })
    )



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer_id',
        'slug',
        'full_name',
        'contact_number',
        'address',
        'email_address',
    )
    list_display_links = ('full_name',)
    search_fields = [
        'customer_id',
        'slug',
        'first_name',
        'middle_name',
        'last_name',
        'contact_number',
        'address',
        'email_address',
    ]
    fieldsets = (
        ('Full Name', {
            'fields': ('first_name', 'middle_name', 'last_name')
        }),
        ('Contact Information', {
            'fields': (('contact_number', 'email_address'), 'address')
        })
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # date_hierarchy = 'reservation_date_time',

    list_display = (
        'reservation_id',

        'customer',
        'staff',
        'no_of_adults',
        'no_of_childrens',
        'reservation_date_time',
        'expected_arrival_date_time',
        'expected_departure_date_time',

    )
    search_fields = [
        'reservation_id',
        'customer',
        'staff',
        'reservation_date_time',
    ]
    list_display_links = ('reservation_id',)
    list_filter = ['customer', 'no_of_adults', 'no_of_childrens']

    # prepopulated_fields = {'slug': ('customer',)}

    # fieldsets = (
    #     ('Customer Information', {
    #         'fields': ('customer', 'no_of_adults', 'no_of_childrens')
    #     }),
    #
    #     ('Date Information', {
    #         'classes': ('collapse',),
    #         'fields': ('reservation_date_time', 'expected_arrival_date_time', 'expected_departure_date_time')
    #     })
    # )


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_display_links = ('name',)
    list_editable = ('price',)
    search_fields = ['name', ]
    ordering = ('name', 'price')
    list_filter = ('name', 'price')


class RoomImageAdmin(admin.TabularInline):
    model = RoomImage


class ImageAdminForSpecificRoom(admin.ModelAdmin):
    inlines = [RoomImageAdmin]
    formfield_overrides = {
    models.TextField: {'widget': AdminPagedownWidget },}
    list_display = (
        'name',
        'category',
        'slug',
        'price',
        'size',
        'capacity',
        'pets',
        'breakfast',
        'features',
        'display_for_room_facility',
        # 'description',
    )

    list_display_links = ('name',)
    list_editable = ('price', 'pets', 'breakfast')
    search_fields = ['name__name', 'category__name', 'pets', 'breakfast', 'slug']
    ordering = ('name', 'category', 'price')
    list_filter = ('name', 'price')
    # prepopulated_fields = {'slug': ('name', 'category',)}
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Room Type',
         {'fields': ('name', 'category', 'slug', 'price', 'description')
          }),
        ('Room Details Information', {
            'fields': ('size', 'capacity', 'pets', 'breakfast', 'features', 'extras')
        })
    )
    filter_horizontal = ('extras',)


admin.site.register(RoomType, ImageAdminForSpecificRoom)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_no',
        'room_type',
        'availability',
        'reservation',
        'display_for_facility',
    )
    list_filter = ('room_no', 'room_type', 'availability')
    list_display_links = ('room_no',)
    search_fields = [
        'room_no',
        'room_type',
        'reservation__customer__first_name',
        'reservation__customer__middle_name',
        'reservation__customer__last_name',
    ]
    fields = (('room_no', 'room_type'), 'reservation', 'facility')
    filter_horizontal = ('facility',)
    # change_list_template = 'Backend/room/room_list.html'

    admin.site.register(RoomTypeName)
    admin.site.register(RoomCatagory)
