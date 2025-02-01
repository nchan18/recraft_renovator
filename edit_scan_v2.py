import trimesh
import numpy as np

def create_xy_plane(mesh, z_position):
    # Get the bounding box of the mesh
    bounding_box = mesh.bounds

    # Define the vertices of the plane
    vertices = np.array([
        [bounding_box[0][0], bounding_box[0][1], z_position],
        [bounding_box[1][0], bounding_box[0][1], z_position],
        [bounding_box[1][0], bounding_box[1][1], z_position],
        [bounding_box[0][0], bounding_box[1][1], z_position]
    ])

    # Define the faces of the plane
    faces = np.array([
        [0, 1, 2],
        [0, 2, 3]
    ])

    # Create the plane mesh
    plane = trimesh.Trimesh(vertices=vertices, faces=faces)
    return plane

if __name__ == '__main__':
    # Load the .glb file
    scene = trimesh.load('house_scan.glb')

    # Define the Z position where you want to add the XY plane
    z_position = 1.5  # Adjust this value based on your mesh

    # Process each mesh in the scene
    for name, mesh in scene.geometry.items():
        # Create a new XY plane
        xy_plane = create_xy_plane(mesh, z_position)

        # Combine the original mesh with the new XY plane
        combined_mesh = trimesh.util.concatenate([mesh, xy_plane])
        scene.geometry[name] = combined_mesh

    # Save the modified scene
    scene.export('house_with_xy_plane.glb')