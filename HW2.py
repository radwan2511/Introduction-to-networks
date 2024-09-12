import random
import math
import numpy as np
import sys

def flip_bit(bit, p):
    """ Simulate bit flipping with probability p """
    rand = random.random()
    return 1 - bit if rand < p else bit

def add_parity_bits(message, d):
    """ Add even parity bits after every d bits """
    message_with_parity = []
    for i in range(0, len(message), d):
        block = message[i:i+d]
        parity = 1 if (sum(block) % 2 == 1) else 0  # If odd number of 1s, parity bit is 1 to make it even
        message_with_parity.extend(block + [parity])
    return message_with_parity


def check_parity_bits(received_message, d):
    """ Check even parity bits to detect errors """
    for i in range(0, len(received_message), d + 1):
        block = received_message[i:i+d+1]
        
          #parity = received_message[i+d]
        if (sum(block) % 2 == 1):
            return random.choice([True, False]), False  # Error detected, maybe  correctable and maybe not correctable

    return True, True  # No error detected, or error corrected



def simulate_sender_receiver(message_length, p, d, times=0):
    """ Simulate sender, noisy channel, and receiver """
    # data_length = message_length - (message_length // d)
    message = [random.randint(0, 1) for _ in range(message_length)]
    
    # Add parity bits or parity matrix
    message_with_error_handling = add_parity_bits(message, d)
    
    # Simulate noisy channel
    received_message = [flip_bit(bit, p) for bit in message_with_error_handling]
    
    # Check for errors and attempt to correct
    detected, corrected = check_parity_bits(received_message, d)
    
    if detected and corrected:
        return len(message_with_error_handling), "Success"
    elif detected: # and "Fixed" or no detection
        return len(message_with_error_handling), "Success"
    else: 
        return len(message_with_error_handling), "No Fix" # failed to fix

def main():
    message_length = 500
    #ps = [0.0001, 0.001, 0.01, 0.05]  # Different error probabilities to test
    ps = [0.05]
    ds = [10, 25, 50, 100]  # Different values for d

    for p in ps:
        for d in ds:
              successful_count = 0
              transmitted_count = 0
              total_count = 1000  # Number of messages to send
              
              for _ in range(total_count):
                  transmitted_bits , result = simulate_sender_receiver(message_length, p, d)
                  if result == "Success":
                      successful_count += transmitted_bits
                      transmitted_count += transmitted_bits
                  else: 
                    while result == "No Fix":
                        transmitted_bits2 , result = simulate_sender_receiver(message_length, p, d)
                        transmitted_bits += transmitted_bits2

                    successful_count += transmitted_bits2   
                    transmitted_count += transmitted_bits

                   
              
              efficiency_factor = (successful_count) / (transmitted_count)
              print(f"For p = {p}, d = {d}, : Efficiency Factor = {efficiency_factor:.4f}")

if __name__ == "__main__":
    main()