#!/usr/bin/env python
__file__       = "gui_pygame.py"
__author__     = "Ka Wa Tsang"
__copyright__  = "Copyright 2019"
__version__    = "1.0.1"
__email__      = "kwtsang@nikhef.nl"
__date__       = "2019 Feb 28"

Description=""" A simple gui to play the board game.
"""

#================================================================
# Module
#================================================================
import os, sys
import numpy as np
import pygame
from pygame.locals import *

#================================================================
# Main
#================================================================
# Basic parameters
Color_dict = {}
Color_dict["white"] = (255,255,255)
Color_dict["black"] = (0,0,0)
Color_dict["brown"] = (160,82,45)
Color_dict["red"]   = (255,0,0)

class Board_gui:
  def __init__(self,
          Nrow = 6,
          Ncol = 7,
          FPS = 30,
          SCREENX = 800,
          SCREENY = 800,
          XGAP = [0,0],
          YGAP = [100,0],
          Color_screen = Color_dict["brown"],
          Color_line = Color_dict["black"],
          Color_font = Color_dict["black"],
          dualgrid = False,
          ):
    self.Nrow = Nrow
    self.Ncol = Ncol
    self.FPS = FPS
    self.SCREENX = SCREENX
    self.SCREENY = SCREENY
    self.XGAP = XGAP
    self.YGAP = YGAP
    self.Color_screen = Color_screen
    self.Color_line = Color_line
    self.Color_font = Color_font
    self.dualgrid = dualgrid

    self.FULL_SCREENX = self.SCREENX + self.XGAP[0] + self.XGAP[1]
    self.FULL_SCREENY = self.SCREENY + self.YGAP[0] + self.YGAP[1]
    #self.SCREEN = pygame.display.set_mode((FULL_SCREENX, FULL_SCREENY),HWSURFACE|DOUBLEBUF|RESIZABLE)
    self.SCREEN = pygame.display.set_mode((self.FULL_SCREENX, self.FULL_SCREENY))
    self.SCREEN.fill(self.Color_screen)
    self.BOARDX = [self.SCREENX*0.1 + self.XGAP[0], self.SCREENX*0.9 + self.XGAP[0]]
    self.BOARDY = [self.SCREENY*0.1 + self.YGAP[0], self.SCREENY*0.9 + self.YGAP[0]]
    self.colLines = np.linspace(self.BOARDX[0], self.BOARDX[1], self.Ncol+1)
    self.rowLines = np.linspace(self.BOARDY[0], self.BOARDY[1], self.Nrow+1)
    self.MidptColLines = 0.5*(self.colLines[1:] + self.colLines[:-1])
    self.MidptRowLines = 0.5*(self.rowLines[1:] + self.rowLines[:-1])
    dx = self.colLines[1] - self.colLines[0]
    dy = self.rowLines[1] - self.rowLines[0]
    self.stone_radius = int(min(dx,dy)*0.4)
    self.line_width = int(min(dx,dy)*0.05)

    pygame.init()
    pygame.display.set_caption('My FiveFiveShortTermMemory Platform')
    self.FPSCLOCK = pygame.time.Clock()
    self.draw_board()

  #================================================================
  # Top part
  #================================================================
  def clean_top(self):
    pygame.draw.rect(self.SCREEN, self.Color_screen, [0, 0, self.FULL_SCREENX, self.BOARDY[0]*0.99])

  def draw_names(self,
          name_player1,
          name_player2,
          current_player=1,
          winner=[False,0],
          score=None,
          ):
    self.clean_top()
    # Draw fonts
    display1 = ""
    display2 = ""
    if not winner[0]:
      if score:
        display1 += "%.1f " % score[1]
        display2 += "%.1f " % score[-1]
      if current_player == 1:
        display1 += "=>"
        display2 += "  "
      elif current_player == -1 or current_player == 2:
        display1 += "  "
        display2 += "=>"
      else:
        display1 += "  "
        display2 += "  "
      display1 += " player1: %s" % name_player1[:22]
      display2 += " player2: %s" % name_player2[:22]
    else:
      if score:
        display1 += "%.1f" % score[1]
        display2 += "%.1f" % score[-1]
      else:
        display1 += "  "
        display2 += "  "
      display1 += " player1: %s" % name_player1[:22]
      display2 += " player2: %s" % name_player2[:22]
      if winner[1] == 1:
        display1 += " (Win)"
      elif winner[1] == -1 or winner[1] == 2:
        display2 += " (Win)"
      else:
        display1 += " (Draw)"
        display2 += " (Draw)"

    self.draw_fonts(display1, self.BOARDX[0], int(self.BOARDY[0]*0.33))
    self.draw_fonts(display2, self.BOARDX[0], int(self.BOARDY[0]*0.66))

  #================================================================
  # Body part
  #================================================================
  def draw_board(self):
    if self.dualgrid:
      for c in self.MidptColLines:
        pygame.draw.line(self.SCREEN, self.Color_line, (c,self.MidptRowLines[0]), (c,self.MidptRowLines[-1]), self.line_width)
      for r in self.MidptRowLines:
        pygame.draw.line(self.SCREEN, self.Color_line, (self.MidptColLines[0],r), (self.MidptColLines[-1],r), self.line_width)
    else:
      for c in self.colLines:
        pygame.draw.line(self.SCREEN, self.Color_line, (c,self.rowLines[0]), (c,self.rowLines[-1]), self.line_width)
      for r in self.rowLines:
        pygame.draw.line(self.SCREEN, self.Color_line, (self.colLines[0],r), (self.colLines[-1],r), self.line_width)
    pygame.display.update()

  def draw_stones(self, state, color="black", radius=1, draw_empty=False):
    if color == "empty":
        color = self.Color_screen
    self.draw_board()
    coord_color = np.argwhere(state == 0)
    if draw_empty:
      for cc in coord_color:
        self.move(cc, self.Color_screen, radius=radius)
    coord_color = np.argwhere(state == 1)
    for cc in coord_color:
      self.move(cc, Color_dict[color], radius=radius)
    pygame.display.update()

  def move(self, coord, color, radius=None):
    Nth_row, Nth_col = coord
    grid_x = int(self.MidptColLines[Nth_col])
    grid_y = int(self.MidptRowLines[Nth_row])
    draw_radius = self.stone_radius
    if radius:
      draw_radius = int(draw_radius*radius)
    pygame.draw.circle(self.SCREEN,color,(grid_x,grid_y),draw_radius)

  #================================================================
  # Utils
  #================================================================
  def draw_fonts(self, content, x, y, size=25, center_pos=False):
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(content, True, self.Color_font)
    if center_pos:
      dx = int(text.get_width()  * 0.5)
      dy = int(text.get_height() * 0.5)
      self.SCREEN.blit(text, (x-dx, y-dy))
    else:
      self.SCREEN.blit(text, (x, y))
    pygame.display.update()

  def asking_for_move(self, guess_state):
    while True:
      for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
          pygame.quit()
          sys.exit("User is terminating the gui ...")
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
          return guess_state, True
        elif event.type == pygame.MOUSEBUTTONUP:
          pos = pygame.mouse.get_pos()
          coord = self.pos_to_coord(pos)
          try:
            guess_state[coord] = 0 if guess_state[coord] else 1
          except:
            pass
          return guess_state, False
      pygame.display.update()
      self.FPSCLOCK.tick(self.FPS)

  def pos_to_coord(self, pos):
    if self.BOARDX[1] > pos[0] > self.BOARDX[0] and self.BOARDY[1] > pos[1] > self.BOARDY[0]:
      Nth_col = np.argmin(np.abs(self.MidptColLines-pos[0]))
      Nth_row = np.argmin(np.abs(self.MidptRowLines-pos[1]))
      return (Nth_row, Nth_col)
    else:
      return None, None

  def freeze(self):
    while True:
      for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
          pygame.quit()
          return 0
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
          return 0
      self.FPSCLOCK.tick(self.FPS)

if __name__ == '__main__':
  Board_gui()

