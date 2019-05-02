# Block ATM generation for gmsh
# Author: Logan Harbour, 2019

import numpy as np

# Resolution used as the fourth value for each point
resolution = 3

# Next indices used in mesh generation
next_point_index = 0
next_line_index = 0
next_line_loop_index = 0
next_surface_index = 0

# Storage for points, lines, line loops, and surfaces from each region
mesh_points = []
mesh_lines = []
mesh_line_loops = []
mesh_surfaces = []

# Loop through each object and generate the points, lines, and line loops
point_files = ['A.txt', 'A_hole.txt', 'T.txt', 'M.txt', 'outside.txt']
for file in point_files:
    # Starting indices for this object
    point_index_start = next_point_index
    line_index_start = next_line_index

    # Load points
    points = np.loadtxt('points/' + file, delimiter=',')

    # Flip across y-axis
    points[:, 1] *= -1

    # add points
    for point in points:
        next_point_index += 1
        mesh_points.append(point)
    point_index_end = next_point_index - 1

    # add lines
    for i in range(point_index_start, point_index_end):
        next_line_index += 1
        mesh_lines.append((i, i + 1))
    next_line_index += 1
    mesh_lines.append((point_index_end, point_index_start))
    line_index_end = next_line_index - 1

    # add line loop
    lines = list(range(line_index_start, line_index_end + 1))
    mesh_line_loops.append(lines)
    next_line_loop_index += 1

out = ''

# store points in gmsh format
for i in range(len(mesh_points)):
    out += 'Point({}) = {{{}, {}, 0, {}}};\n'.format(i, mesh_points[i][0],
                                                     mesh_points[i][1],
                                                     resolution)
out += '\n'

# store lines in gmsh format
for i in range(len(mesh_lines)):
    out += 'Line({}) = {{{}, {}}};\n'.format(i, mesh_lines[i][0], mesh_lines[i][1])

# store line loops
out += '\n'
for i in range(len(mesh_line_loops)):
    out += 'Line Loop({}) = {{'.format(i)
    for line in mesh_line_loops[i]:
        out += '{}, '.format(line)
    out = out[:-2] + '};\n'
out += '\n'

# store surfaces
out += 'Plane Surface(0) = {0, -1};\n'        # block A
out += 'Plane Surface(1) = {-1};\n'           # inside A
out += 'Plane Surface(2) = {2};\n'            # block T
out += 'Plane Surface(3) = {-3};\n'           # block M
out += 'Plane Surface(4) = {0, 2, 3, -4};\n'  # outside
out += '\n'

# store physical surfaces
out += 'Physical Surface(0) = {0, 2, 3};\n' # block
out += 'Physical Surface(1) = {1, 4};\n'    # outside
out += '\n'

# store physical lines
last = next_line_index - 1
out += 'Physical Line(0) = {{{}}};\n'.format(last)     # left
out += 'Physical Line(1) = {{{}}};\n'.format(last - 2) # right
out += 'Physical Line(2) = {{{}}};\n'.format(last - 3) # bottom
out += 'Physical Line(3) = {{{}}};\n'.format(last - 1) # top
out += '\n'

# parameters
out += 'Mesh.Algorithm = 8;\n'
out += 'Mesh.RecombineAll = 1;\n'
out += 'Mesh.SubdivisionAlgorithm = 1;\n'
out += 'Mesh.Smoothing = 20;\n'

# save
with open('atm.geo', 'w') as file:
    file.write(out)
