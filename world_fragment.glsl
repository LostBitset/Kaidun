#version 330

in vec3 vert_color;
in float illum;

out vec3 color;

void main() {
    color = clamp((vert_color * illum), 0.0, 1.0);
}
