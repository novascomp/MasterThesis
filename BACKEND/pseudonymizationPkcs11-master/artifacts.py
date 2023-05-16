from rest_api_module import PseudOptions


class Commander:

    def __init__(self, request_id: str, file_path: str, col_names_to_pseud: list, pseud_options: PseudOptions):
        self.request_id = request_id
        self.col_names_to_pseud = col_names_to_pseud
        self.pseud_options = pseud_options
        self.file_path = file_path


class GeneralModuleResponse:

    def __init__(self, start_time, end_time, result_path):
        self.start_time = start_time
        self.end_time = end_time
        self.result_path = result_path
