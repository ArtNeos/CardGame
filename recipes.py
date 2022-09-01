prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 39, 41, 43, 47, 53]


class Recipe:
    def __init__(self, nums):
        self.nums = nums

    def __eq__(self, other):
        copy_nums = self.nums.copy()
        for num in other.nums:
            if num in copy_nums:
                copy_nums.remove(num)
            else:
                return False
        if len(copy_nums) != 0:
            return False
        return True

    def __hash__(self):
        my_hash = 1
        for i, num in enumerate(self.nums):
            my_hash *= prime_numbers[num-1]
        return my_hash


recipes = {
    Recipe([5, 3]): {  # berry bush and villager -> 3 berries and villager
        'result': (4, 4, 4, 5),
        'duration': 200
    },
    Recipe([5, 1]): {  # villager and wood -> villager and stick
        'result': (6, 5),
        'duration': 300
    },
    Recipe([6, 7]): {  # stick and flint -> campfire
        'result': (8,),
        'duration': 300
    },
    Recipe([5, 9]): {  # villager and tree -> villager and 2 wood
        'result': (1, 1, 5),
        'duration': 200
    },
    Recipe([5, 10]): {  # villager and rock -> villager and 2 stone
        'result': (2, 2, 5),
        'duration': 200
    },
    Recipe([5, 1, 1, 1]): {  # villager and 3 wood -> villager and plank
        'result': (11, 5),
        'duration': 400
    },
    Recipe([5, 2, 2, 2]): {  # villager and 3 stone -> villager and brick
        'result': (12, 5),
        'duration': 400
    },
    Recipe([5, 1, 2, 6]): {  # villager, wood, stone and stick -> villager and shed
        'result': (13, 5),
        'duration': 200
    },
    Recipe([5, 1, 2, 2]): {  # villager, wood and 2 stone -> villager and house
        'result': (14, 5),
        'duration': 200
    },
    Recipe([5, 5, 14]): {  # 2 villagers and house -> 2 villagers, house and baby
        'result': (14, 15, 5, 5),
        'duration': 700
    },
    Recipe([14, 15]): {  # baby and house -> villager and house
        'result': (14, 5),
        'duration': 700
    },
}
