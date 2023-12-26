import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.utils import db_queries
from apps.utils.html_templates import recipe_detail
from core import settings as api_settings


def make_pdf_api_call(recipe_id):
    url = api_settings.PDFENDPOINT_URL
    payload = recipe_detail(db_queries.get_recipe_by_id(pk=recipe_id))
    payload['sandbox'] = True
    payload['delivery_mode'] = 'json'
    payload["page_size"] = 'A4'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_settings.PDFENDPOINT_API_KEY}"
    }

    # Make the API call
    response = requests.post(url, json=payload, headers=headers)
    return response

