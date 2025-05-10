import pygame
import random
import time

# --- Configuration ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
TILE_SIZE = 16
PLAYER_SIZE = 12
TEXT_BOX_HEIGHT = 80
FONT_SIZE = 18

# --- Colors (RGB) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
GREY = (128, 128, 128) # Wall, but we'll use for placeholder Kanto buildings
RED = (255, 0, 0)
WATER_BLUE = (0, 116, 217)
LIGHT_YELLOW = (255, 255, 224)
UI_BORDER_COLOR = (50, 50, 50)
ROOF_RED = (200, 50, 50) # For Kanto house roofs
BUILDING_WALL_LIGHT = (200, 200, 180) # For Kanto building walls

# --- Game States ---
STATE_OVERWORLD = "overworld"
STATE_BATTLE = "battle"
STATE_TEXTBOX = "textbox"

# --- Game World (Tile Types) ---
# 0: Path (Brown)
# 1: Grass (Green) - potential encounter
# 2: Wall/Obstacle (Grey) - Will also be generic Kanto building block
# 3: Water (Water Blue)
# 4: NPC_BLOCK (Looks like a path, but triggers text)
# 5: Kanto House Roof (ROOF_RED)
# 6: Kanto Building Wall (BUILDING_WALL_LIGHT)
# 7: Door (placeholder, looks like path for now)
# 8: Sign (placeholder, triggers text, looks like path)
# 9: Tall Grass (Darker Green) - Higher encounter rate maybe?
# 10: Tree Trunk (Brown)
# 11: Tree Leaves (Dark Green)
# 12: Flowers (Various colors on grass)

# --- Kanto Map Structure ---
# Dimensions for Kanto maps can vary. For now, these are just examples.
KANTO_MAP_BASE_WIDTH = 30 # SCREEN_WIDTH // TILE_SIZE
KANTO_MAP_BASE_HEIGHT = 20 # (SCREEN_HEIGHT - TEXT_BOX_HEIGHT) // TILE_SIZE

# Example: Pallet Town (Tiny version for now)
pallet_town_map_data = [
    [2, 2, 2, 2, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 1, 6, 7, 6, 1, 1, 0, 1, 1, 2, 5, 5, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 6, 6, 6, 1, 0, 0, 0, 1, 2, 6, 6, 2, 1, 8, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 1, 2], # Path to Route 1 -> (0,0,0...)
    [2, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 7, 6, 2, 1, 1, 0, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 1, 2],
    [2, 2, 2, 2, 8, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 1, 1, 1, 9, 9, 9, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2], # Lab area fence / water edge
    [2, 1, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 1, 1, 2],
    [2, 1, 0, 6, 7, 6, 1, 1, 1, 1, 6, 0, 6, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 6, 0, 1, 1, 2], # Prof Oak's lab concept
    [2, 1, 0, 6, 6, 6, 1, 1, 1, 1, 6, 0, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 1, 1, 2],
    [2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2],
    [2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]
# Ensure map height
for _ in range(len(pallet_town_map_data), KANTO_MAP_BASE_HEIGHT):
    pallet_town_map_data.append([2] * KANTO_MAP_BASE_WIDTH)

# --- Placeholder Pokemon Data ---
POKEMON_DATA = {
    "KITTENPUNCH": {"hp": 30, "max_hp": 30, "attack": 8, "defense": 5, "sprite_color": (255, 105, 180)},
    "BARKBITE": {"hp": 35, "max_hp": 35, "attack": 7, "defense": 6, "sprite_color": (160, 82, 45)},
    "PIXELPUP": {"hp": 25, "max_hp": 25, "attack": 9, "defense": 4, "sprite_color": (173, 216, 230)},
}

# --- Simple Text Wrapping ---
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

class RedEmuGame:
    def __init__(self):
        pygame.init()
        self.actual_screen_height = SCREEN_HEIGHT
        self.game_screen_height = SCREEN_HEIGHT - TEXT_BOX_HEIGHT
        self.map_display_width = SCREEN_WIDTH
        self.map_display_height = self.game_screen_height

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, self.actual_screen_height))
        pygame.display.set_caption("RedEMU Kanto")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.large_font = pygame.font.Font(None, FONT_SIZE + 6)

        self.game_state = STATE_OVERWORLD
        
        # --- Kanto Map Management ---
        self.kanto_maps = {}
        self.current_kanto_map_id = "pallet_town"
        self.load_kanto_map_data()
        
        self.current_map_data = self.kanto_maps[self.current_kanto_map_id]["map"]
        self.current_map_width_tiles = len(self.current_map_data[0])
        self.current_map_height_tiles = len(self.current_map_data)

        self.player_map_x_tile = 10
        self.player_map_y_tile = 5
        self.camera_x_tile = 0
        self.camera_y_tile = 0
        self.center_camera_on_player()

        self.textbox_message_queue = []
        self.current_textbox_message_lines = []
        self.textbox_line_index = 0
        self.textbox_active = False

        self.battle_active = False
        self.player_pokemon = None
        self.enemy_pokemon = None
        self.battle_turn = "player"
        self.battle_message = ""
        self.last_battle_message_time = 0

        self.setup_player_pokemon()

        # --- NPC and Sign Data for Kanto ---
        self.kanto_interactions = {
            ("pallet_town", 4, 1): "This is your house! Get in there!",
            ("pallet_town", 4, 4): "RIVAL'S HOUSE - Keep out!",
            ("pallet_town", 12, 1): "PROF. OAK'S LAB - SCIENCE!",
            ("pallet_town", 16, 2): "PALLET TOWN - A sleepy little town.",
            ("pallet_town", 7, 2): "Route 1 this way -> Go get 'em, tiger!",
        }
        self.place_interaction_tiles()

        self.hq_ripper_work_duration_seconds = 3600 * 24
        self.hq_ripper_start_time = time.time()
        print(f"CATSDK: Meow! Activated. Generating Kanto for {self.hq_ripper_work_duration_seconds / 3600:.2f} hours...")

    def place_interaction_tiles(self):
        for (map_id, x, y), message in self.kanto_interactions.items():
            if map_id in self.kanto_maps:
                if "door" in message.lower() or "house" in message.lower() and "sign" not in message.lower():
                    if 0 <= y < len(self.kanto_maps[map_id]["map"]) and 0 <= x < len(self.kanto_maps[map_id]["map"][0]):
                        self.kanto_maps[map_id]["map"][y][x] = 7
                elif "sign" in message.lower() or "town" in message.lower() or "route" in message.lower():
                    if 0 <= y < len(self.kanto_maps[map_id]["map"]) and 0 <= x < len(self.kanto_maps[map_id]["map"][0]):
                        self.kanto_maps[map_id]["map"][y][x] = 8

    def load_kanto_map_data(self):
        self.kanto_maps["pallet_town"] = {
            "map": [row[:] for row in pallet_town_map_data],
            "connections": {
                "NORTH_EDGE": ("route_1", 10, KANTO_MAP_BASE_HEIGHT - 2),
            },
            "encounter_tiles": [1, 9]
        }
        self.current_map_data = self.kanto_maps[self.current_kanto_map_id]["map"]
        self.current_map_width_tiles = len(self.current_map_data[0])
        self.current_map_height_tiles = len(self.current_map_data)

    def center_camera_on_player(self):
        screen_tiles_x = self.map_display_width // TILE_SIZE
        screen_tiles_y = self.map_display_height // TILE_SIZE
        target_cam_x = self.player_map_x_tile - screen_tiles_x // 2
        target_cam_y = self.player_map_y_tile - screen_tiles_y // 2
        self.camera_x_tile = max(0, min(target_cam_x, self.current_map_width_tiles - screen_tiles_x))
        self.camera_y_tile = max(0, min(target_cam_y, self.current_map_height_tiles - screen_tiles_y))

    def setup_player_pokemon(self):
        start_mon_name = "KITTENPUNCH"
        data = POKEMON_DATA[start_mon_name]
        self.player_pokemon = {
            "name": start_mon_name, "hp": data["hp"], "max_hp": data["max_hp"],
            "attack": data["attack"], "defense": data["defense"], "sprite_color": data["sprite_color"]
        }

    def draw_tile(self, surface, tile_type, x_pixel, y_pixel):
        rect = pygame.Rect(x_pixel, y_pixel, TILE_SIZE, TILE_SIZE)
        border_rect = pygame.Rect(x_pixel, y_pixel, TILE_SIZE, TILE_SIZE)
        if tile_type == 0: # Path
            pygame.draw.rect(surface, BROWN, rect)
        elif tile_type == 1: # Grass
            pygame.draw.rect(surface, GREEN, rect)
        elif tile_type == 2: # Wall/Generic Obstacle
            pygame.draw.rect(surface, GREY, rect)
            pygame.draw.rect(surface, BLACK, border_rect, 1)
        elif tile_type == 3: # Water
            pygame.draw.rect(surface, WATER_BLUE, rect)
            pygame.draw.line(surface, WHITE, (x_pixel + 2, y_pixel + TILE_SIZE // 3), (x_pixel + TILE_SIZE - 2, y_pixel + TILE_SIZE // 3), 1)
            pygame.draw.line(surface, WHITE, (x_pixel + 4, y_pixel + 2 * TILE_SIZE // 3), (x_pixel + TILE_SIZE - 4, y_pixel + 2 * TILE_SIZE // 3), 1)
        elif tile_type == 4: # NPC Block
            pygame.draw.rect(surface, BROWN, rect)
        elif tile_type == 5: # Kanto House Roof
            pygame.draw.rect(surface, ROOF_RED, rect)
            pygame.draw.rect(surface, BLACK, border_rect, 1)
        elif tile_type == 6: # Kanto Building Wall
            pygame.draw.rect(surface, BUILDING_WALL_LIGHT, rect)
            pygame.draw.rect(surface, GREY, border_rect, 1)
        elif tile_type == 7: # Door
            pygame.draw.rect(surface, BROWN, rect)
            pygame.draw.rect(surface, BLACK, (x_pixel+2, y_pixel+2, TILE_SIZE-4, TILE_SIZE-4), 2)
            pygame.draw.circle(surface, BLACK, (x_pixel + TILE_SIZE - 4, y_pixel + TILE_SIZE // 2), 2)
        elif tile_type == 8: # Sign
            pygame.draw.rect(surface, BROWN, (x_pixel + TILE_SIZE//3, y_pixel + TILE_SIZE//2, TILE_SIZE//3, TILE_SIZE//2))
            pygame.draw.rect(surface, LIGHT_YELLOW, (x_pixel, y_pixel, TILE_SIZE, TILE_SIZE//2))
            pygame.draw.rect(surface, BROWN, (x_pixel, y_pixel, TILE_SIZE, TILE_SIZE//2),1)
        elif tile_type == 9: # Tall Grass
            pygame.draw.rect(surface, DARK_GREEN, rect)

    def draw_map(self, surface):
        start_tile_x = self.camera_x_tile
        end_tile_x = start_tile_x + (self.map_display_width // TILE_SIZE) + 1
        start_tile_y = self.camera_y_tile
        end_tile_y = start_tile_y + (self.map_display_height // TILE_SIZE) + 1

        for r_idx in range(start_tile_y, min(end_tile_y, self.current_map_height_tiles)):
            for c_idx in range(start_tile_x, min(end_tile_x, self.current_map_width_tiles)):
                tile_val = self.current_map_data[r_idx][c_idx]
                draw_x = (c_idx - self.camera_x_tile) * TILE_SIZE
                draw_y = (r_idx - self.camera_y_tile) * TILE_SIZE
                self.draw_tile(surface, tile_val, draw_x, draw_y)

    def draw_player(self, surface):
        player_screen_x = (self.player_map_x_tile - self.camera_x_tile) * TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) // 2
        player_screen_y = (self.player_map_y_tile - self.camera_y_tile) * TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) // 2
        
        if player_screen_y < self.map_display_height and player_screen_y + PLAYER_SIZE > 0 and \
           player_screen_x < self.map_display_width and player_screen_x + PLAYER_SIZE > 0:
            player_rect = pygame.Rect(player_screen_x, player_screen_y, PLAYER_SIZE, PLAYER_SIZE)
            pygame.draw.rect(surface, RED, player_rect)
            pygame.draw.rect(surface, BLACK, player_rect, 1)

    def draw_textbox(self):
        box_rect = pygame.Rect(0, self.game_screen_height, SCREEN_WIDTH, TEXT_BOX_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_YELLOW, box_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, box_rect, 3)

        if self.current_textbox_message_lines:
            for i, line in enumerate(self.current_textbox_message_lines):
                if i <= self.textbox_line_index:
                    text_surface = self.font.render(line, True, BLACK)
                    self.screen.blit(text_surface, (15, self.game_screen_height + 15 + (i * (FONT_SIZE + 2))))
            if self.textbox_line_index >= len(self.current_textbox_message_lines) - 1:
                indicator_text = self.font.render("v (Z)", True, RED)
                self.screen.blit(indicator_text, (SCREEN_WIDTH - 40, self.actual_screen_height - 25))

    def show_message(self, message):
        self.textbox_message_queue.append(message)
        if not self.textbox_active:
            self._activate_next_message()

    def _activate_next_message(self):
        if self.textbox_message_queue:
            message = self.textbox_message_queue.pop(0)
            self.current_textbox_message_lines = wrap_text(message, self.font, SCREEN_WIDTH - 30)
            self.textbox_line_index = 0
            self.game_state = STATE_TEXTBOX
            self.textbox_active = True
        else:
            self.textbox_active = False
            if not self.battle_active:
                self.game_state = STATE_OVERWORLD

    def handle_textbox_input(self, event):
        if event.key == pygame.K_z:
            self.textbox_line_index += 1
            if self.textbox_line_index >= len(self.current_textbox_message_lines):
                self._activate_next_message()

    def handle_overworld_input(self, event):
        new_player_map_x, new_player_map_y = self.player_map_x_tile, self.player_map_y_tile
        moved = False
        direction_faced = None

        if event.key == pygame.K_LEFT:
            new_player_map_x -= 1
            moved = True
            direction_faced = 'LEFT'
        elif event.key == pygame.K_RIGHT:
            new_player_map_x += 1
            moved = True
            direction_faced = 'RIGHT'
        elif event.key == pygame.K_UP:
            new_player_map_y -= 1
            moved = True
            direction_faced = 'UP'
        elif event.key == pygame.K_DOWN:
            new_player_map_y += 1
            moved = True
            direction_faced = 'DOWN'
        elif event.key == pygame.K_z:
            tiles_to_check_for_interaction = [(self.player_map_x_tile, self.player_map_y_tile)]
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    tiles_to_check_for_interaction.append((self.player_map_x_tile + dx, self.player_map_y_tile + dy))
            
            interaction_triggered = False
            for check_x, check_y in tiles_to_check_for_interaction:
                map_coord_key = (self.current_kanto_map_id, check_x, check_y)
                if map_coord_key in self.kanto_interactions:
                    if 0 <= check_y < self.current_map_height_tiles and \
                       0 <= check_x < self.current_map_width_tiles:
                        tile_type_at_interaction = self.current_map_data[check_y][check_x]
                        if tile_type_at_interaction in [7, 8]:
                            self.show_message(self.kanto_interactions[map_coord_key])
                            interaction_triggered = True
                            break 
            if interaction_triggered:
                return

        if moved:
            if 0 <= new_player_map_x < self.current_map_width_tiles and \
               0 <= new_player_map_y < self.current_map_height_tiles:
                
                target_tile_type = self.current_map_data[new_player_map_y][new_player_map_x]
                impassable_tiles = [2, 3, 5, 6, 10, 11]
                if target_tile_type not in impassable_tiles:
                    self.player_map_x_tile = new_player_map_x
                    self.player_map_y_tile = new_player_map_y
                    self.center_camera_on_player()

                    if target_tile_type in self.kanto_maps[self.current_kanto_map_id].get("encounter_tiles", [1, 9]):
                        encounter_chance = 0.10
                        if target_tile_type == 9:
                            encounter_chance = 0.20
                        if random.random() < encounter_chance:
                            self.start_battle()
                elif target_tile_type == 3:
                    self.show_message("It's water. You can't walk on it.")

    def change_map(self, connection_data):
        pass

    def start_battle(self):
        if not self.player_pokemon or self.player_pokemon["hp"] <= 0:
            self.show_message("Your Pokemon is exhausted!")
            return

        wild_pokemon_name = random.choice(list(POKEMON_DATA.keys()))
        data = POKEMON_DATA[wild_pokemon_name]
        self.enemy_pokemon = {
            "name": wild_pokemon_name, "hp": data["hp"], "max_hp": data["max_hp"],
            "attack": data["attack"], "defense": data["defense"], "sprite_color": data["sprite_color"]
        }
        self.game_state = STATE_BATTLE
        self.battle_active = True
        self.battle_turn = "player"
        self.battle_message = f"A wild {self.enemy_pokemon['name']} appeared! Get ready to battle!"
        self.last_battle_message_time = time.time()

    def draw_battle_ui(self):
        self.screen.fill(BLACK)

        if self.enemy_pokemon:
            enemy_name_surf = self.large_font.render(self.enemy_pokemon["name"], True, WHITE)
            enemy_hp_surf = self.font.render(f"HP: {self.enemy_pokemon['hp']}/{self.enemy_pokemon['max_hp']}", True, WHITE)
            pygame.draw.rect(self.screen, self.enemy_pokemon["sprite_color"], (SCREEN_WIDTH - 120, 50, 80, 80))
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH - 120, 50, 80, 80), 2)
            self.screen.blit(enemy_name_surf, (SCREEN_WIDTH - 150, 20))
            self.screen.blit(enemy_hp_surf, (SCREEN_WIDTH - 150, 20 + FONT_SIZE + 2))

        if self.player_pokemon:
            player_name_surf = self.large_font.render(self.player_pokemon["name"], True, WHITE)
            player_hp_surf = self.font.render(f"HP: {self.player_pokemon['hp']}/{self.player_pokemon['max_hp']}", True, WHITE)
            pygame.draw.rect(self.screen, self.player_pokemon["sprite_color"], (40, self.actual_screen_height - 200, 80, 80))
            pygame.draw.rect(self.screen, WHITE, (40, self.actual_screen_height - 200, 80, 80), 2)
            self.screen.blit(player_name_surf, (30, self.actual_screen_height - 230))
            self.screen.blit(player_hp_surf, (30, self.actual_screen_height - 230 + FONT_SIZE + 2))

        box_rect = pygame.Rect(0, self.game_screen_height, SCREEN_WIDTH, TEXT_BOX_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_YELLOW, box_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, box_rect, 3)

        if self.battle_message:
            lines = wrap_text(self.battle_message, self.font, SCREEN_WIDTH - 30)
            for i, line in enumerate(lines[:2]):
                text_surface = self.font.render(line, True, BLACK)
                self.screen.blit(text_surface, (15, self.game_screen_height + 15 + (i * (FONT_SIZE + 2))))

        if self.battle_turn == "player" and (time.time() - self.last_battle_message_time > 1.0):
            fight_text = self.font.render("1. FIGHT", True, BLACK)
            run_text = self.font.render("2. RUN", True, BLACK)
            self.screen.blit(fight_text, (SCREEN_WIDTH // 2 - 100, self.game_screen_height + 20))
            self.screen.blit(run_text, (SCREEN_WIDTH // 2 - 100, self.game_screen_height + 20 + FONT_SIZE + 5))

    def handle_battle_input(self, event):
        if self.battle_turn == "player" and (time.time() - self.last_battle_message_time > 1.0):
            if event.key == pygame.K_1:
                self.execute_player_attack()
            elif event.key == pygame.K_2:
                self.battle_message = "You ran away! Smart move, maybe."
                self.last_battle_message_time = time.time()
                pygame.time.set_timer(pygame.USEREVENT + 1, 1500, True)

    def execute_player_attack(self):
        if not self.player_pokemon or not self.enemy_pokemon: return

        damage = max(1, self.player_pokemon["attack"] - self.enemy_pokemon["defense"] // 2 + random.randint(-2, 2))
        self.enemy_pokemon["hp"] = max(0, self.enemy_pokemon["hp"] - damage)
        self.battle_message = f"{self.player_pokemon['name']} attacks {self.enemy_pokemon['name']}! Did {damage} damage!"
        self.last_battle_message_time = time.time()

        if self.enemy_pokemon["hp"] <= 0:
            self.battle_message = f"Enemy {self.enemy_pokemon['name']} fainted! You win!"
            pygame.time.set_timer(pygame.USEREVENT + 1, 2000, True)
        else:
            self.battle_turn = "enemy_pending_message"
            pygame.time.set_timer(pygame.USEREVENT + 2, 1500, True)

    def execute_enemy_attack(self):
        if not self.player_pokemon or not self.enemy_pokemon: return

        damage = max(1, self.enemy_pokemon["attack"] - self.player_pokemon["defense"] // 2 + random.randint(-2, 2))
        self.player_pokemon["hp"] = max(0, self.player_pokemon["hp"] - damage)
        self.battle_message = f"Wild {self.enemy_pokemon['name']} attacks! Did {damage} damage to your {self.player_pokemon['name']}!"
        self.last_battle_message_time = time.time()

        if self.player_pokemon["hp"] <= 0:
            self.battle_message = f"Your {self.player_pokemon['name']} fainted! You lost!"
            pygame.time.set_timer(pygame.USEREVENT + 1, 2000, True)
        else:
            self.battle_turn = "player"

    def end_battle(self):
        self.battle_active = False
        self.enemy_pokemon = None
        self.game_state = STATE_OVERWORLD
        self.battle_message = ""
        if self.player_pokemon and self.player_pokemon["hp"] > 0:
            self.player_pokemon["hp"] = min(self.player_pokemon["max_hp"], self.player_pokemon["hp"] + random.randint(3,8))
            self.show_message(f"{self.player_pokemon['name']} feels a bit better.")
        elif self.player_pokemon and self.player_pokemon["hp"] <= 0:
            self.show_message("You should take your Pokemon to a PokeCenter.")

    def run(self):
        running = True
        map_surface = pygame.Surface((self.map_display_width, self.map_display_height))

        while running:
            current_time = time.time()
            if current_time - self.hq_ripper_start_time > self.hq_ripper_work_duration_seconds:
                print("CATSDK: Meow... Work cycle complete. Set a new timer if you want more Kanto!")
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_state == STATE_OVERWORLD:
                        if not self.textbox_active:
                           self.handle_overworld_input(event)
                        else:
                           self.handle_textbox_input(event)
                    elif self.game_state == STATE_TEXTBOX:
                        self.handle_textbox_input(event)
                    elif self.game_state == STATE_BATTLE:
                        self.handle_battle_input(event)

                if event.type == pygame.USEREVENT + 1:
                    self.end_battle()
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                if event.type == pygame.USEREVENT + 2:
                    if self.battle_turn == "enemy_pending_message":
                        self.battle_turn = "enemy"
                        self.execute_enemy_attack()
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)

            self.screen.fill(BLACK)

            if self.game_state == STATE_OVERWORLD or self.game_state == STATE_TEXTBOX:
                map_surface.fill(BLACK)
                self.draw_map(map_surface)
                self.draw_player(map_surface)
                self.screen.blit(map_surface, (0,0))
                self.draw_textbox()

            elif self.game_state == STATE_BATTLE:
                self.draw_battle_ui()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        print("CATSDK: Game over! Hope you enjoyed Kanto!")

if __name__ == '__main__':
    game = RedEmuGame()
    game.run()
