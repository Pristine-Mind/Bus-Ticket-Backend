from rest_framework import response


def custom_response(success=True, msg="", errors="", response_body=None, status_code=200):
    return response.Response({
        "success": success,
        "msg": msg,
        "errors": errors,
        "ResponseBody": response_body
    }, status=status_code)
