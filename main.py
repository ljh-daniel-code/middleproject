import pygame
from random import *


# 레벨에 맞게 설정
def setup(level):
    # 얼마동안 숫자를 보여줄지
    global display_time
    display_time = level // 2
    display_time = max(display_time, 1)  # 1초 미만이면 1초로 처리

    # 얼마나 많은 숫자를 보여줄 것인가?
    number_count = level + 3
    number_count = min(number_count, 40)  # 만약 40을 초과하면 40으로 처리

    # 실제 화면에 grid 형태로 숫자를 랜덤으로 배치
    shuffle_grid(number_count)


# 숫자 섞기
def shuffle_grid(number_count):
    rows = 5
    columns = 9

    cell_size = 130  # 각 Grid cell별 가로, 세로 크기
    button_size = 110  # Grid cell 내에 실제로 그려질 버튼 크기
    screen_left_margin = 55  # 전체 스크린 왼쪽 여백
    screen_top_margin = 20  # 전체 스크린 위쪽 여백

    # [0, 0, 0, 0, 0, 0, 0, 0, 0] X 5
    grid = [[0 for col in range(columns)] for row in range(rows)]  # 5 X 9

    number = 1  # 숫자를 1부터 number_count까지, 만약 5라면 5까지 숫자를 랜덤하게 배치
    while number <= number_count:
        row_idx = randrange(0, rows)  # 0, 1, 2, 3, 4 중에서 랜덤으로 뽑기
        col_idx = randrange(0, columns)  # 0 ~ 8 중에서 랜덤으로 뽑기

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number  # 숫자 지정
            number += 1

            # 현재 grid cell 위치 기준으로 x, y 위치를 구함
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # 숫자 버튼 만들기
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)

    # 배치된 랜덤 숫자 확인
    # print(grid)


# 시작 화면 보여주기
def display_start_screen():
    global lives, curr_level
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)
    # 흰색 동그라미 그림 - 중심 좌표: start_button.center
    # 반지름: 60, 선 두께: 5

    msg2 = game_font.render(f"LEVEL {curr_level}", True, WHITE)
    msg2_rect = msg2.get_rect(center=(screen_width / 2, screen_height / 2 - 80))
    screen.blit(msg2, msg2_rect)

    msg1 = game_font.render(f"{lives} LIVES LEFT", True, WHITE)
    msg1_rect = msg1.get_rect(center=(screen_width / 2, screen_height / 2 + 80))
    screen.blit(msg1, msg1_rect)


# 게임 화면 보여주기
def display_game_screen():
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # ms -> s
        if elapsed_time > display_time:
            hidden = True

    for idx, rect in enumerate(number_buttons, start=1):
        if hidden:  # 숨김 처리
            # 버튼 사각형 그리기
            pygame.draw.rect(screen, WHITE, rect)
        else:
            # 실제 숫자 텍스트 (버튼 중간에 위치하도록)
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)

        # pos에 해당하는 위치가 버튼 안쪽인지 확인


def check_buttions(pos):
    global start, start_ticks

    if start:
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks()  # 타이머 시작 (현재 시간을 저장)


def check_number_buttons(pos):
    global start, curr_level, hidden, level_fail, lives

    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]:  # 올바른 숫자 클릭
                del number_buttons[0]
                if not hidden:
                    hidden = True  # 숫자 숨김 처리
            else:  # 잘못된 숫자 클릭
                if lives <= 1:
                    # Game Over
                    game_over()
                    # running = False
                else:
                    level_fail = True
                    number_buttons.clear()
            break

    # 모든 숫자 맞지면 다음 레벨, 실패하면 목숨 깎고 같은 레벨 다시 도전
    if len(number_buttons) == 0:
        start = False
        hidden = False
        if level_fail == True:
            lives -= 1
            level_fail = False
            setup(curr_level)
        else:
            curr_level += 1
            setup(curr_level)


# 게임 종료 처리, 메세지도 보여줌
def game_over():
    global running

    running = False

    msg = game_font.render(f"GAME OVER", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_width / 2, screen_height / 2 - 80))
    msg3 = game_font.render(f"Failed level {curr_level}", True, WHITE)
    msg3_rect = msg.get_rect(center=(screen_width / 2, screen_height / 2 + 80))

    screen.fill(BLACK)
    screen.blit(msg, msg_rect)
    screen.blit(msg3, msg3_rect)


# 초기화
pygame.init()
screen_width = 1280  # 가로 크기
screen_height = 720  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Game")
game_font = pygame.font.Font(None, 120)  # 폰트 정의

# 시작 버튼
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)

# 색깔 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

number_buttons = []  # 플레이어가 눌러야 하는 버튼들
curr_level = 1  # 현재 레벨
display_time = None  # 숫자를 보여주는 시간
start_ticks = None  # 시간 계산
lives = 3  # 목숨

# 게임 시작 여부
start = False

# 숫자 숨김 여부 (사용자가 1을 클릭했거나, 보여주는 시간 초과했을 떄)
hidden = False

# 레벨 통과 여부
level_fail = False

# 게임 시작 전에 게임 설정 함수 수행
setup(curr_level)

# 게임 루프
running = True  # 게임이 실행중인가?
while running:
    click_pos = None

    # 이벤트 루프
    for event in pygame.event.get():  # 이떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트인가?
            running = False  # 게임이 더 이상 실행중이 아님

        elif event.type == pygame.MOUSEBUTTONUP:  # 사용자가 마우스를 클릭했을 때
            click_pos = pygame.mouse.get_pos()
            # print(click_pos)

    # 화면 전체를 까맣게 색칠
    screen.fill(BLACK)

    # 화면 표시 제어
    if start:
        display_game_screen()  # 게임 화면 표시
    else:
        display_start_screen()  # 시작 화면 표시

    # 사용자가 클릭한 좌표값이 있다면 (어딘가 클릭했다면)
    if click_pos:
        check_buttions(click_pos)

    # 화면 업데이트
    pygame.display.update()

pygame.time.delay(2000)

# 게임 종료
pygame.quit()