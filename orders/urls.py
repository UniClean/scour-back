from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import orders.views as views

urlpatterns = [
    path('orders/', views.OrderList.as_view()),
    path('orders/<int:id>/', views.OrderDetail.as_view(), name='order_detail'),
    path('orders/<int:id>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('orders/<int:id>/delete/', views.OrderDestroy.as_view(), name='order-destroy'),
    path('orders/<int:order_id>/start/', views.start_order, name='order-start'),
    path('orders/<int:order_id>/complete/', views.complete_order, name='order-complete'),
    path('orders/<int:order_id>/confirm/', views.confirm_order, name='order-confirm'),
    path('orders/<int:order_id>/decline/', views.decline_order, name='order-decline'),
    path('orders/<int:order_id>/assign-employees/', views.assign_employees_to_order, name='order-assign-employees'),
    path('orders/<int:order_id>/assigned_employees', views.OrderEmployeeList.as_view(), name='order_employee'),
    path('orders/<int:order_id>/update-supervisor-comments/', views.update_supervisor_comments, name='order-assign-vehicles'),
    path('orders/status/<str:status>/', views.OrderListByStatus.as_view(), name='order_list_by_status'),

    path('orders/attachment/<int:attachment_id>/file/', views.get_order_attachment, name='object-file-retrieve'),
    path('orders/upload_attachment/', views.OrderAttachmentsUploadView.as_view(), name='object-image-upload'),

    path('orders/attachment_evidence/<int:attachment_evidence_id>/file/', views.get_order_attachment_evidence, name='object-file-retrieve'),
    path('orders/upload_attachment_evidence/', views.OrderAttachmentEvidencesUploadView.as_view(), name='object-image-upload'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)