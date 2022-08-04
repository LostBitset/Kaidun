#version 330

in vec3 vert_color;
in float illum;
in float icom_oren_nayar;
in float icom_lighting_maxsc;
in vec3 ideferred_bumpmapping_to_i_nonunit;
in vec3 ideferred_phong_aligned_normal_nonunit;
in float fog_visibility_frac;
in vec3 fog_component_rgb_partial;
in vec3 position_3d;

out vec3 color;

void add_distance_fog(inout vec3 input_color) {
    input_color *= fog_visibility_frac;
    input_color += fog_component_rgb_partial;
}

float lambertian_component_phong(in vec3 to_i, in vec3 aligned_normal) {
    return dot(to_i, aligned_normal);
}

vec3 bumpmapping_heightmap_get() {
    return vec3(0.0, 0.0, 1.0);
}

void bumpmapping_perturb_normal(inout vec3 normal) {
    // todo
}

float deferred_component_bumpmapping_phong_lambertian() {
    vec3 to_i = normalize(
        ideferred_bumpmapping_to_i_nonunit
    );
    vec3 aligned_normal = normalize(
        ideferred_phong_aligned_normal_nonunit
    );
    bumpmapping_perturb_normal(aligned_normal);
    return lambertian_component_phong(to_i, aligned_normal);
}

void main() {
    float illum_frag = illum;
    illum_frag *= deferred_component_bumpmapping_phong_lambertian();
    illum_frag *= icom_oren_nayar;
    illum_frag = clamp(illum_frag, 0.0, icom_lighting_maxsc);

    vec3 color_raw = vert_color;
    color_raw *= illum_frag;

    add_distance_fog(color_raw);

    color = clamp(color_raw, 0.0, 1.0);
}
