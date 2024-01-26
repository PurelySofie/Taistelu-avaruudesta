WIDTH = 1920
HEIGHT = 1080

alien = Actor('alien')
alien.pos = 100, 56

def draw():
    screen.fill((128, 0, 0))
    alien.draw()

