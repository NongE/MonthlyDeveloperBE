class ResponseModel:
    def set_response(self, req_path, code, message, res):
        return  {
            "req_path": req_path,
            "req_result": {
                "code": code,
                "message": message
            },
            "res": res
        }
