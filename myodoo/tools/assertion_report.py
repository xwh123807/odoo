class assertion_report(object):
    def __init__(self):
        self.success = 0
        self.failure = 0

    def record_success(self):
        self.success += 1

    def record_failure(self):
        self.failure += 1

    def record_result(self, result):
        if result is None:
            pass
        elif result is True:
            self.record_success()
        elif result is False:
            self.record_failure()

    def __str__(self):
        res = "Assertion report: %s success, %s failure" % (self.success, self.failure)
        return res
