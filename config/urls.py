from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # Favicon request: redirect to existing logo
    path('favicon.ico', RedirectView.as_view(url='/static/img/LOGO.png', permanent=False)),
    # Fix missing legacy image reference by redirecting to an existing image
    path('static/images/rasm.png', RedirectView.as_view(url='/static/img/tiqxmmi.png', permanent=False)),
    # Catch language-prefixed 'frames' requests like /uz/frames/ and redirect to home
    path('<str:lang>/frames/', RedirectView.as_view(pattern_name='core:home', permanent=False)),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
