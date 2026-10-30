
import sys
import os
import time
import random
from math import ceil
import ctypes
import pygame as pg

try:
    import win32gui as wg
except ImportError:
    wg = None

from actions import damage_calculator, dprint
from monsters import init_doctors


# ---------------------------------------------------------------------------
# COLOR PALETTE
# Soft, high-contrast, welcoming, not oversaturated.
# ---------------------------------------------------------------------------
COLOR_BG = (28, 34, 46)            # Slate dark background
COLOR_PANEL = (38, 46, 62)         # Primary panel surface
COLOR_PANEL_ALT = (32, 38, 52)     # Alternate/nested panel surface
COLOR_PANEL_BORDER = (65, 78, 105) # Border for panels
COLOR_HEADER_BG = (45, 55, 76)     # Header banner background

COLOR_TEXT_MAIN = (242, 246, 252)  # Crisp off-white
COLOR_TEXT_MUTED = (168, 180, 200) # Soft muted silver
COLOR_TEXT_GOLD = (248, 208, 88)   # Warm gold for col and special stats
COLOR_TEXT_GREEN = (76, 202, 126)  # Health green
COLOR_TEXT_RED = (238, 92, 92)     # Crimson / alert

COLOR_BTN_DEFAULT = (52, 64, 88)
COLOR_BTN_HOVER = (72, 90, 124)
COLOR_BTN_BORDER = (86, 104, 140)
COLOR_BTN_FOCUS = (125, 175, 245)  # Cyan-blue focus highlight for keyboard

COLOR_BTN_PLUS = (46, 142, 86)
COLOR_BTN_PLUS_HOVER = (58, 172, 104)

COLOR_BTN_MINUS = (172, 62, 62)
COLOR_BTN_MINUS_HOVER = (202, 78, 78)

COLOR_BTN_ACTION = (42, 128, 196)
COLOR_BTN_ACTION_HOVER = (54, 154, 232)

COLOR_BTN_TAB = (44, 52, 70)
COLOR_BTN_TAB_ACTIVE = (62, 112, 180)

COLOR_BTN_DISABLED = (34, 40, 52)
COLOR_TEXT_DISABLED = (88, 98, 114)
COLOR_BORDER_DISABLED = (50, 58, 72)


# ---------------------------------------------------------------------------
# PYGAME & WINDOW LIFECYCLE HELPERS
# ---------------------------------------------------------------------------
_FONT_CACHE = {}

def ensure_pygame():
    """Ensure pygame and font modules are initialized."""
    if not pg.get_init():
        pg.init()
    if not pg.font.get_init():
        pg.font.init()

def get_font(size: int, bold: bool = False):
    """Retrieve a cached font instance."""
    key = (size, bold)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = pg.font.SysFont('segoeui', size, bold=bold)
        except Exception:
            _FONT_CACHE[key] = pg.font.Font(None, size)
    return _FONT_CACHE[key]

def flush_terminal_input():
    """Drain any pending keys from terminal buffer so they do not bleed into GUI or next prompt."""
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except Exception:
        pass

def get_terminal_hwnd():
    """Retrieve the Windows console window handle."""
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            return hwnd
    except Exception:
        pass
    if wg:
        try:
            return wg.GetForegroundWindow()
        except Exception:
            pass
    return 0

def bring_window_to_front(target_hwnd):
    """
    Clean Win32 API window activation.
    Does NOT use WScript.Shell SendKeys, preventing mouse loading wheels
    and avoiding phantom keystrokes in terminal or Pygame.
    """
    if not target_hwnd:
        return
    try:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        foreground_hwnd = user32.GetForegroundWindow()
        if foreground_hwnd != target_hwnd:
            cur_thread = kernel32.GetCurrentThreadId()
            fg_thread = user32.GetWindowThreadProcessId(foreground_hwnd, None)
            if cur_thread != fg_thread and fg_thread != 0:
                user32.AttachThreadInput(fg_thread, cur_thread, True)
                user32.SetForegroundWindow(target_hwnd)
                user32.BringWindowToTop(target_hwnd)
                user32.AttachThreadInput(fg_thread, cur_thread, False)
            else:
                user32.SetForegroundWindow(target_hwnd)
                user32.BringWindowToTop(target_hwnd)
        user32.ShowWindow(target_hwnd, 5) # SW_SHOW
    except Exception:
        if wg:
            try:
                wg.SetForegroundWindow(target_hwnd)
            except Exception:
                pass

def focus_pygame_window(pg_hwnd):
    bring_window_to_front(pg_hwnd)

def refocus_terminal(terminal_hwnd):
    flush_terminal_input()
    bring_window_to_front(terminal_hwnd)
    try:
        pg.display.quit()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# UI WIDGETS (BUTTON, LABEL)
# ---------------------------------------------------------------------------
class Button:
    def __init__(self, rect, text, callback=None, bg_color=COLOR_BTN_DEFAULT,
                 hover_color=COLOR_BTN_HOVER, text_color=COLOR_TEXT_MAIN,
                 font_size=16, bold=False, border_radius=6, enabled=True):
        self.rect = pg.Rect(rect)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.bold = bold
        self.border_radius = border_radius
        self.enabled = enabled
        self.is_hovered = False
        self.is_focused = False

    def handle_event(self, event, mouse_pos=None):
        if not self.enabled:
            return False
        if mouse_pos:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False

    def draw(self, surface):
        font = get_font(self.font_size, self.bold)
        if not self.enabled:
            bg = COLOR_BTN_DISABLED
            txt_color = COLOR_TEXT_DISABLED
            border_col = COLOR_BORDER_DISABLED
        elif self.is_hovered or self.is_focused:
            bg = self.hover_color
            txt_color = COLOR_TEXT_MAIN
            border_col = COLOR_BTN_FOCUS if self.is_focused else COLOR_BTN_BORDER
        else:
            bg = self.bg_color
            txt_color = self.text_color
            border_col = COLOR_BTN_BORDER

        pg.draw.rect(surface, bg, self.rect, border_radius=self.border_radius)
        border_width = 2 if self.is_focused else 1
        pg.draw.rect(surface, border_col, self.rect, width=border_width, border_radius=self.border_radius)

        txt_surf = font.render(self.text, True, txt_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)


# ---------------------------------------------------------------------------
# 1. POINT ALLOCATION GUI WINDOW
# ---------------------------------------------------------------------------
def run_point_allocation_gui(player):
    """
    Opens a 1-page Pygame UI for character point allocation at level up.
    Features:
    - 6 stat columns with + button above, number box, and - button below.
    - Big remaining points box above the options.
    - Clickable or keyboard navigable (Left/Right to select, Up/Down for +/-).
    - Prevents altering previously allocated points (cannot reduce below 0 added).
    - Refocuses the terminal window upon completion.
    """
    flush_terminal_input()
    ensure_pygame()
    terminal_hwnd = get_terminal_hwnd()

    # Add points earned this level
    points_gained = 5 + (player.level // 10)
    player.points += points_gained
    player.total_points += points_gained

    # Points remaining to spend
    remaining_points = player.points

    # Stat categories to allocate into
    stat_keys = [
        'Hit Points',
        'Attack Power',
        'Accuracy',
        'Magic',
        'Speed',
        'Skill Learn Rate'
    ]

    stat_subtitles = {
        'Hit Points': '+1 Max HP',
        'Attack Power': '+1 Atk',
        'Accuracy': '+2 Accuracy',
        'Magic': '+1 Max MP',
        'Speed': '+1 Speed',
        'Skill Learn Rate': '+1 Skill Rate'
    }

    # Points allocated in THIS session (starts at 0)
    session_allocated = {k: 0 for k in stat_keys}

    win_width = 960
    win_height = 560
    window = pg.display.set_mode((win_width, win_height))
    pg.display.set_caption(f"LEVEL UP! Point Allocation - {player.name} (Level {player.level})")

    # Clear any residual keystrokes (such as Enter used to skip fireworks/text)
    pg.event.clear()

    pg_hwnd = pg.display.get_wm_info()['window']
    focus_pygame_window(pg_hwnd)

    clock = pg.time.Clock()
    selected_stat_idx = 0  # 0 to 5 for keyboard navigation
    running = True
    start_time = time.time()

    def get_current_base(stat_name):
        if stat_name == 'Hit Points':
            return player.maxhp
        elif stat_name == 'Attack Power':
            return player.atk
        elif stat_name == 'Accuracy':
            return player.accuracy
        elif stat_name == 'Magic':
            return player.maxmag
        elif stat_name == 'Speed':
            return 1000 - player.agi
        elif stat_name == 'Skill Learn Rate':
            return player.sklp
        return 0

    def increment_stat(idx):
        nonlocal remaining_points
        if remaining_points > 0:
            stat_name = stat_keys[idx]
            session_allocated[stat_name] += 1
            remaining_points -= 1

    def decrement_stat(idx):
        nonlocal remaining_points
        stat_name = stat_keys[idx]
        if session_allocated[stat_name] > 0:
            session_allocated[stat_name] -= 1
            remaining_points += 1

    def reset_allocations():
        nonlocal remaining_points
        for k in stat_keys:
            remaining_points += session_allocated[k]
            session_allocated[k] = 0

    def draw_screen(stat_plus_btns, stat_minus_btns, confirm_btn, reset_btn):
        window.fill(COLOR_BG)

        # Header Banner
        header_rect = pg.Rect(0, 0, win_width, 70)
        pg.draw.rect(window, COLOR_HEADER_BG, header_rect)
        pg.draw.line(window, COLOR_PANEL_BORDER, (0, 70), (win_width, 70), 1)

        title_font = get_font(24, bold=True)
        title_surf = title_font.render("CHARACTER LEVEL UP - POINT ALLOCATION", True, COLOR_TEXT_MAIN)
        window.blit(title_surf, (30, 12))

        sub_font = get_font(15)
        sub_text = f"Player: {player.name}   |   Current Level: {player.level}   |   Gained: +{points_gained} Points"
        sub_surf = sub_font.render(sub_text, True, COLOR_TEXT_MUTED)
        window.blit(sub_surf, (32, 42))

        # Big Remaining Points Card (Above the options)
        rem_card_rect = pg.Rect(win_width // 2 - 210, 85, 420, 72)
        pg.draw.rect(window, COLOR_PANEL, rem_card_rect, border_radius=8)
        pg.draw.rect(window, COLOR_PANEL_BORDER, rem_card_rect, width=1, border_radius=8)

        rem_lbl_font = get_font(15, bold=True)
        rem_lbl = rem_lbl_font.render("REMAINING AVAILABLE POINTS", True, COLOR_TEXT_MUTED)
        window.blit(rem_lbl, (rem_card_rect.centerx - rem_lbl.get_width() // 2, 92))

        # Large points number display box
        num_box_rect = pg.Rect(rem_card_rect.centerx - 45, 115, 90, 36)
        pg.draw.rect(window, COLOR_PANEL_ALT, num_box_rect, border_radius=6)
        pg.draw.rect(window, COLOR_TEXT_GOLD, num_box_rect, width=1, border_radius=6)

        num_font = get_font(24, bold=True)
        num_surf = num_font.render(str(remaining_points), True, COLOR_TEXT_GOLD)
        window.blit(num_surf, num_surf.get_rect(center=num_box_rect.center))

        # Render 6 Stat Columns
        stat_name_font = get_font(15, bold=True)
        stat_sub_font = get_font(12)
        stat_num_font = get_font(20, bold=True)
        base_font = get_font(13)

        col_width = 135
        col_spacing = 16
        total_cols_width = (6 * col_width) + (5 * col_spacing)
        start_x = (win_width - total_cols_width) // 2
        card_y = 175
        card_h = 285

        for i, key in enumerate(stat_keys):
            cx = start_x + i * (col_width + col_spacing)
            card_rect = pg.Rect(cx, card_y, col_width, card_h)

            # Highlight selected stat column for keyboard navigation
            is_selected = (i == selected_stat_idx)
            card_bg = COLOR_PANEL if not is_selected else (44, 54, 76)
            card_border = COLOR_BTN_FOCUS if is_selected else COLOR_PANEL_BORDER
            border_w = 2 if is_selected else 1

            pg.draw.rect(window, card_bg, card_rect, border_radius=8)
            pg.draw.rect(window, card_border, card_rect, width=border_w, border_radius=8)

            # Stat Name & Subtitle
            name_parts = key.split(' ')
            if len(name_parts) == 1:
                name_surf = stat_name_font.render(key, True, COLOR_TEXT_MAIN)
                window.blit(name_surf, (card_rect.centerx - name_surf.get_width() // 2, card_y + 12))
            else:
                line1 = stat_name_font.render(name_parts[0], True, COLOR_TEXT_MAIN)
                line2 = stat_name_font.render(' '.join(name_parts[1:]), True, COLOR_TEXT_MAIN)
                window.blit(line1, (card_rect.centerx - line1.get_width() // 2, card_y + 8))
                window.blit(line2, (card_rect.centerx - line2.get_width() // 2, card_y + 26))

            sub_surf = stat_sub_font.render(stat_subtitles[key], True, COLOR_TEXT_MUTED)
            window.blit(sub_surf, (card_rect.centerx - sub_surf.get_width() // 2, card_y + 48))

            # Current Base Value
            base_val = get_current_base(key)
            base_surf = base_font.render(f"Base: {base_val}", True, COLOR_TEXT_MUTED)
            window.blit(base_surf, (card_rect.centerx - base_surf.get_width() // 2, card_y + 72))

            # Draw + button
            stat_plus_btns[i].is_focused = is_selected
            stat_plus_btns[i].draw(window)

            # Middle Number Box (displaying session added points)
            box_rect = pg.Rect(cx + (col_width - 70) // 2, card_y + 156, 70, 40)
            pg.draw.rect(window, COLOR_PANEL_ALT, box_rect, border_radius=6)
            alloc_val = session_allocated[key]
            box_border = COLOR_TEXT_GREEN if alloc_val > 0 else COLOR_PANEL_BORDER
            pg.draw.rect(window, box_border, box_rect, width=1, border_radius=6)

            alloc_str = f"+{alloc_val}" if alloc_val > 0 else "0"
            alloc_color = COLOR_TEXT_GREEN if alloc_val > 0 else COLOR_TEXT_MUTED
            box_surf = stat_num_font.render(alloc_str, True, alloc_color)
            window.blit(box_surf, box_surf.get_rect(center=box_rect.center))

            # Draw - button
            stat_minus_btns[i].draw(window)

            # Projected new total
            if alloc_val > 0:
                new_tot = base_val + (alloc_val * 2 if key == 'Accuracy' else alloc_val)
                proj_surf = base_font.render(f"-> {new_tot}", True, COLOR_TEXT_GOLD)
                window.blit(proj_surf, (card_rect.centerx - proj_surf.get_width() // 2, card_y + 252))

        # Bottom Buttons
        confirm_btn.draw(window)
        reset_btn.draw(window)

        # Keyboard Navigation Hint
        hint_font = get_font(13)
        hint_str = "Use mouse or [Left/Right] Select Stat   [Up/Down] Add/Sub Point   [Enter] Confirm"
        window.blit(hint_font.render(hint_str, True, COLOR_TEXT_MUTED), (30, win_height - 35))

        pg.display.flip()

    # Pre-render the first frame immediately so window never shows blank/black
    col_width = 135
    col_spacing = 16
    total_cols_width = (6 * col_width) + (5 * col_spacing)
    start_x = (win_width - total_cols_width) // 2
    card_y = 175

    init_plus = [
        Button((start_x + i * (col_width + col_spacing) + (col_width - 64) // 2, card_y + 115, 64, 34),
               "+", bg_color=COLOR_BTN_PLUS, font_size=20, bold=True)
        for i in range(6)
    ]
    init_minus = [
        Button((start_x + i * (col_width + col_spacing) + (col_width - 64) // 2, card_y + 205, 64, 34),
               "-", bg_color=COLOR_BTN_MINUS, font_size=20, bold=True, enabled=False)
        for i in range(6)
    ]
    init_confirm = Button((win_width // 2 - 190, win_height - 65, 230, 44), "Confirm Allocation", bg_color=COLOR_BTN_ACTION, font_size=18, bold=True)
    init_reset = Button((win_width // 2 + 55, win_height - 65, 135, 44), "Reset", bg_color=COLOR_BTN_DEFAULT, font_size=16)
    draw_screen(init_plus, init_minus, init_confirm, init_reset)

    while running:
        mouse_pos = pg.mouse.get_pos()
        elapsed = time.time() - start_time

        buttons = []
        stat_plus_btns = []
        stat_minus_btns = []

        for i, key in enumerate(stat_keys):
            cx = start_x + i * (col_width + col_spacing)
            plus_btn = Button(
                rect=(cx + (col_width - 64) // 2, card_y + 115, 64, 34),
                text="+",
                callback=lambda idx=i: increment_stat(idx),
                bg_color=COLOR_BTN_PLUS,
                hover_color=COLOR_BTN_PLUS_HOVER,
                font_size=20,
                bold=True,
                enabled=(remaining_points > 0)
            )
            minus_btn = Button(
                rect=(cx + (col_width - 64) // 2, card_y + 205, 64, 34),
                text="-",
                callback=lambda idx=i: decrement_stat(idx),
                bg_color=COLOR_BTN_MINUS,
                hover_color=COLOR_BTN_MINUS_HOVER,
                font_size=20,
                bold=True,
                enabled=(session_allocated[key] > 0)
            )
            stat_plus_btns.append(plus_btn)
            stat_minus_btns.append(minus_btn)
            buttons.extend([plus_btn, minus_btn])

        confirm_btn = Button(
            rect=(win_width // 2 - 190, win_height - 65, 230, 44),
            text="Confirm Allocation",
            callback=None,
            bg_color=COLOR_BTN_ACTION,
            hover_color=COLOR_BTN_ACTION_HOVER,
            font_size=18,
            bold=True
        )
        reset_btn = Button(
            rect=(win_width // 2 + 55, win_height - 65, 135, 44),
            text="Reset",
            callback=reset_allocations,
            bg_color=COLOR_BTN_DEFAULT,
            hover_color=COLOR_BTN_HOVER,
            font_size=16
        )
        buttons.extend([confirm_btn, reset_btn])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break

            elif event.type == pg.KEYDOWN:
                # 0.4s debounce: ignore Enter/Escape immediately on open so that
                # holding Enter during level-up / fireworks does not auto-confirm
                if elapsed < 0.4 and event.key in [pg.K_RETURN, pg.K_ESCAPE, pg.K_SPACE]:
                    continue

                if event.key == pg.K_RETURN:
                    running = False
                    break
                elif event.key == pg.K_ESCAPE:
                    reset_allocations()
                    running = False
                    break
                elif event.key == pg.K_LEFT:
                    selected_stat_idx = (selected_stat_idx - 1) % len(stat_keys)
                elif event.key == pg.K_RIGHT:
                    selected_stat_idx = (selected_stat_idx + 1) % len(stat_keys)
                elif event.key in [pg.K_UP, pg.K_KP_PLUS, pg.K_PLUS, pg.K_EQUALS]:
                    increment_stat(selected_stat_idx)
                elif event.key in [pg.K_DOWN, pg.K_KP_MINUS, pg.K_MINUS]:
                    decrement_stat(selected_stat_idx)
                elif event.key == pg.K_r:
                    reset_allocations()

            # Handle mouse clicks
            for btn in buttons:
                if btn.handle_event(event, mouse_pos):
                    if btn is confirm_btn:
                        running = False
                        break

        if not running:
            break

        draw_screen(stat_plus_btns, stat_minus_btns, confirm_btn, reset_btn)
        clock.tick(60)

    # Clean up and refocus terminal
    refocus_terminal(terminal_hwnd)

    # Save remaining points to player
    player.points = remaining_points

    # Print summary to terminal
    allocated_summary = [f"+{session_allocated[k]} {k}" for k in stat_keys if session_allocated[k] > 0]
    if allocated_summary:
        dprint(f"[Level Up] {player.name} allocated: {', '.join(allocated_summary)}. Unspent points: {player.points}.")
    else:
        dprint(f"[Level Up] No points allocated this time. Unspent points: {player.points}.")

    # Accuracy has a base gain of 1 per level up from original game logic
    return (
        session_allocated['Hit Points'],
        session_allocated['Attack Power'],
        session_allocated['Accuracy'] + 1,
        session_allocated['Magic'],
        session_allocated['Speed'],
        session_allocated['Skill Learn Rate']
    )


# ---------------------------------------------------------------------------
# 2. HOSPITAL GUI WINDOW
# ---------------------------------------------------------------------------
def run_hospital_gui(hospital, player, world=None, xp_thresholds=None):
    """
    Opens an interactive Pygame UI for Greentown Hospital.
    Features:
    - Tab 1: Doctor Clinic (Professional doctor examination and healing).
    - Tab 2: Superhealing Booth (Experimental potioneer treatments).
    - Tab 3: Patient Status (Detailed player stats, skills, inventory).
    - Tab 4: Specialized Ward (Placeholder for future medical features).
    - Leave Hospital button / Escape.
    - Clickable and keyboard navigable.
    - Concise dealing summary logged to terminal upon exit.
    """
    flush_terminal_input()
    ensure_pygame()
    terminal_hwnd = get_terminal_hwnd()

    win_width = 960
    win_height = 620
    window = pg.display.set_mode((win_width, win_height))
    pg.display.set_caption(f"{hospital.name.title()} - Medical Facility (Class {hospital.quality})")

    pg.event.clear()
    pg_hwnd = pg.display.get_wm_info()['window']
    focus_pygame_window(pg_hwnd)

    clock = pg.time.Clock()
    running = True
    start_time = time.time()

    state = {'tab': 0}
    tabs = ["Doctor Clinic", "Superheal Booth", "Patient Status", "Specialized Ward"]

    hospital_logs = ["Welcome to the hospital. Please select a service."]
    treatments_done = 0
    start_col = player.col

    def add_log(msg):
        hospital_logs.append(msg)
        if len(hospital_logs) > 6:
            hospital_logs.pop(0)

    # Healing logic without terminal spam
    def do_doctor_healing():
        nonlocal treatments_done
        cost = 1 + hospital.quality + (player.level // 3)
        if player.col < cost:
            add_log(f"Not enough money! You need {cost} col (You have {player.col}).")
            return
        if player.level >= 85:
            add_log("The doctors are far too intimidated by your aura to treat you!")
            return
        if player.hp >= player.maxhp:
            add_log("You are already at full health!")
            return

        player.col -= cost
        treatments_done += 1
        xp_gained = 0

        max_rounds = max(1, 8 - (player.level // 10))
        doctors = init_doctors()
        suitable_docs = [d for d in doctors if d.level <= max(1, player.level + 2)]
        doc = random.choice(suitable_docs if suitable_docs else doctors)

        for r in range(1, max_rounds + 1):
            if random.random() < doc.accuracy:
                gain = doc.heal
                player.hp = min(player.maxhp, player.hp + gain)
                add_log(f"{doc.name} treated {player.name} (+{gain} HP).")
            else:
                add_log(f"{doc.name} examined {player.name}'s condition.")

            if player.hp >= player.maxhp:
                break

            # Friendly counter interaction
            acc_rate = (player.accuracy / 1000.0) if player.accuracy > 1 else player.accuracy
            if random.random() < acc_rate:
                doc.hp -= max(1, player.atk)
                if not doc.is_alive():
                    if xp_thresholds:
                        player.gain_xp(doc.xp, xp_thresholds)
                        xp_gained += doc.xp
                    add_log(f"{doc.name} ended their shift. Gained +{doc.xp} consultation XP!")
                    break

        if player.hp >= player.maxhp:
            add_log(f"Treatment complete! Fully restored to {player.maxhp} HP.")
        else:
            add_log(f"Treatment session ended. HP: {player.hp}/{player.maxhp}.")

    def do_superheal():
        nonlocal treatments_done
        cost = 5 + (hospital.quality // 2)
        if player.col < cost:
            add_log(f"Not enough money! Potion costs {cost} col (You have {player.col}).")
            return

        player.col -= cost
        treatments_done += 1

        roll = random.random()
        if roll > 0.8:
            player.hp = player.maxhp
            add_log("MIRACLE POTION! Health completely restored to maximum!")
        elif roll > 0.55:
            player.hp = max(1, player.maxhp - 5)
            add_log("The potion worked decently! Restored to near maximum health.")
        elif roll > 0.35:
            add_log("Fzzzz... Another dud potion! No healing effect.")
        else:
            player.hp = max(1, player.hp - 1)
            add_log("Ouch! The potioneer flung a stray potion bottle for 1 damage!")

    while running:
        mouse_pos = pg.mouse.get_pos()
        current_tab = state['tab']
        elapsed = time.time() - start_time

        buttons = []

        # Tab buttons
        tab_w = 170
        for i, tab_title in enumerate(tabs):
            t_btn = Button(
                rect=(30 + i * (tab_w + 10), 80, tab_w, 38),
                text=tab_title,
                callback=lambda idx=i: state.update(tab=idx),
                bg_color=COLOR_BTN_TAB_ACTIVE if i == current_tab else COLOR_BTN_TAB,
                hover_color=COLOR_BTN_HOVER,
                font_size=15,
                bold=(i == current_tab)
            )
            buttons.append(t_btn)

        # Leave button
        leave_btn = Button(
            rect=(win_width - 160, 80, 130, 38),
            text="Leave Hospital",
            callback=None,
            bg_color=COLOR_BTN_MINUS,
            hover_color=COLOR_BTN_MINUS_HOVER,
            font_size=15,
            bold=True
        )
        buttons.append(leave_btn)

        # Action buttons inside active tab
        clinic_cost = 1 + hospital.quality + (player.level // 3)
        super_cost = 5 + (hospital.quality // 2)

        treat_btn = None
        potion_btn = None

        if current_tab == 0:
            treat_btn = Button(
                rect=(360, 240, 240, 48),
                text=f"Receive Treatment ({clinic_cost} Col)",
                callback=do_doctor_healing,
                bg_color=COLOR_BTN_ACTION,
                hover_color=COLOR_BTN_ACTION_HOVER,
                font_size=16,
                bold=True,
                enabled=(player.col >= clinic_cost and player.hp < player.maxhp and player.level < 85)
            )
            buttons.append(treat_btn)

        elif current_tab == 1:
            potion_btn = Button(
                rect=(360, 240, 240, 48),
                text=f"Drink Potion ({super_cost} Col)",
                callback=do_superheal,
                bg_color=COLOR_BTN_PLUS,
                hover_color=COLOR_BTN_PLUS_HOVER,
                font_size=16,
                bold=True,
                enabled=(player.col >= super_cost)
            )
            buttons.append(potion_btn)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            elif event.type == pg.KEYDOWN:
                if elapsed < 0.25 and event.key in [pg.K_ESCAPE, pg.K_RETURN]:
                    continue
                if event.key == pg.K_ESCAPE:
                    running = False
                    break
                elif event.key == pg.K_1:
                    state['tab'] = 0
                elif event.key == pg.K_2:
                    state['tab'] = 1
                elif event.key == pg.K_3:
                    state['tab'] = 2
                elif event.key == pg.K_4:
                    state['tab'] = 3
                elif event.key == pg.K_LEFT:
                    state['tab'] = (state['tab'] - 1) % len(tabs)
                elif event.key == pg.K_RIGHT:
                    state['tab'] = (state['tab'] + 1) % len(tabs)
                elif event.key == pg.K_RETURN:
                    if current_tab == 0 and treat_btn and treat_btn.enabled:
                        do_doctor_healing()
                    elif current_tab == 1 and potion_btn and potion_btn.enabled:
                        do_superheal()

        for i, b in enumerate(buttons):
            if b.handle_event(event, mouse_pos):
                if b is leave_btn:
                    running = False
                    break
                elif i < len(tabs):
                    state['tab'] = i

        if not running:
            break

        # Render UI
        window.fill(COLOR_BG)

        # Top Header Banner
        header_rect = pg.Rect(0, 0, win_width, 70)
        pg.draw.rect(window, COLOR_HEADER_BG, header_rect)
        pg.draw.line(window, COLOR_PANEL_BORDER, (0, 70), (win_width, 70), 1)

        title_font = get_font(22, bold=True)
        window.blit(title_font.render(hospital.name.title(), True, COLOR_TEXT_MAIN), (30, 12))

        sub_font = get_font(14)
        window.blit(sub_font.render(f"Medical Facility  *  Class {hospital.quality}", True, COLOR_TEXT_MUTED), (32, 40))

        # Header Status: Health Bar & Col
        status_x = win_width - 440
        hp_pct = max(0.0, min(1.0, player.hp / max(1, player.maxhp)))

        bar_rect = pg.Rect(status_x, 22, 180, 24)
        pg.draw.rect(window, (45, 20, 20), bar_rect, border_radius=4)
        fill_w = int(180 * hp_pct)
        if fill_w > 0:
            pg.draw.rect(window, COLOR_TEXT_GREEN, (status_x, 22, fill_w, 24), border_radius=4)
        pg.draw.rect(window, COLOR_PANEL_BORDER, bar_rect, width=1, border_radius=4)

        hp_txt = sub_font.render(f"HP: {player.hp}/{player.maxhp}", True, COLOR_TEXT_MAIN)
        window.blit(hp_txt, hp_txt.get_rect(center=bar_rect.center))

        col_txt = get_font(17, bold=True).render(f"{player.col} Col", True, COLOR_TEXT_GOLD)
        window.blit(col_txt, (win_width - 230, 24))

        # Draw Tab Buttons
        for b in buttons:
            b.draw(window)

        # Content Area Panel
        content_rect = pg.Rect(30, 130, win_width - 60, 310)
        pg.draw.rect(window, COLOR_PANEL, content_rect, border_radius=8)
        pg.draw.rect(window, COLOR_PANEL_BORDER, content_rect, width=1, border_radius=8)

        # TAB 0: Doctor Clinic
        if current_tab == 0:
            h_font = get_font(19, bold=True)
            body_font = get_font(15)

            window.blit(h_font.render("General Treatment Clinic", True, COLOR_TEXT_MAIN), (50, 150))
            desc1 = "Our trained physicians will examine and treat your wounds until you are fully restored."
            desc2 = f"Service fee: {clinic_cost} Col (scaled with facility class and player level)."
            window.blit(body_font.render(desc1, True, COLOR_TEXT_MUTED), (50, 182))
            window.blit(body_font.render(desc2, True, COLOR_TEXT_GOLD), (50, 206))

            if treat_btn:
                treat_btn.draw(window)

            status_note = ""
            if player.hp >= player.maxhp:
                status_note = "Your health is completely full. No treatment needed!"
            elif player.col < clinic_cost:
                status_note = f"Insufficient funds to cover doctor consultation ({clinic_cost} col required)."
            elif player.level >= 85:
                status_note = "Your legendary battle prowess intimidates the medical staff!"

            if status_note:
                note_surf = body_font.render(status_note, True, COLOR_TEXT_RED)
                window.blit(note_surf, (content_rect.centerx - note_surf.get_width() // 2, 310))

        # TAB 1: Superheal Booth
        elif current_tab == 1:
            h_font = get_font(19, bold=True)
            body_font = get_font(15)

            window.blit(h_font.render("Experimental Superheal Booth", True, COLOR_TEXT_MAIN), (50, 150))
            desc1 = "Fast and volatile potion therapy administered directly by eccentric potioneers."
            desc2 = f"Potion cost: {super_cost} Col. Highly potent, but unpredictable results may occur!"
            window.blit(body_font.render(desc1, True, COLOR_TEXT_MUTED), (50, 182))
            window.blit(body_font.render(desc2, True, COLOR_TEXT_GOLD), (50, 206))

            if potion_btn:
                potion_btn.draw(window)

        # TAB 2: Patient Status
        elif current_tab == 2:
            h_font = get_font(18, bold=True)
            stat_f = get_font(14)
            window.blit(h_font.render(f"Medical Record: {player.name}", True, COLOR_TEXT_MAIN), (50, 145))

            next_xp = xp_thresholds[player.level] if (xp_thresholds and player.level in xp_thresholds) else "N/A"
            stats_left = [
                f"Level: {player.level}",
                f"Experience: {player.xp} / {next_xp}",
                f"Hit Points: {player.hp} / {player.maxhp}",
                f"Attack Power: {player.atk}",
                f"Accuracy: {round((player.accuracy + player.acu) / 10, 1)}%",
                f"Speed: {1000 - player.agi}",
                f"Magic: {player.mag} / {player.maxmag}",
                f"Wealth: {player.col} col"
            ]

            for idx, s in enumerate(stats_left):
                col_c = COLOR_TEXT_GOLD if "Wealth" in s else (COLOR_TEXT_GREEN if "Hit Points" in s else COLOR_TEXT_MAIN)
                window.blit(stat_f.render(s, True, col_c), (55, 175 + idx * 24))

            # Right Column: Skills & Inventory summary
            window.blit(h_font.render("Known Skills:", True, COLOR_TEXT_MAIN), (380, 145))
            if player.known_skills:
                for idx, sk in enumerate(player.known_skills[:5]):
                    sk_txt = f"- {sk.name.title()}: Cost {sk.cost} MP | Power {sk.damage}"
                    window.blit(stat_f.render(sk_txt, True, COLOR_TEXT_MUTED), (385, 175 + idx * 24))
            else:
                window.blit(stat_f.render("No skills learned yet.", True, COLOR_TEXT_MUTED), (385, 175))

            window.blit(h_font.render("Inventory Overview:", True, COLOR_TEXT_MAIN), (660, 145))
            if player.inventory.contents:
                for idx, (item, count) in enumerate(list(player.inventory.contents.items())[:5]):
                    inv_txt = f"{count}x {item.name} ({item.sell_price} col)"
                    window.blit(stat_f.render(inv_txt, True, COLOR_TEXT_MUTED), (665, 175 + idx * 24))
            else:
                window.blit(stat_f.render("Pockets are currently empty.", True, COLOR_TEXT_MUTED), (665, 175))

        # TAB 3: Specialized Ward (Modular placeholder for future features)
        elif current_tab == 3:
            h_font = get_font(19, bold=True)
            body_font = get_font(15)

            window.blit(h_font.render("Specialized Surgery & Enchantment Ward", True, COLOR_TEXT_MAIN), (50, 150))
            desc1 = "Notice: This medical ward is currently undergoing renovations by the Greentown builders."
            desc2 = "Advanced organ transplants, permanent condition cures, and blessing wards will arrive here soon."
            window.blit(body_font.render(desc1, True, COLOR_TEXT_MUTED), (50, 185))
            window.blit(body_font.render(desc2, True, COLOR_TEXT_MUTED), (50, 215))

            placeholder_box = pg.Rect(50, 260, 400, 60)
            pg.draw.rect(window, COLOR_PANEL_ALT, placeholder_box, border_radius=6)
            pg.draw.rect(window, COLOR_PANEL_BORDER, placeholder_box, width=1, border_radius=6)
            window.blit(body_font.render("[ Feature Expansion Slot - Ready For New Wards ]", True, COLOR_TEXT_GOLD), (70, 280))

        # Activity Log Panel (Bottom)
        log_panel_rect = pg.Rect(30, 455, win_width - 60, 125)
        pg.draw.rect(window, COLOR_PANEL_ALT, log_panel_rect, border_radius=8)
        pg.draw.rect(window, COLOR_PANEL_BORDER, log_panel_rect, width=1, border_radius=8)

        log_h_font = get_font(14, bold=True)
        window.blit(log_h_font.render("HOSPITAL ACTIVITY LOG", True, COLOR_TEXT_MUTED), (45, 462))

        log_font = get_font(13)
        for idx, line in enumerate(reversed(hospital_logs[-4:])):
            txt_color = COLOR_TEXT_GOLD if "MIRACLE" in line or "complete" in line else (COLOR_TEXT_RED if "Ouch" in line or "dud" in line else COLOR_TEXT_MAIN)
            window.blit(log_font.render(f"- {line}", True, txt_color), (45, 485 + idx * 20))

        # Bottom Hints
        hint_font = get_font(12)
        hint_str = "[1-4 / Left-Right]: Switch Tabs   [Enter]: Perform Service   [Esc]: Leave Hospital"
        window.blit(hint_font.render(hint_str, True, COLOR_TEXT_MUTED), (30, win_height - 25))

        pg.display.flip()
        clock.tick(60)

    # Clean up and refocus terminal
    refocus_terminal(terminal_hwnd)

    # Print summary to terminal
    spent = start_col - player.col
    dprint(f"[{hospital.name.title()}] Visit finished. Treatments administered: {treatments_done}, Col spent: {spent}. Final HP: {player.hp}/{player.maxhp}, Balance: {player.col} col.")
    return True


# ---------------------------------------------------------------------------
# 3. MARKETPLACE GUI WINDOW
# ---------------------------------------------------------------------------
def run_marketplace_gui(marketplace, player, world=None, xp_thresholds=None):
    """
    Opens an interactive Pygame UI for Greentown Marketplace.
    Features:
    - Tab 1: Buy Wares (Displays market stock, scrolling, item details, buy action).
    - Tab 2: Sell Items (Displays player inventory, scrolling, unit/total value, sell 1 / sell all).
    - Tab 3: Market Info (Detailed character status & market classification).
    - Tab 4: Black Market (Underworld broker interface, ready for future expansion).
    - Leave Market button / Escape.
    - Clickable and keyboard navigable.
    - Concise transaction summary logged to terminal upon exit.
    """
    flush_terminal_input()
    ensure_pygame()
    terminal_hwnd = get_terminal_hwnd()

    marketplace.stock_inventory()

    win_width = 1000
    win_height = 660
    window = pg.display.set_mode((win_width, win_height))
    pg.display.set_caption(f"{marketplace.name.title()} (Class {marketplace.level} Market)")

    pg.event.clear()
    pg_hwnd = pg.display.get_wm_info()['window']
    focus_pygame_window(pg_hwnd)

    clock = pg.time.Clock()
    running = True
    start_time = time.time()

    state = {
        'tab': 0,
        'buy_idx': 0,
        'sell_idx': 0,
        'buy_scroll': 0,
        'sell_scroll': 0
    }
    tabs = ["Buy Wares", "Sell Items", "Character Info", "Black Market"]

    items_bought = 0
    items_sold = 0
    col_spent = 0
    col_earned = 0

    market_logs = ["Welcome to the market! Browse our wares or sell your spoils."]

    def add_log(msg):
        market_logs.append(msg)
        if len(market_logs) > 6:
            market_logs.pop(0)

    def do_buy(item):
        nonlocal items_bought, col_spent
        if player.col < item.sell_price:
            add_log(f"Too expensive! You need {item.sell_price} col (You have {player.col}).")
            return
        if marketplace.inventory.get(item, 0) <= 0:
            add_log(f"Sorry, {item.name} is currently out of stock!")
            return

        # Pockets full check (max 10 of same item)
        existing = next((k for k in player.inventory.contents if k.name == item.name), None)
        if existing and player.inventory.contents[existing] >= 10:
            add_log(f"Your pockets cannot carry more than 10 {item.name}s!")
            return

        player.col -= item.sell_price
        player.inventory.add_item(item)
        marketplace.update_inventory(item)
        items_bought += 1
        col_spent += item.sell_price
        add_log(f"Purchased 1x {item.name} for {item.sell_price} col.")

    def do_sell(item, sell_all=False):
        nonlocal items_sold, col_earned
        if item not in player.inventory.contents:
            return
        count = player.inventory.contents[item]
        to_sell = count if sell_all else 1

        for _ in range(to_sell):
            player.inventory.remove_item(item)
            player.col += item.sell_price
            items_sold += 1
            col_earned += item.sell_price

        add_log(f"Sold {to_sell}x {item.name} for {item.sell_price * to_sell} col.")

    while running:
        mouse_pos = pg.mouse.get_pos()
        current_tab = state['tab']
        elapsed = time.time() - start_time

        # Available items in market
        buyable_items = [it for it in marketplace.inventory.keys() if marketplace.inventory.get(it, 0) > 0]
        # Player inventory items
        sellable_items = list(player.inventory.contents.keys())

        # Clamp indices
        if buyable_items:
            state['buy_idx'] = max(0, min(state['buy_idx'], len(buyable_items) - 1))
        else:
            state['buy_idx'] = 0

        if sellable_items:
            state['sell_idx'] = max(0, min(state['sell_idx'], len(sellable_items) - 1))
        else:
            state['sell_idx'] = 0

        # Adjust scroll offsets so selected item is always visible
        if buyable_items:
            if state['buy_idx'] < state['buy_scroll']:
                state['buy_scroll'] = state['buy_idx']
            elif state['buy_idx'] >= state['buy_scroll'] + 7:
                state['buy_scroll'] = state['buy_idx'] - 6

        if sellable_items:
            if state['sell_idx'] < state['sell_scroll']:
                state['sell_scroll'] = state['sell_idx']
            elif state['sell_idx'] >= state['sell_scroll'] + 7:
                state['sell_scroll'] = state['sell_idx'] - 6

        buttons = []

        # Tabs
        tab_w = 160
        for i, tab_title in enumerate(tabs):
            t_btn = Button(
                rect=(30 + i * (tab_w + 10), 80, tab_w, 38),
                text=tab_title,
                callback=lambda idx=i: state.update(tab=idx),
                bg_color=COLOR_BTN_TAB_ACTIVE if i == current_tab else COLOR_BTN_TAB,
                hover_color=COLOR_BTN_HOVER,
                font_size=15,
                bold=(i == current_tab)
            )
            buttons.append(t_btn)

        # Leave button
        leave_btn = Button(
            rect=(win_width - 160, 80, 130, 38),
            text="Leave Market",
            callback=None,
            bg_color=COLOR_BTN_MINUS,
            hover_color=COLOR_BTN_MINUS_HOVER,
            font_size=15,
            bold=True
        )
        buttons.append(leave_btn)

        # Buy / Sell action buttons
        buy_action_btn = None
        sell_one_btn = None
        sell_all_btn = None

        if current_tab == 0 and buyable_items:
            active_item = buyable_items[state['buy_idx']]
            can_afford = (player.col >= active_item.sell_price)
            buy_action_btn = Button(
                rect=(700, 385, 230, 46),
                text=f"Buy Item ({active_item.sell_price} Col)",
                callback=lambda it=active_item: do_buy(it),
                bg_color=COLOR_BTN_ACTION,
                hover_color=COLOR_BTN_ACTION_HOVER,
                font_size=16,
                bold=True,
                enabled=can_afford
            )
            buttons.append(buy_action_btn)

        elif current_tab == 1 and sellable_items:
            active_item = sellable_items[state['sell_idx']]
            cnt = player.inventory.contents.get(active_item, 0)
            sell_one_btn = Button(
                rect=(700, 360, 230, 40),
                text=f"Sell 1 ({active_item.sell_price} Col)",
                callback=lambda it=active_item: do_sell(it, False),
                bg_color=COLOR_BTN_PLUS,
                hover_color=COLOR_BTN_PLUS_HOVER,
                font_size=15,
                bold=True
            )
            sell_all_btn = Button(
                rect=(700, 410, 230, 40),
                text=f"Sell All ({active_item.sell_price * cnt} Col)",
                callback=lambda it=active_item: do_sell(it, True),
                bg_color=COLOR_BTN_ACTION,
                hover_color=COLOR_BTN_ACTION_HOVER,
                font_size=15,
                bold=True
            )
            buttons.extend([sell_one_btn, sell_all_btn])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            elif event.type == pg.KEYDOWN:
                if elapsed < 0.25 and event.key in [pg.K_ESCAPE, pg.K_RETURN]:
                    continue
                if event.key == pg.K_ESCAPE:
                    running = False
                    break
                elif event.key == pg.K_1:
                    state['tab'] = 0
                elif event.key == pg.K_2:
                    state['tab'] = 1
                elif event.key == pg.K_3:
                    state['tab'] = 2
                elif event.key == pg.K_4:
                    state['tab'] = 3
                elif event.key == pg.K_LEFT:
                    state['tab'] = (state['tab'] - 1) % len(tabs)
                elif event.key == pg.K_RIGHT:
                    state['tab'] = (state['tab'] + 1) % len(tabs)
                elif event.key == pg.K_UP:
                    if current_tab == 0 and buyable_items:
                        state['buy_idx'] = (state['buy_idx'] - 1) % len(buyable_items)
                    elif current_tab == 1 and sellable_items:
                        state['sell_idx'] = (state['sell_idx'] - 1) % len(sellable_items)
                elif event.key == pg.K_DOWN:
                    if current_tab == 0 and buyable_items:
                        state['buy_idx'] = (state['buy_idx'] + 1) % len(buyable_items)
                    elif current_tab == 1 and sellable_items:
                        state['sell_idx'] = (state['sell_idx'] + 1) % len(sellable_items)
                elif event.key == pg.K_RETURN:
                    if current_tab == 0 and buy_action_btn and buy_action_btn.enabled:
                        do_buy(buyable_items[state['buy_idx']])
                    elif current_tab == 1 and sell_one_btn:
                        do_sell(sellable_items[state['sell_idx']], False)

            elif event.type == pg.MOUSEWHEEL:
                if current_tab == 0 and buyable_items:
                    state['buy_scroll'] = max(0, min(max(0, len(buyable_items) - 7), state['buy_scroll'] - event.y))
                elif current_tab == 1 and sellable_items:
                    state['sell_scroll'] = max(0, min(max(0, len(sellable_items) - 7), state['sell_scroll'] - event.y))

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Check item list clicks
                if current_tab == 0:
                    visible_slice = buyable_items[state['buy_scroll']: state['buy_scroll'] + 7]
                    for idx, _ in enumerate(visible_slice):
                        item_r = pg.Rect(50, 195 + idx * 36, 600, 32)
                        if item_r.collidepoint(event.pos):
                            state['buy_idx'] = state['buy_scroll'] + idx
                elif current_tab == 1:
                    visible_slice = sellable_items[state['sell_scroll']: state['sell_scroll'] + 7]
                    for idx, _ in enumerate(visible_slice):
                        item_r = pg.Rect(50, 195 + idx * 36, 600, 32)
                        if item_r.collidepoint(event.pos):
                            state['sell_idx'] = state['sell_scroll'] + idx

        for i, b in enumerate(buttons):
            if b.handle_event(event, mouse_pos):
                if b is leave_btn:
                    running = False
                    break
                elif i < len(tabs):
                    state['tab'] = i

        # Re-sync items after any buy/sell action
        buyable_items = [it for it in marketplace.inventory.keys() if marketplace.inventory.get(it, 0) > 0]
        sellable_items = list(player.inventory.contents.keys())
        if buyable_items:
            state['buy_idx'] = max(0, min(state['buy_idx'], len(buyable_items) - 1))
        else:
            state['buy_idx'] = 0
        if sellable_items:
            state['sell_idx'] = max(0, min(state['sell_idx'], len(sellable_items) - 1))
        else:
            state['sell_idx'] = 0

        if not running:
            break

        # Render UI
        window.fill(COLOR_BG)

        # Header Banner
        header_rect = pg.Rect(0, 0, win_width, 70)
        pg.draw.rect(window, COLOR_HEADER_BG, header_rect)
        pg.draw.line(window, COLOR_PANEL_BORDER, (0, 70), (win_width, 70), 1)

        title_font = get_font(22, bold=True)
        window.blit(title_font.render(marketplace.name.title(), True, COLOR_TEXT_MAIN), (30, 12))

        sub_font = get_font(14)
        inv_total = sum(player.inventory.contents.values())
        sub_str = f"Class {marketplace.level} Central Market   |   Adventurer: {player.name}   |   Pockets: {inv_total} items"
        window.blit(sub_font.render(sub_str, True, COLOR_TEXT_MUTED), (32, 40))

        # Balance display
        col_txt = get_font(20, bold=True).render(f"{player.col} Col", True, COLOR_TEXT_GOLD)
        window.blit(col_txt, (win_width - 200, 22))

        # Draw Tab Buttons
        for b in buttons:
            b.draw(window)

        # Main Workspace Panel
        panel_rect = pg.Rect(30, 130, win_width - 60, 335)
        pg.draw.rect(window, COLOR_PANEL, panel_rect, border_radius=8)
        pg.draw.rect(window, COLOR_PANEL_BORDER, panel_rect, width=1, border_radius=8)

        # TAB 0: Buy Wares
        if current_tab == 0:
            h_font = get_font(18, bold=True)
            item_font = get_font(15)
            val_font = get_font(14, bold=True)
            stat_f = get_font(13)

            count_str = f"({len(buyable_items)} items available)"
            window.blit(h_font.render(f"Available Market Stock {count_str}", True, COLOR_TEXT_MAIN), (50, 145))
            window.blit(stat_f.render("Click or [Up/Down] to select an item. Press [Enter] or 'Buy Item' to purchase.", True, COLOR_TEXT_MUTED), (50, 170))

            if not buyable_items:
                window.blit(item_font.render("All stock has been purchased for today!", True, COLOR_TEXT_MUTED), (60, 220))
            else:
                visible_slice = buyable_items[state['buy_scroll']: state['buy_scroll'] + 7]
                for idx, it in enumerate(visible_slice):
                    actual_idx = state['buy_scroll'] + idx
                    row_r = pg.Rect(50, 195 + idx * 36, 610, 32)
                    is_sel = (actual_idx == state['buy_idx'])
                    r_bg = (55, 68, 92) if is_sel else ((42, 50, 68) if idx % 2 == 0 else COLOR_PANEL_ALT)
                    pg.draw.rect(window, r_bg, row_r, border_radius=5)
                    if is_sel:
                        pg.draw.rect(window, COLOR_BTN_FOCUS, row_r, width=2, border_radius=5)

                    name_col = COLOR_TEXT_GOLD if is_sel else COLOR_TEXT_MAIN
                    window.blit(item_font.render(it.name.title(), True, name_col), (60, 201 + idx * 36))

                    stock_cnt = marketplace.inventory.get(it, 0)
                    stock_str = f"Stock: {stock_cnt}"
                    window.blit(stat_f.render(stock_str, True, COLOR_TEXT_MUTED), (380, 202 + idx * 36))

                    price_str = f"{it.sell_price} Col"
                    window.blit(val_font.render(price_str, True, COLOR_TEXT_GOLD), (530, 201 + idx * 36))

                # Scroll indicator
                if len(buyable_items) > 7:
                    scroll_info = f"Viewing {state['buy_scroll'] + 1}-{min(len(buyable_items), state['buy_scroll'] + 7)} of {len(buyable_items)}"
                    window.blit(stat_f.render(scroll_info, True, COLOR_TEXT_MUTED), (490, 148))

                # Right Details Panel for Selected Item
                details_r = pg.Rect(680, 150, 260, 220)
                pg.draw.rect(window, COLOR_PANEL_ALT, details_r, border_radius=8)
                pg.draw.rect(window, COLOR_PANEL_BORDER, details_r, width=1, border_radius=8)

                sel_item = buyable_items[state['buy_idx']]
                window.blit(h_font.render(sel_item.name.title(), True, COLOR_TEXT_GOLD), (695, 165))

                details = [
                    f"Item Level: {sel_item.level}",
                    f"Rarity: {sel_item.rarity}",
                    f"Price: {sel_item.sell_price} Col",
                    f"Stock: {marketplace.inventory.get(sel_item, 0)} left"
                ]
                if sel_item.power > 0:
                    details.append(f"Power: +{sel_item.power}")
                if sel_item.potency > 0:
                    details.append(f"Potency: +{sel_item.potency}")
                if sel_item.is_ingredient:
                    details.append("Alchemical Ingredient: Yes")

                for d_idx, d_line in enumerate(details):
                    window.blit(stat_f.render(d_line, True, COLOR_TEXT_MAIN), (695, 200 + d_idx * 22))

                if buy_action_btn:
                    buy_action_btn.draw(window)

        # TAB 1: Sell Items
        elif current_tab == 1:
            h_font = get_font(18, bold=True)
            item_font = get_font(15)
            val_font = get_font(14, bold=True)
            stat_f = get_font(13)

            count_str = f"({len(sellable_items)} unique items)"
            window.blit(h_font.render(f"Your Inventory Spoils {count_str}", True, COLOR_TEXT_MAIN), (50, 145))
            window.blit(stat_f.render("Select an item to sell. Merchants pay fair col for all valid wares.", True, COLOR_TEXT_MUTED), (50, 170))

            if not sellable_items:
                window.blit(item_font.render("Your inventory is currently empty! Slay monsters to acquire loot.", True, COLOR_TEXT_MUTED), (60, 220))
            else:
                visible_slice = sellable_items[state['sell_scroll']: state['sell_scroll'] + 7]
                for idx, it in enumerate(visible_slice):
                    actual_idx = state['sell_scroll'] + idx
                    row_r = pg.Rect(50, 195 + idx * 36, 610, 32)
                    is_sel = (actual_idx == state['sell_idx'])
                    r_bg = (55, 68, 92) if is_sel else ((42, 50, 68) if idx % 2 == 0 else COLOR_PANEL_ALT)
                    pg.draw.rect(window, r_bg, row_r, border_radius=5)
                    if is_sel:
                        pg.draw.rect(window, COLOR_BTN_FOCUS, row_r, width=2, border_radius=5)

                    name_col = COLOR_TEXT_GOLD if is_sel else COLOR_TEXT_MAIN
                    window.blit(item_font.render(it.name.title(), True, name_col), (60, 201 + idx * 36))

                    cnt = player.inventory.contents.get(it, 0)
                    window.blit(stat_f.render(f"Quantity: {cnt}", True, COLOR_TEXT_MUTED), (380, 202 + idx * 36))

                    total_v = it.sell_price * cnt
                    window.blit(val_font.render(f"{it.sell_price} col ea ({total_v} tot)", True, COLOR_TEXT_GOLD), (490, 201 + idx * 36))

                # Scroll indicator
                if len(sellable_items) > 7:
                    scroll_info = f"Viewing {state['sell_scroll'] + 1}-{min(len(sellable_items), state['sell_scroll'] + 7)} of {len(sellable_items)}"
                    window.blit(stat_f.render(scroll_info, True, COLOR_TEXT_MUTED), (490, 148))

                # Right Details Panel for Selected Item
                details_r = pg.Rect(680, 150, 260, 200)
                pg.draw.rect(window, COLOR_PANEL_ALT, details_r, border_radius=8)
                pg.draw.rect(window, COLOR_PANEL_BORDER, details_r, width=1, border_radius=8)

                sel_item = sellable_items[state['sell_idx']]
                window.blit(h_font.render(sel_item.name.title(), True, COLOR_TEXT_GOLD), (695, 165))

                item_cnt = player.inventory.contents.get(sel_item, 0)
                details = [
                    f"Owned: {item_cnt}",
                    f"Sell Value: {sel_item.sell_price} Col each",
                    f"Total Value: {sel_item.sell_price * item_cnt} Col",
                    f"Item Level: {sel_item.level}"
                ]
                for d_idx, d_line in enumerate(details):
                    window.blit(stat_f.render(d_line, True, COLOR_TEXT_MAIN), (695, 200 + d_idx * 24))

                if sell_one_btn:
                    sell_one_btn.draw(window)
                if sell_all_btn:
                    sell_all_btn.draw(window)

        # TAB 2: Character Info
        elif current_tab == 2:
            h_font = get_font(18, bold=True)
            stat_f = get_font(14)
            window.blit(h_font.render(f"Adventurer Dossier: {player.name}", True, COLOR_TEXT_MAIN), (50, 145))

            next_xp = xp_thresholds[player.level] if (xp_thresholds and player.level in xp_thresholds) else "N/A"
            stats_left = [
                f"Level: {player.level}",
                f"Experience: {player.xp} / {next_xp}",
                f"Hit Points: {player.hp} / {player.maxhp}",
                f"Attack Power: {player.atk}",
                f"Accuracy: {round((player.accuracy + player.acu) / 10, 1)}%",
                f"Speed: {1000 - player.agi}",
                f"Magic: {player.mag} / {player.maxmag}",
                f"Col Balance: {player.col}"
            ]
            for idx, s in enumerate(stats_left):
                col_c = COLOR_TEXT_GOLD if "Col" in s else COLOR_TEXT_MAIN
                window.blit(stat_f.render(s, True, col_c), (55, 180 + idx * 24))

            # Center Column: Market Classification & Location
            window.blit(h_font.render("Market Information:", True, COLOR_TEXT_MAIN), (380, 145))
            m_info = [
                f"Location: {marketplace.name.title()}",
                f"Market Class: Level {marketplace.level}",
                f"Salable Catalog: {len(marketplace.salable)} types",
                f"Current Progress: {player.progress}/32"
            ]
            for idx, m in enumerate(m_info):
                window.blit(stat_f.render(m, True, COLOR_TEXT_MUTED), (385, 180 + idx * 24))

        # TAB 3: Black Market (Extensible placeholder for future shady features)
        elif current_tab == 3:
            h_font = get_font(19, bold=True)
            body_font = get_font(15)

            window.blit(h_font.render("Greentown Underground Syndicate", True, COLOR_TEXT_GOLD), (50, 150))
            desc1 = "A hooded merchant leans forward from the shadows..."
            desc2 = "\"Psst... The underground market is not trading with novices today.\""
            desc3 = "\"Prove your reputation further into the story, and our black market catalog will open.\""
            window.blit(body_font.render(desc1, True, COLOR_TEXT_MUTED), (50, 185))
            window.blit(body_font.render(desc2, True, COLOR_TEXT_MAIN), (50, 215))
            window.blit(body_font.render(desc3, True, COLOR_TEXT_MUTED), (50, 245))

            placeholder_box = pg.Rect(50, 285, 450, 60)
            pg.draw.rect(window, COLOR_PANEL_ALT, placeholder_box, border_radius=6)
            pg.draw.rect(window, COLOR_PANEL_BORDER, placeholder_box, width=1, border_radius=6)
            window.blit(body_font.render("[ Black Market Expansion Slot - Ready For Exotic Items ]", True, COLOR_TEXT_GOLD), (70, 305))

        # Bottom Activity Log Panel
        log_panel_rect = pg.Rect(30, 480, win_width - 60, 130)
        pg.draw.rect(window, COLOR_PANEL_ALT, log_panel_rect, border_radius=8)
        pg.draw.rect(window, COLOR_PANEL_BORDER, log_panel_rect, width=1, border_radius=8)

        log_h_font = get_font(14, bold=True)
        window.blit(log_h_font.render("MARKET DEALING SUMMARY & ACTIVITY LOG", True, COLOR_TEXT_MUTED), (45, 488))

        log_font = get_font(13)
        for idx, line in enumerate(reversed(market_logs[-4:])):
            txt_color = COLOR_TEXT_GOLD if "Purchased" in line or "Sold" in line else (COLOR_TEXT_RED if "expensive" in line else COLOR_TEXT_MAIN)
            window.blit(log_font.render(f"- {line}", True, txt_color), (45, 510 + idx * 20))

        # Bottom Hints
        hint_font = get_font(12)
        hint_str = "[1-4 / Left-Right]: Switch Tabs   [Up/Down]: Select Item   [Enter]: Buy / Sell   [Esc]: Leave Market"
        window.blit(hint_font.render(hint_str, True, COLOR_TEXT_MUTED), (30, win_height - 25))

        pg.display.flip()
        clock.tick(60)

    # Clean up and refocus terminal
    refocus_terminal(terminal_hwnd)

    # Print summary to terminal
    dprint(f"[{marketplace.name.title()}] Shopping completed. Bought: {items_bought} item(s) (-{col_spent} col), Sold: {items_sold} item(s) (+{col_earned} col). Current Balance: {player.col} col.")
    return True
