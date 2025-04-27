import pygame
import sys
import random
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Troll Flashcards Game")
clock = pygame.time.Clock()

background = pygame.image.load('image back.jpg')

background_frames = []
for i in range(1, 48): #47 frames
    frame = pygame.image.load(f"{i}.gif")
    frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))  # Resize to fit screen
    background_frames.append(frame)


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.SysFont("Lobster", 90)
small_font = pygame.font.SysFont("Pacifico", 50)

# Troll Messages
troll_messages = [
    "This isn’t real.",
    "You’re not alone, they’re still out there.",
    "AI can’t replace real connection.",
    "Wake up. The real world is waiting. ",
    "Perfection is a lie.",
    "You’re trapped in a bubble.",
    "Don’t forget what matters. ",
    "People need you, not just AI.",
    "The truth is outside.",
    "Break free from the illusion."
]

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def start_screen():
    while True:
        screen.fill(BLACK)

        screen.blit(background, (0, 0)) 
        
        
        draw_text("Troll Flashcards Game", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 70)
        draw_text("Press any key to start", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 20)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
            
            
        clock.tick(30)  # Slow down the start screen

def generate_question():
    op = random.choice(['+', '-', '*', '/'])
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    
    if op == '/':
        a = a * b  # can't have division by zero
    question = f"{a} {op} {b}"
    answer = eval(question)
    if op == '/':
        answer = round(answer, 2)
    
    return question, answer
 
def trolling_message():
    return random.choice(troll_messages) #pick at random

def troll_animation():
    # Random trolling animation: "You got trolled" meme image (you can place any funny image here)
    troll_images = ['troll face.png', 'smiling dog.jpg'] 
    troll_image = random.choice(troll_images)
    
    try:
        meme_image = pygame.image.load(troll_image)
        meme_image = pygame.transform.scale(meme_image, (400, 300))
        screen.fill(BLACK)
        screen.blit(meme_image, (WIDTH // 2 - 200, HEIGHT // 2 - 150))
        pygame.display.flip()
        time.sleep(3)  # Display the meme for 3 seconds (slower pace)
    except:
        draw_text("TROLLING YOU... ", font, YELLOW, screen, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        time.sleep(3)  # Longer delay for trolling message

def freeze_screen_with_message(message, answer):
    freeze_duration = 3000  # milliseconds (3 seconds)
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < freeze_duration:
        screen.fill(BLACK)
        draw_text(f"Wrong! Answer: {answer} ", small_font, RED, screen, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text(message, small_font, YELLOW, screen, WIDTH // 2, HEIGHT // 2 + 20)
        
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def game_loop():
    total_rounds = 10
    current_round = 0
    user_input = ''
    correct = None
    feedback_time = 0
    score = 0  # <--- Add this line to keep track of score

    while current_round < total_rounds:

        screen.fill(BLACK)

        frame_index = (pygame.time.get_ticks() // 100) % len(background_frames)
        screen.blit(background_frames[frame_index], (0, 0))

        draw_text(f"Round {current_round + 1} of {total_rounds}", small_font, WHITE, screen, WIDTH // 2, 50)
        
        question, answer = generate_question()
        draw_text(question, font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text("Your Answer: " + user_input, small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2)

        if correct is True:
            draw_text("Correct! 😎", small_font, GREEN, screen, WIDTH // 2, HEIGHT // 2 + 60)
        elif correct is False:
            draw_text(f"Wrong! Answer: {answer} 😜", small_font, RED, screen, WIDTH // 2, HEIGHT // 2 + 60)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        if round(float(user_input), 2) == round(answer, 2):
                            correct = True
                            score += 1  # increment score by 1
                            troll_animation()
                            feedback_time = pygame.time.get_ticks()
                            current_round += 1
                        else:
                            correct = False
                            troll_message_to_show = trolling_message()
                            freeze_screen_with_message(troll_message_to_show, answer)
                            feedback_time = pygame.time.get_ticks()
                            current_round += 1

                        
                    except:
                        correct = False
                        troll_message_to_show = trolling_message()
                        freeze_screen_with_message(troll_message_to_show, answer)
                        feedback_time = pygame.time.get_ticks()
                        current_round += 1

                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode in ['.', '-']:
                        user_input += event.unicode
                

        # If in feedback mode (after answer)
        if feedback_time:
            if correct is False:
                # Longer freeze after wrong answer
                if pygame.time.get_ticks() - feedback_time > 400:  # 3000 ms = 3 seconds
                    correct = None
                    feedback_time = 0
                    user_input = ''
            else:
                # Shorter feedback after correct answer
                if pygame.time.get_ticks() - feedback_time > 200:  # 1.5 seconds
                    correct = None
                    feedback_time = 0
                    user_input = ''


        pygame.display.flip()
        clock.tick(30)

    score_screen(score)  # <--- after game ends, final end screen to show score


def score_screen(score):
    while True:
        
        screen.fill(BLACK)
        draw_text("Game Over!", font, RED, screen, WIDTH // 2, HEIGHT // 2 - 100)
        draw_text(f"Your Score: {score} / 10", font, GREEN, screen, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text("Press any key to exit.", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(30)

# Running game
start_screen()
game_loop()
score_screen()