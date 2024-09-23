import string
import random
from django.conf import settings
from django.utils import timezone


'''generateur code de referemce'''
def CodeGenerator(self, model, start_by_text, end_by_text):
    count = model.objects.filter(created_at__year=timezone.now().year, created_at__month=timezone.now().month, created_at__day=timezone.now().day).count()
    current_number = count + 1
    result = f"{start_by_text}{timezone.now().year}{timezone.now().month}{timezone.now().day}{random.choice(string.ascii_letters).upper()}{current_number:03d}"
    return result