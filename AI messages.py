import pygame
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions and font
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('AI Interaction')
font = pygame.font.SysFont("Arial", 30)

# AI Module class definition
class AI_Module:
    def __init__(self, values):
        self.values = values  # Values define the AI's personality

    def generate_message(self):
        # Example values-driven message generation
        messages = []
        
        if 'kindness' in self.values:
            messages.extend([
                "You're doing great! Keep going!",
                "You are valued and capable!"
            ])
        if 'helpfulness' in self.values:
            messages.extend([
                "How can I assist you further?",
                "Let me know if you need anything else."
            ])
        if 'optimism' in self.values:
            messages.extend([
                "The journey is just as important as the destination.",
                "You are on the right track!"
            ])
        if 'honesty' in self.values:
            messages.extend([
                "Let’s be honest, things may seem tough right now, but you'll make it through.",
                "Truth is, you're stronger than you think."
            ])

        # Return a random message from the generated list
        return random.choice(messages)

# Define the AI with specific values
ai = AI_Module(values=['kindness', 'helpfulness', 'optimism'])

# Function to display the message on the screen
def display_message(message):
    text_surface = font.render(message, True, (255, 255, 255))  # White color text
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(text_surface, (100, 250))  # Position of the message on the screen
    pygame.display.flip()  # Update the display

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate and display a message every 5 seconds (5000 ms)
    message = ai.generate_message()
    display_message(message)

    # Wait 5000 milliseconds (5 seconds) before displaying another message
    pygame.time.wait(5000)

# Quit Pygame
pygame.quit()