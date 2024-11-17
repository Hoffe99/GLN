import pygame
import random
import sys
import time

# Pygame initialisieren
pygame.init()

# Bildschirmgröße und andere Konstanten
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BALL_RADIUS = 15
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
SPEED = 5

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 255, 255)
DEEP_BLUE = (0,0,139)
DARK_ORANGE = (255, 140, 0)
DEEP_PINK = (255, 20, 147)

# Fenster erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DodgeBlock")

background_image = pygame.image.load("TGBBZ.jpg")  # Dein Hintergrundbild
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Game:
    def __init__(self):
        self.reverseTracker = 1
        self.life = 0
        self.undefeat = False  # Neues Attribut für den Unzerstörbarkeitsmodus
        self.undefeat_start_time = 0  # Startzeit für den Unzerstörbarkeitsmodus
        
    def reverse(self):
        self.reverseTracker *= -1
    
    def addLife(self):
        self.life += 1  
        
    def removeLife(self):
        self.life -= 1
    
    def activate_undefeat(self, ball):
        self.undefeat = True
        self.undefeat_start_time = pygame.time.get_ticks()  # Setze die Startzeit
        ball.color = YELLOW
        
    
    def deactivate_undefeat(self, ball):
        self.undefeat = False  # Deaktiviere den Unzerstörbarkeitsmodus
        ball.color = BLUE
        
           
    def check_undefeat_timeout(self, ball):
        # Prüfe, ob 10 Sekunden vergangen sind
        if self.undefeat and pygame.time.get_ticks() - self.undefeat_start_time > 10000:
            self.deactivate_undefeat(ball)
            
        
# Ball- und Hindernis-Klassen
class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - BALL_RADIUS - 10
        self.velocity_x = 0
        self.velocity_y = 0
        self.ball_radius = 15
        self.color = BLUE
        self.speed = 5
    
    def move(self):
        self.x += self.velocity_x
        
        if self.x < BALL_RADIUS:
            self.x = SCREEN_WIDTH - BALL_RADIUS
        if self.x > SCREEN_WIDTH - BALL_RADIUS:
            self.x = BALL_RADIUS
    def bigger(self):
        self.ball_radius += 5
        
    def smaller(self):
        if self.ball_radius > 5:
            self.ball_radius -= 5
    
    def faster(self):
        self.speed *= 1.25
        
    def slower(self):
        self.speed /= 1.25
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.ball_radius)
    def draw_undefeat(self):
        pygame.draw.circle(screen, random.choice((BLACK, YELLOW)), (self.x, self.y), self.ball_radius)
        

class Obstacle:
    def __init__(self, speed):
        self.x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        self.y = -OBSTACLE_HEIGHT
        self.baseSpeed = 3
        self.speed = random.randint(self.baseSpeed, speed)
        self.color = random.choice((GREEN, RED, DEEP_BLUE, DEEP_PINK, DARK_ORANGE))
    
    def move(self):
        self.y += self.speed
        
    def speedIncrease(self, increment):
        if self.speed <7 and self.baseSpeed <7:
            if self.speed < 7:
                self.speed += increment
            else:
                self.baseSpeed += increment
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    
    def reset(self, speed):
        self.__init__(speed)  # Aufruf von __init__, um alle Attribute zurückzusetzen

class MysteryBox:
    def __init__(self, speed):
        self.x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        self.y = -OBSTACLE_HEIGHT
        self.baseSpeed = 3
        self.speed = random.randint(self.baseSpeed, speed)
        self.color = random.choice((GREEN, RED, DEEP_BLUE, DEEP_PINK, DARK_ORANGE))
        self.effect = random.choice(["speed_boost", "speed_bump", "bigger", "smaller", "reverse", "extra_life", "undefeatable"])  # Zufällige Effekte
        self.font = pygame.font.SysFont(None, 48)  # Schriftart für das Fragezeichen

    def move(self):
        self.y += self.speed

    def draw(self):
        # Box zeichnen
        pygame.draw.rect(screen, self.color, (self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        
        # Fragezeichen zeichnen
        question_text = self.font.render("?", True, BLACK)  # Fragezeichen als Text
        text_rect = question_text.get_rect(center=(self.x + OBSTACLE_WIDTH // 2, self.y + OBSTACLE_HEIGHT // 2))  # Position des Textes in der Mitte der Box
        screen.blit(question_text, text_rect)  # Text auf die Box zeichnen

    def reset(self, speed):
        self.__init__(speed)

    def apply_effect(self, ball, playData):
        # Wende den Effekt an und gebe den aktualisierten Wert von playData zurück
        if self.effect == "speed_boost":
            ball.faster()  # Geschwindigkeit erhöhen
        elif self.effect == "speed_bump":
            ball.slower()
        elif self.effect == "bigger":
            ball.bigger()
        elif self.effect == "smaller":
            ball.smaller()
        elif self.effect == "reverse":
            playData.reverse()    
        elif self.effect == "extra_life":
            playData.addLife()
        elif self.effect == "undefeatable":
            playData.activate_undefeat(ball)
        return playData, self.effect, ball    
    
def load_highscores():
    highscores = {}
    try:
        with open('highscore.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                difficulty, score = line.strip().split('=')
                highscores[difficulty] = int(score)
    except FileNotFoundError:
        # Falls die Datei nicht existiert, erstellen wir sie mit den Standardwerten
        with open('highscore.txt', 'w') as file:
            file.write("easy=0\nnormal=0\nhard=0\n")
        highscores = {"easy": 0, "normal": 0, "hard": 0}
    
    return highscores

def save_highscores(highscores):
    with open('highscore.txt', 'w') as file:
        for difficulty, score in highscores.items():
            file.write(f"{difficulty}={score}\n")



        
# Funktion für die Schwierigkeitsauswahl
def select_difficulty():
    font = pygame.font.SysFont(None, 48)
    
    easy_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)
    normal_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    hard_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)
    
    while True:
        screen.blit(background_image, (0, 0))
        title_text = font.render("Wähle eine Schwierigkeit", True, RED)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))
        
        pygame.draw.rect(screen, BLACK, easy_button)
        pygame.draw.rect(screen, BLACK, normal_button)
        pygame.draw.rect(screen, BLACK, hard_button)
        
        easy_text = font.render("Easy", True, WHITE)
        normal_text = font.render("Normal", True, WHITE)
        hard_text = font.render("Hard", True, WHITE)
        
        screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(normal_text, (SCREEN_WIDTH // 2 - normal_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_x, mouse_y):
                    return "easy"
                elif normal_button.collidepoint(mouse_x, mouse_y):
                    return "normal"
                elif hard_button.collidepoint(mouse_x, mouse_y):
                    return "hard"
        
def show_countdown():
    font = pygame.font.SysFont(None, 100)
    text = ["READY", "SET", "GO!!"]
    for i in range(3):
        screen.blit(background_image, (0, 0))
        countdown_text = font.render(text[i], True, WHITE)
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
        pygame.display.flip()  # screen reset
        pygame.time.wait(1000)  # wait


# Funktion für das Spiel
def game_loop():
    highscores = load_highscores()  # Lade die Highscores
    difficulty_key = select_difficulty()
    difficulties = {"easy": [5, 4, 40],
                    "normal": [6, 5, 35], 
                    "hard": [6, 6, 30]}
    difficulty = difficulties[difficulty_key]
    diff_increase = 0
    effect = ""
    playData = Game()
    reverseFactor = playData.reverseTracker
    mystery_boxes = [MysteryBox(speed=difficulty[0]) for _ in range(1)]
    
    ball = Ball()
    obstacles = [Obstacle(speed=difficulty[0]) for _ in range(difficulty[1] + diff_increase)]
    clock = pygame.time.Clock()
    score = 0
    font = pygame.font.SysFont(None, 36)
    
    show_countdown()
    
    # Haupt-Spielschleife
    while True:
        screen.blit(background_image, (0, 0))
        
        # check the undefeat status
        playData.check_undefeat_timeout(ball)

        # Ereignisse (z. B. Tastendruck)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Steuerung des Balls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ball.velocity_x = -ball.speed * reverseFactor
        elif keys[pygame.K_RIGHT]:
            ball.velocity_x = ball.speed * reverseFactor
        else:
            ball.velocity_x = 0

        # Ball bewegen
        ball.move()
        
        # Hindernisse bewegen
        for obstacle in obstacles:
            obstacle.move()
            if obstacle.y > SCREEN_HEIGHT:
                obstacle.reset(speed=difficulty[0])
                score += 1  # Punkte hinzufügen, wenn das Hindernis den Bildschirm verlässt
                if score % difficulty[2] == 0:
                    diff_increase += 1
                    obstacle.speedIncrease(diff_increase)
                    obstacles.append(Obstacle(speed=difficulty[0]+diff_increase))
            
            # Unzerstörbarkeitsmodus
            if playData.undefeat == True:
                ball.draw_undefeat()
                if (ball.x - BALL_RADIUS < obstacle.x + OBSTACLE_WIDTH and
                    ball.x + BALL_RADIUS > obstacle.x and
                    ball.y - BALL_RADIUS < obstacle.y + OBSTACLE_HEIGHT and
                    ball.y + BALL_RADIUS > obstacle.y):
                    obstacles.remove(obstacle)
                    obstacles.append(Obstacle(speed=difficulty[0]+diff_increase))
            
            # Überprüfung auf Kollision
            elif (ball.x - BALL_RADIUS < obstacle.x + OBSTACLE_WIDTH and
                ball.x + BALL_RADIUS > obstacle.x and
                ball.y - BALL_RADIUS < obstacle.y + OBSTACLE_HEIGHT and
                ball.y + BALL_RADIUS > obstacle.y):
                
                if playData.life == 0:  # Kollision erkannt, Spiel endet
                    time.sleep(1)
                    game_over(score, difficulty_key, diff_increase, highscores)
                else:
                    obstacles.remove(obstacle)
                    playData.removeLife()
                    obstacles.append(Obstacle(speed=difficulty[0]+diff_increase))

            obstacle.draw()
        
        for box in mystery_boxes:
            box.move()
            if box.y > SCREEN_HEIGHT:
                box.reset(speed=difficulty[0])

            # Kollision mit MysteryBox
            if (ball.x - BALL_RADIUS < box.x + OBSTACLE_WIDTH and
                ball.x + BALL_RADIUS > box.x and
                ball.y - BALL_RADIUS < box.y + OBSTACLE_HEIGHT and
                ball.y + BALL_RADIUS > box.y):
                # Effekt der MysteryBox anwenden
                playData, effect, ball = box.apply_effect(ball, playData)
                reverseFactor = playData.reverseTracker
                box.reset(speed=difficulty[0])  # Box nach Anwendung des Effekts zurücksetzen

            box.draw()

        # Ball zeichnen
        ball.draw()

        # Statistiken anzeigen (links auf dem Bildschirm)
        stat_font = pygame.font.SysFont(None, 40)
        stats_x = 10
        stats_y = 70
        screen.blit(stat_font.render(f"Points: {score}", True, BLACK), (stats_x, stats_y - 60))
        screen.blit(stat_font.render(f"Lives: {playData.life}", True, RED), (stats_x, stats_y-30 ))
        screen.blit(stat_font.render(f"Effect: {effect}", True, BLACK), (stats_x, stats_y + 30))
        if reverseFactor == -1:
            screen.blit(stat_font.render("REVERSED", True, BLACK), (stats_x, stats_y + 60))

        # Highscore anzeigen für jede Schwierigkeit
        screen.blit(stat_font.render(f"Highscore: {highscores[difficulty_key]}", True, RED), (stats_x, stats_y ))
        

        # Bildschirm aktualisieren
        pygame.display.flip()

        # FPS (Frames pro Sekunde)
        clock.tick(60)


# Funktion für Game Over mit Neustart-Button
def game_over(score, diff, diff_increase, highscores):
    font = pygame.font.SysFont(None, 48)
    go_font = pygame.font.SysFont(None, 60)
    text = go_font.render(f"Game Over! Punkte: {score}.", True, RED)
    mode_text = go_font.render(f"Difficulty: {diff}.", True, RED)
    stage_text = go_font.render(f"Stage: {diff_increase}.", True, RED)
    screen.blit(background_image, (0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 150 ))
    screen.blit(mode_text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 110 ))
    screen.blit(stage_text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 70 ))
    
    # Update Highscore für die jeweilige Schwierigkeit, wenn der Score höher ist
    if score > highscores[diff]:
        highscores[diff] = score
        save_highscores(highscores)
    
    # Highscore anzeigen
    highscore_text = go_font.render(f"Highscore: {highscores[diff]}", True, RED)
    screen.blit(highscore_text, (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    # restart button
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
    pygame.draw.rect(screen, BLACK, restart_button)
    restart_text = font.render("Neu starten", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 115))
    
    pygame.display.flip()

    # restart action
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_x, mouse_y):
                    # Neustarten
                    game_loop()


# Spiel starten
game_loop()
