import random

def break_into_subgroups(group):
    iters = 0
    acceptable = False
    remainder = len(group) % 3
    groups_of_two = 0 if remainder == 0 else abs(remainder - 3)

    final_groups = []

    while not acceptable and iters < 10:
        acceptable = True
        final_groups = []
        group_copy = group.copy()
        random.shuffle(group_copy)

        for _ in range(groups_of_two):
            final_groups.append(group_copy[:2])
            group_copy = group_copy[2:]
        while len(group_copy) > 0:
            final_groups.append(group_copy[:3])
            group_copy = group_copy[3:]

        for final_group in final_groups:
            if len(final_group) == 2 and any(attendee.can_pair == False for attendee in final_group):
                acceptable = False
                iters += 1
                break

    return final_groups