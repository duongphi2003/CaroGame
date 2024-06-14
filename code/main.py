import pygame
import sys
import time
import random
from PIL import Image

# Initialize pygame
pygame.init()

# Initialize mixer
pygame.mixer.init()

# Load background music
pygame.mixer.music.load('D:/Caro/Sound/audio.mp3')
pygame.mixer.music.play(-1)  # Play the music indefinitely

BOARD_SIZE = 20
CELL_SIZE = 30
# Define window size
window_size = (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE + 50) # + 50 because bottom bar (players)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Home")

# Create buttons with rounded corners
play_button = pygame.Rect(window_size[0] /2 - 200/2, 150, 200, 50)
play_ai_button = pygame.Rect(window_size[0] /2 - 200/2, 220, 200, 50)
settings_button = pygame.Rect(window_size[0] /2 - 200/2, 290, 200, 50)
quit_button = pygame.Rect(window_size[0] /2 - 200/2, 360, 200, 50)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
TOMATO = (255, 99, 71)

# Load custom font
font_path = 'D:/Caro/font/VNTIME.TTF'
font_size = 70
button_font_size = 30
font = pygame.font.Font(font_path, font_size)
button_font = pygame.font.Font(font_path, button_font_size)

# Load GIF and convert to frames
gif_image = Image.open('D:/Caro/images/bgrd.gif')
frames = []
for frame in range(gif_image.n_frames):
    gif_image.seek(frame)
    frame_image = gif_image.copy().convert('RGBA')
    frame_image = frame_image.resize(window_size, Image.LANCZOS)
    frames.append(pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode))

def draw_text_centered(text, font, color, surface, rect):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=rect.center)
    surface.blit(textobj, textrect)

def draw_button(rect, text, font_size, color, surface, hover=False):
    if hover:
        color = TOMATO
        font = pygame.font.Font(font_path, int(font_size * 1.1))  # Increase font size by 10%
    else:
        font = pygame.font.Font(font_path, font_size)
    pygame.draw.rect(surface, color, rect, border_radius=10)
    draw_text_centered(text, font, WHITE, surface, rect)

# Game constants
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
SCREEN_SIZE = (BOARD_WIDTH, BOARD_HEIGHT + 50)
WIN_CONDITION = 5

# Image paths
background_image_path = 'D:/Caro/images/brgt.jpg'
icon_image_path = 'D:/Caro/images/bieutuong.png'
piece_image_path = 'D:/Caro/images/icon.png'
player1_icon_path = 'D:/Caro/images/bt.png'
player2_icon_path = 'D:/Caro/images/bt3.png'
settings_icon_path = 'D:/Caro/images/iconsetting.jpg'

def load_background():
    return pygame.image.load(background_image_path)

def load_icon():
    return pygame.image.load(icon_image_path)

def load_pieces():
    pieces_img = pygame.image.load(piece_image_path)
    piece_width = pieces_img.get_width() // 2
    piece_height = pieces_img.get_height() // 2
    x_img = pygame.Surface((piece_width, piece_height), pygame.SRCALPHA)
    o_img = pygame.Surface((piece_width, piece_height), pygame.SRCALPHA)
    x_img.blit(pieces_img, (0, 0), (piece_width, 0, piece_width, piece_height))
    o_img.blit(pieces_img, (0, 0), (0, 0, piece_width, piece_height))
    return x_img, o_img

def load_player_icon(path):
    icon = pygame.image.load(path)
    return pygame.transform.scale(icon, (50, 50))

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.x_img, self.o_img = load_pieces()

    def draw(self, screen):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if self.grid[y][x] == 'X':
                    screen.blit(pygame.transform.scale(self.x_img, (CELL_SIZE, CELL_SIZE)), rect.topleft)
                elif self.grid[y][x] == 'O':
                    screen.blit(pygame.transform.scale(self.o_img, (CELL_SIZE, CELL_SIZE)), rect.topleft)

    def place_piece(self, x, y, piece):
        if self.grid[y][x] is None:
            self.grid[y][x] = piece
            return True
        return False

    def check_win(self, piece):
        def check_direction(start_x, start_y, dx, dy):
            count = 0
            for i in range(WIN_CONDITION):
                x = start_x + i * dx
                y = start_y + i * dy
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.grid[y][x] == piece:
                    count += 1
                else:
                    break
            return count

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.grid[y][x] == piece:
                    if check_direction(x, y, 1, 0) >= WIN_CONDITION or\
                       check_direction(x, y, 0, 1) >= WIN_CONDITION or\
                       check_direction(x, y, 1, 1) >= WIN_CONDITION or\
                       check_direction(x, y, 1, -1) >= WIN_CONDITION:
                        return True
        return False

class Player:
    def __init__(self, piece, icon):
        self.piece = piece
        self.icon = icon
        self.time_left = 60

class Game:
    def __init__(self, play_with_ai=False):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Caro Game')
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.players = [Player('X', load_player_icon(player1_icon_path)),
                        Player('O', load_player_icon(player2_icon_path))]
        self.current_player_index = 0
        self.font = pygame.font.Font(None, 36)
        self.winner = None
        self.win_time = None
        self.turn_start_time = time.time()
        self.play_with_ai = play_with_ai

        self.background = load_background()
        self.background = pygame.transform.scale(self.background, SCREEN_SIZE)
        self.icon = load_icon()
        self.settings_icon = pygame.image.load(settings_icon_path)
        self.settings_icon = pygame.transform.scale(self.settings_icon, (50, 50))
        self.settings_icon_rect = self.settings_icon.get_rect(topleft=(window_size[0] - 50, BOARD_HEIGHT + 5))
        pygame.display.set_icon(self.icon)

    def reset_game(self):
        self.board = Board()
        self.current_player_index = 0
        self.winner = None
        self.win_time = None
        for player in self.players:
            player.time_left = 60

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % 2
        self.turn_start_time = time.time()

    def ai_move(self):
        empty_cells = [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if self.board.grid[y][x] is None]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.board.place_piece(x, y, self.players[self.current_player_index].piece)
            if self.board.check_win(self.players[self.current_player_index].piece):
                self.winner = self.players[self.current_player_index].piece
                self.win_time = time.time()
            else:
                self.switch_player()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.settings_icon_rect.collidepoint(event.pos):
                        result = self.show_settings()
                        if result == "back_home":
                            return
                    elif self.winner is None and (not self.play_with_ai or self.current_player_index == 0):
                        mouse_x, mouse_y = event.pos
                        if mouse_y < BOARD_HEIGHT:
                            x = mouse_x // CELL_SIZE
                            y = mouse_y // CELL_SIZE
                            if self.board.place_piece(x, y, self.players[self.current_player_index].piece):
                                self.players[self.current_player_index].time_left = 60
                                if self.board.check_win(self.players[self.current_player_index].piece):
                                    self.winner = self.players[self.current_player_index].piece
                                    self.win_time = time.time()
                                else:
                                    self.switch_player()

            if self.play_with_ai and self.current_player_index == 1 and not self.winner:
                time.sleep(0.5)  # Pause for a moment to simulate thinking
                self.ai_move()

            self.screen.blit(self.background, (0, 0))
            self.board.draw(self.screen)

            if self.winner:
                text = self.font.render(f"Player {self.winner} wins!", True, BLACK)
                self.screen.blit(text, (10, BOARD_HEIGHT + 10))
                if time.time() - self.win_time > 3:
                    self.reset_game()
            else:
                current_time = time.time()
                elapsed_time = current_time - self.turn_start_time
                self.players[self.current_player_index].time_left -= elapsed_time
                if self.players[self.current_player_index].time_left <= 0:
                    self.winner = self.players[(self.current_player_index + 1) % 2].piece
                    self.win_time = current_time
                self.turn_start_time = current_time

                player_icon = self.players[self.current_player_index].icon
                self.screen.blit(player_icon, (10, BOARD_HEIGHT + 10))
                timer_text = self.font.render(f"{int(self.players[self.current_player_index].time_left)}s", True, BLACK)
                self.screen.blit(timer_text, (70, BOARD_HEIGHT + 10))

            # Draw the settings icon
            self.screen.blit(self.settings_icon, self.settings_icon_rect.topleft)

            pygame.display.flip()
            self.clock.tick(30)

    def show_settings(self):
        settings_screen = pygame.Surface(window_size)
        pygame.display.set_caption("Settings")

        frame_index = 0
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 30)
        continue_button = pygame.Rect(window_size[0] / 2 - 200/2, 150, 200, 50)
        off_button = pygame.Rect(window_size[0] / 2 - 200/2, 250, 200, 50)
        back_home_button = pygame.Rect(window_size[0] / 2 - 200/2, 350, 200, 50)

        title_rect = pygame.Rect(300, 50, 200, 50)
        music_playing = pygame.mixer.music.get_busy()
            
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        return "continue"
                    elif off_button.collidepoint(event.pos):
                        if music_playing:
                            pygame.mixer.music.pause()
                            music_playing = False
                        else:
                            pygame.mixer.music.unpause()
                            music_playing = True
                    elif back_home_button.collidepoint(event.pos):
                        return "back_home"

            settings_screen.blit(frames[frame_index], (0, 0))
            frame_index = (frame_index + 1) % len(frames)

            draw_text_centered('Settings Menu', font, BLACK, settings_screen, title_rect)
            draw_button(continue_button, 'Continue', button_font_size, DARK_GRAY, settings_screen, hover=continue_button.collidepoint(mouse_pos))
            draw_button(off_button, 'ON' if music_playing else 'OFF', button_font_size, DARK_GRAY, settings_screen, hover=off_button.collidepoint(mouse_pos))
            draw_button(back_home_button, 'Back Home', button_font_size, DARK_GRAY, settings_screen, hover=back_home_button.collidepoint(mouse_pos))

            self.screen.blit(settings_screen, (0, 0))
            pygame.display.update()
            clock.tick(10)

# Initialize frame index and clock
frame_index = 0
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                Game().run()
                continue
            if play_ai_button.collidepoint(event.pos):
                Game(play_with_ai=True).run()
                continue
            if settings_button.collidepoint(event.pos):
                Game().show_settings()
                continue
            if quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    screen.blit(frames[frame_index], (0, 0))
    frame_index = (frame_index + 1) % len(frames)

    draw_text_centered('Game Menu', font, BLACK, screen, pygame.Rect(280, 50, 200, 50))
    draw_button(play_button, 'Play', button_font_size, DARK_GRAY, screen, hover=play_button.collidepoint(mouse_pos))
    draw_button(play_ai_button, 'Play with AI', button_font_size, DARK_GRAY, screen, hover=play_ai_button.collidepoint(mouse_pos))
    draw_button(settings_button, 'Settings', button_font_size, DARK_GRAY, screen, hover=settings_button.collidepoint(mouse_pos))
    draw_button(quit_button, 'Quit', button_font_size, DARK_GRAY, screen, hover=quit_button.collidepoint(mouse_pos))

    pygame.display.update()
    clock.tick(10)
