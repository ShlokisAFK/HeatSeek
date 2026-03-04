import pygame
import random
import numpy as np
import os
if os.path.exists("heatmap.npy"):
    heatmap = np.load("heatmap.npy")
else:
    heatmap = np.zeros((15, 20))
print(f"Heatmap loaded, max value: {np.max(heatmap)}")
from collections import deque
def bfs(start_row, start_col, target_row, target_col):
    queue = deque()
    queue.append((start_row, start_col))
    visited = set()
    visited.add((start_row, start_col))
    parent = {}
    
    while queue:
        r, c = queue.popleft()
        if r == target_row and c == target_col:
            path = []
            current = (target_row, target_col)
            while current != (start_row, start_col):
                path.append(current)
                current = parent[current]
            path.reverse()
            if not path:
                return None
            return path[0]    
        pass
        
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and game_map[nr][nc] != 1:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    
    return None
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hide and Seek")
def caught_row():
    if player_row==seeker_row:
        x,y=player_col,seeker_col
        wall=0
        if x>y:
            for i in range(y,x):
                if game_map[player_row][i]==1:
                    wall+=1
        if x<y:
            for i in range(x,y):
                if game_map[player_row][i]==1:
                    wall+=1
        if wall==0:
            print("Game over")
            np.save("heatmap.npy", heatmap)
            print(f"Heatmap saved, max value: {np.max(heatmap)}")
            return False
    return True
def caught_col():
    if player_col==seeker_col:
        x,y=player_row,seeker_row
        wall=0
        if x>y:
            for i in range(y,x):
                if game_map[i][player_col]==1:
                    wall+=1
        if x<y:
            for i in range(x,y):
                if game_map[i][player_col]==1:
                    wall+=1
        if wall==0:
            print("Game over")
            np.save("heatmap.npy", heatmap)
            print(f"Heatmap saved, max value: {np.max(heatmap)}")
            return False
    return True
game_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,1,1,0,1,0,0,0,1],
    [1,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,1,1,1],
    [1,0,1,1,1,0,1,1,0,1,1,1,0,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,1,1,0,1,0,1,0,1,0,1,0,0,0,1],
    [1,1,1,0,1,0,0,1,0,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,1],
    [1,0,0,0,1,0,1,1,0,0,0,1,1,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,1,1,0,1,0,1,1,1,0,0,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
seeker_row=13
seeker_col=18
player_row = 1
player_col = 1
l_dc=l_dr=0

running = True
clock = pygame.time.Clock()
frame=0
while running:
    screen.fill((0, 0, 0))
    frame+=10
    heatmap[player_row][player_col] += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            np.save("heatmap.npy", heatmap)
            print(f"Heatmap saved, max value: {np.max(heatmap)}")
            running = False     
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_w:
                if game_map[player_row - 1][player_col] != 1:
                    player_row=player_row - 1
            if event.key==pygame.K_s:
                if game_map[player_row + 1][player_col] != 1:
                    player_row=player_row + 1
            if event.key==pygame.K_a:
                if game_map[player_row ][player_col - 1] != 1:
                    player_col=player_col - 1
            if event.key==pygame.K_d:
                if game_map[player_row ][player_col + 1] != 1:
                    player_col=player_col + 1
    if frame == 120:
        target = np.unravel_index(np.argmax(heatmap), heatmap.shape)
        target_row_h, target_col_h = target

        if np.max(heatmap) and random.random() < 0.7:
            next_step = bfs(seeker_row, seeker_col, target_row_h, target_col_h)
            if next_step:
                seeker_row, seeker_col = next_step
            else:
                directions = [(-1,0), (1,0), (0,-1), (0,1)]
                dr, dc = random.choice(directions)
                if game_map[seeker_row + dr][seeker_col + dc] != 1:
                    seeker_row += dr
                    seeker_col += dc
        frame=0
    if running:
        running=caught_row() and caught_col()
    pygame.draw.rect(screen, (0,255,0), (player_col*40, player_row*40, 40, 40))
    pygame.draw.rect(screen, (255,0,0), (seeker_col*40, seeker_row*40, 40, 40))
    for r, row in enumerate(game_map):
         for c, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (255,255,255), (c*40, r*40, 40, 40))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()