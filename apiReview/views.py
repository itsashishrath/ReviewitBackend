from django.shortcuts import render 
from rest_framework.views import APIView 
from .models import *
from rest_framework.response import Response 
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .main import *
from .formatter import *
import json

@api_view(['GET'])
def search_mobile_phones_view(request):
    # Ignore the actual search query for now
    mobile_name = request.GET.get('query', '')
    print(mobile_name)

    LLMreview, video_info = review(mobile_name)

    # finalData= restructure_llm_output(LLMreview.text, video_info)
    
    # print(json.dumps(finalData, indent=2))

    input_data= json.loads(LLMreview.text)
    x = restructure_data(input_data , video_info)
    print(x)
    return JsonResponse(x)
