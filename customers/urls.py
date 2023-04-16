from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import customers.views as views

urlpatterns = [
    path('customers/', views.CustomerList.as_view()),
    path('customers/<int:id>/', views.CustomerDetail.as_view(), name='customer-retrieve'),
    path('customers/<int:id>/update/', views.CustomerUpdate.as_view(), name='customer-update'),
    path('customers/<int:id>/delete/', views.CustomerDestroy.as_view(), name='customer-destroy'),
    path('customers/contract/<int:id>/', views.CustomerContractDetail.as_view(), name='customer-retrieve'),
    path('customers/contract/<int:id>/file/', views.get_contract_file_content, name='customer-file-retrieve'),
    path('customers/contracts/by-customer-id/<int:customer_id>/', views.ContractsByCustomerId.as_view(), name='contracts-list-by-customer-id'),
    path('customers/upload_contract_file/', views.CustomerContractUploadView.as_view(), name='customer-contract-upload'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)