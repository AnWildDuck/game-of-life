from pygame import *
clock = time.Clock()

info = {
    'window_size': (500, 300),
    'grid_size': 50,
    'background': (50, 50, 50),

    'live_colour': (255, 255, 255),
}

def make_grid(size):
    grid = [False for i in range(size ** 2)]
    return grid

def pos_to_index(info, pos):
    index = pos[0]
    index += pos[1] * info['grid_size']
    return index

def index_to_pos(info, index):
    y = (int(index / info['grid_size']))
    x = (index - (y * info['grid_size']))
    return x, y

def change_cells(grid, info):

    change = None
    if mouse.get_pressed()[0]: change = True
    if mouse.get_pressed()[2]: change = False

    if not change == None:
        pos = get_pos_on_game(info)

        # Is it in a valid spot?
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] <= info['grid_size'] and pos[1] <= info['grid_size']:

            index = pos_to_index(info, pos)
            grid[index] = change
    return grid


def get_pos_on_game(info):

    pos = list(mouse.get_pos())
    game_scale = info['game_size'] / info['grid_size']

    pos[0] -= (info['window_size'][0] - info['game_size']) / 2
    pos[1] -= (info['window_size'][1] - info['game_size']) / 2

    pos[0] /= game_scale
    pos[1] /= game_scale

    pos[0] = int(pos[0])
    pos[1] = int(pos[1])

    return pos


def show_cells(window, grid, info):

    game_scale = info['game_size'] / info['grid_size']
    for value_index in range(len(grid)):

        # Change index to pos
        x, y = index_to_pos(info, value_index)

        value = grid[value_index]
        if value: draw.rect(window, info['live_colour'], (x * game_scale, y * game_scale, int(game_scale + .5), int(game_scale + .5)))


def update_cells(info, grid):
    copy = list(grid)

    for index in range(len(grid)):
        neighbours = 0
        pos = index_to_pos(info, index)

        for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
            new_pos = pos[0] + x, pos[1] + y

            # Is the new spot valid
            if new_pos[0] >= 0 and new_pos[1] >= 0 and new_pos[0] < info['grid_size'] and new_pos[1] < info['grid_size']:

                new_index = pos_to_index(info, new_pos)
                if copy[new_index]: neighbours += 1

        # If live
        if not grid[index]:
            if neighbours == 3:
                grid[index] = True

        else:
            if neighbours < 2: grid[index] = False
            elif neighbours <= 3: pass
            elif neighbours >= 4: grid[index] = False

        # If dead

    return grid


def game(info):

    # Add the game size (NOT window size) to info
    info['game_size'] = int(min(info['window_size']))
    grid = make_grid(info['grid_size'])

    global clock

    # Set windows
    main_window = display.set_mode(info['window_size'], RESIZABLE)
    game_window = Surface((info['game_size'],) * 2)

    running = 0
    time = 0

    while True:

        # Resize loop
        for e in event.get():
            if e.type == VIDEORESIZE:

                # Set sizes
                info['window_size'] = e.w, e.h
                info['game_size'] = int(min(info['window_size']))

                # Set Surfaces
                main_window = display.set_mode(info['window_size'], RESIZABLE)
                game_window = Surface((info['game_size'],) * 2)

            if e.type == QUIT: quit()

            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    running = abs(running - 1)

                if e.key == K_SPACE:
                    grid = update_cells(info, grid)

                if e.key == K_c:
                    grid = make_grid(info['grid_size'])

        game_window.fill(info['background'])

        grid = change_cells(grid, info)
        show_cells(game_window, grid, info)

        display.set_caption(str(time))

        time_to_update = 0.1

        if running:
            time += clock.tick() / 1000
            if time > time_to_update:
                grid = update_cells(info, grid)
                time -= time_to_update

        clock.tick()


        # Add the game window to the main and show
        main_window.blit(game_window, ((info['window_size'][0] - info['game_size']) / 2, (info['window_size'][1] - info['game_size']) / 2))
        display.update()



game(info)
