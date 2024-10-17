from django.urls import path
from . import views

urlpatterns=[
    path('AddeventDetails',views.AddeventDetails,name='AddeventDetails'),
    path('enter_product_details/<int:event_id>/', views.enterProductDetails, name='enter_product_details'),
    path('event_selection_view',views.event_selection_view,name='event_selection_view'),
    path('return_product_views',views.return_product_views,name='return_product_views'),
    path('return-product/<int:event_id>/',views.return_product_to_office, name='return_product_to_office'),
     path('temporaryaddevent<int:event_id>/',views.temporaryaddevent, name='temporaryaddevent'),
    path('event_views',views.event_views,name='event_views'),
    path('event_views_active',views.event_views_active,name='event_views_active'),
    path('event_selection_all',views.event_selection_all,name='event_selection_all'),
    path('export-excel', views.export_excel, name='export_excel'),
    path('remark_note/<int:event_id>/',views.remark_note,name='remark_note'),

]