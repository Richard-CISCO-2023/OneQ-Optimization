OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg c[5];
x q[0];
measure q[4] -> c[0];
reset q[4];
rz(pi/2) q[4];
sx q[4];
rz(pi/2) q[4];
cx q[4],q[2];
cx q[4],q[0];
cx q[0],q[1];
rz(pi/2) q[0];
sx q[0];
rz(pi/2) q[0];
cx q[1],q[0];
rz(-pi/4) q[0];
if(c==1) rz(pi/2) q[4];
rz(pi/2) q[4];
sx q[4];
rz(pi/2) q[4];
measure q[4] -> c[1];
reset q[4];
rz(pi/2) q[4];
sx q[4];
rz(pi/2) q[4];
cx q[4],q[0];
rz(pi/4) q[0];
cx q[1],q[0];
rz(-pi/4) q[0];
rz(pi/4) q[1];
cx q[4],q[0];
rz(3*pi/4) q[0];
sx q[0];
rz(pi/2) q[0];
cx q[4],q[1];
rz(-pi/4) q[1];
rz(pi/4) q[4];
cx q[4],q[1];
cx q[0],q[1];
cx q[1],q[2];
rz(pi/2) q[1];
sx q[1];
rz(pi/2) q[1];
cx q[2],q[1];
rz(-pi/4) q[1];
cx q[4],q[1];
rz(pi/4) q[1];
cx q[2],q[1];
rz(-pi/4) q[1];
rz(pi/4) q[2];
cx q[4],q[1];
rz(3*pi/4) q[1];
sx q[1];
rz(pi/2) q[1];
cx q[4],q[2];
rz(-pi/4) q[2];
rz(pi/4) q[4];
cx q[4],q[2];
cx q[1],q[2];
cx q[2],q[3];
rz(pi/2) q[2];
sx q[2];
rz(pi/2) q[2];
cx q[3],q[2];
rz(-pi/4) q[2];
cx q[4],q[2];
rz(pi/4) q[2];
cx q[3],q[2];
rz(-pi/4) q[2];
rz(pi/4) q[3];
cx q[4],q[2];
rz(3*pi/4) q[2];
sx q[2];
rz(pi/2) q[2];
cx q[4],q[3];
rz(-pi/4) q[3];
rz(pi/4) q[4];
cx q[4],q[3];
cx q[2],q[3];
cx q[4],q[3];
cx q[4],q[2];
cx q[4],q[1];
cx q[4],q[0];
if(c==3) rz(3*pi/4) q[4];
if(c==2) rz(pi/2) q[4];
if(c==1) rz(pi/4) q[4];
rz(pi/2) q[4];
sx q[4];
rz(pi/2) q[4];
measure q[4] -> c[2];
