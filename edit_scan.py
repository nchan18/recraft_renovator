import trimesh
import numpy as np

def remove_top_portion(mesh, portion_height):
    # Find the highest point in the mesh
    max_z = mesh.vertices[:, 2].max()

    # Define the height threshold to remove the top portion
    height_threshold = max_z - portion_height

    # Find faces above the height threshold in the Z direction
    face_centers = mesh.triangles_center
    top_faces = np.where(face_centers[:, 2] > height_threshold)[0]

    # Remove the top faces
    mesh.update_faces(~np.isin(np.arange(len(mesh.faces)), top_faces))
    return mesh
def create_ceiling(mesh, height):
    # Get the bounding box of the mesh
    bounding_box = mesh.bounds

    # Define the vertices of the plane
    vertices = np.array([
        [bounding_box[0][0], bounding_box[0][1], height],
        [bounding_box[1][0], bounding_box[0][1], height],
        [bounding_box[1][0], bounding_box[1][1], height],
        [bounding_box[0][0], bounding_box[1][1], height]
    ])
    mesh.vertices = np.vstack([mesh.vertices, vertices])
def rotate_mesh(mesh, axis, angle):
    # Create a rotation matrix
    rotation_matrix = trimesh.transformations.rotation_matrix(
        angle=np.radians(angle),
        direction=axis,
        point=mesh.centroid
    )
    # Apply the rotation to the mesh
    mesh.apply_transform(rotation_matrix)
    return mesh

if __name__ == '__main__':
    # Load the .glb file
    scene = trimesh.load('house_scan.glb')

    # Define the height threshold to identify the ceiling
    height_threshold = 0.5  # Adjust this value based on your mesh

    # Define the rotation axis and angle
    rotation_axis = [1, 0, 0]  # Rotate around the X-axis
    rotation_angle = 90  # Rotate 90 degrees

    # Process each mesh in the scene
    for name, mesh in scene.geometry.items():
        # Rotate the mesh
        scene.geometry[name] = rotate_mesh(mesh, rotation_axis, rotation_angle)
        # Remove the ceiling
        scene.geometry[name] = remove_top_portion(mesh, height_threshold)
        max_z = mesh.vertices[:, 2].max()
        ceiling = create_ceiling(mesh, max_z)

    
    rotation_angle = -90  # Rotate 90 degrees

    # Process each mesh in the scene
    for name, mesh in scene.geometry.items():
        # Rotate the mesh
        scene.geometry[name] = rotate_mesh(mesh, rotation_axis, rotation_angle)

    # Save the modified scene
    scene.export('house_no_ceiling2.glb')