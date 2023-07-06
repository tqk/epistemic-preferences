
import argparse


ACHIEVE_TEMPLATE = """
(:action achieve_pref_{n}
 :precondition (and (collect-prefs){doneprev} {pref})
 :effect (done{n})
)
"""

FORGO_TEMPLATE = """
(:action forgo_pref_{n}
 :precondition (and (collect-prefs){doneprev} (not (and {pref})))
 :effect (and (done{n}) (increase (total-cost) 1))
)
"""

SWITCH_ACTION_TEMPLATE = """
(:action switch_to_prefs
 :precondition (and (not (collect-prefs)) {goal})
 :effect (collect-prefs)
)
"""

GOAL_TEMPLATE = """
(:goal (and (collect-prefs) {goal}))
"""


def generate_misconception_prefs(agents, usable_primitives, usable_beliefs, usable_possibles):
    prefs = []
    for p in usable_primitives:
        for a in agents:
            if p.startswith('(not_'):
                bpred = f'(B{a}_{p[5:]}'
            else:
                bpred = f'(B{a}_not_{p[1:]}'
            assert bpred in usable_beliefs
            prefs.append(f'{p} {bpred}')
    return prefs

def generate_truth_prefs(agents, usable_primitives, usable_beliefs, usable_possibles):
    prefs = []
    for p in usable_primitives:
        for a in agents:
            bpred = f'(B{a}_{p[1:-1]})'
            assert bpred in usable_beliefs
            prefs.append(f'{p} {bpred}')
    return prefs

def generate_oblivious_prefs(agents, usable_primitives, usable_beliefs, usable_possibles):
    return usable_possibles

def generate_conscious_prefs(agents, usable_primitives, usable_beliefs, usable_possibles):
    return usable_beliefs

def go(agents, dname, pname, mode, ignore_goal):
    with open(dname, 'r') as f:
        dcontents = f.read()

    all_preds = {p.strip() for p in dcontents.split('(:predicates\n')[1].split(')\n\n    (:action')[0].strip().split('\n')}

    primitive_preds = set()
    for p in all_preds:

        if not any([p.startswith(f'({o}{a}_') for a in agents for o in 'BP']):
            primitive_preds.add(p)

    usable_primitives = set()
    usable_beliefs = set()
    usable_possibles = set()
    for p in primitive_preds:
        for o in 'BP':
            for a in agents:
                ep_pred = f'({o}{a}_{p[1:-1]})'
                if ep_pred in all_preds:
                    if o == 'B':
                        usable_beliefs.add(ep_pred)
                    elif o == 'P':
                        usable_possibles.add(ep_pred)
                    usable_primitives.add(p)

    assert len(agents)*len(usable_primitives) == len(usable_beliefs) == len(usable_possibles)

    if mode == 'misconception':
        prefs = generate_misconception_prefs(agents, usable_primitives, usable_beliefs, usable_possibles)
    elif mode == 'truth':
        prefs = generate_truth_prefs(agents, usable_primitives, usable_beliefs, usable_possibles)
    elif mode == 'oblivious':
        prefs = generate_oblivious_prefs(agents,usable_primitives, usable_beliefs, usable_possibles)
    elif mode == 'conscious':
        prefs = generate_conscious_prefs(agents, usable_primitives, usable_beliefs, usable_possibles)
    else:
        raise Exception(f'Unknown mode {mode}')

    actions = []
    done_preds = []
    for i, p in enumerate(prefs):
        done_preds.append(f'(done{i})')
        if i == 0:
            doneprev = ''
        else:
            doneprev = f' (done{i-1})'
        actions.append(ACHIEVE_TEMPLATE.format(n=i, pref=p, doneprev=doneprev))
        actions.append(FORGO_TEMPLATE.format(n=i, pref=p, doneprev=doneprev))

    # get the original goal
    with open(pname, 'r') as f:
        pcontents = f.read()

    goal = pcontents.split('(:goal (and\n')[1].split('\n    ))')[0].strip()
    goal = ' '.join([l.strip() for l in goal.split('\n')])

    if ignore_goal:
        goal = ''

    # include the switch action
    actions.append(SWITCH_ACTION_TEMPLATE.format(goal=goal))

    # add the negated phase to all preconditions
    dcontents = dcontents.replace(':precondition (and', ':precondition (and (not (collect-prefs))')

    # new predicates
    new_preds = '\n'.join(done_preds)
    new_preds += '\n\n    (collect-prefs)\n'
    dcontents = dcontents.split('(:predicates\n')[0] + '(:predicates\n' + new_preds + '\n' + dcontents.split('(:predicates\n')[1]

    # new goal
    new_goal = GOAL_TEMPLATE.format(goal=done_preds[-1])
    pcontents = pcontents.split('(:goal')[0] + f'{new_goal}\n\n    (:metric minimize (total-cost))\n)'

    # add the total-cost function to the domain
    dcontents = dcontents.split('(:predicates\n')[0] + '(:functions (total-cost))\n\n(:predicates\n' + dcontents.split('(:predicates\n')[1]

    # add the initial total-cost of 0
    pcontents = pcontents.split('(:init\n')[0] + '(:init\n    (= (total-cost) 0)\n' + pcontents.split('(:init\n')[1]

    # check that the last line is the closing bracket, and insert our new actions
    assert dcontents.split('\n')[-1] == ')'
    dcontents = dcontents.split('\n')
    dcontents.insert(-1, ''.join(actions))
    dcontents = '\n'.join(dcontents)

    # write the new domain and problem files with a .pref extension
    with open(dname + '.pref', 'w') as f:
        f.write(dcontents)
    with open(pname + '.pref', 'w') as f:
        f.write(pcontents)


    print(f'Compiled {len(prefs)} preferences.')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Required ption for the list of comma-separated agents
    parser.add_argument('--agents', type=str, required=True)

    # Compiled PDKB domain file
    parser.add_argument('--domain', type=str, required=True)

    # Compiled PDKB problem file
    parser.add_argument('--problem', type=str, required=True)

    # Boolean if we should ignore the goal
    parser.add_argument('--ignore-goal', default=False, action='store_true')

    # Mode of preferences: must be either 'misconception', 'truth', 'oblivious', or 'conscious'
    parser.add_argument('--mode', type=str, required=True, choices=['misconception', 'truth', 'oblivious', 'conscious'])

    args = parser.parse_args()
    go(args.agents.split(','), args.domain, args.problem, args.mode, args.ignore_goal)

