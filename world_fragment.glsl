#version 330

in vec3 vert_color;
in float illum;
in vec3 illum_frag_phong_oren_nayar_to_i;
in vec3 illum_frag_phong_oren_nayar_to_r;
in float illum_frag_phong_oren_nayar_const_frac;
in float illum_frag_phong_oren_nayar_scale_frac;
in float illum_frag_phong_lighting_ambient;
in float illum_frag_phong_lighting_maxsc;
in vec3 phong_surf_normal;
in float fog_visibility_frac;
in vec3 fog_component_rgb_partial;

out vec3 color;

void update_illum_ambient_frag(inout float illum) {
    float lighting_ambient = illum_frag_phong_lighting_ambient;
    float lighting_maxsc = illum_frag_phong_lighting_maxsc;
    illum = clamp(illum + lighting_ambient, 0.0, lighting_maxsc);
}

vec3 proj_onto_surf_subspace(in vec3 v) {
    vec3 normal = aux_surf_normal;
    return cross(normal, cross(v, normal));
}

float angle3(in vec3 a, in vec3 b) {
    float cosine_distance = dot(a, b) / (length(a) * length(b));
    return acos(cosine_distance);
}

void update_illum_oren_nayar_ext_frag(inout float illum) {
    vec3 to_i = illum_frag_phong_oren_nayar_to_i;
    vec3 to_r = illum_frag_phong_oren_nayar_to_r;
    float theta_i = acos(dot(to_i, phong_surf_normal));
    float theta_r = acos(dot(to_r, phong_surf_normal));
    float alpha = max(theta_i, theta_r);
    float beta = min(theta_i, theta_r);
    vec3 proj2_i = proj_onto_surf_subspace(to_i);
    vec3 proj2_r = proj_onto_surf_subspace(to_r);
    float azimuthal_delta = angle3(proj2_i, proj2_r);
    float azimuthal_part = max(0, cos(azimuthal_delta));
    float fac = azimuthal_part * sin(alpha) * tan(beta);
    float const_frac = illum_frag_phong_oren_nayar_const_frac;
    float scale_frac = illum_frag_phong_oren_nayar_scale_frac;
    float a = 1.0 - (0.5 * const_frac);
    float b = 0.45 * scale_frac;
    illum *= a + (b * fac);
}

void add_distance_fog(inout vec3 input_color) {
    input_color *= fog_visibility_frac;
    input_color += fog_component_rgb_partial;
}

void main() {
    float illum_phong = illum;
    update_illum_oren_nayar_ext_frag(illum_phong);
    update_illum_ambient_frag(illum_phong);

    vec3 color_raw = vert_color;
    color_raw *= illum;
    add_distance_fog(color_raw);
    color = clamp(color_raw, 0.0, 1.0);
}
