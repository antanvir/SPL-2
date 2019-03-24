# ===========Remaining Tasks======== #
#
import time
import sys
import random
import math
import pygame
from pygame.locals import *

class JigsawPuzzle():

	def pointerIsInSurface(mouseX, mouseY, TILE):
		if (TILE[0] <= mouseX <= TILE[2]) and (TILE[1] <= mouseY <= TILE[3]):
			return True
		return False


	pygame.init()
	start_time = pygame.time.get_ticks()

	
	deviceDisplay = pygame.display.Info()
	#display = pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE)
	#display = pygame.display.set_mode((0,0), pygame.RESIZABLE)
	display = pygame.display.set_mode((deviceDisplay.current_w, deviceDisplay.current_h), pygame.RESIZABLE)
	pygame.display.set_caption("JIGSAW PUZZLE : MAKING OBJECT FROM PIECES!")


	image = pygame.image.load("mango.jpg")
	width, height = image.get_size()

	IMAGE_SIZE = (width, height)
	DISPLAY_SIZE = (4*width, 3*height + height//2)

	#ver_gap = (height/2)/4
	ver_gap = (deviceDisplay.current_h/4)/4
	hor_gap = (width/2)/4
	#hor_gap = (deviceDisplay.current_w/2)/4

	COLUMNS = 2
	ROWS = 2

	TILE_WIDTH = int(width / COLUMNS) + 1
	TILE_HEIGHT = int(height / ROWS) + 1

	SILVER = (192, 192, 192)
	GRAY = (128, 128, 128)
	BLACK = (0, 0, 0)
	CUSTOM_DISPLAY = (30, 89, 94)
	FONT_COLOR = (0, 255, 0)

	silver_rect = pygame.Surface((TILE_WIDTH , TILE_HEIGHT))
	silver_rect.fill(SILVER)

	gray_rect = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
	gray_rect.fill(GRAY)

	black_rect = pygame.Surface((TILE_WIDTH , TILE_HEIGHT))
	black_rect.fill(BLACK)

	hor_line = pygame.Surface((width, 1))
	hor_line.fill(BLACK)
	ver_line = pygame.Surface((1, height))
	ver_line.fill(BLACK)

	ver_divider = pygame.Surface((1, deviceDisplay.current_h - 4*ver_gap))
	ver_divider.fill(SILVER)
	

	image1 = pygame.image.load("IMG-0.jpg")
	image2 = pygame.image.load("IMG-1.jpg")
	image3 = pygame.image.load("IMG-2.jpg")
	image4 = pygame.image.load("IMG-3.jpg")

	# display main picture & main-picture-divider from pieces
	display.fill(CUSTOM_DISPLAY)
	display.blit(image, (5.8*deviceDisplay.current_w/8, ver_gap))	
	display.blit(ver_divider, (5.2*deviceDisplay.current_w/8, ver_gap))	

	# positions of 4 piece images 
	display.blit(image1, (3*hor_gap, ver_gap))
	display.blit(image2, (4*hor_gap + TILE_WIDTH, ver_gap))
	display.blit(image3, (5*hor_gap + 2*TILE_WIDTH, ver_gap))
	display.blit(image4, (6*hor_gap + 3*TILE_WIDTH, ver_gap))

	# position of blank tiles to hold 4 pieces of images
	display.blit(silver_rect, (4*hor_gap + TILE_WIDTH, 2*height + ver_gap))
	display.blit(gray_rect, (4*hor_gap + 2*TILE_WIDTH + 1, 2*height + ver_gap))
	display.blit(gray_rect, (4*hor_gap + TILE_WIDTH, 2*height + ver_gap + TILE_HEIGHT+1))
	display.blit(silver_rect, (4*hor_gap + 2*TILE_WIDTH + 1, 2*height + ver_gap + TILE_HEIGHT+1))

	# TILE -> (left, top, right, bottom)
	IMAGE1_TILE = (3*hor_gap, ver_gap, 3*hor_gap + TILE_WIDTH, ver_gap+TILE_HEIGHT)
	IMAGE2_TILE = (4*hor_gap + TILE_WIDTH, ver_gap, 4*hor_gap + 2*TILE_WIDTH, ver_gap+TILE_HEIGHT)
	IMAGE3_TILE = (5*hor_gap + 2*TILE_WIDTH, ver_gap, 5*hor_gap + 3*TILE_WIDTH, ver_gap+TILE_HEIGHT)
	IMAGE4_TILE = (6*hor_gap + 3*TILE_WIDTH, ver_gap, 6*hor_gap + 4*TILE_WIDTH, ver_gap+TILE_HEIGHT)

	BLANK_TILE1 = (4*hor_gap + TILE_WIDTH, 2*height + ver_gap, 
					4*hor_gap + 2*TILE_WIDTH, 2*height + ver_gap + TILE_HEIGHT)
	BLANK_TILE2 = (4*hor_gap + 2*TILE_WIDTH + 1, 2*height + ver_gap, 
					4*hor_gap + 3*TILE_WIDTH + 1, 2*height + ver_gap + TILE_HEIGHT)
	BLANK_TILE3 = (4*hor_gap + TILE_WIDTH, 2*height + ver_gap + TILE_HEIGHT+1, 
					4*hor_gap + 2*TILE_WIDTH, 2*height + ver_gap + 2*TILE_HEIGHT)
	BLANK_TILE4 = (4*hor_gap + 2*TILE_WIDTH + 1, 2*height + ver_gap + TILE_HEIGHT+1, 
					4*hor_gap + 3*TILE_WIDTH + 1, 2*height + ver_gap + 2*TILE_HEIGHT)

	# black portion of the screen // Rect((left, top), (width, height))
	screen_middle = Rect((0, IMAGE1_TILE[3]), 
					(5.2*deviceDisplay.current_w/8 , BLANK_TILE1[1]-IMAGE1_TILE[3]) )
	screen_left = Rect((0, IMAGE1_TILE[3]), (BLANK_TILE1[0], deviceDisplay.current_h-IMAGE1_TILE[3])) 
	screen_right = Rect((BLANK_TILE2[2], IMAGE1_TILE[3]), 
					(5.2*deviceDisplay.current_w/8-BLANK_TILE2[2], deviceDisplay.current_h-IMAGE1_TILE[3]))
	screen_down = Rect((0, BLANK_TILE4[3]),
					(5.2*deviceDisplay.current_w/8 , deviceDisplay.current_h-BLANK_TILE4[3]))
	timer_screen = Rect((5.8*deviceDisplay.current_w/8, BLANK_TILE1[1]-ver_gap), (width, TILE_HEIGHT))

	left_button_pressed = False
	mouse_dragged = False

	image1_dragged, image2_dragged, image3_dragged, image4_dragged = False, False, False, False
	image1_placed, image2_placed, image3_placed, image4_placed = False, False, False, False

	timer = "00:00:00"
	pygame.font.init()
	gameFont = pygame.font.Font('freesansbold.ttf', 25)
	timerText = gameFont.render('Timer : ' + str(timer), False, FONT_COLOR)
	display.blit(timerText, (6*deviceDisplay.current_w/8, BLANK_TILE1[1]-ver_gap))

	pygame.display.flip()

	clock = pygame.time.Clock()

	while True:
		clock.tick(60)
		
		cur_time = pygame. time.get_ticks()
		#global start_time
		times = cur_time - start_time
		#global timer
		times = times%1000
		#print("timer: ", timer, "seconds: ", seconds)
		#timer += (seconds)
		hours = times / 3600

		times = times%3600
		minutes = times / 60
		times %= 60
		seconds = times 

		#displayTimer = math.trunc(seconds)
		displayTimer = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)


		display.fill(CUSTOM_DISPLAY, timer_screen)

		timerText = gameFont.render('Timer : ' + str(displayTimer), False, FONT_COLOR)
		display.blit(timerText, (6*deviceDisplay.current_w/8, BLANK_TILE1[1]-ver_gap))
		#pygame.display.update()

		for event in pygame.event.get():

			if event.type == QUIT:
				exit()

			elif event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1: 
				left_button_pressed = True

				mouseX, mouseY = pygame.mouse.get_pos()

				if pointerIsInSurface(mouseX, mouseY, IMAGE1_TILE) and image1_placed == False:
					image1_dragged = True
					display.blit(black_rect, (IMAGE1_TILE[0], IMAGE1_TILE[1]))
						
				elif pointerIsInSurface(mouseX, mouseY, IMAGE2_TILE) and image2_placed == False:
						image2_dragged = True
						display.blit(black_rect, (IMAGE2_TILE[0], IMAGE2_TILE[1]))

				elif pointerIsInSurface(mouseX, mouseY, IMAGE3_TILE) and image3_placed == False:
						image3_dragged = True
						display.blit(black_rect, (IMAGE3_TILE[0], IMAGE3_TILE[1]))

				elif pointerIsInSurface(mouseX, mouseY, IMAGE4_TILE) and image4_placed == False:
						image4_dragged = True
						display.blit(black_rect, (IMAGE4_TILE[0], IMAGE4_TILE[1]))

			

			elif mouse_dragged and event.type == pygame.MOUSEBUTTONUP:
				left_button_pressed = False
				mouse_dragged = False

				mouseX, mouseY = pygame.mouse.get_pos()

				if mouseX < BLANK_TILE1[0] and mouseY < BLANK_TILE1[1]:
					if image1_dragged:
						display.blit(image1, (IMAGE1_TILE[0], IMAGE1_TILE[1]))
						image1_dragged = False

					elif image2_dragged:
						display.blit(image2, (IMAGE2_TILE[0], IMAGE2_TILE[1]))
						image2_dragged = False

					elif image3_dragged:
						display.blit(image3, (IMAGE3_TILE[0], IMAGE3_TILE[1]))
						image3_dragged = False

					elif image4_dragged:
						display.blit(image4, (IMAGE4_TILE[0], IMAGE4_TILE[1]))
						image4_dragged = False

				else:
					if pointerIsInSurface(mouseX, mouseY, BLANK_TILE1):
						if image1_dragged:
							display.blit(image1, (BLANK_TILE1[0], BLANK_TILE1[1]))
							image1_placed = True

					elif pointerIsInSurface(mouseX, mouseY, BLANK_TILE2):
						if image2_dragged:
							display.blit(image2, (BLANK_TILE2[0], BLANK_TILE2[1]))
							image2_placed = True

					elif pointerIsInSurface(mouseX, mouseY, BLANK_TILE3):
						if image3_dragged:
							display.blit(image3, (BLANK_TILE3[0], BLANK_TILE3[1]))
							image3_placed = True

					elif pointerIsInSurface(mouseX, mouseY, BLANK_TILE4):
						if image4_dragged:
							display.blit(image4, (BLANK_TILE4[0], BLANK_TILE4[1]))
							image4_placed = True

					if image1_placed == False:
						display.blit(image1, (IMAGE1_TILE[0], IMAGE1_TILE[1]))

					if image2_placed == False:
						display.blit(image2, (IMAGE2_TILE[0], IMAGE2_TILE[1]))

					if image3_placed == False:
						display.blit(image3, (IMAGE3_TILE[0], IMAGE3_TILE[1]))

					if image4_placed == False:
						display.blit(image4, (IMAGE4_TILE[0], IMAGE4_TILE[1]))

					image1_dragged = False
					image2_dragged = False
					image3_dragged = False
					image4_dragged = False




			elif left_button_pressed and event.type == pygame.MOUSEMOTION:
				mouse_dragged = True

				mouseX, mouseY = pygame.mouse.get_pos()
				mouseX -= TILE_WIDTH / 2
				mouseY -= TILE_HEIGHT / 2

				if mouseY  > ver_gap + TILE_HEIGHT and mouseX < 5.2*deviceDisplay.current_w/8:
					if image1_dragged:
						display.blit(image1, (mouseX, mouseY))

					elif image2_dragged:
						display.blit(image2, (mouseX, mouseY))

					elif image3_dragged:
						display.blit(image3, (mouseX, mouseY))

					elif image4_dragged:
						display.blit(image4, (mouseX, mouseY))



			pygame.display.flip()
			display.fill(CUSTOM_DISPLAY, screen_middle)
			display.fill(CUSTOM_DISPLAY, screen_left)
			display.fill(CUSTOM_DISPLAY, screen_right)
			display.fill(CUSTOM_DISPLAY, screen_down)

			'''display.blit(hor_line, (4*hor_gap + TILE_WIDTH, 2*height + ver_gap + TILE_HEIGHT))
			display.blit(ver_line, (4*hor_gap + 2*TILE_WIDTH, 2*height + ver_gap))
			'''
			display.blit(hor_line, (BLANK_TILE1[0], BLANK_TILE1[1]+TILE_HEIGHT))
			display.blit(ver_line, (BLANK_TILE2[0]-1, BLANK_TILE2[1]-1))

			if image1_placed:
				display.blit(image1, (BLANK_TILE1[0], BLANK_TILE1[1]))
			else:
				display.blit(silver_rect, (BLANK_TILE1[0], BLANK_TILE1[1]))

			if image2_placed:
				display.blit(image2, (BLANK_TILE2[0], BLANK_TILE2[1]))
			else:
				display.blit(gray_rect, (BLANK_TILE2[0], BLANK_TILE2[1]))

			if image3_placed:
				display.blit(image3, (BLANK_TILE3[0], BLANK_TILE3[1])) 
			else:  
				display.blit(gray_rect, (BLANK_TILE3[0], BLANK_TILE3[1]))

			if image4_placed:
				display.blit(image4, (BLANK_TILE4[0], BLANK_TILE4[1]))
			else:
				display.blit(silver_rect, (BLANK_TILE4[0], BLANK_TILE4[1]))


if __name__ == "__main__":
	jigsaw = JigsawPuzzle()

