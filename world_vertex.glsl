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

vec3 camspace_tr() {
    return -cam_ctr;
}

mat3x4 perspective(in mat3 rot, in vec3 tr) {
    vec3 tr2 = rot * tr;
    return mat3x4(
        rot[0][0], rot[1][0], rot[2][0], tr2.x,
        rot[0][1], rot[1][1], rot[2][1], tr2.y,
        rot[0][2], rot[1][2], rot[2][2], tr2.z
    );
}

vec3 pdiv3(in vec4 homogenous) {
    return homogenous.xyz / homogenous.w;
}

vec2 pdiv2(in vec3 homogenous) {
    return homogenous.xy / homogenous.z;
}

void main() {
    mat3x4 persp = perspective(camspace_rot(), camspace_tr());
    vec4 vert_h = vec4(vert, 1.0);
    vec3 pos_h = vert_h * persp;
    vec2 pos = pdiv2(pos_h);
    gl_Position = vec4(pos, 0.0, 1.0);
    vert_color = vec3(1.0, 0.0, 0.0);
}
