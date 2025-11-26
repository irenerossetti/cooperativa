import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from reports.views import ReportViewSet
from tenants.models import Organization
from users.models import User

print("Testing report API endpoint...")
print("=" * 50)

# Get or create organization
org = Organization.objects.first()
if not org:
    print("ERROR: No organization found in database!")
    exit(1)

print(f"Organization: {org.name} (subdomain: {org.subdomain})")

# Get a user
user = User.objects.first()
if not user:
    print("ERROR: No user found in database!")
    exit(1)

print(f"User: {user.username}")

# Create a request
factory = RequestFactory()
request = factory.get('/api/reports/reports/performance_by_parcel/')
request.user = user
request.organization = org

# Set the organization in thread-local
from tenants.middleware import set_current_organization
set_current_organization(org)

# Call the view
view = ReportViewSet.as_view({'get': 'performance_by_parcel'})
response = view(request)

print(f"\nResponse status: {response.status_code}")
print(f"Response data: {response.data[:2] if hasattr(response, 'data') and response.data else 'No data'}")

print("\n" + "=" * 50)
print("Test completed!")
