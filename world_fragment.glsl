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

float bumpmapping_heightmap_get(in vec3 sample) {
    return sin(20.0*sample.x)/2.0;
}

vec3 span_2_orthogonal_complement(in vec3 a, in vec3 b) {
    return normalize(cross(a, b));
}

vec3 bumpmapping_new_normal(in vec3 normal) {
    vec3 derived_u_basis = ideferred_bumpmapping_finite_diff_x_proj_u;
    vec3 derived_v_basis = ideferred_bumpmapping_finite_diff_y_proj_v;
    float heightmap_origin = bumpmapping_heightmap_get(position_3d);
    vec3 heightmap_finite_diff_0 = heightmap_origin * normal;
    float heightmap_derived_u = bumpmapping_heightmap_get(
        position_3d + derived_u_basis
    );
    vec3 heightmap_finite_diff_1 = heightmap_derived_u * normal;
    heightmap_finite_diff_1 += derived_u_basis;
    float heightmap_derived_v = bumpmapping_heightmap_get(
        position_3d + derived_v_basis
    );
    vec3 heightmap_finite_diff_2 = heightmap_derived_v * normal;
    heightmap_finite_diff_2 += derived_v_basis;
    vec3 resolved_surf_basis_1 = heightmap_finite_diff_1 - heightmap_finite_diff_0;
    vec3 resolved_surf_basis_2 = heightmap_finite_diff_2 - heightmap_finite_diff_0;
    vec3 resolved_surf_normal = span_2_orthogonal_complement(
        resolved_surf_basis_1,
        resolved_surf_basis_2
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
    color /= 10000000000000000000.0;
    //color += vec3(bumpmapping_heightmap_get(position_3d), 0.0, 0.0);
    color += normalize(ideferred_bumpmapping_finite_diff_y_proj_v);
    /*color += normalize(
        ideferred_phong_aligned_normal_nonunit
    ) - bumpmapping_new_normal(
        normalize(
            ideferred_phong_aligned_normal_nonunit
        )
    );
    //*/
}
