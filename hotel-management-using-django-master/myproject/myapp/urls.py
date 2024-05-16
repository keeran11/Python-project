from django.contrib.auth import views as auth_views
from django.urls import path
from .import views
app_name = 'myapp'
urlpatterns = [
    path('main_backend_page/', views.main_backend_page, name='main_backend_page'),

    # Room Add
    path('RoomAdd/', views.RoomAdd, name='RoomAdd'),

    # Room List View
    path('RoomListView/', views.RoomListView.as_view(), name='RoomListView'),

    # Room Search View
    path('room_serach/', views.room_serach, name='room_serach'),

    # Room Edit
    path('RoomEdit/<int:pk>/', views.RoomEdit.as_view(), name='RoomEdit'),

    # Room Detail View
    path('RoomListView/<str:pk>/', views.RoomDetailView.as_view(), name='RoomDetailView'),

    path('Reserve/', views.Reserve, name='Reserve'),
    # Reservation List
    path('reservation/', views.ReservationListView.as_view(), name='ReservationListView'),
    # Reservation Detail
    path('ReservationDetailView/<str:pk>/', views.ReservationDetailView.as_view(), name='ReservationDetailView'),


    path('reserve_success/', views.reserve_success, name='reserve_success'),

    # Customer Detail
    path('CustomerDetailView/<str:pk>/', views.CustomerDetailView.as_view(), name='CustomerDetailView'),

    # Staff List
    path('StaffList/', views.StaffList.as_view(), name='StaffList'),

    # Staff Details
    path('StaffDetailView/<str:pk>', views.StaffDetailView.as_view(), name='StaffDetailView'),

    # Staff Add
    path('AddStaff/', views.AddStaff, name='AddStaff'),

    # Staff Edit
    path('StaffEdit/<str:pk>/', views.StaffEdit, name='StaffEdit'),

    # Add Facility
    path('AddFacility/', views.AddFacility, name='AddFacility'),

    # Facility List
    path('FacilityList/', views.FacilityList.as_view(), name='FacilityList'),

    # Facility 
    path('FacilityEdit/<str:pk>/', views.FacilityEdit, name='FacilityEdit'),

    # Room Type List
    path('RoomTypeNameList/', views.RoomTypeNameList.as_view(), name='RoomTypeNameList'),

    # Room Type Detail
    path('RoomTypeDetail/<str:pk>/', views.RoomTypeDetail.as_view(), name='RoomTypeDetail'),

    # Add Room Type name
    path('AddRoomTypeName/', views.AddRoomTypeName, name='AddRoomTypeName'),

    # Edit Room Type name
    path('RoomTypeNameEdit/<str:pk>/', views.RoomTypeNameEdit, name='RoomTypeNameEdit'),


    # RoomType List
    path('RoomTypeList/', views.RoomTypeList.as_view(), name='RoomTypeList'),

    # Add Room Type
    path('AddRoomType/', views.AddRoomType, name='AddRoomType'),

    # Edit Room Type
    path('EditRoomType/<str:pk>/', views.EditRoomType, name='EditRoomType'),
    
    path('signup/', views.signup, name='signup'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]