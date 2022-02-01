from services.map_service import get_map
from collections import deque as queue
from services.robot_service import *
from services.cleaning_history_service import *
from environment import *
import timeit


def clean_floor(type):
    start_time = timeit.default_timer()
    # get map
    data = get_map()['data']
    map, row_size, col_size, base_row, base_col = data['map'], data['map_size_row'], data['map_size_col'], data['map_base_row'], data['map_base_col']

    # Direction vectors
    dRow = [-1, 0, 1, 0]
    dCol = [0, 1, 0, -1]

    visited = [[False for i in range(row_size)] for i in range(col_size)]

    def valid(visited, row, col):

        # If cell lies out of bounds
        if row < 0 or col < 0 or row >= row_size or col >= col_size:
            return False

        # If cell is already visited
        if visited[row][col]:
            return False

        # If it's not reachable
        if map[row][col] != 0:
            return False

        return True

    def bfs(grid, visited, row, col):
        # get battery level
        data = get_battery_level()['data']
        battery_level = data['value']

        if type == 0:
            # get bin level
            data = get_bin_level()['data']
            bin_level = data['value']
            # get cleaning settings
            data = get_cleaning_settings(type)['data']
            frequency, power = data['frequency'], data['power']
        else:
            # get resource level
            data = get_resource_level()['data']
            resource_level = data['value']
            # get cleaning settings
            data = get_cleaning_settings(type)['data']
            frequency = data['frequency']

        path = ""
        messages = ""
        # Stores indices of the matrix cells
        q = queue()

        # Mark the starting cell as visited
        # and push it into the queue
        q.append((row, col))
        visited[row][col] = True

        # Iterate while the queue
        # is not empty
        dirt = get_dirt_level()
        while len(q) > 0:
            cell = q.popleft()
            x = cell[0]
            y = cell[1]
            path += str((x, y))
            battery_level -= (dirt * power if type == 0 else dirt * 3)
            if type == 0:
                bin_level += dirt
                if bin_level >= 100:
                    bin_level = 0
                    messages += "Done automatic bin empty | "
            else:
                resource_level -= dirt * 2
                if resource_level <= 0:
                    resource_level = 100
                    messages += "Done automatic resource refill | "

            if battery_level <= 20:
                battery_level = 100
                messages += "Done automatic battery recharge | "

            # Go to the adjacent cells
            for i in range(4):
                adjx = x + dRow[i]
                adjy = y + dCol[i]
                if valid(visited, adjx, adjy):
                    q.append((adjx, adjy))
                    visited[adjx][adjy] = True
        set_battery_level(battery_level)
        if type == 0:
            set_bin_level(bin_level)
        else:
            set_resource_level(resource_level)

        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        insert_cleaning_history(type, elapsed_time)

        return path, messages

    return bfs(map, visited, base_row, base_col)


