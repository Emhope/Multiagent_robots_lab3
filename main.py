import pygame
import numpy as np
import scene_tools
import itertools
import time
import random


def chase(chaser: scene_tools.Object, goal: scene_tools.Object, t=1.0, max_speed=10.0, min_distance=20) -> None:
    if np.linalg.norm(goal.get_middle_point() - chaser.get_middle_point()) < min_distance:
        chaser.set_speed([0, 0])
        return True

    goal_future_pos = goal.get_middle_point() + goal.get_speed() * t
    speed = goal_future_pos - chaser.get_middle_point()
    
    if np.linalg.norm(speed) > max_speed:
        speed *= (max_speed / np.linalg.norm(speed))
    
    chaser.set_speed(speed)
    return False


def find_nearest(robot: scene_tools.Object, goals: list[scene_tools.Object]) -> scene_tools.Object:
    return min(goals, key=lambda g: np.linalg.norm(g.get_middle_point() - robot.get_middle_point()))


def main(width=600, height=400, fps=30):
    '''
    robots are red
    not passed goals are blue
    passed goals are green
    '''
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))

    max_speed = 100
    robots = [scene_tools.Object(scene_tools.create_square([random.randint(0, width), random.randint(0, height)], 10), color=(255, 0, 0), width=0) for _ in range(random.randint(5, 7))]
    for i, robot in enumerate(robots):
        robot.set_color((int(255/len(robots)*i), 0, 0))
    
    list_goals = [scene_tools.Object(scene_tools.create_square([random.randint(50, width), random.randint(50, height)], 10), color=(30, 30, 230), width=0) for _ in range(random.randint(13, 15))]
    unreached_goals = list_goals.copy()
    current_goal = find_nearest(robots[-1], unreached_goals)
    unreached_goals.remove(current_goal)

    start = time.perf_counter()
    running = True
    while running:
        clock.tick(fps) #similar to timerDelay

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        if chase(chaser=robots[-1], goal=current_goal, max_speed=max_speed):
            try:
                current_goal.set_color((0, 255, 0))
                current_goal = find_nearest(robots[-1], unreached_goals)
                unreached_goals.remove(current_goal)
                #current_goal = next(goals)
            except:
                running = False

        for i, robot in enumerate(robots):
            if i < len(robots) - 1:
                chase(chaser=robot, goal=robots[i+1], max_speed=max_speed, min_distance=50)    
            robot.simulate(1/fps)
            robot.draw(screen)

        for goal in list_goals:
            goal.draw(screen)

        pygame.display.flip()


    pygame.quit()
    print(f'time: {round(time.perf_counter() - start, 2)}s')
    


if __name__ == '__main__':
    main(fps=30, width=1200, height=720)