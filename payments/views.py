from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .mpesa import stk_push

@csrf_exempt
def initiate_payment(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)

            phone = data.get("phone")
            amount = data.get("amount")

            # ✅ Validate input
            if not phone or not amount:
                return JsonResponse({"error": "Phone and amount required"}, status=400)

            # ✅ Convert amount to int (VERY IMPORTANT)
            amount = int(float(amount))

            print("📞 Phone:", phone)
            print("💰 Amount:", amount)

            response = stk_push(phone, amount)

            print("📲 MPESA RESPONSE:", response)

            return JsonResponse(response)

        return JsonResponse({"error": "Invalid request"}, status=400)

    except Exception as e:
        print("❌ ERROR:", str(e))
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def mpesa_callback(request):
    try:
        data = json.loads(request.body)
        print("📥 M-PESA CALLBACK:", data)

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

    except Exception as e:
        print(" CALLBACK ERROR:", str(e))
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Failed"})