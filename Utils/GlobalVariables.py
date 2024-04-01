## GLOBAL VARIABLES
import pygame
import sys
import os

pygame.init()

Width = 1280
Height = 720

pygame.display.set_mode((Width, Height))

FPS = 60

Background_Color = (41, 41, 41)

Text_Forecolor = (255, 255, 255)
Text_Hovercolor = (0, 255, 255)

def font(size):
    return pygame.font.SysFont("Consolas", size)

Account_Username = ""
Account_ID = ""

Player_size_X = 64
Player_size_Y = 64

FirstPlayer_RightStandingImage = pygame.image.load(os.path.join(sys.path[0], './Assets/8BitAvatarStandingStill.png')).convert_alpha()
FirstPlayer_RightStandingImage = pygame.transform.scale(FirstPlayer_RightStandingImage, (Player_size_X, Player_size_Y))
FirstPlayer_LeftStandingImage = pygame.transform.flip(FirstPlayer_RightStandingImage, True, False)
FirstPlayer_RightRunningImage = pygame.image.load(os.path.join(sys.path[0], './Assets/8BitAvatarRunning.png')).convert_alpha()
FirstPlayer_RightRunningImage = pygame.transform.scale(FirstPlayer_RightRunningImage, (Player_size_X, Player_size_Y))
FirstPlayer_LeftRunningImage = pygame.transform.flip(FirstPlayer_RightRunningImage, True, False)

SecondPlayer_RightStandingImage = pygame.image.load(os.path.join(sys.path[0], './Assets/8BitAvatarStandingStill.png')).convert_alpha()
SecondPlayer_RightStandingImage = pygame.transform.scale(SecondPlayer_RightStandingImage, (Player_size_X, Player_size_Y))
SecondPlayer_LeftStandingImage = pygame.transform.flip(SecondPlayer_RightStandingImage, True, False)
SecondPlayer_RightRunningImage = pygame.image.load(os.path.join(sys.path[0], './Assets/8BitAvatarRunning.png')).convert_alpha()
SecondPlayer_RightRunningImage = pygame.transform.scale(SecondPlayer_RightRunningImage, (Player_size_X, Player_size_Y))
SecondPlayer_LeftRunningImage = pygame.transform.flip(SecondPlayer_RightRunningImage, True, False)