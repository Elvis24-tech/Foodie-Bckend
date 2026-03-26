from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .mpesa import stk_push

@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        phone = data.get("phone")
        amount = data.get("amount")

        response = stk_push(phone, amount)
        return JsonResponse(response)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)

    print("M-PESA CALLBACK:", data)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})