from lib_load_image import load_image
import pygame

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tiles_group, all_sprites):
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dx, dy):
        self.rect.x -= dx * tile_width
        self.rect.y -= dy * tile_height
        if self.rect.x < 0:
            self.rect.x = 9 * tile_width + dx * tile_width
        elif self.rect.x > 11 * tile_width:
            self.rect.x = -dx * tile_width
        if self.rect.y > 11 * tile_height:
            self.rect.y = -dy * tile_height
        elif self.rect.y < 0:
            self.rect.y = 9 * tile_height + dy * tile_height


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_group, all_sprites):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.direction = None
        self.x = pos_x
        self.y = pos_y

    def move(self, dx, dy, tiles_group):
        self.rect.x += dx * tile_width
        self.rect.y += dy * tile_height
        for i in pygame.sprite.spritecollide(self, tiles_group, False):
            tile_type = getattr(i, 'tile_type', None)
            if tile_type == 'wall':
                self.rect.x -= dx * tile_width
                self.rect.y -= dy * tile_height
            else:
                self.rect.x -= dx * tile_width
                self.rect.y -= dy * tile_height
                tiles_group.update(dx, dy)


def generate_level(level, player_group, tiles_group, all_sprites):
    new_player, player_x, player_y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, tiles_group, all_sprites)
            elif level[y][x] == '#':
                Tile('wall', x, y, tiles_group, all_sprites)
            elif level[y][x] == '@':
                Tile('empty', x, y, tiles_group, all_sprites)
                new_player = Player(x, y, player_group, all_sprites)
                player_x, player_y = x, y
    # вернем игрока, а также размер поля в клетках
    return new_player, player_x, player_y
