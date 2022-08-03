#version 330

in vec3 vert_color;
// This is the initial illumination value
in float illum;
// Normally the whole point of Phong Shading is to interpolate the surface
// normal in order to accurately light smooth surfaces
// For this, we're the only thing we're interpolating is the normalized
// vector to the light source, so that we avoid the artifacts caused by
// Gouraud shading
// Normally, these artifacts are caused by the specular component, which
// this just flat out doesn't have, but the Oren-Nayar model yields a similar
// effect
// It isn't technically Phong Shading, but it's close enough for me to
// shove 'phong' into the variable names
// I'm interpolating vectors that vary across the surface for lighting
// calculations, just with the surface-to-light vector instead of the normal
// Fine. This is pseudo-Phong shading, and 'phong' in the code is just shorthand
flat in vec3 illum_frag_phong_oren_nayar_to_i;
in vec3 illum_frag_phong_oren_nayar_to_r;
// Another note: Yes, I could have calculated proj2_i and proj2_r
// in the fragment shader and saved a bit of time
// It's true that four cross products isn't a ton, but it does add up
// However, I would have to interpolate proj2_r, which makes it be the cost
// of a few extra bytes and an interpolation vs. four cross products
// The difference seems incredibly insignificant and doesn't seem worth
// dealing with
flat in float illum_frag_phong_oren_nayar_coef_a;
flat in float illum_frag_phong_oren_nayar_coef_b;
// The ambient component has to be done here to avoid some strange artifacts
// It might seem like the interpolated vector will always be in between the
// points, but it's possible for it to line up and go above lighting_maxsc
// (which is accessed as illum_frag_phong_lighting_maxsc here)
// This manifests as bright spots closer to the vertices being less bright
// (because they actually have to deal with lighting_maxsc)
// and bright spots farther from the vertices being extra bright
// Moving the ambient component into the fragment shader prevents this
// issue from occuring
// All must be subject to the rule of the almighty lighting_maxsc!!!
flat in float illum_frag_phong_lighting_ambient;
flat in float illum_frag_phong_lighting_maxsc;
// See the comment about pseudo-Phong shading
// I know this line is an oxymoron. Leave me alone.
flat in vec3 phong_surf_normal;
// Also interpolate distance fog values
in float fog_visibility_frac;
in vec3 fog_component_rgb_partial;

out vec3 color;

void update_illum_ambient_frag(inout float illum) {
    float lighting_ambient = illum_frag_phong_lighting_ambient;
    float lighting_maxsc = illum_frag_phong_lighting_maxsc;
    illum = clamp(illum + lighting_ambient, 0.0, lighting_maxsc);
}

// Project a 3D vector onto a subspace of R^3 defined as the plane
// defined by the given normal vector, located at the origin
vec3 proj_onto_surf_subspace(in vec3 v) {
    vec3 normal = phong_surf_normal;
    return cross(normal, cross(v, normal));
}

// Basically just a 3D version of atan2(b) - atan2(a)
// Finds the angle between two 3-vectors
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
    float a = illum_frag_phong_oren_nayar_coef_a;
    float b = illum_frag_phong_oren_nayar_coef_b;
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
