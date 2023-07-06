
import glob, json, re, argparse, os



def extract_variant(resdir):
    data = {}
    if 'justgoal' in resdir:
        data['num_prefs'] = 0
    else:
        with open(resdir+'/addprefs.log', 'r') as f:
            data['num_prefs'] = int(re.search(r'Compiled (\d+) preferences.', f.read()).group(1))

    # Get the sas_plan files
    sas_plans = glob.glob(f'{resdir}/sas_plan.*')

    if len(sas_plans) == 0:
        data['solved'] = False
        return data
    data['solved'] = True
    
    data['out_of_mem'] = False
    with open(resdir+'/lama.log', 'r') as f:
        if "Memory limit has been reached." in f.read():
            data['out_of_mem']= True

    with open(resdir+'/lama.log', 'r') as f:
        data['planner_time'] = float(re.search(r'Planner time: (\d+\.\d+)s', f.read()).group(1))

    # Get the highest index one
    initial_sas_plan = min(sas_plans, key=lambda x: int(x.split('.')[-1]))
    sas_plan = max(sas_plans, key=lambda x: int(x.split('.')[-1]))

    data['num_plans'] = len(sas_plans)

    with open(sas_plan, 'r') as f:
        plan = f.readlines()

    plan = [l.strip() for l in plan]
    # filter out empty lines and ; comments
    plan = [l for l in plan if l != '' and l[0] != ';']

    data['total_plan_length'] = len(plan)
    data['plan_length'] = len([l for l in plan \
                                       if 'forgo_' not in l and \
                                        'achieve_' not in l and \
                                        'switch_to_prefs' not in l])
    data['prefs_satisfied'] = len([l for l in plan if 'achieve_' in l])

    with open(initial_sas_plan, 'r') as f:
        initial_plan = f.readlines()

    initial_plan = [l.strip() for l in initial_plan]
    # filter out empty lines and ; comments
    initial_plan = [l for l in initial_plan if l != '' and l[0] != ';']

    data['initial_total_plan_length'] = len(initial_plan)
    data['initial_plan_length'] = len([l for l in initial_plan \
                                       if 'forgo_' not in l and \
                                        'achieve_' not in l and \
                                        'switch_to_prefs' not in l])
    data['initial_prefs_satisfied'] = len([l for l in initial_plan if 'achieve_' in l])

    return data

def extract(resdir):
    data = {}

    with open(resdir + '/rpmep.log', 'r') as f:
        contents = f.read()

    data['num_agents'] = int(re.search(r'Agents: (\d+)', contents).group(1))
    data['num_props'] = int(re.search(r'Props: (\d+)', contents).group(1))
    data['num_acts'] = int(re.search(r'Acts: (\d+)', contents).group(1))
    data['num_effs'] = int(re.search(r'Effs: (\d+)', contents).group(1))
    data['depth'] = int(re.search(r'Depth: (\d+)', contents).group(1))

    data['variants'] = {}
    if os.path.exists(f'{resdir}/justgoal'):
        data['variants']['justgoal'] = extract_variant(f'{resdir}/justgoal')
    for mode in ['misconception', 'truth', 'oblivious', 'conscious']:
        if os.path.exists(f'{resdir}/goal-and-{mode}'):
            data['variants'][f'goal-and-{mode}'] = extract_variant(f'{resdir}/goal-and-{mode}')

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Put data from experiments in json file.')
    parser.add_argument('--time', type=str)
    args = parser.parse_args()
    time_limit = args.time
    
    # Get all of the result directories
    resdirs = glob.glob(f'data{time_limit}/*')
    
    all_data = {}
    for resdir in resdirs:
        if 'data.json' in resdir:
            continue
        all_data[resdir.split('/')[1]] = extract(resdir)

    with open(f'data{time_limit}.json', 'w') as f:
        json.dump(all_data, f, indent=4)
