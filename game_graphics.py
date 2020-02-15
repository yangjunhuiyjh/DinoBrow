import pygame


class GameGraphics:
    def __init__(self,game):
        self.game = game

        self.size_x = 1280
        self.size_y = 720
        pygame.init()
        self.game_display = pygame.display.set_mode((self.size_x, self.size_y))

        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Dino')

        self.background = pygame.Surface(self.game_display.get_size())
        self.background.fill((255, 255, 255))

        self.ground_len = 1200

        self.ground_x = 50
        self.ground_y = 300

        self.graph_ratio = self.ground_len / self.game.max_pos

        self.dino_img = pygame.image.load('dino.png')
        self.dino_size_x = 100
        self.dino_size_y = 100
        self.dino_img = pygame.transform.scale(self.dino_img, (self.dino_size_x, self.dino_size_y))

        self.tree_img = pygame.image.load('tree.png')
        self.tree_size_y = game.tree_height * self.graph_ratio
        self.tree_size_x = self.tree_size_y
        self.tree_img = pygame.transform.scale(self.tree_img, (int(self.tree_size_x), int(self.tree_size_y)))

    def draw(self):
        pygame.draw.rect(self.background, (0, 0, 0), (self.ground_x, self.ground_y, self.ground_len, 5))
        self.game_display.blit(self.background, (0,0))

        dino_pos_x = self.game.dino_pos * self.graph_ratio + self.ground_x
        dino_pos_y = self.ground_y - self.dino_size_y + -self.graph_ratio * self.game.dino_y
        self.game_display.blit(self.dino_img, (dino_pos_x, dino_pos_y))

        for tree_pos in self.game.trees:
            tree_pos_x = tree_pos * self.graph_ratio + self.ground_x
            tree_pos_y = self.ground_y - self.tree_size_y
            self.game_display.blit(self.tree_img, (tree_pos_x, tree_pos_y))


        pygame.display.update()
        self.clock.tick(60)

    def stop(self):
        pygame.quit()
        quit()