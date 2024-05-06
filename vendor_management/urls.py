from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
#JWT Token for autherization
    path('token/', ObtainToken.as_view(), name='token_obtain'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
# Vendor Profile Management Endpoints
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/', VendorRetrieveUpdateDelete.as_view(), name='vendor-retrieve-update-delete'),
 # Purchase Order Tracking Endpoints
    path('purchase_orders/', PurchaseOrderListCreate.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDelete.as_view(), name='purchase-order-retrieve-update-delete'),
    
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge-purchase-order'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformance.as_view(), name='vendor-performance'),
]