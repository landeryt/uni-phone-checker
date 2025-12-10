from django.http import HttpResponse, JsonResponse
import re
from .models import User

# Returns list of registered users
def users(request):
    user_list = User.objects.all().values("id", "name", "email", "phone_number", "created_at")
    return JsonResponse(list(user_list))

def math_checker(s: str):
    # Boolean values to return a check on each condition
    isValid = False
    correctLength = False
    allDigits = False
    hasNonZeroDigit = False
    sumFirstEqualsLast = False
    sumOddEqualsEven = False

    # length check
    if len(s) == 6:
        correctLength = True
    else:
        return {
            "isValid": isValid, 
            "correctLength": correctLength,
            "allDigits": "", 
            "hasNonZeroDigit": "",
            "sumFirstEqualsLast": "",
            "sumOddEqualsEven": "",
        }
    
    # all digits check
    for char in s:
        if not char.isdigit():
            allDigits = False
            return {
                "isValid": isValid,
                "correctLength": correctLength,
                "allDigits": allDigits,
                "hasNonZeroDigit": "",
                "sumFirstEqualsLast": "",
                "sumOddEqualsEven": "",
            }
        
    allDigits = True # digits checked, we know it's true now    

    # Parse all characters to integers
    digits = [int(char) for char in s]

    # Check if there is at least one non zero digit
    for num in digits:
        if num != 0:
            hasNonZeroDigit = True
            break

    # Check if sum of first three equals sum of last three
    if sum(digits[0:3]) == sum(digits[3:6]):
        sumFirstEqualsLast = True

    # Check if sum of digits at odd positions equals sum at even positions
    if (digits[0] + digits[2] + digits[4]) == (digits[1] + digits[3] + digits[5]):
        sumOddEqualsEven = True 

    # Final validity check
    if (correctLength and allDigits and hasNonZeroDigit and 
        sumFirstEqualsLast and sumOddEqualsEven):
        isValid = True

    return {
        "isValid": isValid,
        "correctLength": correctLength,
        "allDigits": allDigits,
        "hasNonZeroDigit": hasNonZeroDigit,
        "sumFirstEqualsLast": sumFirstEqualsLast,
        "sumOddEqualsEven": sumOddEqualsEven,
    }

def count(request):
    return HttpResponse("Phone count endpoint.")

def validate(request):
    if request.method == "POST":
        # get phone number
        phone_number = request.POST.get("phone_number", "").strip()

        if not phone_number:
            return JsonResponse({"error": "No phone number provided."}, status=400)

        # Return JSON response for validation
        try:
            result = math_checker(phone_number)
            # According to mr teacher's requirements, an incorrect number will get a 400 status
            if result["isValid"] is False:
                return JsonResponse(result, status=400)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse("POST method required.", status=405)

def registration(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()

        # Basic validation
        if not name or not email or not phone_number:
            return JsonResponse({"error": "Name, email, and phone number are required."}, status=400)

        # validate email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return JsonResponse({"error": "Invalid email format."}, status=400)
        
        # validate phone number
        phone_result = math_checker(phone_number)
        if not phone_result["isValid"]:
            return JsonResponse({"error": "Invalid phone number."}, status=400)
        
        # Check for phone number uniqueness
        if User.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({"error": "Phone number already registered."}, status=400)
        
        # Create and save user
        try:
            user = User.objects.create(name=name, email=email, phone_number=phone_number)
            return JsonResponse({
                                    "message": "Registration successful.", 
                                    "user_id": user.id, 
                                    "name": user.name,
                                    "email": user.email,
                                    "phone_number": user.phone_number,
                                    "created_at": user.created_at.isoformat()
                                 },
                                  status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


    return HttpResponse("POST method required.", status=405)



