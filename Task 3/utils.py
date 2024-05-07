from MapGeneration import generateMap, WINDOW_WIDTH


class Player:
    def __init__(self):
        self.__Map, self.__position = generateMap()

    def move_horizontal(self, n_pixels):
        i, j = self.__position

        left_first = j - 1
        right_first = j + 1

        while self.__Map[i][left_first] > 0:
            left_first -= 1
        while self.__Map[i][right_first] > 0:
            right_first += 1

        new_pos = (i, j)

        if n_pixels > 0:
            if j + n_pixels < right_first:
                new_pos = (i, j + n_pixels)
            else:
                new_pos = (i, right_first - 1)
        elif n_pixels < 0:
            if j + n_pixels > left_first:
                new_pos = (i, j + n_pixels)
            else:
                new_pos = (i, left_first + 1)

        self.__position = new_pos
        return new_pos[1] - j

    def move_vertical(self, n_pixels):
        i, j = self.__position

        top_first = i - 1
        bottom_first = i + 1

        while self.__Map[top_first][j] > 0:
            top_first -= 1
        while self.__Map[bottom_first][j] > 0:
            bottom_first += 1

        new_pos = (i, j)

        if n_pixels > 0:
            if i + n_pixels < bottom_first:
                new_pos = (i + n_pixels, j)
            else:
                new_pos = (bottom_first - 1, j)
        elif n_pixels < 0:
            if i + n_pixels > top_first:
                new_pos = (i + n_pixels, j)
            else:
                new_pos = (top_first + 1, j)

        self.__position = new_pos
        return new_pos[0] - i

    def getMap(self):
        return self.__Map

    def getSnapShot(self):
        i, j = self.__position
        return self.__Map[
            i - WINDOW_WIDTH // 2 : i + WINDOW_WIDTH // 2 + 1,
            j - WINDOW_WIDTH // 2 : j + WINDOW_WIDTH // 2 + 1,
        ]
