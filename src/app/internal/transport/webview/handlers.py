from django.http import HttpResponse
from django.views import View

from app.models import Client

class MeViewHtml(View):
    def get(self, request, id: int):
        user = Client.objects.get(external_id=id)

        html = f"""
        <html>
            <body>
                <h1>{user.first_name}</h1>
                <p>Your id: {user.external_id}</p>
                <p>Phone number: {user.phone_number}</p>
                <p>Email: {user.email}</p>
            <body>
        </html>
        """
       
        return HttpResponse(html)