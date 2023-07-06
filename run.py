import argparse, os, time

os.environ['PATH'] += os.pathsep + '/root/.planutils/bin'

# TIME_LIMIT = 30

def get_slug(name):
    dom = name.split('/')[-2]
    prob = name.split('/')[-1].split('.')[0]
    return f'{dom}---{prob}'

def go(pfile, agents, time_limit):

    # Confirm that pfile is an absolute path that exists
    if not os.path.isabs(pfile):
        print(f'Error: {pfile} must be an absolute path.')
        return
    if not os.path.exists(pfile):
        print(f'Error: {pfile} does not exist.')
        return

    slug = get_slug(pfile)
    
    data_dir = f'data{time_limit}'
    data_subdir = f'{data_dir}/{slug}'

    # Check if the data directory exists
    if os.path.exists(data_subdir):
        # Confirm if it should be removed or halt
        print(f'Warning: {data_subdir} already exists. Overwrite? (y/n)')
        if input() == 'y':
            print('Overwriting...')
            os.system(f'rm -rf {data_subdir}')
        else:
            print('Halting...')
            return
    os.makedirs(data_subdir)

    # Compile the pddl
    print(f'Compiling {slug}...', end='', flush=True)
    tic = time.perf_counter()
    os.system(f'cd {data_subdir}; rpmep {pfile} --keep-files > rpmep.log 2>&1')
    toc = time.perf_counter()
    print(f'done in {toc - tic:0.2f} seconds')

    # Add preferences
    # print("Adding preferences...", end='', flush=True)
    os.makedirs(f'{data_subdir}/justgoal')
    os.system(f'cp {data_subdir}/pdkb-domain.pddl {data_subdir}/justgoal/d.pddl')
    os.system(f'cp {data_subdir}/pdkb-problem.pddl {data_subdir}/justgoal/p.pddl')

    for mode in ['truth', 'oblivious', 'misconception', 'conscious']:
        os.makedirs(f'{data_subdir}/goal-and-{mode}')
        tic = time.perf_counter()
        os.system(f'python3 addprefs.py --agents {agents} --domain {data_subdir}/pdkb-domain.pddl --problem {data_subdir}/pdkb-problem.pddl --mode {mode} > {data_subdir}/goal-and-{mode}/addprefs.log 2>&1')
        toc = time.perf_counter()
        print(f'added preferences of type "{mode}" in {toc - tic:0.2f} seconds')
        
        os.system(f'cp {data_subdir}/pdkb-domain.pddl.pref {data_subdir}/goal-and-{mode}/d.pddl')
        os.system(f'cp {data_subdir}/pdkb-problem.pddl.pref {data_subdir}/goal-and-{mode}/p.pddl')

    print("")

    # Solve with lama
    print("Solving with lama...", end='', flush=True)
    os.system(f'cd {data_subdir}/justgoal; lama{f" --search-time-limit {time_limit}" if time_limit is not None else ""} d.pddl p.pddl > lama.log 2>&1')
    for mode in ['truth', 'oblivious', 'misconception', 'conscious']:
        os.system(f'cd {data_subdir}/goal-and-{mode}; lama{f" --search-time-limit {time_limit}" if time_limit is not None else ""} d.pddl p.pddl > lama.log 2>&1')
    print("done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile the pddl, add preferences, and run the planner.')
    parser.add_argument('--problem', type=str, required=True)
    parser.add_argument('--agents', type=str, required=True)
    parser.add_argument('--time', type=str)
    args = parser.parse_args()
    go(args.problem, args.agents, args.time)
