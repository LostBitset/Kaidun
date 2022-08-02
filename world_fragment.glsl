#version 330

in vec3 vert_color;
in float illum;
in float fog_visibility_frac;
in vec3 fog_component_rgb_partial;

out vec3 color;

void add_distance_fog(inout vec3 input_color) {
    input_color *= fog_visibility_frac;
    input_color += fog_component_rgb_partial;
}

void main() {
    vec3 color_raw = vert_color;
    add_distance_fog(color_raw);
    color_raw *= illum;
    color = clamp(color_raw, 0.0, 1.0);
}
