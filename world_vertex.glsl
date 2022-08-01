#version 330

in vec3 vert;
out vec3 vert_color;

uniform vec3 cam_ctr;
uniform float cam_yaw;
uniform float cam_pitch;
uniform float cam_roll;

mat3 camspace_rot() {
    float a = cam_yaw; float b = cam_pitch; float c = cam_roll;
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

float zbuffer_value(vec2 pos) {
    vec3 up = vec3(0.0, 0.0, 1.0);
    up *= camspace_rot();
    return dot(vert, up);
}

void main() {
    vec3 v = vert;
    camspace(v);
    vec2 pos = v.xy / v.z;
    gl_Position = vec4(pos, zbuffer_value(pos), 1.0);
    vert_color = vert;
}
