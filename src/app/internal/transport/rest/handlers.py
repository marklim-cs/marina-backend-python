from django.http import JsonResponse
from django.views import View

from app.models import Student



class MeView(View):
    def get(self, request, id: int):
        user = Student.objects.get(external_id=id)
        user_data = dict(
            phone_number = user.phone_number,
            email = user.email,
            personal_id = user.external_id
        )
        return JsonResponse(user_data)