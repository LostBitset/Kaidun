#version 330

in vec3 vert_color;

out vec4 color;

void main() {
    color = vec4(vert_color, 0.1);
}
