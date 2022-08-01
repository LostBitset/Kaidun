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

vec3 camspace() {
    return (vert - cam_ctr) * camspace_rot();
}

mat3x4 perspective() {
    return mat3x4(
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0
    );
}

void main() {
    vec4 camspace_h = vec4(camspace(), 1.0);
    vec3 pos_h =  camspace_h * perspective();
    vec2 pos = pos_h.xy / pos_h.z;
    gl_Position = vec4(pos, vert.z, 1.0);
    vert_color = vert;
}
