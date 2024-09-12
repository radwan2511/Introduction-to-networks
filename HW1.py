import random
import time


class TailDropQueue:
    def __init__(self):
        self.queue = []
        self.max_size = 100

    def enqueue(self, request):
        if len(self.queue) < self.max_size:
            self.queue.append(request)
        else:
            print("maxed queue request dropped!")

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def adjust_rate(self):
        return 1

class HeadDropQueue:
    def __init__(self):
        self.queue = []
        self.max_size = 100

    def enqueue(self, request):
        if len(self.queue) < self.max_size:
            self.queue.append(request)
        else:
            print("maxed queue request dropped!")

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop()
        return None

    def is_empty(self):
        return len(self.queue) == 0
    
    def adjust_rate(self):
        return 1
    
class REDQueue:
    def __init__(self):
        self.queue = []
        self.max_size = 7
        self.min_threshold = 2
        self.max_threshold = 5
        self.drop_probability = 0.5

    def enqueue(self, request):
        if len(self.queue) > self.max_size:
            print("maxed queue request dropped!")
        else:
            # Calculate average queue length
            avg_queue_length = len(self.queue)
            # Randomly drop packets based on drop probability and queue length
            if avg_queue_length < self.min_threshold:
                # No drop if queue length is below min threshold
                self.queue.append(request)
            elif avg_queue_length >= self.max_threshold:
                # Drop packet if queue length exceeds max threshold
                print("Packet dropped due to queue length exceeding max threshold")
                return
            else:
                # Randomly drop packet based on probability
                if random.uniform(0, 1) < self.drop_probability:
                    print("Packet dropped due to congestion.")
                else:
                    self.queue.append(request)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0
    
    def adjust_rate(self):
        return 1


class QARTQueue:
    def __init__(self):
        self.queue = []
        self.min_rate = 1
        self.max_rate = 4
        self.max_size = 7
        
    def is_empty(self):
        return len(self.queue) == 0
    def enqueue(self, request):
        if len(self.queue) < self.max_size:
            self.queue.append(request)
        else:
            print("maxed queue request dropped!")

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def adjust_rate(self):
        if len(self.queue) > 0:
            current_queue_length = len(self.queue)
            # Adjust processing rate based on queue length
            processing_rate = self.max_rate - (current_queue_length / len(self.queue)) * (self.max_rate - self.min_rate)
            return int(processing_rate)
        else:
            return self.max_rate  # Default to max rate if queue is empty

class Request:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.processing_time = random.uniform(0.001, 0.1)  # Random processing time between 1 ms to 100 ms
        self.deadline = 2.0  # Fixed deadline of 100 ms
        self.completed = False

def generate_request(arrival_time):
    return Request(arrival_time)

def simulate_web_service(arrival_rate, queue, simulation_time):
    successful_requests = 0
    total_requests = 0
    arrival_time = 0.0

    while arrival_time < simulation_time:
        # Generate requests based on Poisson process (exponential distribution)
        if random.uniform(0, 1) < arrival_rate:
            #new_request = generate_request(arrival_time)
            new_request = generate_request(time.time())
            queue.enqueue(new_request)
            total_requests += 1
        
        # Process requests based on queue algorithm or randomly ingnore and get another packet
        if not queue.is_empty() and random.uniform(0, 1) > 0.25:
        #if not queue.is_empty():
            for _ in range(queue.adjust_rate()):
                if queue.is_empty():
                    break
                current_request = queue.dequeue()
                time.sleep(current_request.processing_time)  # Simulate request processing
                
                if time.time() <= current_request.arrival_time + current_request.deadline:
                    current_request.completed = True
                    successful_requests += 1

        arrival_time += 0.001  # Increment by a small time step (e.g., 1 ms)

    success_rate = successful_requests / total_requests if total_requests > 0 else 0
    return success_rate

if __name__ == "__main__":
    arrival_rate = 0.9  # Requests per millisecond (adjust based on desired workload)
    simulation_time = 1.0  # Simulation time in seconds

    # Choose the queueing algorithm to use (e.g., FIFOQueue, REDQueue, CoDelQueue, QARTQueue)
    queue = TailDropQueue()  # Replace with the desired queue algorithm

    success_rate = simulate_web_service(arrival_rate, queue, simulation_time)

    # Output results
    print(f"Success Rate: {success_rate:.2%}")


