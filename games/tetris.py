import pygame
import random

# 색상 정의
COLORS = [
    (0, 0, 0),        # 검정 (배경)
    (120, 37, 179),   # 보라
    (100, 179, 179),  # 청록
    (80, 34, 22),     # 갈색
    (80, 134, 22),    # 초록
    (180, 34, 22),    # 빨강
    (180, 34, 122),   # 분홍
]

# 테트리스 블록 모양 정의
SHAPES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
    [[1, 2, 5, 6]],  # O
    [[5, 6, 8, 9], [1, 5, 6, 10]],  # S
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
    [[4, 5, 9, 10], [2, 6, 5, 9]]  # Z
]

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.figure = None
        self.x = 0
        self.y = 0
        
        self.clear_field()
        
    def clear_field(self):
        self.field = []
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)
            
    def new_figure(self):
        self.figure = Figure(3, 0)
        
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                       j + self.figure.x > self.width - 1 or \
                       j + self.figure.x < 0 or \
                       self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection
        
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
            
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1-1][j]
        self.score += lines ** 2
        
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()
        
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()
            
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
            
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(SHAPES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0
        
    def image(self):
        return SHAPES[self.type][self.rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.type])

# 게임 초기화
pygame.init()

# 상수 정의
CELL_SIZE = 30
FIELD_WIDTH = 10
FIELD_HEIGHT = 20
GAME_RESOLUTION = FIELD_WIDTH * CELL_SIZE, FIELD_HEIGHT * CELL_SIZE
GAME_FPS = 25

# 화면 설정
screen = pygame.display.set_mode(GAME_RESOLUTION)
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# 게임 객체 생성
game = Tetris(FIELD_HEIGHT, FIELD_WIDTH)
counter = 0
pressing_down = False

# 게임 루프
while True:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (GAME_FPS // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    # 화면 그리기
    screen.fill(COLORS[0])

    # 게임 필드 그리기
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, COLORS[game.field[i][j]],
                           [j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE], 0)
            pygame.draw.rect(screen, (128, 128, 128),
                           [j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE], 1)

    # 현재 블록 그리기
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, COLORS[game.figure.color],
                                   [(game.figure.x + j) * CELL_SIZE,
                                    (game.figure.y + i) * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE], 0)
                    pygame.draw.rect(screen, (128, 128, 128),
                                   [(game.figure.x + j) * CELL_SIZE,
                                    (game.figure.y + i) * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE], 1)

    # 점수 표시
    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render("Score: " + str(game.score), True, (255, 255, 255))
    screen.blit(text, [0, 0])

    # 게임 오버 메시지
    if game.state == "gameover":
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, [GAME_RESOLUTION[0]//3, GAME_RESOLUTION[1]//2])

    pygame.display.flip()
    clock.tick(GAME_FPS) 