import pygame
import sys
#initialising screen
pygame.init()
SCREENDIMENSIONS = (900, 900)
screen = pygame.display.set_mode((SCREENDIMENSIONS[0], SCREENDIMENSIONS[1]))
pygame.display.set_caption('tic-tac-toe!')
clock = pygame.time.Clock()

turn = "circle"

#list of cross and circle locations
crossLocation = list()
circleLocation = list()

#initialising circles and crosses
circle_surface = pygame.image.load("circle.png").convert_alpha()
circle_rect = circle_surface.get_rect(center=(0,0))
cross_surface = pygame.image.load("cross.png").convert_alpha()
cross_rect = cross_surface.get_rect(center=(0,0))
board_surface = pygame.image.load('3x3 board.png').convert_alpha()


#shows the 3x3 board
def showBoard(board_surface):
    board_rect = board_surface.get_rect(center=(450,450))
    screen.blit(board_surface, board_rect)


#converts coordinates to numbers so its easier to do the logic calculations
CoordsToLabel = {(150, 150):1,
                 (450, 150):2,
                 (750, 150):3,
                 (150, 450):4,
                 (450, 450):5,
                 (750, 450):6,
                 (150, 750):7,
                 (450, 750):8,
                 (750, 750):9}


#gets the center coord of each square where mouse is clicked
def getPos(mouse_pos):
    x = mouse_pos[0]
    y = mouse_pos[1]
    coord = set()
    if y<=300:
        if x<=300:return (150, 150)
        elif x<600:return (450, 150)
        else:return (750, 150)
    elif y<=600:
        if x<=300:return (150, 450)
        elif x<600:return (450, 450)
        else:return (750, 450)
    else:
        if x<=300:return (150, 750)
        elif x<600:return (450, 750)
        else:return (750, 750)


#iterates through the circleLocation and crossLocation lists and displays all of them
def showMarker():
    for location in circleLocation:
        circle_rect = circle_surface.get_rect(center=location)
        screen.blit(circle_surface, circle_rect)
    for location in crossLocation:
        cross_rect = cross_surface.get_rect(center=location)
        screen.blit(cross_surface, cross_rect)
    pygame.display.flip()



#we have a list of circle and cross coordinates and a list of possible triplet combinations
#if all the items of a triplet are found in either cross or circle's list of coordinate game finish
triplets = list()
def findWinner():
    winner = str()
    circleNumLocation = list(map(lambda coord:CoordsToLabel.get(coord), circleLocation))
    crossNumLocation = list(map(lambda coord:CoordsToLabel.get(coord), crossLocation))

    #Horizontal
    for row in range(3):
        triplet = [row * 3 + 1, row * 3 + 2, row * 3 + 3]
        triplets.append(triplet)

    #Vertical
    for column in range(1, 4):
        triplet = [column, column + 3, column + 6]
        triplets.append(triplet)

    #diagonal
    triplets.append([1,5,9])
    triplets.append([3,5,7])

    for triplet in triplets:
        if all(item in circleNumLocation for item in triplet):
            winner = "circle"
            return winner
        elif all(item in crossNumLocation for item in triplet):
            winner = "cross"
            return winner
    return False


#text surface that displays winner
def displayWinnerStatus(winner):
    text_font = pygame.font.Font(None, 50)
    if winner in ['circle', 'cross']:
        text_surface = text_font.render(f"{winner} won!", True, 'Red')
        text_rect = text_surface.get_rect(center=(450, 50))
        screen.blit(text_surface, text_rect)
    else:
        text_surface = text_font.render("Its a draw!", True, 'Red')
        text_rect = text_surface.get_rect(center=(450, 50))
        screen.blit(text_surface, text_rect)
    
        
#clicks is the times a symbol is added (max=9)
clicks = 0
while True:
    showBoard(board_surface)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                coord = getPos(mouse_pos)
                #if coordinate is already clicked...
                if coord in circleLocation or coord in crossLocation:
                    print("invalid location")
                else:
                    #appends the coord to the list, and switches the turn
                    clicks += 1
                    if turn == "circle":
                        circleLocation.append(coord)
                        turn = "cross"
                    elif turn == "cross":
                        crossLocation.append(coord)
                        turn = "circle"
                          
    showMarker()
    winner = findWinner()
    #check if game over
    if clicks > 2:
        if winner != False or clicks == 9:
            displayWinnerStatus(winner)
            
    pygame.display.update()
    clock.tick(60)
        
