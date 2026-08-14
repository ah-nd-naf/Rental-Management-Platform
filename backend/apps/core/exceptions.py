from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Standardizes API error responses across the entire backend.
    Wraps standard DRF errors in a consistent dictionary structure.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize the error payload to always include an 'errors' key
        custom_data = {
            "status_code": response.status_code,
            "errors": response.data
        }
        response.data = custom_data

    return response