#version 330

in vec2 vert;
out vec3 vert_color;

uniform vec

void main() {
    gl_Position = vec4(vert, 0.0, 1.0);
    vert_color = vec3(1.0, 0.0, 0.0);
}
