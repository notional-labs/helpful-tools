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
    memberContributions = github_monitor.queryContributions()
    print(data_output.compareView(memberContributions))
    print(data_output.detailView(memberContributions))

benchmark(query_and_prints)