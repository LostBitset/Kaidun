#version 330

#define PI 3.1415926538

#define UP vec3(0.0, 0.0, 1.0)

/*
 * To make this easier, citations that involve uniforms
 * can be found attached to the uniforms, and NOT the
 * functions that use them.
 * This is done because these algorithms are split
 * across many functions and two shader files.
 *****************************************************/

in vec3 vert;
in vec3 drv_surf_normal;
in vec3 aux_rgb;
in float bumpmapping_amt;

out vec3 vert_color;
out float illum;
							// Citation https://www.cs.columbia.edu/CAVE/projects/oren/oren.php
out float icom_oren_nayar;				// Citation https://en.wikipedia.org/wiki/Oren%E2%80%93Nayar_reflectance_model
out float icom_lighting_maxsc;
out vec3 ideferred_bumpmapping_to_i_nonunit;		// Citation https://en.wikipedia.org/wiki/Bump_mapping
out vec3 ideferred_phong_aligned_normal_nonunit;	// Citation https://web.eecs.umich.edu/~sugih/courses/eecs487/lectures/16-Phong+Shading.pdf
out vec3 ideferred_bumpmapping_finite_diff_x_proj_u;
out vec3 ideferred_bumpmapping_finite_diff_y_proj_v;
out float fog_visibility_frac;				// See fog_attenuation_coef for citation
out vec3 fog_component_rgb_partial;
out vec3 position_3d;
// For now just only either do bump mapping or don't
flat out float fwd_bumpmapping_amt;

uniform vec3 cam_ctr;
uniform float cam_yaw;					// See camspace_rot for citation
uniform float cam_pitch;
uniform float cam_roll;
uniform float cam_near;
uniform float cam_dist;

uniform float lighting_ambient;
uniform float lighting_maxsc;
uniform vec3 lighting_light_ctr;
uniform float lighting_light_brightness;

uniform float surf_albedo;				// Citation https://en.wikipedia.org/wiki/Lambertian_reflectance
uniform float surf_roughness;				// Citation https://graphicscompendium.com/gamedev/15-pbr

uniform vec3 fog_color;
							// Citation https://en.wikipedia.org/wiki/Light_scattering_by_particles
uniform float fog_attenuation_coef;			// Citation https://en.wikipedia.org/wiki/Attenuation_coefficient

// Arguments are Tait-Bryan angles
// [: Citation https://en.wikipedia.org/wiki/Rotation_matrix#General_rotations :] 
mat3 camspace_rot() {
    float a = cam_yaw;
    float b = cam_pitch;
    float c = cam_roll;
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

void camspace(inout vec3 v) {
    v -= cam_ctr;
    v *= camspace_rot();
}

// [: Citation https://en.wikipedia.org/wiki/Z-buffering :] 
float zbuffer_value(float z) {
    return sqrt(z - cam_near) / sqrt(cam_dist);
}

void set_illum(out float illum) {
    vec3 deltas = vert - lighting_light_ctr;
    float dist = length(deltas);
    illum = lighting_light_brightness / (dist * dist);
    illum *= surf_albedo / PI;
}

// Found here:
// [: Citation https://www.quora.com/How-do-you-project-a-point-onto-a-plane-along-the-direction-of-a-given-vector-projection-matrices-projection-math :] 
vec3 proj_onto_surf_subspace(in vec3 v) {
    vec3 normal = drv_surf_normal;
    return cross(normal, cross(v, normal));
}

void setup_bumpmapping_lambertian(out vec3 to_i_nonunit, out vec3 aligned_normal) {
    vec3 to_i_raw = lighting_light_ctr - vert;
    if (dot(normalize(to_i_raw), drv_surf_normal) < 0.0) {
        aligned_normal = -drv_surf_normal;
    } else {
        aligned_normal = drv_surf_normal;
    }
    to_i_nonunit = to_i_raw;
}

void setup_bumpmapping_finite_diff(out vec3 x_proj_u, out vec3 y_proj_v) {
    vec3 rough_x_basis = vec3(0.9, 0.1, 0.1);
    vec3 rough_y_basis = vec3(0.1, 0.9, 0.1);
    x_proj_u = proj_onto_surf_subspace(rough_x_basis);
    y_proj_v = proj_onto_surf_subspace(rough_y_basis);
    x_proj_u /= 50.0;
    y_proj_v /= 50.0;
}

float atan2(in vec2 v) {
    return atan(v.y, v.x);
}

// Derived from information at:
// [: Citation https://en.wikipedia.org/wiki/Cosine_similarity :]
float angle3(in vec3 a, in vec3 b) {
    float cosine_distance = dot(a, b) / (length(a) * length(b));
    return acos(cosine_distance);
}

// Oren-nayar reflectance
// Done with Gouraud shading to save compute
// Most of this came from these very helpful slides:
// [: Citation http://www.cs.cmu.edu/afs/cs/academic/class/16823-s16/www/pdfs/appearance-modeling-5.pdf :]
float get_icom_oren_nayar(in float illum) {
    vec3 to_i = normalize(lighting_light_ctr - vert);
    vec3 to_r = normalize(cam_ctr - vert);
    float theta_i = acos(abs(dot(to_i, drv_surf_normal)));
    float theta_r = acos(abs(dot(to_r, drv_surf_normal)));
    float microfacet_var = surf_roughness * surf_roughness;
    float alpha = max(theta_i, theta_r);
    float beta = min(theta_i, theta_r);
    vec3 proj2_i = proj_onto_surf_subspace(to_i);
    vec3 proj2_r = proj_onto_surf_subspace(to_r);
    float azimuthal_delta = angle3(proj2_i, proj2_r);
    float azimuthal_part = max(0, cos(azimuthal_delta));
    float fac = azimuthal_part * sin(alpha) * tan(beta);
    float const_frac = microfacet_var / (microfacet_var + 0.33);
    float scale_frac = microfacet_var / (microfacet_var + 0.09);
    float a = 1.0 - (0.5 * const_frac);
    float b = 0.45 * scale_frac;
    return a + (b * fac);
}

void update_illum_ambient(inout float illum) {
    illum = clamp(illum + lighting_ambient, 0.0, lighting_maxsc);
}

// [: Citation https://en.wikipedia.org/wiki/Light_scattering_by_particles :]
float distance_fog_amt(in float current_zbuffer) {
    float contrast = exp(-fog_attenuation_coef * current_zbuffer);
    return 1.0 - contrast;
}

vec3 distance_fog_rgb_partial(in float fog_amt) {
    return fog_color * fog_amt;
}

float distance_fog_visibility_frac(in float fog_amt) {
    return 1.0 - fog_amt;
}

void main() {
    // Perspective transform
    // [: Citation https://en.wikipedia.org/wiki/Camera_matrix :]
    // [: Citation https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula :]
    // [: Citation https://staff.fnwi.uva.nl/r.vandenboomgaard/IPCV20172018/LectureNotes/MATH/homogenous.html :]
    // [: Citation http://www.songho.ca/math/homogeneous/homogeneous.html :]
    vec3 v = vert;
    camspace(v);
    vec2 pos = v.xy / v.z;
    float z = zbuffer_value(v.z);

    set_illum(illum);
    update_illum_ambient(illum);

    icom_oren_nayar = get_icom_oren_nayar(illum);
    icom_lighting_maxsc = lighting_maxsc;

    setup_bumpmapping_lambertian(
        ideferred_bumpmapping_to_i_nonunit,
        ideferred_phong_aligned_normal_nonunit
    );
    setup_bumpmapping_finite_diff(
        ideferred_bumpmapping_finite_diff_x_proj_u,
        ideferred_bumpmapping_finite_diff_y_proj_v
    );
    fwd_bumpmapping_amt = bumpmapping_amt;

    float fog_amt = distance_fog_amt(z);
    fog_component_rgb_partial = distance_fog_rgb_partial(fog_amt);
    fog_visibility_frac = distance_fog_visibility_frac(fog_amt);

    vert_color = aux_rgb;

    gl_Position = vec4(pos, z, 1.0);
    position_3d = vert;
}

