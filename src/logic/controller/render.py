import pygame
import math

from src.simulator import GlobalConfig

def render_nodes(*, window, nodes, state):
    cfg = GlobalConfig.cfg()
    for idx, node in nodes.iterrows():
        color = cfg.render.body.colors.levels[-1]
        
        
        if node["fault"]:
            color = cfg.render.node.colors.fault

        position = node["x"], node["y"]
        
        if not node["fault"] and cfg.render.body.show_communication_radius:
           pygame.draw.circle(window, color, position, cfg.params.rc[0], 1)

        if not node["fault"] and cfg.render.body.show_perceive_radius:
            pygame.draw.circle(window, color, position, cfg.params.rs[0], 1)



        if "display_ids" not in state or not state["display_ids"]:
            if not node["fault"]:
                #pygame.draw.circle(window, color, position, cfg.render.body.size)   # draws point for node
                x, y = position
                angle = node["heading"]

                points = [
                (x, y - (cfg.render.body.height / 2)),
                (x - (cfg.render.body.width / 2), y + (cfg.render.body.height /2)),
                (x, y + (cfg.render.body.height / 4)),
                (x + (cfg.render.body.width / 2), y + (cfg.render.body.height / 2)),
                (x, y - (cfg.render.body.height / 2)),
                (x, y + (cfg.render.body.height / 4)),
                ]

                position = pygame.math.Vector2((x, y))
                rotated_points = [
                    (pygame.math.Vector2(p) - position) \
                    .rotate_rad(angle + math.pi/2) \
                    for p in points
                ]

                translated_points = [(position + p) for p in rotated_points]

                pygame.draw.polygon(
                    window,
                    color,
                    translated_points
                )
        else:
            font = pygame.font.SysFont("Comic Sans MS", 20)
            text_surface = font.render(f"{node.id}", False, (0, 0, 0))
            pos = pygame.math.Vector2(position)
            window.blit(text_surface, pos - pygame.math.Vector2(5, 5))