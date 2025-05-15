import pygame
import random
import sys
import os

# 게임 초기화
pygame.init()

# 상수 정의
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Battle")
clock = pygame.time.Clock()

# 폰트 설정
try:
    font = pygame.font.SysFont('malgungothic', 16)
except:
    font = pygame.font.SysFont(None, 16)

class Pokemon:
    def __init__(self, name, hp, attack, defense, moves, image_path=None):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves
        self.image_path = image_path
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.is_fainted = False
        self.image = None
        if image_path and os.path.exists(image_path):
            try:
                img = pygame.image.load(image_path)
                self.image = pygame.transform.scale(img, (120, 120))
            except Exception as e:
                print(f"이미지 로딩 실패: {image_path}", e)
                self.image = None
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense // 2)
        self.hp = max(0, self.hp - actual_damage)
        if self.hp == 0:
            self.is_fainted = True
        return actual_damage

class Move:
    def __init__(self, name, power, accuracy, move_type):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.move_type = move_type

class Battle:
    def __init__(self):
        self.player_pokemon = None
        self.computer_pokemon = None
        self.selected_move = None
        self.battle_state = "select_move"  # select_move, attack, computer_turn, game_over
        self.message = ""
        self.message_timer = 0
        
    def initialize_pokemon(self):
        # 포켓몬 데이터 정의
        moves = {
            "Tackle": Move("Tackle", 40, 100, "normal"),
            "Thunder Shock": Move("Thunder Shock", 50, 90, "electric"),
            "Ember": Move("Ember", 45, 95, "fire"),
            "Water Gun": Move("Water Gun", 55, 85, "water"),
            "Razor Leaf": Move("Razor Leaf", 45, 95, "grass"),
            "Tackle2": Move("Tackle2", 35, 100, "normal"),
            "Thunder Shock2": Move("Thunder Shock2", 45, 90, "electric"),
            "Ember2": Move("Ember2", 40, 95, "fire")
        }
        
        # 플레이어 포켓몬
        self.player_pokemon = Pokemon(
            "Pikachu",
            100,
            55,
            40,
            [moves["Tackle"], moves["Thunder Shock"]],
            image_path="images/pikachu.png"
        )
        
        # 컴퓨터 포켓몬
        self.computer_pokemon = Pokemon(
            "Bulbasaur",
            120,
            45,
            50,
            [moves["Tackle2"], moves["Razor Leaf"]],
            image_path="images/bulbasaur.png"
        )
    
    def handle_click(self, pos):
        if self.battle_state == "select_move":
            # 공격 버튼 영역 확인
            for i, move in enumerate(self.player_pokemon.moves):
                button_rect = pygame.Rect(50, 400 + i * 50, 200, 40)
                if button_rect.collidepoint(pos):
                    self.selected_move = move
                    self.battle_state = "attack"
                    self.execute_move()
                    return
    
    def execute_move(self):
        if self.battle_state == "attack":
            # 플레이어의 공격
            if random.randint(1, 100) <= self.selected_move.accuracy:
                damage = self.player_pokemon.attack * self.selected_move.power // 100
                actual_damage = self.computer_pokemon.take_damage(damage)
                self.message = f"{self.player_pokemon.name} used {self.selected_move.name}! {self.computer_pokemon.name} took {actual_damage} damage!"
            else:
                self.message = f"{self.player_pokemon.name}'s attack missed!"
            
            self.message_timer = 60
            self.battle_state = "computer_turn"
            
        elif self.battle_state == "computer_turn":
            # 컴퓨터의 공격
            computer_move = random.choice(self.computer_pokemon.moves)
            if random.randint(1, 100) <= computer_move.accuracy:
                damage = self.computer_pokemon.attack * computer_move.power // 100
                actual_damage = self.player_pokemon.take_damage(damage)
                self.message = f"{self.computer_pokemon.name} used {computer_move.name}! {self.player_pokemon.name} took {actual_damage} damage!"
            else:
                self.message = f"{self.computer_pokemon.name}'s attack missed!"
            
            self.message_timer = 60
            self.battle_state = "select_move"
            
            # 게임 오버 체크
            if self.player_pokemon.is_fainted or self.computer_pokemon.is_fainted:
                self.battle_state = "game_over"
    
    def draw(self):
        screen.fill((200, 200, 200))
        
        # 포켓몬 이미지 표시
        if self.player_pokemon.image:
            screen.blit(self.player_pokemon.image, (100, 200))
        if self.computer_pokemon.image:
            screen.blit(self.computer_pokemon.image, (SCREEN_WIDTH - 220, 80))
        
        # HP 바 그리기
        def draw_hp_bar(x, y, pokemon):
            bar_width = 200
            bar_height = 20
            hp_ratio = pokemon.hp / pokemon.max_hp
            
            # HP 바 배경
            pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
            # 현재 HP
            pygame.draw.rect(screen, GREEN, (x, y, bar_width * hp_ratio, bar_height))
            # HP 바 테두리
            pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height), 2)
            
            # HP 텍스트
            font = pygame.font.SysFont('malgungothic', 16)
            hp_text = font.render(f"{pokemon.name} HP: {pokemon.hp}/{pokemon.max_hp}", True, BLACK)
            screen.blit(hp_text, (x, y - 25))
        
        # 플레이어와 컴퓨터의 HP 바
        draw_hp_bar(50, 100, self.player_pokemon)
        draw_hp_bar(SCREEN_WIDTH - 250, 100, self.computer_pokemon)
        
        # 공격 버튼
        if self.battle_state == "select_move":
            for i, move in enumerate(self.player_pokemon.moves):
                button_rect = pygame.Rect(50, 400 + i * 50, 200, 40)
                pygame.draw.rect(screen, BLUE, button_rect)
                pygame.draw.rect(screen, BLACK, button_rect, 2)
                
                font = pygame.font.SysFont('malgungothic', 16)
                text = font.render(f"{move.name} (위력: {move.power})", True, WHITE)
                text_rect = text.get_rect(center=button_rect.center)
                screen.blit(text, text_rect)
        
        # 메시지 표시
        if self.message and self.message_timer > 0:
            font = pygame.font.SysFont('malgungothic', 20)
            text = font.render(self.message, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 300))
            screen.blit(text, text_rect)
            self.message_timer -= 1
        
        # 게임 오버 메시지
        if self.battle_state == "game_over":
            font = pygame.font.SysFont('malgungothic', 40)
            if self.player_pokemon.is_fainted:
                text = font.render("패배!", True, RED)
            else:
                text = font.render("승리!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, text_rect)
        
        pygame.display.flip()

def main():
    battle = Battle()
    battle.initialize_pokemon()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 버튼
                    battle.handle_click(event.pos)
        
        battle.draw()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 