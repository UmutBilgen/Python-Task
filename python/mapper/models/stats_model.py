class Stats:
    def __init__(self, elapsed_time, count, date, success_count, fail_count):
        """
        Stats constructor.

        Parameters:
        - elapsed_time (float): Elapsed time for the operation.
        - count (int): Total count of processed items.
        - date (str): Date of the operation.
        - success_count (int): Count of successful operations.
        - fail_count (int): Count of failed operations.
        """
        self.elapsed_time = elapsed_time
        self.count = count
        self.date = date
        self.success_count = success_count
        self.fail_count = fail_count
