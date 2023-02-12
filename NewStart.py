import pygame
import sys
import os


# Начальный экран


def start_screen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 580))
    fps = 70
    running = True
    intro_text = ["Вы попали в страшный замок",
                  "1 уровень",
                  "", "Попытайтесь выбраться,",
                  "остерегаясь препятствий"
                  "", "", "Пробел - начать игру",
                  "", "Escape - выйти"
                  ]
    font = pygame.font.Font(None, 40)
    text_coord = 50
    black = (65, 105, 225)
    screen.fill((255, 204, 153))
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color(black))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    game()
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(fps)




# 1 level


def game():
    def load_level(filename):
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def load_image(name):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением'{fullname}'не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass1.png'),
        "win": load_image("portal.png"),
        "spikes": load_image("spikes.png"),
        "fakel": load_image("fakel.png"),
    }
    player_image = load_image('mario.png')
    player_image1 = load_image('mario1.png')
    player_image2 = load_image('mario2.png')
    player_imageu = load_image('mariou.png')

    tile_width = 50
    tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    win_group = pygame.sprite.Group()
    fakel_group = pygame.sprite.Group()
    spikes_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            if tile_type == 'wall':
                walls_group.add(self)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if tile_type == 'win':
                win_group.add(self)
            if tile_type == "spikes":
                spikes_group.add(self)
            if tile_type == 'fakel':
                fakel_group.add(self)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.pos = 40 * pos_x, 40 * pos_y
            self.rect = self.image.get_rect().move(
                self.pos[0], self.pos[1])
            self.velocity = 1

        def move(self, dx, dy):
            self.pos = self.pos[0] + dx * self.velocity, \
                       self.pos[1] + dy * self.velocity
            self.rect = self.image.get_rect().move(
                self.pos[0], self.pos[1])
            if pygame.sprite.spritecollideany(self, walls_group):
                self.pos = self.pos[0] - dx * self.velocity, \
                           self.pos[1] - dy * self.velocity
                self.rect = self.image.get_rect().move(
                    self.pos[0], self.pos[1])
            if pygame.sprite.spritecollideany(self, win_group):
                pygame.quit()
                startlev_srceen()
                sys.exit()
            if pygame.sprite.spritecollideany(self, spikes_group):
                pygame.quit()
                end_screen()
            if pygame.sprite.spritecollideany(self, fakel_group):
                self.pos = self.pos[0] - dx * self.velocity, \
                           self.pos[1] - dy * self.velocity
                self.rect = self.image.get_rect().move(
                    self.pos[0], self.pos[1])

        def turn(self, r=0, ll=0, u=0, d=0):
            if r == 1:
                self.image = player_image1
            if ll == 1:
                self.image = player_image2
            if u == 1:
                self.image = player_imageu
            if d == 1:
                self.image = player_image

        def rturn(self):
            self.image = player_image
        # print(dx, dy, self.pos, "-", self.rect.centerx, self.rect.centery)
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    win_group = pygame.sprite.Group()

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == ':':
                    Tile('win', x, y)
                elif level[y][x] == '^':
                    Tile('spikes', x, y)
                elif level[y][x] == '%':
                    Tile('fakel', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self, target):
            self.target = target

        # сдвинуть объект obj на смещение камеры
        def apply(self, sprite_group):
            size = width, height = 500, 500
            dx = -(self.target.pos[0] - pygame.display.set_mode(size).get_rect().centerx)
            dy = -(self.target.pos[1] - pygame.display.set_mode(size).get_rect().centery)
            for obj in sprite_group:
                # if obj is not self.target:
                obj.rect.x += dx
                obj.rect.y += dy
            self.target.pos = pygame.display.set_mode(size).get_rect().center

    player = None
    player, level_x, level_y = generate_level(load_level('map.txt'))
    size = width, height = 500, 500
    fps = 70
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    camera = Camera(player)
    running = True
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                    move_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False
        screen.fill((0, 0, 0))
        if move_left:
            player.move(-5, 0)
            player.turn(0, 1)
        if move_right:
            player.move(5, 0)
            player.turn(1, 0)
        if move_up:
            player.move(0, -5)
            player.turn(0, 0, 1)
        if move_down:
            player.move(0, 5)
            player.turn(0, 0, 0, 1)
        camera.apply(all_sprites)
        all_sprites.draw(screen)
        all_sprites.update()
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

#Конечный экран 1 уровня
def end_screen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 560))
    fps = 70
    running = True
    intro_text = ["Get Out",
                  "", "Сожалею но вы ,",
                  "попали в ловушку",
                  "Соберитесь с силами",
                  "и попытайтесь вновь"
                  "", "", "Пробел - начать игру заново",
                  "", "Escape - сдаться"
                  ]
    font = pygame.font.Font(None, 40)
    text_coord = 50
    black = (119, 221, 231)
    screen.fill((255, 204, 153))
    for line in intro_text:
        string_rendered = font.render(line, True, (65, 105, 225))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    start_screen()
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(fps)

#Начальный экран 2 уровня
def startlev_srceen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 580))
    fps = 70
    running = True
    intro_text = ["Get Out",
                  "", "Поздравляю вы прошли,",
                  "первый уровень",
                  "но расслабляться рано",
                  "портал отправил вас в пирамиду"
                  "", "", "Пробел - начать игру",
                  "", "Escape - выйти"
                  ]
    font = pygame.font.Font(None, 40)
    text_coord = 50
    black = (65, 105, 225)
    screen.fill((255, 204, 153))
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color(black))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    game_gam()
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(fps)


# 2 level


def game_gam():
    def load_level(filename):
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def load_image(name):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением'{fullname}'не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    tile_images = {
        'wall': load_image('wall.png'),
        'empty': load_image('pol.png'),
        "win": load_image("portal.png"),
        "lekaf": load_image("lekaf.png"),
        "bugs": load_image("bugs.png"),
        "dec": load_image("dec.png")
    }
    player_image = load_image('mario.png')
    player_image1 = load_image('mario1.png')
    player_image2 = load_image('mario2.png')
    player_imageu = load_image('mariou.png')

    tile_width = 50
    tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    win_group = pygame.sprite.Group()
    bugs_group = pygame.sprite.Group()
    dec_group = pygame.sprite.Group()
    lekaf_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            if tile_type == 'wall':
                walls_group.add(self)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if tile_type == 'win':
                win_group.add(self)
            if tile_type == 'bugs':
                bugs_group.add(self)
            if tile_type == 'dec':
                dec_group.add(self)
            if tile_type == 'lekaf':
                lekaf_group.add(self)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.pos = tile_width * pos_x, tile_height * pos_y
            self.rect = self.image.get_rect().move(
                self.pos[0], self.pos[1])
            self.velocity = 1

        def move(self, dx, dy):
            self.pos = self.pos[0] + dx * self.velocity, \
                       self.pos[1] + dy * self.velocity
            self.rect = self.image.get_rect().move(
                self.pos[0], self.pos[1])
            if pygame.sprite.spritecollideany(self, walls_group):
                self.pos = self.pos[0] - dx * self.velocity, \
                           self.pos[1] - dy * self.velocity
                self.rect = self.image.get_rect().move(
                    self.pos[0], self.pos[1])
            if pygame.sprite.spritecollideany(self, win_group):
                pygame.quit()
                startlevv_srceen()
                sys.exit()
            if pygame.sprite.spritecollideany(self, bugs_group):
                pygame.quit()
                end1_screen()
                sys.exit()
            if pygame.sprite.spritecollideany(self, lekaf_group):
                self.pos = self.pos[0] - dx * self.velocity, \
                           self.pos[1] - dy * self.velocity
                self.rect = self.image.get_rect().move(
                    self.pos[0], self.pos[1])

        def turn(self, r=0, ll=0, u=0, d=0):
            if r == 1:
                self.image = player_image1
            if ll == 1:
                self.image = player_image2
            if u == 1:
                self.image = player_imageu
            if d == 1:
                self.image = player_image
        # print(dx, dy, self.pos, "-", self.rect.centerx, self.rect.centery)
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    win_group = pygame.sprite.Group()

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == ':':
                    Tile('win', x, y)
                elif level[y][x] == '%':
                    Tile('lekaf', x, y)
                elif level[y][x] == '^':
                    Tile('bugs', x, y)
                elif level[y][x] == 'd':
                    Tile('dec', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self, target):
            self.target = target

        # сдвинуть объект obj на смещение камеры
        def apply(self, sprite_group):
            size = width, height = 500, 500
            dx = -(self.target.pos[0] - pygame.display.set_mode(size).get_rect().centerx)
            dy = -(self.target.pos[1] - pygame.display.set_mode(size).get_rect().centery)
            for obj in sprite_group:
                # if obj is not self.target:
                obj.rect.x += dx
                obj.rect.y += dy
            self.target.pos = pygame.display.set_mode(size).get_rect().center

    player = None
    player, level_x, level_y = generate_level(load_level('2lev.txt'))
    size = width, height = 500, 500
    fps = 70
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    camera = Camera(player)
    running = True
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                    move_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False
        screen.fill((0, 0, 0))
        if move_left:
            player.move(-5, 0)
            player.turn(0, 1)
        if move_right:
            player.move(5, 0)
            player.turn(1, 0)
        if move_up:
            player.move(0, -5)
            player.turn(0, 0, 1)
        if move_down:
            player.move(0, 5)
            player.turn(0, 0, 0, 1)
        camera.apply(all_sprites)
        all_sprites.draw(screen)
        all_sprites.update()
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

#Конечный экран 2 уровня
def end1_screen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 560))
    fps = 70
    running = True
    intro_text = ["Get Out",
                  "", "Сожалею но вас ,",
                  "сьел жук-скоробей",
                  "Не сдавайтесь",
                  "Вы можете выбраться"
                  "", "", "Пробел - прогрызть себе путь наружу",
                  "", "Escape - смириться и стать перевареным"
                  ]
    font = pygame.font.Font(None, 40)
    text_coord = 50
    black = (65, 105, 225)
    screen.fill((255, 204, 153))
    for line in intro_text:
        string_rendered = font.render(line, True, (65, 105, 225))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    startlev_srceen()
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(fps)


def startlevv_srceen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 560))
    fps = 70
    running = True
    intro_text = ["Get Out",
                  "", "Поздравляю вы прошли,",
                  "второй уровень",
                  "но расслабляться рано",
                  "портал отправил вас в зачарованный лес",
                  "", "", "Пробел - начать игру",
                  "", "Escape - выйти"
                  ]
    font = pygame.font.Font(None, 40)
    text_coord = 50
    black = (65, 105, 225)
    screen.fill((255, 204, 153))
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color(black))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    game1_gam()
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(fps)

#3 уровень
def game1_gam():
    def load_level(filename):
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def load_image(name):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением'{fullname}'не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    tile_images = {
        'wall': load_image('lec.png'),
        'empty': load_image('grass.png'),
        'sec': load_image('lec.png'),
        "win": load_image("portal.png"),
        "lekaf": load_image("lekaf.png"),
        "bugs": load_image("ork.png"),
        "dec": load_image("dec.png")
    }
    player_image = load_image('mario.png')
    player_image1 = load_image('mario1.png')
    player_image2 = load_image('mario2.png')
    player_imageu = load_image('mariou.png')

    tile_width = 50
    tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    sec_group = pygame.sprite.Group()
    win_group = pygame.sprite.Group()
    bugs_group = pygame.sprite.Group()
    dec_group = pygame.sprite.Group()
    lekaf_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            if tile_type == 'wall':
                walls_group.add(self)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if tile_type == 'win':
                win_group.add(self)
            if tile_type == 'bugs':
                bugs_group.add(self)
            if tile_type == 'dec':
                dec_group.add(self)
            if tile_type == 'sec':
                sec_group.add(self)
            if tile_type == 'lekaf':
                lekaf_group.add(self)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.pos = tile_width * pos_x, tile_height * pos_y
            self.rect = self.image.get_rect().move(
                self.pos[0], self.pos[1])
            self.velocity = 1

        def move(self, dx, dy):
            self.pos = self.pos[0] + dx * self.velocity, \
                       self.pos[1] + dy * self.velocity
            self.rect = self.image.get_rect().move(
                self.pos[0], self.pos[1])
            if pygame.sprite.spritecollideany(self, walls_group):
                self.pos = self.pos[0] - dx * self.velocity, \
                           self.pos[1] - dy * self.velocity
                self.rect = self.image.get_rect().move(
                    self.pos[0], self.pos[1])
            if pygame.sprite.spritecollideany(self, win_group):
                pygame.quit()
                startt_screen()
                sys.exit()
            if pygame.sprite.spritecollideany(self, bugs_group):
                pygame.quit()
                ende_screen()
                sys.exit()
            if pygame.sprite.spritecollideany(self, lekaf_group):
                self.pos = self.pos[0] - dx * self.velocity, \
                           self.pos[1] - dy * self.velocity
                self.rect = self.image.get_rect().move(
                    self.pos[0], self.pos[1])

        def turn(self, r=0, ll=0, u=0, d=0):
            if r == 1:
                self.image = player_image1
            if ll == 1:
                self.image = player_image2
            if u == 1:
                self.image = player_imageu
            if d == 1:
                self.image = player_image

        def rturn(self):
            self.image = player_image
        # print(dx, dy, self.pos, "-", self.rect.centerx, self.rect.centery)
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    win_group = pygame.sprite.Group()

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == ':':
                    Tile('win', x, y)
                elif level[y][x] == '%':
                    Tile('lekaf', x, y)
                elif level[y][x] == '^':
                    Tile('bugs', x, y)
                elif level[y][x] == '*':
                    Tile('sec', x, y)
                elif level[y][x] == 'd':
                    Tile('dec', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self, target):
            self.target = target

        # сдвинуть объект obj на смещение камеры
        def apply(self, sprite_group):
            size = width, height = 500, 500
            dx = -(self.target.pos[0] - pygame.display.set_mode(size).get_rect().centerx)
            dy = -(self.target.pos[1] - pygame.display.set_mode(size).get_rect().centery)
            for obj in sprite_group:
                # if obj is not self.target:
                obj.rect.x += dx
                obj.rect.y += dy
            self.target.pos = pygame.display.set_mode(size).get_rect().center

    player = None
    player, level_x, level_y = generate_level(load_level('3lev.txt'))
    size = width, height = 500, 500
    fps = 70
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    camera = Camera(player)
    running = True
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                    move_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False
        screen.fill((0, 0, 0))
        if move_left:
            player.move(-5, 0)
            player.turn(0, 1)
        if move_right:
            player.move(5, 0)
            player.turn(1, 0)
        if move_up:
            player.move(0, -5)
            player.turn(0, 0, 1)
        if move_down:
            player.move(0, 5)
            player.turn(0, 0, 0, 1)
        camera.apply(all_sprites)
        all_sprites.draw(screen)
        all_sprites.update()
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

def ende_screen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 560))
    fps = 70
    running = True
    intro_text = ["Get Out",
                  "", "Вы погибли от смеха",
                  "Когда увидели троля",
                  "", "", "Пробел - попробовать снова",
                  "", "Escape - пойти домой"
                  ]
    font = pygame.font.Font(None, 40)
    text_coord = 50
    black = (65, 105, 225)
    screen.fill((255, 204, 153))
    for line in intro_text:
        string_rendered = font.render(line, True, (65, 105, 225))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    startlevv_srceen()
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(fps)

#Заключительный экран

def startt_screen():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 560))
    fps = 70
    running = True
    intro_text = ["Get Out",
                  "", "Поздравляю вы выбрались ,",
                  "Можете поправу назвать себя",
                  "Воином",
                  "", "", "Пробел - если вам не хватило",
                  "", "Escape - уйти с почётом"
                  ]
    font = pygame.font.Font(None, 40)
    text_coord = 50
    black = (65, 105, 225)
    screen.fill((255, 204, 153))
    for line in intro_text:
        string_rendered = font.render(line, True, (65, 105, 225))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    start_screen()
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(fps)

start_screen()
