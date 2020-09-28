from rest_framework.response import Response


class MediaResponse(Response):
    def __init__(self, result_code, details, code=200, result=None):
        data = {
            'result': result,
            'resultCode': result_code,
            'details': details
        }
        super().__init__(data=data, status=code)
