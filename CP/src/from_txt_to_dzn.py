import glob


for filepath in glob.iglob('../../ins/*.txt'):
    lines = []
    with open(filepath) as f:
        for line in f:
            lines.append(line)
    lines = [line.replace('\n','').split(' ') for line in lines]

    w = int(lines[0][0])
    n = int(lines[1][0])
    ws = [int(line[0]) for line in lines[2:]]
    ls = [int(line[1]) for line in lines[2:]]
    with open(f'ins/{filepath.split("/")[-1]}'.replace('.txt','.dzn'), 'w') as f:
        f.write(f'plate_width = {w};\nn_circuits = {n};\nwidths = {ws};\nlengths = {ls};')

    sizes = []
    for size in zip(ws,ls):
        if size[0] != size[1]:
            sizes += [size, size[::-1]]
        else:
            sizes.append(size)
    n_shapes = len(sizes)
    offsets = [(0,0) for _ in range(n_shapes)]
    shapes = [{i+1} for i in range(n_shapes)]
    valid_shapes = []
    i = 1
    while i <= n_shapes:
        for size in zip(ws,ls):
            if size[0] != size[1]:
                valid_shapes.append({i,i+1})
                i += 2
            else:
                valid_shapes.append({i})
                i += 1
    with open(f'ins_rot/{filepath.split("/")[-1]}'.replace('.txt','.dzn'), 'w') as f:
        f.write(f'plate_width = {w};\nn_circuits = {n};\nn_shapes = {n_shapes};\n')
        f.write(f'widths = {ws};\nlengths = {ls};\n')
        f.write(f'sizes = {sizes};\n'.replace('(','| ').replace('),','').replace(')]',' |]'))
        f.write(f'offsets = {offsets};\n'.replace('(','| ').replace('),','').replace(')]',' |]'))
        f.write(f'shapes = {shapes};\n')
        f.write(f'valid_shapes = {valid_shapes};')
