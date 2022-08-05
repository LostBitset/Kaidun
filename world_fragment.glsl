#version 330

in vec3 vert_color;
in float illum;
in float icom_oren_nayar;
in float icom_lighting_maxsc;
in vec3 ideferred_bumpmapping_to_i_nonunit;
in vec3 ideferred_phong_aligned_normal_nonunit;
in vec3 ideferred_bumpmapping_finite_diff_x_proj_u;
in vec3 ideferred_bumpmapping_finite_diff_y_proj_v;
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

float rand(in vec2 co) {
    return fract(sin(dot(co.xy,
                         vec2(12.9898,78.233)))
                 * 43758.5453123);
}

float noise2(in vec2 co) {
    vec2 i = floor(co);
    vec2 f = fract(co);
    float a = rand(i);
    float b = rand(i + vec2(1.0, 0.0));
    float c = rand(i + vec2(0.0, 1.0));
    float d = rand(i + vec2(1.0, 1.0));
    vec2 u = f*f*(3.0-2.0*f);
    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

float noise2small(in vec2 co) {
    float result = noise2(15.0* co);
    result /= 200.0;
    return result;
}

float bumpmapping_heightmap_get(in vec3 sample) {
    vec3 u_basis_1 = normalize(ideferred_bumpmapping_finite_diff_x_proj_u);
    vec3 v_basis_1 = normalize(cross(
        u_basis_1,
        ideferred_phong_aligned_normal_nonunit
    ));
    vec3 v_basis_2 = normalize(ideferred_bumpmapping_finite_diff_y_proj_v);
    vec3 u_basis_2 = normalize(cross(
        v_basis_2,
        ideferred_phong_aligned_normal_nonunit
    ));
    float result_uv1 = noise2small(vec2(
        dot(sample, u_basis_1),
        dot(sample, v_basis_1)
    ));
    float result_uv2 = noise2small(vec2(
        dot(sample, u_basis_2),
        dot(sample, v_basis_2)
    ));
    return max(result_uv1, result_uv2);
}

vec3 span_2_orthogonal_complement(in vec3 a, in vec3 b) {
    return normalize(cross(a, b));
}

vec3 bumpmapping_new_normal(in vec3 normal) {
    vec3 derived_u_basis = ideferred_bumpmapping_finite_diff_x_proj_u;
    vec3 derived_v_basis = ideferred_bumpmapping_finite_diff_y_proj_v;
    float heightmap_origin = bumpmapping_heightmap_get(position_3d);
    float heightmap_derived_u = bumpmapping_heightmap_get(
        position_3d + derived_u_basis
    );
    vec3 heightmap_finite_diff_1 = (heightmap_derived_u - heightmap_origin) * normal;
    heightmap_finite_diff_1 += derived_u_basis;
    float heightmap_derived_v = bumpmapping_heightmap_get(
        position_3d + derived_v_basis
    );
    vec3 heightmap_finite_diff_2 = (heightmap_derived_v - heightmap_origin) * normal;
    heightmap_finite_diff_2 += derived_v_basis;
    vec3 resolved_surf_normal = span_2_orthogonal_complement(
        heightmap_finite_diff_1,
        heightmap_finite_diff_2
    );
    if (dot(resolved_surf_normal, normal) < 0.0) {
        resolved_surf_normal *= -1;
    }
    return resolved_surf_normal;
}

void bumpmapping_perturb_normal(inout vec3 normal) {
    normal = bumpmapping_new_normal(normal);
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
    //color /= 10000000000000000000.0;
    //color += vec3(bumpmapping_heightmap_get(position_3d), 0.0, 0.0);
    //color += normalize(ideferred_bumpmapping_finite_diff_y_proj_v);
    /*color += bumpmapping_new_normal(
        normalize(
            ideferred_phong_aligned_normal_nonunit
        )
    );
    //*/
}
