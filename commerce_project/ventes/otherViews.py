
from .models import Shopper

def findShopper(user: object) -> Shopper:
    if user.is_authenticated:
        return Shopper.objects.filter(user=user)[0]
    return None