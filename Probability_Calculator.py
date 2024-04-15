import random

class Hat:
    def __init__(self, **balls):
        # Convert the dictionary of balls into a list
        self.contents = []
        for color, count in balls.items():
            self.contents.extend([color] * count)
    
    def draw(self, num_balls):
        # If num_balls is greater than the available balls, draw all the balls
        if num_balls > len(self.contents):
            num_balls = len(self.contents)
        
        # Draw the specified number of balls randomly from the hat
        drawn_balls = random.sample(self.contents, num_balls)
        
        # Remove the drawn balls from the contents
        for ball in drawn_balls:
            self.contents.remove(ball)
        
        return drawn_balls


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    successful_draws = 0
    
    # Perform the experiment num_experiments times
    for _ in range(num_experiments):
        # Create a copy of the hat
        hat_copy = Hat(**{color: hat.contents.count(color) for color in set(hat.contents)})
        
        # Draw the specified number of balls
        drawn_balls = hat_copy.draw(num_balls_drawn)
        
        # Create a dictionary of the drawn balls
        drawn_balls_dict = {}
        for ball in drawn_balls:
            drawn_balls_dict[ball] = drawn_balls_dict.get(ball, 0) + 1
        
        # Check if the drawn balls match the expected balls
        successful = True
        for color, count in expected_balls.items():
            if drawn_balls_dict.get(color, 0) < count:
                successful = False
                break
        
        # Increment the count of successful draws if the draw matches the expected balls
        if successful:
            successful_draws += 1
    
    # Calculate the probability as the ratio of successful draws to the total number of experiments
    probability = successful_draws / num_experiments
    return probability


# Example usage:

hat = Hat(blue=5, red=4, green=2)
probability = experiment(hat=hat,
                        expected_balls={"red":1, "green":2},
                        num_balls_drawn=4,
                        num_experiments=2000)

print(f"Probability: {probability:.3f}")