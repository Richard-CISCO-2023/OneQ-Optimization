OPENQASM 2.0;
include "qelib1.inc";
qreg cin[1];
qreg a[4];
qreg b[4];
qreg cout[1];
creg ans[5];
x a[0];
x b[0];
cx a[0],b[0];
cx a[0],cin[0];
rz(pi/2) a[0];
sx a[0];
rz(pi/2) a[0];
cx b[0],a[0];
rz(-pi/4) a[0];
cx cin[0],a[0];
rz(pi/4) a[0];
cx b[0],a[0];
rz(-pi/4) a[0];
cx cin[0],a[0];
rz(3*pi/4) a[0];
sx a[0];
rz(pi/2) a[0];
rz(pi/4) b[0];
cx cin[0],b[0];
rz(pi/4) cin[0];
rz(-pi/4) b[0];
cx cin[0],b[0];
x b[1];
cx a[1],b[1];
cx a[1],a[0];
rz(pi/2) a[1];
sx a[1];
rz(pi/2) a[1];
cx b[1],a[1];
rz(-pi/4) a[1];
cx a[0],a[1];
rz(pi/4) a[1];
cx b[1],a[1];
rz(-pi/4) a[1];
cx a[0],a[1];
rz(3*pi/4) a[1];
sx a[1];
rz(pi/2) a[1];
rz(pi/4) b[1];
cx a[0],b[1];
rz(pi/4) a[0];
rz(-pi/4) b[1];
cx a[0],b[1];
x b[2];
cx a[2],b[2];
cx a[2],a[1];
rz(pi/2) a[2];
sx a[2];
rz(pi/2) a[2];
cx b[2],a[2];
rz(-pi/4) a[2];
cx a[1],a[2];
rz(pi/4) a[2];
cx b[2],a[2];
rz(-pi/4) a[2];
cx a[1],a[2];
rz(3*pi/4) a[2];
sx a[2];
rz(pi/2) a[2];
rz(pi/4) b[2];
cx a[1],b[2];
rz(pi/4) a[1];
rz(-pi/4) b[2];
cx a[1],b[2];
x b[3];
cx a[3],b[3];
cx a[3],a[2];
rz(pi/2) a[3];
sx a[3];
rz(pi/2) a[3];
cx b[3],a[3];
rz(-pi/4) a[3];
cx a[2],a[3];
rz(pi/4) a[3];
cx b[3],a[3];
rz(-pi/4) a[3];
cx a[2],a[3];
rz(3*pi/4) a[3];
sx a[3];
rz(pi/2) a[3];
rz(pi/4) b[3];
cx a[2],b[3];
rz(pi/4) a[2];
rz(-pi/4) b[3];
cx a[2],b[3];
cx a[3],cout[0];
rz(pi/2) a[3];
sx a[3];
rz(pi/2) a[3];
cx b[3],a[3];
rz(-pi/4) a[3];
cx a[2],a[3];
rz(pi/4) a[3];
cx b[3],a[3];
rz(-pi/4) a[3];
cx a[2],a[3];
rz(3*pi/4) a[3];
sx a[3];
rz(pi/2) a[3];
rz(pi/4) b[3];
cx a[2],b[3];
rz(pi/4) a[2];
rz(-pi/4) b[3];
cx a[2],b[3];
cx a[3],a[2];
cx a[2],b[3];
rz(pi/2) a[2];
sx a[2];
rz(pi/2) a[2];
cx b[2],a[2];
rz(-pi/4) a[2];
cx a[1],a[2];
rz(pi/4) a[2];
cx b[2],a[2];
rz(-pi/4) a[2];
cx a[1],a[2];
rz(3*pi/4) a[2];
sx a[2];
rz(pi/2) a[2];
rz(pi/4) b[2];
cx a[1],b[2];
rz(pi/4) a[1];
rz(-pi/4) b[2];
cx a[1],b[2];
cx a[2],a[1];
cx a[1],b[2];
rz(pi/2) a[1];
sx a[1];
rz(pi/2) a[1];
cx b[1],a[1];
rz(-pi/4) a[1];
cx a[0],a[1];
rz(pi/4) a[1];
cx b[1],a[1];
rz(-pi/4) a[1];
cx a[0],a[1];
rz(3*pi/4) a[1];
sx a[1];
rz(pi/2) a[1];
rz(pi/4) b[1];
cx a[0],b[1];
rz(pi/4) a[0];
rz(-pi/4) b[1];
cx a[0],b[1];
cx a[1],a[0];
cx a[0],b[1];
rz(pi/2) a[0];
sx a[0];
rz(pi/2) a[0];
cx b[0],a[0];
rz(-pi/4) a[0];
cx cin[0],a[0];
rz(pi/4) a[0];
cx b[0],a[0];
rz(-pi/4) a[0];
cx cin[0],a[0];
rz(3*pi/4) a[0];
sx a[0];
rz(pi/2) a[0];
rz(pi/4) b[0];
cx cin[0],b[0];
rz(pi/4) cin[0];
rz(-pi/4) b[0];
cx cin[0],b[0];
cx a[0],cin[0];
cx cin[0],b[0];
measure b[0] -> ans[0];
measure b[1] -> ans[1];
measure b[2] -> ans[2];
measure b[3] -> ans[3];
measure cout[0] -> ans[4];
