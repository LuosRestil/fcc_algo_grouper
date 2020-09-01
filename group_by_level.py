from break_into_subgroups import break_into_subgroups

def group_by_level(group):
    initial_groups = {
        'javascript': [],
        'python': [],
        'c#': [],
        'other': []
    }

    final_groups = []

    for attendee in group:
        if attendee.lang1 == 'other':
            if initial_groups.get(attendee.lang_other, False):
                initial_groups[attendee.lang_other].append(attendee)
            else:
                initial_groups[attendee.lang_other] = [attendee]
        else:
            initial_groups[attendee.lang1].append(attendee)

    del initial_groups['other']

    # Reassign 'other' groups with only one person
    def reassign_singles(lang):
        print(f'reassign_singles({lang})')
        attendees = initial_groups[lang]
        if len(attendees) == 1:
            attendee = attendees[0]
            attempt = 1
            assigned = False
            print('REASSIGNMENT NEEDED:')
            print(f'\t{attendee}')
            while attempt <= 3 and not assigned:
                if attempt == 1:
                    print('first attempt at reassignment')
                    next_lang = attendee.lang2
                    if next_lang != 'other':
                        initial_groups[next_lang].append(attendee)
                        assigned = True
                elif attempt == 2:
                    print('second attempt at reassignment')
                    next_lang = attendee.lang3
                    if next_lang != 'other':
                        initial_groups[next_lang].append(attendee)
                        assigned = True
                elif attempt == 3:
                    attendee.can_pair = False
                    # TODO assign to largest group (currently using javascript as default)
                    largest_group = ''
                    largest_group_size = 0
                    for group in initial_groups:
                        if len(initial_groups[group]) > largest_group_size:
                            largest_group_size = len(initial_groups[group])
                            largest_group = group
                    initial_groups[largest_group].append(attendee)
                    print(f'no home for attendee, setting can_pair to false, adding to {largest_group}')
                    assigned = True
                if assigned:
                    initial_groups[lang] = []
                attempt += 1
    
    for group in initial_groups:
        if group != 'javascript' and group != 'python' and group != 'c#':
            reassign_singles(group)
    reassign_singles('c#')
    reassign_singles('python')
    reassign_singles('javascript')

    inadvertent_loners = []

    for group, attendees in initial_groups.items():
        if len(attendees) != 0:
            grouped = break_into_subgroups(attendees)
            for group in grouped:
                final_groups.append(group)
        if len(attendees) == 1:
            inadvertent_loners.append([attendees[0]])

    if len(inadvertent_loners) > 0:
        final_groups.append(inadvertent_loners)
    
    return final_groups

