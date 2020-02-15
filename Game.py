import random
import  game_graphics
import  pygame
import  math

class Game:
    def __init__(self,detector):
        self.trees = [60, 90]
        self.dino_pos = 20
        self.min_pos = 0
        self.max_pos = 100

        self.trees2 = [60, 90]
        self.dino_pos2 = 20

        self.new_tree_prob = 0.01


        self.dino_y = 0
        self.dino_dy = 0

        self.dino_y2 = 0
        self.dino_dy2 = 0

        self.speed_x = -30

        self.tree_height = 6


        self.failed = True
        self.failed2 = True

        self.detector = detector

        self.graphics = game_graphics.GameGraphics(self)


    def step(self):
        dt = 0.016

        g = -200
        self.dino_y += self.dino_dy * dt
        self.dino_dy += g * dt
        if self.dino_y < 0:
            self.dino_y = 0
            self.dino_dy = 0

        self.dino_y2 += self.dino_dy2 * dt
        self.dino_dy2 += g * dt
        if self.dino_y2 < 0:
            self.dino_y2 = 0
            self.dino_dy2 = 0

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
            if len(self.trees)>0:
                prev_tree_pos = self.trees[-1]
            else:
                prev_tree_pos = 0
            if self.max_pos - prev_tree_pos > 20 or self.max_pos - prev_tree_pos < 8:
                self.trees.append(self.max_pos - 1)

        self.trees2 = self.trees

        self.check_failure()

    def check_failure(self):
        for tree_pos in self.trees:
            x_diff = tree_pos - self.dino_pos
            y_diff = self.dino_y
            dist =  math.sqrt(x_diff*x_diff + y_diff*y_diff)
            if dist < self.tree_height * 0.5:
                self.failed = False
    
    def check_failure2(self):
        for tree_pos2 in self.trees2:
            x_diff = tree_pos2 - self.dino_pos2
            y_diff = self.dino_y2
            dist = math.sqrt(x_diff*x_diff + y_diff*y_diff)
            if dist < self.tree_height * 0.5:
                self.failed2 = False

    def jump(self):
        print(self.dino_y)
        if self.dino_y == 0:
            self.dino_dy = 60
    
    def jump2(self):
        print(self.diino_y2)
        if self.dino_y2 == 0:
            self.dino_dy2 = 60



if __name__ == "__main__":
    game = Game()
    while True:
        if not game.failed:
            game.graphics.drawFailure()
        else:
            game.step()
            game.graphics.draw()
        game.graphics.swap_buf()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.jump()
                if event.key == pygame.K_ESCAPE:
                    game.graphics.stop()
