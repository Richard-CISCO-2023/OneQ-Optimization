OPENQASM 2.0;
include "qelib1.inc";
qreg q[15];
creg c[10];
rz(pi/2) q[0];
rz(pi/2) q[0];
rz(pi/2) q[1];
rz(pi/2) q[1];
rz(pi/2) q[2];
rz(pi/2) q[2];
rz(pi/2) q[3];
rz(pi/2) q[3];
rz(pi/2) q[4];
rz(pi/2) q[4];
rz(pi/2) q[5];
rz(pi/2) q[5];
rz(pi/2) q[6];
rz(pi/2) q[6];
rz(pi/2) q[7];
rz(pi/2) q[7];
rz(pi/2) q[8];
rz(pi/2) q[8];
rz(pi/2) q[9];
rz(pi/2) q[9];
x q[10];
x q[12];
x q[14];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14];
rz(pi/2) q[12];;
rz(pi/2) q[12];
cx q[10],q[12];
rz(-pi/4) q[12];
rz(pi/2) q[13];;
rz(pi/2) q[13];
rz(pi/2) q[14];;
rz(pi/2) q[14];
cx q[9],q[12];
rz(pi/4) q[12];
cx q[10],q[12];
rz(pi/4) q[10];
rz(-pi/4) q[12];
cx q[9],q[12];
rz(3*pi/4) q[12];;
rz(pi/2) q[12];
cx q[12],q[13];
rz(-pi/4) q[13];
cx q[11],q[13];
rz(pi/4) q[13];
cx q[12],q[13];
rz(pi/4) q[12];
rz(-pi/4) q[13];
cx q[11],q[13];
cx q[11],q[12];
rz(pi/4) q[11];
rz(-pi/4) q[12];
cx q[11],q[12];
rz(3*pi/4) q[13];;
rz(pi/2) q[13];
cx q[13],q[14];
rz(pi/2) q[13];;
rz(pi/2) q[13];
cx q[12],q[13];
rz(-pi/4) q[13];
cx q[11],q[13];
rz(pi/4) q[13];
cx q[12],q[13];
rz(pi/4) q[12];
rz(-pi/4) q[13];
cx q[11],q[13];
cx q[11],q[12];
rz(pi/4) q[11];
rz(-pi/4) q[12];
cx q[11],q[12];
rz(pi/2) q[12];;
rz(pi/2) q[12];
rz(3*pi/4) q[13];;
rz(pi/2) q[13];
rz(pi/2) q[14];;
rz(pi/2) q[14];
cx q[9],q[10];
rz(-pi/4) q[10];
rz(pi/4) q[9];
cx q[9],q[10];
cx q[10],q[12];
rz(-pi/4) q[12];
cx q[9],q[12];
rz(pi/4) q[12];
cx q[10],q[12];
rz(pi/4) q[10];
rz(-pi/4) q[12];
cx q[9],q[12];
rz(3*pi/4) q[12];;
rz(pi/2) q[12];
cx q[9],q[10];
rz(-pi/4) q[10];
rz(pi/4) q[9];
cx q[9],q[10];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14];
rz(-pi/1024) q[9];
cx q[9],q[0];
rz(pi/1024) q[0];
cx q[9],q[0];
rz(-pi/1024) q[0];
rz(-pi/512) q[9];
cx q[9],q[1];
rz(pi/512) q[1];
cx q[9],q[1];
rz(-pi/512) q[1];
rz(-pi/256) q[9];
cx q[9],q[2];
rz(pi/256) q[2];
cx q[9],q[2];
rz(-pi/256) q[2];
rz(-pi/128) q[9];
cx q[9],q[3];
rz(pi/128) q[3];
cx q[9],q[3];
rz(-pi/128) q[3];
rz(-pi/64) q[9];
cx q[9],q[4];
rz(pi/64) q[4];
cx q[9],q[4];
rz(-pi/64) q[4];
rz(-pi/32) q[9];
cx q[9],q[5];
rz(pi/32) q[5];
cx q[9],q[5];
rz(-pi/32) q[5];
rz(-pi/16) q[9];
cx q[9],q[6];
rz(pi/16) q[6];
cx q[9],q[6];
rz(-pi/16) q[6];
rz(-pi/8) q[9];
cx q[9],q[7];
rz(pi/8) q[7];
cx q[9],q[7];
rz(-pi/8) q[7];
rz(-pi/4) q[9];
cx q[9],q[8];
rz(pi/4) q[8];
cx q[9],q[8];
rz(-0.79153409) q[8];
cx q[8],q[0];
rz(pi/512) q[0];
cx q[8],q[0];
rz(-pi/512) q[0];
rz(-pi/256) q[8];
cx q[8],q[1];
rz(pi/256) q[1];
cx q[8],q[1];
rz(-pi/256) q[1];
rz(-pi/128) q[8];
cx q[8],q[2];
rz(pi/128) q[2];
cx q[8],q[2];
rz(-pi/128) q[2];
rz(-pi/64) q[8];
cx q[8],q[3];
rz(pi/64) q[3];
cx q[8],q[3];
rz(-pi/64) q[3];
rz(-pi/32) q[8];
cx q[8],q[4];
rz(pi/32) q[4];
cx q[8],q[4];
rz(-pi/32) q[4];
rz(-pi/16) q[8];
cx q[8],q[5];
rz(pi/16) q[5];
cx q[8],q[5];
rz(-pi/16) q[5];
rz(-pi/8) q[8];
cx q[8],q[6];
rz(pi/8) q[6];
cx q[8],q[6];
rz(-pi/8) q[6];
rz(-pi/4) q[8];
cx q[8],q[7];
rz(pi/4) q[7];
cx q[8],q[7];
rz(-0.79767001) q[7];
cx q[7],q[0];
rz(pi/256) q[0];
cx q[7],q[0];
rz(-pi/256) q[0];
rz(-pi/128) q[7];
cx q[7],q[1];
rz(pi/128) q[1];
cx q[7],q[1];
rz(-pi/128) q[1];
rz(-pi/64) q[7];
cx q[7],q[2];
rz(pi/64) q[2];
cx q[7],q[2];
rz(-pi/64) q[2];
rz(-pi/32) q[7];
cx q[7],q[3];
rz(pi/32) q[3];
cx q[7],q[3];
rz(-pi/32) q[3];
rz(-pi/16) q[7];
cx q[7],q[4];
rz(pi/16) q[4];
cx q[7],q[4];
rz(-pi/16) q[4];
rz(-pi/8) q[7];
cx q[7],q[5];
rz(pi/8) q[5];
cx q[7],q[5];
rz(-pi/8) q[5];
rz(-pi/4) q[7];
cx q[7],q[6];
rz(pi/4) q[6];
cx q[7],q[6];
rz(-0.80994186) q[6];
cx q[6],q[0];
rz(pi/128) q[0];
cx q[6],q[0];
rz(-pi/128) q[0];
rz(-pi/64) q[6];
cx q[6],q[1];
rz(pi/64) q[1];
cx q[6],q[1];
rz(-pi/64) q[1];
rz(-pi/32) q[6];
cx q[6],q[2];
rz(pi/32) q[2];
cx q[6],q[2];
rz(-pi/32) q[2];
rz(-pi/16) q[6];
cx q[6],q[3];
rz(pi/16) q[3];
cx q[6],q[3];
rz(-pi/16) q[3];
rz(-pi/8) q[6];
cx q[6],q[4];
rz(pi/8) q[4];
cx q[6],q[4];
rz(-pi/8) q[4];
rz(-pi/4) q[6];
cx q[6],q[5];
rz(pi/4) q[5];
cx q[6],q[5];
rz(-0.83448555) q[5];
cx q[5],q[0];
rz(pi/64) q[0];
cx q[5],q[0];
rz(-pi/64) q[0];
rz(-pi/32) q[5];
cx q[5],q[1];
rz(pi/32) q[1];
cx q[5],q[1];
rz(-pi/32) q[1];
rz(-pi/16) q[5];
cx q[5],q[2];
rz(pi/16) q[2];
cx q[5],q[2];
rz(-pi/16) q[2];
rz(-pi/8) q[5];
cx q[5],q[3];
rz(pi/8) q[3];
cx q[5],q[3];
rz(-pi/8) q[3];
rz(-pi/4) q[5];
cx q[5],q[4];
rz(pi/4) q[4];
cx q[5],q[4];
rz(-0.88357293) q[4];
cx q[4],q[0];
rz(pi/32) q[0];
cx q[4],q[0];
rz(-pi/32) q[0];
rz(-pi/16) q[4];
cx q[4],q[1];
rz(pi/16) q[1];
cx q[4],q[1];
rz(-pi/16) q[1];
rz(-pi/8) q[4];
cx q[4],q[2];
rz(pi/8) q[2];
cx q[4],q[2];
rz(-pi/8) q[2];
rz(-pi/4) q[4];
cx q[4],q[3];
rz(pi/4) q[3];
cx q[4],q[3];
rz(-5*pi/16) q[3];
cx q[3],q[0];
rz(pi/16) q[0];
cx q[3],q[0];
rz(-pi/16) q[0];
rz(-pi/8) q[3];
cx q[3],q[1];
rz(pi/8) q[1];
cx q[3],q[1];
rz(-pi/8) q[1];
rz(-pi/4) q[3];
cx q[3],q[2];
rz(pi/4) q[2];
cx q[3],q[2];
rz(-3*pi/8) q[2];
cx q[2],q[0];
rz(pi/8) q[0];
cx q[2],q[0];
rz(-pi/8) q[0];
rz(-pi/4) q[2];
cx q[2],q[1];
rz(pi/4) q[1];
cx q[2],q[1];
rz(-pi/2) q[1];
cx q[1],q[0];
rz(pi/4) q[0];
cx q[1],q[0];
rz(-pi/4) q[0];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8],q[9],q[10],q[11],q[12],q[13],q[14];
rz(pi/2) q[0];
rz(pi/2) q[0];
rz(pi/2) q[1];
rz(pi/2) q[1];
rz(pi/2) q[2];
rz(pi/2) q[2];
rz(pi/2) q[3];
rz(pi/2) q[3];
rz(pi/2) q[4];
rz(pi/2) q[4];
rz(pi/2) q[5];
rz(pi/2) q[5];
rz(pi/2) q[6];
rz(pi/2) q[6];
rz(pi/2) q[7];
rz(pi/2) q[7];
rz(pi/2) q[8];
rz(pi/2) q[8];
rz(pi/2) q[9];
rz(pi/2) q[9];
measure q[7] -> c[7];
measure q[8] -> c[8];
measure q[9] -> c[9];
