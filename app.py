import pygame
import random
import time
 
pygame.init()
 
# Colors
HVIT = (255, 255, 255)
SVART = (0, 0, 0)
BLA = (0, 0, 255)
ROD = (255, 0, 0)
GRA = (195, 195, 195)
 
# Screen settings
BREDDE, HOYDE = 600, 600
vindu = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("Memory Spill")
font = pygame.font.Font(None, 30)
 
kort_storrelse = 100
margin = 20

 #possisjonerer kortene i vinduet
def kort_posisjon():
    pos = []
    for i in range(4):
        for j in range(4):
            x = margin + j * (kort_storrelse + margin)
            y = margin + i * (kort_storrelse + margin)
            pos.append((x, y))
    return pos
 
posisjoner = kort_posisjon()
 
 # genererer kortene (alltid i par)
def generate_pairs():
    symboler = [
        pygame.transform.scale(pygame.image.load('images/Mexico.png'), (kort_storrelse, kort_storrelse)),
        pygame.transform.scale(pygame.image.load('images/Albania.png'), (kort_storrelse, kort_storrelse)),
        pygame.transform.scale(pygame.image.load('images/Norway.png'), (kort_storrelse, kort_storrelse)),
        pygame.transform.scale(pygame.image.load('images/Sweden.png'), (kort_storrelse, kort_storrelse)),
        pygame.transform.scale(pygame.image.load('images/Germany.png'), (kort_storrelse, kort_storrelse)),
        pygame.transform.scale(pygame.image.load('images/France.png'), (kort_storrelse, kort_storrelse)),
        pygame.transform.scale(pygame.image.load('images/Spain.png'), (kort_storrelse, kort_storrelse)),
        pygame.transform.scale(pygame.image.load('images/Italy.png'), (kort_storrelse, kort_storrelse))
    ]
 
    symboler *= 2
    random.shuffle(symboler)
    return symboler
 
par = generate_pairs()
 
class Kort:
    def __init__(self, symbol, posisjon):
        self.symbol = symbol
        self.posisjon = posisjon
        self.rect = pygame.Rect(posisjon[0], posisjon[1], kort_storrelse, kort_storrelse)
        self.vist = False
        self.matcha = False
 
    def hent(self, vindu):
        if self.vist or self.matcha:
            pygame.draw.rect(vindu, HVIT, self.rect)  # Draw the card background
            vindu.blit(self.symbol, self.posisjon)  # Display the image symbol
        else:
            pygame.draw.rect(vindu, BLA, self.rect)  # Draw the back of the card
 
kortene = [Kort(par[i], posisjoner[i]) for i in range(16)]
 
# Game variables
forste_kort = None
andre_kort = None
par_riktig = 0
antall = 0
run = True
klokke = pygame.time.Clock()
venter = False # forteller spillet at det skal vente litt før reset
selected_card = None
state = 'start' # can be start, play or end
 


def start_game():
    global state
    # Show all cards for memorization at the start
    for Kort in kortene:
        Kort.vist = True

    for Kort in kortene:
        Kort.hent(vindu)
    
    vindu.blit(font.render("Husk parene!!", True, ROD), (10, 500))
    pygame.display.flip()
    
    # vent 500 ms, så skjuler vi kortene og setter state til play
    pygame.time.wait(5000)
    for Kort in kortene:
        Kort.vist = False
    state = 'play'
    return True

 
# Hide the cards again
for Kort in kortene:
    Kort.vist = False
# itererer over all events i pygame og returnerer.
def get_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event
        if event.type == pygame.MOUSEBUTTONDOWN:
            return event
    return None


def get_card(event) -> Kort:
    for Kort in kortene:
        if Kort.rect.collidepoint(event.pos) and not Kort.vist and not Kort.matcha:
           return Kort
    return None

def check_match(card1:Kort, card2: Kort):
    return card1.symbol == card2.symbol

def fail_handler(card1:Kort, card2:Kort):
    card1.vist = False
    card2.vist = False
   
def success_handler(card1:Kort, card2:Kort):
    card1.matcha = True
    card2.matcha = True

# Main game loop
while run:
    vindu.fill(GRA)

    if state == 'start':
        start_game()
    elif state == 'play':
    # sjekk alle events i pygame
        event = get_event()
        if event and event.type == pygame.QUIT:
            run = False
        elif event and event.type == pygame.MOUSEBUTTONDOWN:
            # sjekk om det er et kort som er klikket på
            clicked_card = get_card(event)
            # et kort har blitt klikket på
            if clicked_card is not None:
                clicked_card.vist = True
                # ingen kort er valgt (det er det første klikket)
                if selected_card is None:
                    selected_card = clicked_card
                # et kort er allerede valgt (det er det andre klikket)
                else:
                    venter = True

        # iterate over and show all cards marked to be shown
        for Kort in kortene:
            Kort.hent(vindu)              
        # update the display
        pygame.display.flip()
        klokke.tick(30)   


        # venter forteller oss at vi ikke skal gå videre før vi har ventet 500ms
        if venter:
            pygame.time.wait(500)
            if check_match(selected_card, clicked_card):
                success_handler(selected_card, clicked_card)
                par_riktig += 1
            else:
                fail_handler(selected_card, clicked_card)
            selected_card = None
            clicked_card = None
            venter = False



     
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            run = False
#        elif event.type == pygame.MOUSEBUTTONDOWN and not venter:
            # if forste_kort is None:
            #     for Kort in kortene:
            #         if Kort.rect.collidepoint(event.pos) and not Kort.vist and not Kort.matcha:
            #             forste_kort = Kort
            #             Kort.vist = True
            # elif andre_kort is None:
            #     for Kort in kortene:
            #         if Kort.rect.collidepoint(event.pos) and not Kort.vist and not Kort.matcha:
            #             andre_kort = Kort
            #             Kort.vist = True
            #             antall += 1
            #             venter = True
    # if venter:
    #     pygame.time.wait(500)
    #     if forste_kort.symbol == andre_kort.symbol:
    #         forste_kort.matcha = True
    #         andre_kort.matcha = True
    #         par_riktig += 1
    #     else:
    #         forste_kort.vist = False
    #         andre_kort.vist = False
    #     forste_kort = None
    #     andre_kort = None
    #     venter = False
 

    # oppdater score underveis
    text = font.render(f"Par funnet: {par_riktig} Forsøk: {antall}", True, ROD)
    vindu.blit(text, (10, 500))
    # sjekk om du har vunnet
    if par_riktig == 8:
        vinne = font.render("DU VANT!", True, BLA)
        vindu.blit(vinne, (BREDDE // 2 - 100, HOYDE // 2 - 50))
 

 
pygame.quit()