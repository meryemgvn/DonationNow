class Requests:
    def __init__(self, userid, req_time, br_id, req_name, amount, report, is_paid, code ):
        self.userid = userid
        self.req_time = req_time
        self.br_id = br_id
        self.req_name = req_name
        self.amount = amount
        self.report = report
        self.is_paid = is_paid
        self.code = code