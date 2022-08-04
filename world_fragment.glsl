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

mat3 rot_mat3(in vec3 tait_bryan) {
    float a = tait_bryan.x;
    float b = tait_bryan.y;
    float c = tait_bryan.z;
    return mat3(
        /* 0 0 */ cos(b)*cos(c),
        /* 0 1 */ cos(b)*sin(c),
        /* 0 2 */ -sin(b),
        /* 1 0 */ (sin(a)*sin(b)*cos(c))-(cos(a)*sin(c)),
        /* 1 1 */ (sin(a)*sin(b)*sin(c))+(cos(a)*cos(c)),
        /* 1 2 */ sin(a)*cos(b),
        /* 2 0 */ (cos(a)*sin(b)*cos(c))+(sin(a)*sin(c)),
        /* 2 1 */ (cos(a)*sin(b)*sin(c))-(sin(a)*cos(c)),
        /* 2 2 */ cos(a)*cos(b)
    );
}

void add_distance_fog(inout vec3 input_color) {
    input_color *= fog_visibility_frac;
    input_color += fog_component_rgb_partial;
}

float lambertian_component_phong(in vec3 to_i, in vec3 aligned_normal) {
    return dot(to_i, aligned_normal);
}

vec3 bumpmapping_get_rnormal() {
    return normalize(mod(position_3d*3.0, 1.0));
}

void bumpmapping_perturb_normal(inout vec3 normal) {
    normal += bumpmapping_get_rnormal();
    normal *= 0.5;
    normal = normalize(normal);
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
