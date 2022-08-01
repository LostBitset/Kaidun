#version 330

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in vec3 vertices[];

out vec3 vert;

void main() {
    for (int i = 0; i < 3; i += 1) {
        vert = vertices[i];
        EmitVertex();
    }
    EndPrimitive();
}
