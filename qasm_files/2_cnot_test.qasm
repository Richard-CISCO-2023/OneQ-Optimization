OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg c[4];
cx q[0],q[1];
cx q[2],q[3];
