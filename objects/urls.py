from django.urls import path
import objects.views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('objects/', views.ObjectList.as_view()),
    path('objects/<int:id>/', views.ObjectDetail.as_view(), name='object-retrieve'),
    path('objects/<int:id>/update/', views.ObjectUpdate.as_view(), name='object-update'),
    path('objects/<int:id>/delete/', views.ObjectDestroy.as_view(), name='object-destroy'),
    path('required-object-inventory/', views.RequiredObjectInventoryList.as_view()),
    path('required-object-inventory/object/<int:object_id>/', views.RequiredObjectInventoryListByObjectId.as_view(), name='required-object-inventory-by-object-id'),
    path('required-object-inventory/create-several/', views.add_required_object_inventories, name='add-several-required-object-inventories'),
    path('required-object-inventory/<int:id>/', views.RequiredObjectInventoryDetail.as_view(), name='required-object-inventory-retrieve'),
    path('required-object-inventory/<int:id>/update/', views.RequiredObjectInventoryUpdate.as_view(), name='required-object-inventory-update'),
    path('required-object-inventory/<int:id>/delete/', views.RequiredObjectInventoryDestroy.as_view(), name='required-object-inventory-destroy'),


    path('objects/image/<str:filename>/', views.view_that_serves_photo, name='photo_view'),
    path('objects/image/<int:object_id>/file/', views.get_object_image, name='object-file-retrieve'),
    path('objects/upload_image/', views.ObjectImageUploadView.as_view(), name='object-image-upload'),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)