#version 330

#define PI 3.1415926538

#define UP vec3(0.0, 0.0, 1.0)

in vec3 vert;
in vec3 aux_surf_normal;

out vec3 vert_color;
out float illum;

uniform vec3 cam_ctr;
uniform float cam_yaw;
uniform float cam_pitch;
uniform float cam_roll;
uniform float cam_near;
uniform float cam_dist;

uniform float lighting_ambient;
uniform float lighting_maxsc;
uniform vec3 lighting_light_ctr;
uniform float lighting_light_brightness;

uniform float surf_albedo;
uniform float surf_roughness;

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

float zbuffer_value(float z) {
    return sqrt(z - cam_near) / sqrt(cam_dist);
}

void set_illum(out float illum) {
    vec3 deltas = vert - lighting_light_ctr;
    float dist = length(deltas);
    illum = lighting_light_brightness / (dist * dist);
}

void update_illum_lambertian(inout float illum) {
    illum *= surf_albedo / PI;
    vec3 to_i = normalize(lighting_light_ctr - vert);
    illum *= abs(dot(to_i, aux_surf_normal));
}

float atan2(in vec2 v) {
    return atan(v.y, v.x);
}

vec3 proj_onto_surf_subspace(in vec3 v) {
    vec3 normal = aux_surf_normal;
    return cross(normal, cross(v, normal));
}

float angle3(in vec3 a, in vec3 b) {
    float cosine_distance = dot(a, b) / (length(a) * length(b));
    return acos(cosine_distance);
}

void update_illum_oren_nayar_ext(inout float illum) {
    vec3 to_i = normalize(lighting_light_ctr - vert);
    vec3 to_r = normalize(cam_ctr - vert);
    float theta_i = acos(dot(to_i, aux_surf_normal));
    float theta_r = acos(dot(to_r, aux_surf_normal));
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
    illum *= a + (b * fac);
}

void update_illum_ambient(inout float illum) {
    illum = clamp(illum + lighting_ambient, 0.0, lighting_maxsc);
}

void main() {
    vec3 v = vert;
    camspace(v);
    vec2 pos = v.xy / v.z;
    float z = zbuffer_value(v.z);
    gl_Position = vec4(pos, z, 1.0);
    vert_color = vert;
    set_illum(illum);
    update_illum_lambertian(illum);
    update_illum_oren_nayar_ext(illum);
    update_illum_ambient(illum);
}
