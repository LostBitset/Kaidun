#version 330

in vec3 vert_color;
in float illum;

out vec3 color;

void main() {
    color = vec3(illum, illum, illum);
}
