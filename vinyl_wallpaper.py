import pygame
import requests
from io import BytesIO
from spotify_auth import get_current_song
import spotipy

pygame.init()

#screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spotify Vunyl Wallpaper")

#Load default vinyl record image
vinyl_img = pygame.image.load("vinyl.png")
vinyl_img = pygame.transform.scale(vinyl_img, (300, 300))

# Spotify client (for controlling playback)
CLIENT_ID = "532883e4b1284629b6289ad1ec3ef4ce"
CLIENT_SECRET = "b62c1395829d428f8979ee46e1844fdb"
REDIRECT_URI = "http://127.0.0.1:8080/callback"
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-currently-playing user-modify-playback-state"
))

def get_album_cover(url):
    #fetch and return an album cover image from the given url
    response = requests.get(url)
    album_img = pygame.image.load(BytesIO(response.content))
    return pygame.transform.scale(album_img,(150, 150)) #resize for vunyl center

#rotation angel for spinning effect
angle = 0

#define buttons
button_width = 150
button_height = 50
button_color = (100, 100, 255)
button_hover_color = (50, 50, 200)
font = pygame.font.Font(None, 36)

# Button Rects
next_button = pygame.Rect(WIDTH // 2 + 160, HEIGHT - 100, button_width, button_height)
prev_button = pygame.Rect(WIDTH // 2 - 310, HEIGHT - 100, button_width, button_height)
pause_button = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 100, button_width, button_height)

def draw_button(button_rect, text):
    #draw a button with text
    pygame.draw.rect(screen, button_color, button_rect)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (button_rect.centerx - text_surface.get_width() // 2, button_rect.centery - text_surface.get_height() // 2))

def handle_button_click(pos):
    if next_button.collidepoint(pos):
        sp.next_track()
    elif prev_button.collidepoint(pos):
        sp.previous_track()
    elif pause_button.collidepoint(pos):
        current_playback = sp.current_playback()
        if current_playback and current_playback['is_playing']:
            sp.pause_playback()
        else:
            sp.start.playback()

running = True
while running:
    screen.fill((20, 20, 20)) #Dark background

    #fetch song details
    song, artist, album_cover_urls = get_current_song()
    print(f"Song: {song}, Artist: {artist}")
    if song and artist:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"{song} - {artist}", True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 50))

        #get and dispaly album cover
        album_img = get_album_cover(album_cover_urls)
        album_center_x, album_center_y = WIDTH // 2 - 75, HEIGHT //2 - 75

        #rotate vinyl and draw
        rotated_vinyl = pygame.transform.rotate(vinyl_img, angle)
        rect = rotated_vinyl.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(rotated_vinyl, rect.topleft)

        #overlay album cover at the center of the vinyl
        screen.blit(album_img, (album_center_x, album_center_y))

        #increase rotation angel
        angle -= 1

    # Draw buttons
    draw_button(next_button, "Next")
    draw_button(prev_button, "Previous")
    draw_button(pause_button, "Pause")

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #left click
                handle_button_click(event.pos)

    pygame.display.flip() #update display
    pygame.time.delay(30) #control frame rate

pygame.quit()