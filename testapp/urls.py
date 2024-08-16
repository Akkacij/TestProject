from django.urls import path
from .views import UniqueManufacturersView, ManufacturerView, ProductView, ContractView, CreditApplicationView

urlpatterns = [
    path('manufacturers/', ManufacturerView.as_view(), name='manufacturer_list_create'),
    path('manufacturers/<int:id>/', ManufacturerView.as_view(), name='manufacturer_detail'),
    path('unique-manufacturers/<int:contract_id>/', UniqueManufacturersView.as_view(), name='unique_manufacturers'),

    path('products/', ProductView.as_view(), name='product_list_create'),
    path('products/<int:id>/', ProductView.as_view(), name='product_detail'),

    path('contracts/', ContractView.as_view(), name='contract_list_create'),
    path('contracts/<int:id>/', ContractView.as_view(), name='contract_detail'),

    path('credit-applications/', CreditApplicationView.as_view(), name='credit_application_list_create'),
    path('credit-applications/<int:id>/', CreditApplicationView.as_view(), name='credit_application_detail'),
]