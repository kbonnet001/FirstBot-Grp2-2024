import time
from contextlib import contextmanager

class Timer:
    """
    A context manager to measure execution time with pause and resume functionality.
    """
    def __enter__(self):
        """
        Starts the timer and initializes pause tracking.
        """
        self.start_time = time.time()
        self.total_paused_time = 0
        self.paused_start_time = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Stops the timer and accounts for any paused time.
        """
        if self.paused_start_time is not None:  # If paused at the end, account for it
            self.total_paused_time += time.time() - self.paused_start_time
        self.end_time = time.time()
        self.execution_time = self.end_time - self.start_time - self.total_paused_time

    def pause(self):
        """
        Pauses the timer if it is not already paused.
        """
        if self.paused_start_time is None:  # Prevent multiple pauses
            self.paused_start_time = time.time()

    def resume(self):
        """
        Resumes the timer if it is paused.
        """
        if self.paused_start_time is not None:  # Prevent resume without pause
            paused_duration = time.time() - self.paused_start_time
            self.total_paused_time += paused_duration
            self.paused_start_time = None

@contextmanager
def measure_time():
    """ Context manager for measuring execution time with pause and resume functionality.

    Example:
    with measure_time() as timer:
        function_example("Something")
        timer.pause()
        print("Some information to ignore")
        plt.show()
        # [...]
        timer.resume()
        print("Some information")
    print(f"Time execution: {timer.execution_time:.6f} seconds")
    """
    
    timer = Timer()
    timer.__enter__()
    try:
        yield timer
    finally:
        timer.__exit__(None, None, None)