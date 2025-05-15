import pygame
import random
import os
from PIL import Image

# 게임 초기화
pygame.init()

# 상수 정의
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 140
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("포켓몬 카드 게임")
clock = pygame.time.Clock()

class Card:
    def __init__(self, name, hp, attack, defense, image_path=None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.image_path = image_path
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        self.selected = False
        self.face_up = False
        
    def draw(self, surface, x, y):
        self.rect.x = x
        self.rect.y = y
        
        # 카드 배경
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        if self.face_up:
            # 카드 정보 표시
            font = pygame.font.SysFont('malgungothic', 12)
            name_text = font.render(self.name, True, BLACK)
            hp_text = font.render(f"HP: {self.hp}", True, BLACK)
            attack_text = font.render(f"공격: {self.attack}", True, BLACK)
            defense_text = font.render(f"방어: {self.defense}", True, BLACK)
            
            surface.blit(name_text, (x + 5, y + 5))
            surface.blit(hp_text, (x + 5, y + 25))
            surface.blit(attack_text, (x + 5, y + 45))
            surface.blit(defense_text, (x + 5, y + 65))
        else:
            # 카드 뒷면
            font = pygame.font.SysFont('malgungothic', 20)
            text = font.render("?", True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.field = []
        self.deck = []
        self.hp = 30
        
    def draw_card(self):
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)
            return True
        return False
    
    def play_card(self, card_index):
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            self.field.append(card)
            return True
        return False

class Game:
    def __init__(self):
        self.player = Player("플레이어")
        self.computer = Player("컴퓨터")
        self.current_player = self.player
        self.selected_card = None
        self.game_state = "playing"  # playing, game_over
        self.initialize_decks()
        
    def initialize_decks(self):
        # 포켓몬 카드 데이터
        pokemon_data = [
            ("피카츄", 60, 20, 10),
            ("이상해씨", 50, 15, 15),
            ("파이리", 55, 25, 5),
            ("꼬부기", 65, 10, 20),
            ("푸린", 70, 5, 25),
            ("고라파덕", 45, 30, 5),
            ("냐옹", 40, 35, 5),
            ("디그다", 30, 40, 5),
        ]
        
        # 덱 초기화
        for _ in range(20):  # 각 플레이어당 20장의 카드
            for pokemon in pokemon_data:
                self.player.deck.append(Card(*pokemon))
                self.computer.deck.append(Card(*pokemon))
        
        # 덱 섞기
        random.shuffle(self.player.deck)
        random.shuffle(self.computer.deck)
        
        # 시작 카드 5장 뽑기
        for _ in range(5):
            self.player.draw_card()
            self.computer.draw_card()
    
    def handle_click(self, pos):
        if self.game_state != "playing":
            return
            
        # 플레이어의 카드 선택
        for i, card in enumerate(self.player.hand):
            if card.rect.collidepoint(pos):
                self.selected_card = i
                return
                
        # 필드에 카드 내기
        if self.selected_card is not None:
            if 100 <= pos[1] <= 300:  # 필드 영역
                if self.player.play_card(self.selected_card):
                    self.selected_card = None
                    self.computer_turn()
    
    def computer_turn(self):
        # 컴퓨터의 턴
        if self.computer.hand:
            # 랜덤하게 카드 선택
            card_index = random.randint(0, len(self.computer.hand) - 1)
            self.computer.play_card(card_index)
            self.computer.draw_card()
    
    def draw(self):
        screen.fill((200, 200, 200))
        
        # 플레이어 정보 표시
        font = pygame.font.SysFont('malgungothic', 20)
        player_hp = font.render(f"플레이어 HP: {self.player.hp}", True, BLACK)
        computer_hp = font.render(f"컴퓨터 HP: {self.computer.hp}", True, BLACK)
        screen.blit(player_hp, (10, 10))
        screen.blit(computer_hp, (SCREEN_WIDTH - 150, 10))
        
        # 플레이어의 카드 그리기
        for i, card in enumerate(self.player.hand):
            card.draw(screen, 50 + i * (CARD_WIDTH + 10), SCREEN_HEIGHT - CARD_HEIGHT - 20)
        
        # 컴퓨터의 카드 그리기
        for i, card in enumerate(self.computer.hand):
            card.draw(screen, 50 + i * (CARD_WIDTH + 10), 20)
        
        # 필드의 카드 그리기
        for i, card in enumerate(self.player.field):
            card.draw(screen, 50 + i * (CARD_WIDTH + 10), SCREEN_HEIGHT - CARD_HEIGHT - 200)
        
        for i, card in enumerate(self.computer.field):
            card.draw(screen, 50 + i * (CARD_WIDTH + 10), 200)
        
        # 게임 오버 메시지
        if self.game_state == "game_over":
            font = pygame.font.SysFont('malgungothic', 40)
            if self.player.hp <= 0:
                text = font.render("컴퓨터 승리!", True, RED)
            else:
                text = font.render("플레이어 승리!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, text_rect)
        
        pygame.display.flip()

def main():
    game = Game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 버튼
                    game.handle_click(event.pos)
        
        game.draw()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main() 