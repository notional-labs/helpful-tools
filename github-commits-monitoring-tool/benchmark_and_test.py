from typing import Callable
from datetime import datetime
import github_monitor.github_monitor as github_monitor
import data_output

def benchmark(func: Callable):
    start_time = datetime.now().timestamp()
    func()
    total_execution_time = datetime.now().timestamp() - start_time

    print("Total execution time in milliseconds = {}".format(total_execution_time * 1000))

def query_and_prints():
    member_contributions = github_monitor.query_member_contributions()
    print(data_output.time_print(data_output.pretty_print_details(member_contributions)))

benchmark(query_and_prints)