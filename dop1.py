import pygame
import sys
import os


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                x1 = x
                y1 = y
    # вернем игрока, а также его координаты
    return new_player, x1, y1


def update_level(level, xp, yp):
    nx = len(level[0])
    ny = len(level)
    for y in range(yp - my // 2, yp + my // 2 + 1):
        for x in range(xp - mx // 2, xp + 1 + mx // 2):
            if level[y % ny][x % nx] == '.':
                Tile('empty', x, y)
            elif level[y % ny][x % nx] == '#':
                Tile('wall', x, y)
            elif level[y % ny][x % nx] == '@':
                Tile('empty', x, y)


def terminate():
    pygame.quit()
    sys.exit()

def start_screen(x, y):
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (x, y))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


#уровень
running = True
try:
    level_name = 'level3.txt'
    level = load_level(level_name)
except FileNotFoundError:
    print('файл не найден')
    running = False

#тайлы
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png')
tile_width = tile_height = 50

# экран
pygame.init()
display = pygame.display
width = 450
height = 350
screen = display.set_mode((width, height))
screen.fill((0, 0, 255))

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

#старт меню
start_screen(width, height)
camera = Camera()
mx = 9
my = 7

start = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if not start:
                player, player_x, player_y = generate_level(level)
                all_sprites.draw(screen)
                start = True
                player1 = Player(mx // 2, my // 2)
                player_group.add(player1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if level[player_y % len(level)][(player_x + 1) % len(level[0])] != '#':
                    player.rect.x += tile_width
                    player_x += 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if level[player_y % len(level)][(player_x - 1) % len(level[0])] != '#':
                    player.rect.x -= tile_width
                    player_x -= 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if level[(player_y - 1) % len(level)][player_x % len(level[0])] != '#':
                    player.rect.y -= tile_height
                    player_y -= 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if level[(player_y + 1) % len(level)][player_x % len(level[0])] != '#':
                    player.rect.y += tile_height
                    player_y += 1
    if start:
        all_sprites = pygame.sprite.Group()
        update_level(level, player_x, player_y)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()
