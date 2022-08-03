#version 330

in vec3 vert_color;
in float illum;
in float icom_oren_nayar;
in float icom_lighting_maxsc;
in float fog_visibility_frac;
in vec3 fog_component_rgb_partial;

out vec3 color;

void add_distance_fog(inout vec3 input_color) {
    input_color *= fog_visibility_frac;
    input_color += fog_component_rgb_partial;
}

void main() {
    float illum_frag = illum;
    illum_frag *= icom_oren_nayar;
    illum_frag = clamp(illum_frag, 0.0, icom_lighting_maxsc);

    vec3 color_raw = vert_color;
    color_raw *= illum_frag;

    add_distance_fog(color_raw);

    color = clamp(color_raw, 0.0, 1.0);
}
