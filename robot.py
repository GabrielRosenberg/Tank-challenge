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
        normalized_surroundings = [left,right,down,up]

    elif direction == "down":
        normalized_surroundings = [down,up,right,left] 

    elif direction == "left":
        normalized_surroundings = [right,left,up,down]

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

        # 
        for i in range(up):
            playground[self.position[0] - i][self.position[1]] = ' ' 
        for i in range(down): 
            playground[self.position[0] + i][self.position[1]] = ' '
        for i in range(right): 
            playground[self.position[0]][self.position[1] + i] = ' ' 
        for i in range(left):
            playground[self.position[0]][self.position[1] - i] = ' '

        # Update what's above us
        if playground[self.position[0] - up][self.position[1]] != '#':
            playground[self.position[0] - up][self.position[1]] = target_marker if self.direction == 'up' else '0'

        # Update what's below us
        if playground[self.position[0] + down][self.position[1]] != '#':
            playground[self.position[0] + down][self.position[1]] = target_marker if self.direction == 'down' else '0'

        # Update what's right of us
        if playground[self.position[0]][self.position[1] + right] != '#':
            playground[self.position[0]][self.position[1] + right] = target_marker if self.direction == 'right' else '0'

        # Update what's left of us
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
            if surroundings[3] > 1 and surroundings[3] > surroundings[2]:
                api.turn_left()
                new_dir = 'right'
            else:
                api.turn_right()
                new_dir = 'left'

        self.direction = new_dir


    ########## TANK MOVEMENT METHODS
    def new_turn_function(self, new_direction="up"):
        """
        Inputs a direction and turns the tank clock-wise until it faces the new direction
        
        :param new_direction: String value indicating the direction, e.g "left"
        """
        # For translating directions to numerical values
        directions = ["up","right","down","left"]
            
        # Gets index for direction
        old_dir_index = directions.index(self.direction)    # 2 if "down"
        new_dir_index = directions.index(new_direction)     # 0 if "up"

        # new_dir - old_dir -  ger ett värde för hur mycket vi ska svänga.
        diff = new_dir_index-old_dir_index 

        # Check diff
        if diff == 3:
            turns = -1
        elif diff == -3:
            turns = 1
        else:
            turns = diff

        # Turns är antal steg att svänga 
        # Positiva värden är steg åt höger, Negativa värden är steg åt vänster
        return turns

    def move_forward(self, playground):
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

    ##########




playground = [[' ' for i in range(41)] for j in range(41)]
tank = Tank()

class Solution:
    def __init__(self):
        self.counter = 0

    def update(self):
        surroundings = scan_surroundings(tank.direction)

        if tank.target_ahead():
            tank.fire_cannon()
        
        # turn? = eval_space(surroundings)
        
        elif playground[self.position[0] - surroundings[0]][self.position[1]] == ' ':
            turn('up')
        elif playground[self.position[0] + surroundings[1]][self.position[1]] == ' ':
            turn('down')
        elif playground[self.position[0]][self.position[1] + surroundings[3]] == ' ':
            turn('right')
        elif playground[self.position[0]][self.position[1] - left] == ' ':
            turn('left')
        elif api.lidar_front() > 1:
            tank.move(playground)
        else:
            tank.turn(surroundings)

        tank.update_playground(surroundings, playground)

        """if tank.target_ahead():
            tank.fire_cannon()
        elif api.lidar_front() > 1:
            tank.move_forward(playground)
        else:
            tank.turn(surroundings)"""

        #Printar mappen var 10e frame
        if (self.counter%10) == 0:
            print("\n\n\n")
            for row in playground:
                print(row)
            

        self.counter += 1




