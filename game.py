import random
import  game_graphics
import  pygame
class Game:
    def __init__(self):
        self.trees = [60, 90]
        self.dino_pos = 20
        self.min_pos = 0
        self.max_pos = 100

        self.new_tree_prob = 0.01


        self.dino_y = 0
        self.dino_dy = 0

        self.speed_x = -30

        self.tree_height = 6

        self.graphics = game_graphics.GameGraphics(self)


    def step(self):
        dt = 0.016

        g = -200
        self.dino_y += self.dino_dy * dt
        self.dino_dy += g * dt
        if self.dino_y < 0:
            self.dino_y = 0
            self.dino_dy = 0

        new_trees = []

        for tree_pos in self.trees:
            tree_pos += dt * self.speed_x
            if tree_pos < self.min_pos or tree_pos >= self.max_pos:
                pass
            else:
                new_trees.append(tree_pos)

        self.trees = new_trees

        rand_float = random.random()
        if rand_float <= self.new_tree_prob:
            self.trees.append(self.max_pos - 1)


    def jump(self):
        print(self.dino_y)
        if self.dino_y == 0:
            self.dino_dy = 60

if __name__ == "__main__":
    game = Game()
    while True:
        game.step()
        game.graphics.draw()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.jump()
                if event.key == pygame.K_ESCAPE:
                    game.graphics.stop()