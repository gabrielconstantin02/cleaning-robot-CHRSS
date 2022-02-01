from map_service import get_map


def clean_floor():
    map, row_size, col_size, base_row, base_col = get_map(False)
    from collections import deque as queue

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

        # Stores indices of the matrix cells
        q = queue()

        # Mark the starting cell as visited
        # and push it into the queue
        q.append((row, col))
        visited[row][col] = True

        # Iterate while the queue
        # is not empty
        while len(q) > 0:
            cell = q.popleft()
            x = cell[0]
            y = cell[1]
            print(grid[x][y], end=" ")

            # q.pop()

            # Go to the adjacent cells
            for i in range(4):
                adjx = x + dRow[i]
                adjy = y + dCol[i]
                if valid(visited, adjx, adjy):
                    q.append((adjx, adjy))
                    visited[adjx][adjy] = True

    bfs(map, visited, base_row, base_col)
    return 'All Clean!'

