import api


def scan_surroundings(direction):
    """
    Funktionen läser av tankens omgivning och returnerar avstånden från tanken
    till närmaste lodräta och vågräta hinder. Avstånden returneras i ett format som baseras på kartans orientering.

    :param direction: Det håll tanken är riktad åt
    :return: [avstånd upp, avstånd ner, avstånd vänster, avstånd höger]
    """

    up = api.lidar_front()
    down = api.lidar_back()
    left = api.lidar_left()
    right = api.lidar_right()

    normalized_surroundings = [up, down, left, right]

    if direction == "right":
        normalized_surroundings[0] = left
        normalized_surroundings[1] = right
        normalized_surroundings[2] = down
        normalized_surroundings[3] = up

    elif direction == "down":
        normalized_surroundings[0] = down
        normalized_surroundings[1] = up
        normalized_surroundings[2] = right
        normalized_surroundings[3] = left

    elif direction == "left":
        normalized_surroundings[0] = right
        normalized_surroundings[1] = left
        normalized_surroundings[2] = up
        normalized_surroundings[3] = down

    return normalized_surroundings


class Tank:
    """
    Klassen representerar tanken och allt vad den kan göra.
    """
    def __init__(self):
        self.position = [20, 20]
        self.direction = "up"

    def update_playground(self, surroundings, playground):
        """
        Uppdaterar kartan med den information som vi får av att skanna omgivningen. Om tanken tittar
        framåt och ser ett objekt som inte är ett target vet vi att det är en vägg. Då representerar
        vi den punkten på kartan med '#' och låter den förbli så tills spelet är slut. En skannad punkt
        som vi inte vet vad det är representerar vi med '0'.

        :param surroundings: Avstånd till omgivning från tanken baserat från åskådarens perspektiv
        :param playground: Karta
        :return: True om vi ska skjuta annars false
        """
        up = surroundings[0]
        down = surroundings[1]
        left = surroundings[2]
        right = surroundings[3]

        if not api.identify_target():
            target_marker = '#'
        else:
            target_marker = ' '

        if playground[self.position[0] - up][self.position[1]] != '#':
            playground[self.position[0] - up][self.position[1]] = target_marker if self.direction == 'up' else '0'

        if playground[self.position[0] + down][self.position[1]] != '#':
            playground[self.position[0] + down][self.position[1]] = target_marker if self.direction == 'down' else '0'

        if playground[self.position[0]][self.position[1] + right] != '#':
            playground[self.position[0]][self.position[1] + right] = target_marker if self.direction == 'right' else '0'

        if playground[self.position[0]][self.position[1] - left] != '#':
            playground[self.position[0]][self.position[1] - left] = target_marker if self.direction == 'left' else '0'

        return api.identify_target()

    def turn(self, surroundings):
        """
        Tanken vrider sig åt det håll det finns mest utrymme åt.
        Efter den har vridit sig så ändras tankens riktning.

        :param surroundings: Avstånd till omgivning från tanken baserat från åskådarens perspektiv
        """
        new_dir = ''

        if self.direction == 'up':
            if surroundings[2] > 1 and surroundings[2] > surroundings[3]:
                api.turn_left()
                new_dir = 'left'
            else:
                api.turn_right()
                new_dir = 'right'

        elif self.direction == 'left':
            if surroundings[1] > 1 and surroundings[1] > surroundings[0]:
                api.turn_left()
                new_dir = 'down'
            else:
                api.turn_right()
                new_dir = 'up'

        elif self.direction == 'right':
            if surroundings[0] > 1 and surroundings[0] > surroundings[1]:
                api.turn_left()
                new_dir = 'up'
            else:
                api.turn_right()
                new_dir = 'down'

        elif self.direction == 'down':
            if surroundings[2] > 1 and surroundings[2] > surroundings[3]:
                api.turn_left()
                new_dir = 'right'
            else:
                api.turn_right()
                new_dir = 'left'

        self.direction = new_dir

    def move(self, playground):
        """
        Ändrar tankens position baserat på vilken riktning den har.

        :param playground: Karta
        """
        api.move_forward()
        playground[self.position[0]][self.position[1]] = ' '
        if self.direction == 'up':
            self.position[0] -= 1
        elif self.direction == 'down':
            self.position[0] += 1
        elif self.direction == 'left':
            self.position[1] -= 1
        elif self.direction == 'right':
            self.position[1] += 1
        playground[self.position[0]][self.position[1]] = '3'

    def fire_cannon(self):
        """
        Skjuter
        """
        api.fire_cannon()

    def target_ahead(self):
        return api.identify_target()


playground = [[' ' for i in range(41)] for j in range(41)]
tank = Tank()


class Solution:
    def __init__(self):
        self.counter = 0

    def update(self):
        surroundings = scan_surroundings(tank.direction)
        tank.update_playground(surroundings, playground)

        if tank.target_ahead():
            tank.fire_cannon()
        elif api.lidar_front() > 1:
            tank.move(playground)
        else:
            tank.turn(surroundings)

        if self.counter > 50:
            for row in playground:
                print(row)

        self.counter += 1




