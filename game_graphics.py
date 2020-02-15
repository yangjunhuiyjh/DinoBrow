import pygame
import cv2
import numpy

class GameGraphics:
    def __init__(self,game):
        self.game = game
        self.detector = game.detector

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

        self.figure_x = 50
        self.figure_y = 50
        self.figure_size_x = 150

        self.figure_img = None



        self.dino_img = pygame.image.load('dino.png')
        self.dino_size_x = 100
        self.dino_size_y = 100
        self.dino_img = pygame.transform.scale(self.dino_img, (self.dino_size_x, self.dino_size_y))

        self.tree_img = pygame.image.load('tree.png')
        self.tree_size_y = game.tree_height * self.graph_ratio
        self.tree_size_x = self.tree_size_y
        self.tree_img = pygame.transform.scale(self.tree_img, (int(self.tree_size_x), int(self.tree_size_y)))

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def draw(self):
        self.game_display.fill((255,255,255))

        pygame.draw.rect(self.background, (0, 0, 0), (self.ground_x, self.ground_y, self.ground_len, 5))
        self.game_display.blit(self.background, (0, 0))

        self.figure_img = self.detector.getLastFrame()
        self.figure_img = cv2.cvtColor(self.figure_img, cv2.COLOR_BGR2RGB)
        self.figure_img = numpy.rot90(self.figure_img)
        img_ratio = self.figure_img.shape[1]/self.figure_img.shape[0]
        self.figure_img = pygame.surfarray.make_surface(self.figure_img)
        self.figure_img = pygame.transform.scale(self.figure_img, (self.figure_size_x, int(self.figure_size_x*img_ratio)))

        dino_pos_x = self.game.dino_pos * self.graph_ratio + self.ground_x
        dino_pos_y = self.ground_y - self.dino_size_y + -self.graph_ratio * self.game.dino_y
        self.game_display.blit(self.dino_img, (dino_pos_x, dino_pos_y))

        figure_pos_x = self.figure_x
        figure_pos_y = self.figure_y
        self.game_display.blit(self.figure_img, (figure_pos_x, figure_pos_y))

        for tree_pos in self.game.trees:
            tree_pos_x = tree_pos * self.graph_ratio + self.ground_x
            tree_pos_y = self.ground_y - self.tree_size_y
            self.game_display.blit(self.tree_img, (tree_pos_x, tree_pos_y))


    def drawFailure(self):
        textsurface = self.font.render('Lost', False, (0, 0, 0))
        self.game_display.blit(textsurface, (self.size_x/2, self.size_y/10))

    def draw_calib(self,calib_count,ref_y):

        self.game_display.blit(self.background, (0, 0))
        text = 'Calibrating, #datapoints: '+ str(calib_count)+"    ref_y:"+str(ref_y)
        textsurface = self.font.render(text, False, (0, 0, 0))
        self.game_display.blit(textsurface, (0, self.size_y / 10))

        text = 'Click s to start!'
        textsurface = self.font.render(text, False, (0, 0, 0))
        self.game_display.blit(textsurface, (0, self.size_y / 2))

    def swap_buf(self):
        pygame.display.update()
        self.clock.tick(60)


    def stop(self):
        pygame.quit()
