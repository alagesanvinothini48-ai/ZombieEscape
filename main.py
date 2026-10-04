import pygame
import sys
import math
from array import array

pygame.init()

# ================= FULL SCREEN =================

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Zombie Escape")

clock = pygame.time.Clock()

# ================= SOUND =================

sound_enabled = True

try:
    pygame.mixer.init(frequency=44100, size=-16, channels=1)

    def make_sound(frequency, duration, volume=0.3):
        sample_rate = 44100
        samples = int(sample_rate * duration)
        sound_data = array("h")

        for i in range(samples):
            wave = math.sin(
                2 * math.pi * frequency * i / sample_rate
            )
            value = int(wave * 32767 * volume)
            sound_data.append(value)

        return pygame.mixer.Sound(buffer=sound_data.tobytes())

    key_sound = make_sound(900, 0.15, 0.3)
    hit_sound = make_sound(150, 0.35, 0.4)
    escape_sound = make_sound(600, 0.25, 0.3)
    win_sound = make_sound(1000, 0.5, 0.3)
    gameover_sound = make_sound(100, 0.6, 0.4)

except Exception:
    sound_enabled = False
    key_sound = None
    hit_sound = None
    escape_sound = None
    win_sound = None
    gameover_sound = None


def play_sound(sound):
    if sound_enabled and sound is not None:
        sound.play()


# ================= COLORS =================

BLACK = (15, 15, 20)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
RED = (255, 60, 60)
GREEN = (0, 220, 80)
YELLOW = (255, 220, 0)
GRAY = (120, 120, 130)
PURPLE = (180, 80, 255)
ORANGE = (255, 140, 0)
DARK_GRAY = (35, 35, 45)

LIGHT_GREEN = (80, 255, 130)
LIGHT_PURPLE = (210, 130, 255)
LIGHT_RED = (255, 110, 110)


# ================= FONTS =================

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 80)


# ==================================================
#                    CREATE LEVEL
# ==================================================

def create_level(level):

    player = pygame.Rect(50, 50, 35, 35)

    exit_area = pygame.Rect(
        WIDTH - 90,
        HEIGHT - 90,
        60,
        60
    )

    if level == 1:

        key = pygame.Rect(
            WIDTH // 2,
            HEIGHT // 2,
            25,
            25
        )

        zombies = [
            pygame.Rect(250, 180, 35, 35),
            pygame.Rect(520, 350, 35, 35),
            pygame.Rect(680, 100, 35, 35)
        ]

        boss = None

    elif level == 2:

        key = pygame.Rect(
            WIDTH - 250,
            HEIGHT - 150,
            25,
            25
        )

        zombies = [
            pygame.Rect(220, 180, 35, 35),
            pygame.Rect(400, 150, 35, 35),
            pygame.Rect(520, 350, 35, 35),
            pygame.Rect(680, 100, 35, 35),
            pygame.Rect(650, 400, 35, 35)
        ]

        boss = None

    else:

        key = pygame.Rect(
            WIDTH - 250,
            150,
            25,
            25
        )

        zombies = [
            pygame.Rect(220, 180, 35, 35),
            pygame.Rect(400, 150, 35, 35),
            pygame.Rect(520, 350, 35, 35),
            pygame.Rect(680, 100, 35, 35),
            pygame.Rect(650, 400, 35, 35)
        ]

        boss = pygame.Rect(
            WIDTH - 250,
            250,
            55,
            55
        )

    walls = [

        pygame.Rect(150, 0, 30, 300),
        pygame.Rect(150, 370, 30, HEIGHT - 370),

        pygame.Rect(300, 100, 30, 300),
        pygame.Rect(300, 470, 30, HEIGHT - 470),

        pygame.Rect(450, 0, 30, 230),
        pygame.Rect(450, 300, 30, HEIGHT - 300),

        pygame.Rect(600, 100, 30, 300),
        pygame.Rect(600, 470, 30, HEIGHT - 470),

        pygame.Rect(180, 100, 120, 30),
        pygame.Rect(330, 400, 120, 30),
        pygame.Rect(480, 230, 120, 30)
    ]

    return player, key, exit_area, walls, zombies, boss


# ==================================================
#                    PLAYER MOVEMENT
# ==================================================

def move_player(player, walls, dx, dy):

    player.x += dx

    for wall in walls:

        if player.colliderect(wall):

            if dx > 0:
                player.right = wall.left

            elif dx < 0:
                player.left = wall.right

    player.y += dy

    for wall in walls:

        if player.colliderect(wall):

            if dy > 0:
                player.bottom = wall.top

            elif dy < 0:
                player.top = wall.bottom


# ==================================================
#                       HEARTS
# ==================================================

def draw_hearts(lives):

    for i in range(3):

        x = WIDTH - 220 + (i * 55)
        y = 25

        color = RED if i < lives else DARK_GRAY

        pygame.draw.circle(screen, color, (x, y), 10)
        pygame.draw.circle(screen, color, (x + 18, y), 10)

        pygame.draw.polygon(
            screen,
            color,
            [
                (x - 10, y + 5),
                (x + 28, y + 5),
                (x + 9, y + 28)
            ]
        )


# ==================================================
#                    HOW TO PLAY
# ==================================================

def show_instructions():

    while True:

        screen.fill(BLACK)

        title = big_font.render(
            "HOW TO PLAY",
            True,
            YELLOW
        )

        screen.blit(
            title,
            (WIDTH // 2 - 180, 80)
        )

        instructions = [

            "1. Move using WASD or ARROW KEYS",
            "2. Find the YELLOW KEY",
            "3. The key opens the GREEN EXIT",
            "4. Avoid the RED ZOMBIES",
            "5. Level 3 has a powerful BOSS",
            "6. You have 3 LIVES",
            "7. Press P to PAUSE the game",
            "8. Complete all 3 levels to WIN"
        ]

        y = 190

        for item in instructions:

            text = small_font.render(
                item,
                True,
                WHITE
            )

            screen.blit(
                text,
                (WIDTH // 2 - 250, y)
            )

            y += 45

        back = font.render(
            "PRESS ESC TO GO BACK",
            True,
            GREEN
        )

        screen.blit(
            back,
            (WIDTH // 2 - 145, HEIGHT - 90)
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return

        clock.tick(60)


# ==================================================
#                    MAIN MENU
# ==================================================

def start_screen():

    while True:

        screen.fill(BLACK)

        title = big_font.render(
            "ZOMBIE ESCAPE",
            True,
            GREEN
        )

        screen.blit(
            title,
            (WIDTH // 2 - 230, HEIGHT // 2 - 220)
        )

        subtitle = font.render(
            "SURVIVE. FIND. ESCAPE.",
            True,
            WHITE
        )

        screen.blit(
            subtitle,
            (WIDTH // 2 - 150, HEIGHT // 2 - 140)
        )

        play_button = pygame.Rect(
            WIDTH // 2 - 150,
            HEIGHT // 2 - 70,
            300,
            60
        )

        how_button = pygame.Rect(
            WIDTH // 2 - 150,
            HEIGHT // 2 + 10,
            300,
            60
        )

        quit_button = pygame.Rect(
            WIDTH // 2 - 150,
            HEIGHT // 2 + 90,
            300,
            60
        )

        mouse_position = pygame.mouse.get_pos()

        play_color = (
            LIGHT_GREEN
            if play_button.collidepoint(mouse_position)
            else GREEN
        )

        how_color = (
            LIGHT_PURPLE
            if how_button.collidepoint(mouse_position)
            else PURPLE
        )

        quit_color = (
            LIGHT_RED
            if quit_button.collidepoint(mouse_position)
            else RED
        )

        pygame.draw.rect(
            screen,
            play_color,
            play_button,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            how_color,
            how_button,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            quit_color,
            quit_button,
            border_radius=12
        )

        play_text = font.render(
            "PLAY GAME",
            True,
            BLACK
        )

        screen.blit(
            play_text,
            (WIDTH // 2 - 75, HEIGHT // 2 - 52)
        )

        how_text = font.render(
            "HOW TO PLAY",
            True,
            WHITE
        )

        screen.blit(
            how_text,
            (WIDTH // 2 - 90, HEIGHT // 2 + 28)
        )

        quit_text = font.render(
            "QUIT",
            True,
            WHITE
        )

        screen.blit(
            quit_text,
            (WIDTH // 2 - 35, HEIGHT // 2 + 108)
        )

        footer = small_font.render(
            "Use mouse to select an option",
            True,
            GRAY
        )

        screen.blit(
            footer,
            (WIDTH // 2 - 125, HEIGHT - 50)
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if play_button.collidepoint(event.pos):
                    return

                if how_button.collidepoint(event.pos):
                    show_instructions()

                if quit_button.collidepoint(event.pos):

                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

        clock.tick(60)


# ==================================================
#                    PAUSE MENU
# ==================================================

def pause_menu():

    while True:

        # Dark transparent-looking overlay
        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.fill(BLACK)
        overlay.set_alpha(210)

        screen.blit(
            overlay,
            (0, 0)
        )

        # PAUSED title

        paused_text = big_font.render(
            "GAME PAUSED",
            True,
            YELLOW
        )

        screen.blit(
            paused_text,
            (
                WIDTH // 2 - 190,
                HEIGHT // 2 - 180
            )
        )

        # RESUME BUTTON

        resume_button = pygame.Rect(
            WIDTH // 2 - 150,
            HEIGHT // 2 - 70,
            300,
            60
        )

        # MAIN MENU BUTTON

        menu_button = pygame.Rect(
            WIDTH // 2 - 150,
            HEIGHT // 2 + 10,
            300,
            60
        )

        mouse_position = pygame.mouse.get_pos()

        if resume_button.collidepoint(mouse_position):

            resume_color = LIGHT_GREEN

        else:

            resume_color = GREEN

        if menu_button.collidepoint(mouse_position):

            menu_color = LIGHT_PURPLE

        else:

            menu_color = PURPLE

        pygame.draw.rect(
            screen,
            resume_color,
            resume_button,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            menu_color,
            menu_button,
            border_radius=12
        )

        resume_text = font.render(
            "RESUME",
            True,
            BLACK
        )

        screen.blit(
            resume_text,
            (
                WIDTH // 2 - 55,
                HEIGHT // 2 - 52
            )
        )

        menu_text = font.render(
            "MAIN MENU",
            True,
            WHITE
        )

        screen.blit(
            menu_text,
            (
                WIDTH // 2 - 70,
                HEIGHT // 2 + 28
            )
        )

        help_text = small_font.render(
            "Press P to resume",
            True,
            GRAY
        )

        screen.blit(
            help_text,
            (
                WIDTH // 2 - 85,
                HEIGHT // 2 + 110
            )
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:

                    return "resume"

                if event.key == pygame.K_ESCAPE:

                    return "resume"

            if event.type == pygame.MOUSEBUTTONDOWN:

                if resume_button.collidepoint(event.pos):

                    return "resume"

                if menu_button.collidepoint(event.pos):

                    return "menu"

        clock.tick(60)


# ==================================================
#                    LEVEL SCREEN
# ==================================================

def level_screen(level):

    screen.fill(BLACK)

    if level == 1:

        message = "LEVEL 1"
        info = "Find the yellow key and escape!"

    elif level == 2:

        message = "LEVEL 2"
        info = "More zombies are coming!"

    else:

        message = "LEVEL 3 - BOSS"
        info = "Escape the Boss Zombie!"

    text = big_font.render(
        message,
        True,
        PURPLE
    )

    screen.blit(
        text,
        (WIDTH // 2 - 170, HEIGHT // 2 - 80)
    )

    info_text = font.render(
        info,
        True,
        YELLOW
    )

    screen.blit(
        info_text,
        (WIDTH // 2 - 190, HEIGHT // 2 + 30)
    )

    pygame.display.update()

    pygame.time.wait(1800)


# ==================================================
#                    END SCREEN
# ==================================================

def end_screen(message, score):

    if message == "YOU ESCAPED!":

        play_sound(win_sound)

    else:

        play_sound(gameover_sound)

    while True:

        screen.fill(BLACK)

        if message == "YOU ESCAPED!":

            result = big_font.render(
                message,
                True,
                GREEN
            )

            info = "You survived all 3 levels!"

        else:

            result = big_font.render(
                message,
                True,
                RED
            )

            info = "The zombies caught you."

        screen.blit(
            result,
            (WIDTH // 2 - 190, HEIGHT // 2 - 130)
        )

        info_text = font.render(
            info,
            True,
            WHITE
        )

        screen.blit(
            info_text,
            (WIDTH // 2 - 170, HEIGHT // 2 - 30)
        )

        score_text = font.render(
            "FINAL SCORE: " + str(score),
            True,
            YELLOW
        )

        screen.blit(
            score_text,
            (WIDTH // 2 - 120, HEIGHT // 2 + 30)
        )

        restart = font.render(
            "PRESS R TO PLAY AGAIN",
            True,
            GREEN
        )

        screen.blit(
            restart,
            (WIDTH // 2 - 140, HEIGHT // 2 + 100)
        )

        quit_text = small_font.render(
            "PRESS ESC TO QUIT",
            True,
            GRAY
        )

        screen.blit(
            quit_text,
            (WIDTH // 2 - 100, HEIGHT // 2 + 150)
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    return True

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

        clock.tick(60)


# ==================================================
#                    MAIN GAME
# ==================================================

while True:

    start_screen()

    level = 1
    lives = 3
    score = 0

    game_finished = False
    return_to_menu = False

    while level <= 3 and not game_finished:

        (
            player,
            key,
            exit_area,
            walls,
            zombies,
            boss
        ) = create_level(level)

        has_key = False

        if level == 1:

            zombie_speed = 1

        elif level == 2:

            zombie_speed = 2

        else:

            zombie_speed = 2

        level_screen(level)

        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_p:

                        pause_result = pause_menu()

                        if pause_result == "menu":

                            running = False
                            return_to_menu = True
                            game_finished = True

            if return_to_menu:

                break

            keys = pygame.key.get_pressed()

            dx = 0
            dy = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -5

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 5

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -5

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 5

            move_player(
                player,
                walls,
                dx,
                dy
            )

            # ================= KEY =================

            if player.colliderect(key) and not has_key:

                has_key = True
                score += 100

                play_sound(key_sound)

            # ================= ZOMBIES =================

            for zombie in zombies:

                if zombie.x < player.x:
                    zombie.x += zombie_speed

                elif zombie.x > player.x:
                    zombie.x -= zombie_speed

                if zombie.y < player.y:
                    zombie.y += zombie_speed

                elif zombie.y > player.y:
                    zombie.y -= zombie_speed

            # ================= BOSS =================

            if boss is not None:

                if boss.x < player.x:
                    boss.x += 2

                elif boss.x > player.x:
                    boss.x -= 2

                if boss.y < player.y:
                    boss.y += 2

                elif boss.y > player.y:
                    boss.y -= 2

            # ================= COLLISION =================

            hit = False

            for zombie in zombies:

                if player.colliderect(zombie):

                    hit = True
                    break

            if boss is not None:

                if player.colliderect(boss):
                    hit = True

            if hit:

                lives -= 1

                play_sound(hit_sound)

                player.x = 50
                player.y = 50

                if lives <= 0:

                    running = False
                    game_finished = True
                    result = "GAME OVER!"

            # ================= EXIT =================

            if player.colliderect(exit_area) and has_key:

                score += 100

                play_sound(escape_sound)

                running = False

            # ================= DRAW =================

            screen.fill(BLACK)

            # Walls

            for wall in walls:

                pygame.draw.rect(
                    screen,
                    GRAY,
                    wall,
                    border_radius=4
                )

            # Key

            if not has_key:

                pygame.draw.circle(
                    screen,
                    YELLOW,
                    key.center,
                    9,
                    4
                )

                pygame.draw.rect(
                    screen,
                    YELLOW,
                    (
                        key.centerx + 5,
                        key.centery - 3,
                        20,
                        6
                    )
                )

            # Exit

            exit_color = GREEN if has_key else RED

            pygame.draw.rect(
                screen,
                exit_color,
                exit_area,
                border_radius=8
            )

            pygame.draw.circle(
                screen,
                YELLOW,
                (
                    exit_area.right - 12,
                    exit_area.centery
                ),
                5
            )

            # Player

            pygame.draw.circle(
                screen,
                BLUE,
                player.center,
                20
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (
                    player.centerx - 7,
                    player.centery - 5
                ),
                4
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (
                    player.centerx + 7,
                    player.centery - 5
                ),
                4
            )

            # Zombies

            for zombie in zombies:

                pygame.draw.circle(
                    screen,
                    RED,
                    zombie.center,
                    20
                )

                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        zombie.centerx - 7,
                        zombie.centery - 5
                    ),
                    4
                )

                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        zombie.centerx + 7,
                        zombie.centery - 5
                    ),
                    4
                )

            # Boss

            if boss is not None:

                pygame.draw.circle(
                    screen,
                    ORANGE,
                    boss.center,
                    30
                )

                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        boss.centerx - 10,
                        boss.centery - 7
                    ),
                    5
                )

                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        boss.centerx + 10,
                        boss.centery - 7
                    ),
                    5
                )

                boss_text = font.render(
                    "BOSS",
                    True,
                    ORANGE
                )

                screen.blit(
                    boss_text,
                    (
                        boss.centerx - 35,
                        boss.top - 40
                    )
                )

            # ================= HUD =================

            pygame.draw.rect(
                screen,
                DARK_GRAY,
                (
                    0,
                    0,
                    WIDTH,
                    75
                )
            )

            title = font.render(
                "ZOMBIE ESCAPE",
                True,
                GREEN
            )

            screen.blit(
                title,
                (25, 20)
            )

            level_text = font.render(
                "LEVEL " + str(level),
                True,
                PURPLE
            )

            screen.blit(
                level_text,
                (
                    WIDTH // 2 - 50,
                    20
                )
            )

            score_text = font.render(
                "SCORE: " + str(score),
                True,
                WHITE
            )

            screen.blit(
                score_text,
                (
                    WIDTH - 450,
                    20
                )
            )

            lives_label = small_font.render(
                "LIVES",
                True,
                WHITE
            )

            screen.blit(
                lives_label,
                (
                    WIDTH - 215,
                    15
                )
            )

            draw_hearts(lives)

            # Pause hint

            pause_hint = small_font.render(
                "P = PAUSE",
                True,
                GRAY
            )

            screen.blit(
                pause_hint,
                (
                    WIDTH - 125,
                    HEIGHT - 45
                )
            )

            # Bottom message

            pygame.draw.rect(
                screen,
                DARK_GRAY,
                (
                    0,
                    HEIGHT - 60,
                    WIDTH,
                    60
                )
            )

            if level == 3 and not has_key:

                message = "FIND THE KEY - AVOID THE BOSS!"

            elif has_key:

                message = "KEY FOUND! GO TO THE GREEN EXIT!"

            else:

                message = "FIND THE YELLOW KEY!"

            message_text = font.render(
                message,
                True,
                GREEN if has_key else YELLOW
            )

            screen.blit(
                message_text,
                (
                    WIDTH // 2 - 220,
                    HEIGHT - 45
                )
            )

            pygame.display.update()

            clock.tick(60)

        if return_to_menu:

            break

        if game_finished:

            break

        if level < 3:

            level += 1

        else:

            game_finished = True
            result = "YOU ESCAPED!"

    # Return directly to main menu

    if return_to_menu:

        continue

    play_again = end_screen(
        result,
        score
    )

    if not play_again:

        break


pygame.quit()
sys.exit()

