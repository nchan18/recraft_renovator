import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import trimesh
import os

class GLBViewer(QOpenGLWidget):
    def __init__(self, glb_file, parent=None):
        super().__init__(parent)
        self.glb_file = glb_file
        self.vertices = []
        self.faces = []
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.rotation_z = 0.0
        self.translation_x = 0.0
        self.translation_y = 0.0
        self.translation_z = -5.0  # Start with the camera slightly back
        self.load_glb()

    def load_glb(self):
        # Load the GLB file using Trimesh
        try:
            print(f"Attempting to load file: {os.path.abspath(self.glb_file)}")
            if not os.path.isfile(self.glb_file):
                raise FileNotFoundError(f"The file '{self.glb_file}' does not exist.")
            
            print("Loading GLB file...")
            scene = trimesh.load(self.glb_file)  # Load the GLB file
            
            print("Processing mesh...")
            # Extract the first mesh from the scene (GLB files may contain multiple meshes)
            if isinstance(scene, trimesh.Scene):
                print("Combining multiple meshes into one...")
                mesh = scene.dump(concatenate=True)  # Combine all meshes into one
            else:
                mesh = scene
            
            # Simplify the mesh if it has too many faces
            try:
                if len(mesh.faces) > 10000:
                    print("Simplifying mesh to reduce face count...")
                    mesh = mesh.simplify_quadric_decimation(face_count=10000)  # Reduce to 10k faces
            except ImportError:
                print("Skipping mesh simplification (fast_simplification not installed).")
            
            self.vertices = np.array(mesh.vertices, dtype=np.float32)
            self.faces = np.array(mesh.faces, dtype=np.uint32)
            
            # Debug: Print the number of vertices and faces
            print(f"Loaded {len(self.vertices)} vertices and {len(self.faces)} faces.")
            print(f"First 5 vertices: {self.vertices[:5]}")  # Print first 5 vertices
            print(f"First 5 faces: {self.faces[:5]}")       # Print first 5 faces
            
            print(f"Successfully loaded {self.glb_file}.")
        except Exception as e:
            print(f"Error loading {self.glb_file}: {e}")

    def initializeGL(self):
        # Initialize OpenGL settings
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Set background color (dark gray)
        glEnable(GL_DEPTH_TEST)          # Enable depth testing
        glEnable(GL_LIGHTING)            # Enable lighting
        glEnable(GL_LIGHT0)              # Enable light source 0
        glEnable(GL_COLOR_MATERIAL)      # Enable material coloring

        # Set up lighting
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])  # Light position
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])   # Light color

    def resizeGL(self, w, h):
        # Set up the viewport and projection matrix
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 100.0)  # Perspective projection
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        # Clear the screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply translation
        glTranslatef(self.translation_x, self.translation_y, self.translation_z)

        # Apply rotation
        glRotatef(self.rotation_x, 1, 0, 0)  # Rotate around X-axis
        glRotatef(self.rotation_y, 0, 1, 0)  # Rotate around Y-axis
        glRotatef(self.rotation_z, 0, 0, 1)  # Rotate around Z-axis

        # Draw the mesh
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex_index in face:
                glVertex3fv(self.vertices[vertex_index])
        glEnd()

    def keyPressEvent(self, event):
        # Handle keyboard input for movement and rotation
        step = 0.1  # Translation step size
        angle_step = 5.0  # Rotation step size

        if event.key() == Qt.Key_Left:
            self.rotation_y += angle_step  # Rotate left
        elif event.key() == Qt.Key_Right:
            self.rotation_y -= angle_step  # Rotate right
        elif event.key() == Qt.Key_Up:
            self.rotation_x += angle_step  # Rotate up
        elif event.key() == Qt.Key_Down:
            self.rotation_x -= angle_step  # Rotate down
        elif event.key() == Qt.Key_A:
            self.translation_x -= step  # Move left
        elif event.key() == Qt.Key_D:
            self.translation_x += step  # Move right
        elif event.key() == Qt.Key_W:
            self.translation_y += step  # Move up
        elif event.key() == Qt.Key_S:
            self.translation_y -= step  # Move down
        elif event.key() == Qt.Key_Q:
            self.translation_z += step  # Move forward
        elif event.key() == Qt.Key_E:
            self.translation_z -= step  # Move backward
        elif event.key() == Qt.Key_Z:
            self.rotation_z += angle_step  # Rotate clockwise around Z-axis
        elif event.key() == Qt.Key_X:
            self.rotation_z -= angle_step  # Rotate counterclockwise around Z-axis

        # Trigger a redraw
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Path to your .glb file
    dir = os.getcwd()
    glb_file = os.path.join(dir, "house_scan.glb")  # Use "house_scan.glb"
    print(f"Looking for GLB file at: {os.path.abspath(glb_file)}")

    # Create the main window
    viewer = GLBViewer(glb_file)
    viewer.setWindowTitle("GLB Viewer")
    viewer.resize(800, 600)
    viewer.show()

    sys.exit(app.exec_())