import Detector
import Game
import game_graphics
import pygame

def no_data(face_max, face_min, brow_ave_height):
    return face_max==0 and face_min==0 and brow_ave_height == 0


def main():
    detector = Detector.Detector()
    game = Game.Game(detector)


    is_calibrating = True
    ref_y = 0
    calib_count = 0


    while True:
        events = pygame.event.get()

        if is_calibrating:
            game.graphics.draw_calib(calib_count,ref_y)
            game.graphics.swap_buf()

            this_y = detector.getData()
            if this_y is None:
                continue

            print(this_y)
            ref_y = (ref_y*calib_count + this_y) / (calib_count+1)
            calib_count += 1

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        is_calibrating = False


        else:
            if not game.failed:
                game.graphics.drawFailure()
            else:
                game.step()
                game.graphics.draw()
            game.graphics.swap_buf()

            this_y = detector.getData()
            if (this_y-ref_y)/ref_y >= 0.1:
                game.jump()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        game.graphics.stop()
                        game = Game.Game(detector)



if __name__ == "__main__":
    main()