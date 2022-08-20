import pygame,sys
from pygame.locals import *
from random import randint

def loop():
  ancho = 900
  alto = 600
  Enemy_list = []

  class Spaceship(pygame.sprite.Sprite):

    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.ImageSpaceship = pygame.image.load("images_game/nave.jpg")
      self.ImageExplosion = pygame.image.load("images_game/explosion.jpg")

      self.rect = self.ImageSpaceship.get_rect()
      self.rect.centerx = ancho/2
      self.rect.centery = alto-30
      self.listShooting = []
      self.Life = True

      self.velocity = 20

      self.shootSound = pygame.mixer.Sound("music/shoot1.wav")
      self.explosionSound = pygame.mixer.Sound("music/Explosion.wav")

    def RightMovement(self):
      self.rect.right += self.velocity
      self.__Movements()

    def LeftMovement(self):
      self.rect.left -= self.velocity
      self.__Movements()

    def __Movements(self):
      if self.Life == True:
        if self.rect.left < 0:
          self.rect.left  = 30
        elif self.rect.right > 870:
          self.rect.right = 840

    def destruction(self):
      self.explosionSound.play()
      self.Life=False
      self.velocity=0
      self.ImageSpaceship = self.ImageExplosion

    def Shooter(self,x,y):
      bullet1 = Bullet(x,y,"images_game/disparoa.jpg",True)
      self.listShooting.append(bullet1)
      self.shootSound.play()

    def Draw(self,surface):
      surface.blit(self.ImageSpaceship,self.rect)

  class Bullet(pygame.sprite.Sprite):
    def __init__(self,posx,posy,route,character):
      pygame.sprite.Sprite.__init__(self)
      self.ImageBullet = pygame.image.load(route)
      self.rect = self.ImageBullet.get_rect()
      self.shooterVelocity = 5
      self.rect.top = posy
      self.rect.left = posx
      self.shooterCharacter = character

    def Trajectory(self):
      if self.shooterCharacter == True:
        self.rect.top -= self.shooterVelocity
      else:
        self.rect.top += self.shooterVelocity

    def Draw(self,surface):
      surface.blit(self.ImageBullet,self.rect)

  class Invader(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distance,image1,image2):
      pygame.sprite.Sprite.__init__(self)
      self.ImageA = pygame.image.load(image1)
      self.ImageB = pygame.image.load(image2)

      self.listImages = [self.ImageA,self.ImageB]
      self.posImage = 0
      self.ImageInvader = self.listImages[self.posImage]

      self.rect = self.ImageInvader.get_rect()

      self.shooterVelocity = 5
      self.velocity = 20
      self.listShooting = []
      self.rect.top = posy
      self.rect.left = posx

      self.rangeShoot = 1
      self.timeChange = 1

      self.conquista = False

      self.right = True
      self.counter = 0
      self.maxdown = self.rect.top+40
      self.rightlimit = posx + distance
      self.leftlimit = posx - distance

    def __Movements(self):
      if self.counter < 3:
        self.__lateralmovement()
      else:
        self.__downMovement()

    def __downMovement(self):
      if self.maxdown == self.rect.top:
        self.counter = 0
        self.maxdown = self.rect.top + 40
      else:
        self.rect.top += 1

    def __lateralmovement(self):
      if self.right == True:
        self.rect.left = self.rect.left + self.velocity
        if self.rect.left > self.rightlimit:
          self.right = False
          self.counter += 1
      else:
        self.rect.left = self.rect.left -self.velocity
        if self.rect.left < self.leftlimit:
          self.right = True

    def Behaviour(self,time):
      if self.conquista == False:
        self.__Movements()
        self.__Attack()
        if self.timeChange == time:
          self.posImage += 1
          self.timeChange += 1

          if self.posImage > len(self.listImages)-1:
            self.posImage = 0

    def Draw(self,surface):
      self.ImageInvader = self.listImages[self.posImage]
      surface.blit(self.ImageInvader,self.rect)

    def __Attack(self):
      if (randint(0,100)<self.rangeShoot):
        self.__Shoot()

    def __Shoot(self):
      x,y = self.rect.center
      bullet1 = Bullet(x,y,"images_game/disparob.jpg",False)
      self.listShooting.append(bullet1)

  def stopAll():
    for enemy in Enemy_list:
      for Shooter in enemy.listShooting:
        enemy.listShooting.remove(Shooter)
      enemy.conquista = True

  def loadEnemies():
    posx = 100
    for x in range(1,5):
      enemy = Invader(posx,100,40,'images_game/marcianoA.jpg','images_game/MarcianoB.jpg')
      Enemy_list.append(enemy)
      posx = posx + 200
    posx = 100
    for x in range(1,5):
      enemy = Invader(posx,0,40,'images_game/Marciano2A.jpg','images_game/Marciano2B.jpg')
      Enemy_list.append(enemy)
      posx = posx + 200
    posx = 100
    for x in range(1,5):
      enemy = Invader(posx,-100,40,'images_game/Marciano3A.jpg','images_game/Marciano3B.jpg')
      Enemy_list.append(enemy)
      posx = posx + 200

  def SpaceInvader():
    pygame.init()
    window=pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Space Invader")
    ImageBackground = pygame.image.load("images_game/Fondo.jpg")

    pygame.mixer.music.load('music/intro1.mp3')
    pygame.mixer.music.play(100)

    miFuenteSistema = pygame.font.SysFont("Arial",30)
    Texto = miFuenteSistema.render("Game Over!",0,(120,100,40))
    miFuenteSistema1 = pygame.font.SysFont("Arial",30)
    Texto1 = miFuenteSistema.render("You win!",0,(120,100,40))

    player = Spaceship()
    loadEnemies()
    ongoing = True
    timer = pygame.time.Clock()
    playing = True

    while playing:
      timer.tick(60)
      time = int(pygame.time.get_ticks()/1000)

      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        if ongoing == True:
          if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
              player.LeftMovement()

            elif event.key == K_RIGHT:
              player.RightMovement()

            elif event.key == K_SPACE:
              x,y = player.rect.center
              player.Shooter(x,y)


      window.blit(ImageBackground,(0,0))
      player.Draw(window)
      if len(player.listShooting)>0:
        for x in player.listShooting:
          x.Draw(window)
          x.Trajectory()
          if x.rect.top<0:
            player.listShooting.remove(x)
          else:
            for enemy in Enemy_list:
              if x.rect.colliderect(enemy.rect):
                Enemy_list.remove(enemy)
                player.listShooting.remove(x)

      if len(Enemy_list)==0:
        pygame.mixer.music.fadeout(3000)
        window.blit(Texto1,(300,300))

      if len(Enemy_list)>0:
        for enemy in Enemy_list:
          enemy.Behaviour(time)
          enemy.Draw(window)
          if enemy.rect.colliderect(player.rect):
            player.destruction()
            ongoing=False
            stopAll()

          if len(enemy.listShooting)>0:
            for x in enemy.listShooting:
              x.Draw(window)
              x.Trajectory()
              if x.rect.colliderect(player.rect):
                player.destruction()
                ongoing=False
                stopAll()

              if x.rect.top>900:
                enemy.listShooting.remove(x)
              else:
                for Shooter in player.listShooting:
                  if x.rect.colliderect(Shooter.rect):
                    player.listShooting.remove(Shooter)
                    enemy.listShooting.remove(x)


      if ongoing == False:
        pygame.mixer.music.fadeout(3000)
        window.blit(Texto,(300,300))

      pygame.display.update()

  SpaceInvader()
loop()
