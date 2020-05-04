from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def allrooms(player):

    def breadth_for_search(graph, v1, v2):
        # print((" "*2), "breadth_for_search() excueted")

        plan_to_visit = Queue()
        # print((" "*2), "plan_to_visit=>", plan_to_visit)

        plan_to_visit.enqueue([(v1, None)])
        # print((" "*2), "plan_to_visit.queue=>", plan_to_visit.queue)
        visited = set()

        while plan_to_visit.size() > 0:

            path = plan_to_visit.dequeue()

            # print((" "*3), "path=>", path)
            # GRAB THE VERTEX FROM THE END OF THE PATH
            vertex = path[-1][0]
            # print((" "*3), "vertex=>", vertex)

            if vertex not in visited:

                visited.add(vertex)

                if vertex == v2:
                    # IF SO, RETURN THE PATH
                    # print((" "*5), " return path =>", path)
                    return path
                # Enqueue A PATH TO all it's neighbors
                for direction, room in graph[vertex].items():
                    # MAKE A COPY OF THE PATH
                    # print((" "*5), "direction=>", direction)
                    # print((" "*5), "room=>", room)
                    path_copy = path.copy()

                    # append neighbor
                    path_copy.append((room, direction))
                    # ENQUEUE THE COPY
                    plan_to_visit.enqueue(path_copy)
    print()

    visited = set()
    graph = dict()

    previous_room = None
    direction_arrived_from = None

    # define opposite rooms
    mirror = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    while True:
        # backtracking
        while previous_room != player.current_room.id:
            # print((" "*3), 'player.current_room.id=>', player.current_room.id)
            visited.add(player.current_room.id)
            # print((" "*3), "visited=>", visited)
            # get list of exits for room
            exits = player.current_room.get_exits()
            # print((" "*3), "graph=>", graph)
            # print((" "*3), "exits=>", exits)

            # if not visited before
            if player.current_room.id not in graph:
                # add to graph
                graph[player.current_room.id] = dict()
                # print((" "*4), "graph[player.current_room.id]=>",
                #       graph[player.current_room.id])
                # add exits to graph
                for exit in exits:
                    # print((" "*5), "exit=>", exit)
                    graph[player.current_room.id][exit] = '?'

            # var with/ the previous room into current room's entry
            if previous_room is not None:
                graph[player.current_room.id][mirror[direction_arrived_from]
                                              ] = previous_room.id
            # var with/ current room into previous room's entry
            if previous_room is not None:
                graph[previous_room.id][direction_arrived_from] = player.current_room.id

            # find ? room
            for direction, room in graph[player.current_room.id].items():
                # print((" "*4), "direction=>", direction)
                # print((" "*4), "room=>", room)
                possible_exits = []
                if room == '?':
                    possible_exits.append(direction)
            if len(possible_exits) > 0:
                direction_we_are_going = possible_exits.pop()

                previous_room = player.current_room
                direction_arrived_from = direction_we_are_going
                # output traversal list
                traversal_path.append(direction_we_are_going)
                # print("traversal_path=>", traversal_path)

                player.travel(direction_we_are_going)
            else:
                break

        # breadth_for_search
        travel_directions = breadth_for_search(
            graph, player.current_room.id, '?')

        # stop the loop if no unexplored area remains
        if travel_directions is None:
            break

        # remove first room which is redundant bc it is current room
        # travel_directions.pop(0)
        # follow travel_directions
        for room, direction in travel_directions:
            # print((" "*3), "END:room=>", room)
            # print((" "*3), "END:direction=>", direction)
            # print((" "*3), 'END:player.current_room.id=>', player.current_room.id)

            # update rooms
            previous_room = player.current_room
            direction_arrived_from = direction

            # traversal_path
            player.travel(direction)
            traversal_path.append(direction)


# Run the code
allrooms(player)
print("APEX")

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
