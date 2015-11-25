#include <cstdio>
#include <stdlib.h>
#include <assert.h>
#include <iostream>
using namespace std;
#include "vops.h"
#include "general.h"
#include <stdexcept>
namespace ANONYMOUS{

  void assertion(bool b) {
    if (!b) {

      throw std::logic_error( "testing logic_error" );
    }
  }
  
Guard* Guard::create(int  z_, int  o_){
  void* temp= malloc( sizeof(Guard)  ); 
  Guard* rv = new (temp)Guard();
  rv->z =  z_;
  rv->o =  o_;
  return rv;
}
Array* Array::create(int  s_, int*  A_, int A_len){
  int tlen_A = s_; 
  void* temp= malloc( sizeof(Array)   + sizeof(int )*tlen_A); 
  Array* rv = new (temp)Array();
  rv->s =  s_;
  CopyArr(rv->A, A_, tlen_A, A_len ); 
  return rv;
}
void l4__Wrapper() {
  int  tape_index__ANONYMOUS_s100=0;
  glblInit_tape_index__ANONYMOUS_s110(tape_index__ANONYMOUS_s100);
  bool _tt0[143] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  bool*  tape__ANONYMOUS_s99= new bool [143]; CopyArr<bool >(tape__ANONYMOUS_s99,_tt0, 143, 143);
  glblInit_tape__ANONYMOUS_s108(tape__ANONYMOUS_s99);
  l4(tape__ANONYMOUS_s99, tape_index__ANONYMOUS_s100);
  delete[] tape__ANONYMOUS_s99;
}
void l4__WrapperNospec() {}
void l3__Wrapper() {
  int  tape_index__ANONYMOUS_s89=0;
  glblInit_tape_index__ANONYMOUS_s110(tape_index__ANONYMOUS_s89);
  bool _tt1[143] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  bool*  tape__ANONYMOUS_s88= new bool [143]; CopyArr<bool >(tape__ANONYMOUS_s88,_tt1, 143, 143);
  glblInit_tape__ANONYMOUS_s108(tape__ANONYMOUS_s88);
  l3(tape__ANONYMOUS_s88, tape_index__ANONYMOUS_s89);
  delete[] tape__ANONYMOUS_s88;
}
void l3__WrapperNospec() {}
void l1__Wrapper() {
  int  tape_index__ANONYMOUS_s93=0;
  glblInit_tape_index__ANONYMOUS_s110(tape_index__ANONYMOUS_s93);
  bool _tt2[143] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  bool*  tape__ANONYMOUS_s94= new bool [143]; CopyArr<bool >(tape__ANONYMOUS_s94,_tt2, 143, 143);
  glblInit_tape__ANONYMOUS_s108(tape__ANONYMOUS_s94);
  l1(tape__ANONYMOUS_s94, tape_index__ANONYMOUS_s93);
  delete[] tape__ANONYMOUS_s94;
}
void l1__WrapperNospec() {}
void l0__Wrapper() {
  l0();
}
void l0__WrapperNospec() {}
void glblInit_tape__ANONYMOUS_s108(bool* tape__ANONYMOUS_s107/* len = 143 */) {
  bool _tt3[143] = {0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0};
  CopyArr<bool >(tape__ANONYMOUS_s107,_tt3, 143, 143);
}
void glblInit_tape_index__ANONYMOUS_s110(int& tape_index__ANONYMOUS_s109) {
  tape_index__ANONYMOUS_s109 = 0;
}
void l4(bool* tape__ANONYMOUS_s97/* len = 143 */, int& tape_index__ANONYMOUS_s92) {
  int _tt4[3] = {5, 3, 4};
  int _tt5[3] = {3, 4, 5};
  test_case(3, _tt4, _tt5, 2, tape__ANONYMOUS_s97, tape_index__ANONYMOUS_s92);
}
void l3(bool* tape__ANONYMOUS_s95/* len = 143 */, int& tape_index__ANONYMOUS_s96) {
  int _tt6[3] = {4, 5, 3};
  int _tt7[3] = {3, 4, 5};
  test_case(3, _tt6, _tt7, 2, tape__ANONYMOUS_s95, tape_index__ANONYMOUS_s96);
}
void l1(bool* tape__ANONYMOUS_s101/* len = 143 */, int& tape_index__ANONYMOUS_s98) {
  int _tt8[2] = {2, 1};
  int _tt9[2] = {1, 2};
  test_case(2, _tt8, _tt9, 2, tape__ANONYMOUS_s101, tape_index__ANONYMOUS_s98);
}
void l0() {}
void test_case(int n, int* a/* len = n */, int* b/* len = n */, int bnd, bool* tape__ANONYMOUS_s90/* len = 143 */, int& tape_index__ANONYMOUS_s91) {
  Array*  o_s4=NULL;
  constant_array(n, a, o_s4);
  Array*  o_s6=NULL;
  recursive_expression(o_s4, bnd, o_s6, tape__ANONYMOUS_s90, tape_index__ANONYMOUS_s91);
  assertion ((o_s6->s) == (n));;
  assertion (arrCompare((o_s6->A+ 0), n, b, n) && ((n) == (n)));;
}
void constant_array(int n, int* a/* len = n */, Array*& _out) {
  _out = NULL;
  _out = Array::create(n, a, n);
  return;
}
void recursive_expression(Array* a, int bnd, Array*& _out, bool* tape__ANONYMOUS_s106/* len = 143 */, int& tape_index__ANONYMOUS_s85) {
  _out = NULL;
  if ((bnd) < (0)) {
    _out = NULL;
    return;
  }
  tape_index__ANONYMOUS_s85 = 0;
  bool  s1=0;
  bool  s2=0;
  bool  s3=0;
  bool  s4=0;
  bool  s5=0;
  bool  s6=0;
  Guard*  g_s8=NULL;
  guard_expression(a, 3, s1, g_s8, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  int  target_s10=0;
  integer_expression(a, 3, s2, target_s10, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  assertion ((tape_index__ANONYMOUS_s85) == (16));;
  Array*  b_s12=NULL;
  array_expression(a, 4, s3, b_s12, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  Array*  x_s14=NULL;
  array_expression(a, 4, s4, x_s14, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  Array*  x=NULL;
  x = x_s14;
  bool  rx_s16=0;
  flip(rx_s16, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  Array*  y_s18=NULL;
  array_expression(a, 4, s5, y_s18, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  Array*  y=NULL;
  y = y_s18;
  bool  ry_s20=0;
  flip(ry_s20, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  Array*  z_s22=NULL;
  array_expression(a, 4, s6, z_s22, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  Array*  z=NULL;
  z = z_s22;
  bool  rz_s24=0;
  flip(rz_s24, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
  assertion ((s1 && s2) && s3);;
  bool  _out_s26=0;
  run_guard(g_s8, target_s10, _out_s26);
  if (_out_s26) {
    _out = b_s12;
    return;
  }
  assertion ((s4 && s5) && s6);;
  if (rz_s24) {
    assertion ((x_s14->s) < (a->s));;
    Array*  x_s28=NULL;
    recursive_expression(x_s14, bnd - 1, x_s28, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
    x = x_s28;
  }
  if (ry_s20) {
    assertion ((y_s18->s) < (a->s));;
    Array*  y_s30=NULL;
    recursive_expression(y_s18, bnd - 1, y_s30, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
    y = y_s30;
  }
  if (rz_s24) {
    assertion ((z_s22->s) < (a->s));;
    Array*  z_s32=NULL;
    recursive_expression(z_s22, bnd - 1, z_s32, tape__ANONYMOUS_s106, tape_index__ANONYMOUS_s85);
    z = z_s32;
  }
  Array*  _out_s34=NULL;
  concatenate3(x, y, z, _out_s34);
  _out = _out_s34;
  return;
}
void guard_expression(Array* a, int d, bool& success, Guard*& _out, bool* tape__ANONYMOUS_s86/* len = 143 */, int& tape_index__ANONYMOUS_s87) {
  _out = NULL;
  assertion ((d) > (1));;
  bool  zs=0;
  int  z_s66=0;
  integer_expression(a, d - 1, zs, z_s66, tape__ANONYMOUS_s86, tape_index__ANONYMOUS_s87);
  success = zs;
  bool  c1_s68=0;
  flip(c1_s68, tape__ANONYMOUS_s86, tape_index__ANONYMOUS_s87);
  bool  c2_s70=0;
  flip(c2_s70, tape__ANONYMOUS_s86, tape_index__ANONYMOUS_s87);
  int  o=0;
  if (c1_s68) {
    o = 0;
  }
  if (!(c1_s68) && c2_s70) {
    o = 1;
  }
  if (!(c1_s68) && !(c2_s70)) {
    o = 2;
  }
  _out = Guard::create(z_s66, o);
  return;
}
void integer_expression(Array* a, int d, bool& success, int& _out, bool* tape__ANONYMOUS_s104/* len = 143 */, int& tape_index__ANONYMOUS_s105) {
  _out = 0;
  assertion ((d) > (0));;
  if ((d) == (1)) {
    success = 1;
    _out = 0;
    return;
  }
  bool  integer_success=0;
  int  zp_s72=0;
  integer_expression(a, d - 1, integer_success, zp_s72, tape__ANONYMOUS_s104, tape_index__ANONYMOUS_s105);
  Array*  l_s74=NULL;
  bool  array_success=0;
  array_expression(a, d - 1, array_success, l_s74, tape__ANONYMOUS_s104, tape_index__ANONYMOUS_s105);
  bool  c1_s76=0;
  flip(c1_s76, tape__ANONYMOUS_s104, tape_index__ANONYMOUS_s105);
  bool  c2_s78=0;
  flip(c2_s78, tape__ANONYMOUS_s104, tape_index__ANONYMOUS_s105);
  bool  c3_s80=0;
  flip(c3_s80, tape__ANONYMOUS_s104, tape_index__ANONYMOUS_s105);
  if (c1_s76 && c2_s78) {
    success = 1;
    _out = 0;
    return;
  }
  if (c1_s76 && !(c2_s78)) {
    success = integer_success;
    _out = zp_s72 + 1;
    return;
  }
  if (!(c1_s76) && c2_s78) {
    success = integer_success;
    _out = zp_s72 - 1;
    return;
  }
  if (c3_s80) {
    if (array_success) {
      bool  car_success=0;
      int  r_s82=0;
      car(l_s74, car_success, r_s82);
      success = car_success;
      _out = r_s82;
      return;
    }
    success = 0;
    _out = 0;
    return;
  }
  success = array_success;
  _out = l_s74->s;
  return;
}
void array_expression(Array* a, int d, bool& success, Array*& _out, bool* tape__ANONYMOUS_s102/* len = 143 */, int& tape_index__ANONYMOUS_s103) {
  _out = NULL;
  assertion ((d) > (0));;
  bool  c1_s36=0;
  flip(c1_s36, tape__ANONYMOUS_s102, tape_index__ANONYMOUS_s103);
  if ((d) == (1)) {
    success = 1;
    if (c1_s36) {
      Array*  _out_s38=NULL;
      empty_list(_out_s38);
      _out = _out_s38;
      return;
    } else {
      _out = a;
      return;
    }
  }
  bool  c2_s40=0;
  flip(c2_s40, tape__ANONYMOUS_s102, tape_index__ANONYMOUS_s103);
  Array*  lp_s42=NULL;
  bool  array_success=0;
  array_expression(a, d - 1, array_success, lp_s42, tape__ANONYMOUS_s102, tape_index__ANONYMOUS_s103);
  bool  integer_success=0;
  int  z_s44=0;
  integer_expression(a, d - 1, integer_success, z_s44, tape__ANONYMOUS_s102, tape_index__ANONYMOUS_s103);
  bool  cdr_success=0;
  if ((d) > (2)) {
    bool  c3_s46=0;
    flip(c3_s46, tape__ANONYMOUS_s102, tape_index__ANONYMOUS_s103);
    Guard*  g_s48=NULL;
    bool  guard_success=0;
    guard_expression(a, d - 1, guard_success, g_s48, tape__ANONYMOUS_s102, tape_index__ANONYMOUS_s103);
    if ((c1_s36 && c2_s40) && c3_s46) {
      success = 1;
      Array*  _out_s50=NULL;
      empty_list(_out_s50);
      _out = _out_s50;
      return;
    }
    if ((c1_s36 && c2_s40) && !(c3_s46)) {
      success = 1;
      _out = a;
      return;
    }
    if ((c1_s36 && !(c2_s40)) && c3_s46) {
      if (array_success) {
        Array*  r_s52=NULL;
        cdr(lp_s42, cdr_success, r_s52);
        success = cdr_success;
        _out = r_s52;
        return;
      }
      success = 0;
      _out = lp_s42;
      return;
    }
    if ((c1_s36 && !(c2_s40)) && !(c3_s46)) {
      success = integer_success;
      Array*  _out_s54=NULL;
      singleton(z_s44, _out_s54);
      _out = _out_s54;
      return;
    }
    if ((!(c1_s36) && c2_s40) && c3_s46) {
      success = guard_success && array_success;
      Array*  _out_s56=NULL;
      filter(g_s48, lp_s42, _out_s56);
      _out = _out_s56;
      return;
    }
  } else {
    if (c2_s40 && c1_s36) {
      success = 1;
      Array*  _out_s58=NULL;
      empty_list(_out_s58);
      _out = _out_s58;
      return;
    }
    if (c2_s40 && !(c1_s36)) {
      success = 1;
      _out = a;
      return;
    }
    if (!(c2_s40) && c1_s36) {
      if (array_success) {
        Array*  r_s60=NULL;
        cdr(lp_s42, cdr_success, r_s60);
        success = cdr_success;
        _out = r_s60;
        return;
      }
      success = 0;
      _out = lp_s42;
      return;
    }
    if (!(c2_s40) && !(c1_s36)) {
      success = integer_success;
      Array*  _out_s62=NULL;
      singleton(z_s44, _out_s62);
      _out = _out_s62;
      return;
    }
  }
  assertion (0);;
}
void flip(bool& _out, bool* tape__ANONYMOUS_s83/* len = 143 */, int& tape_index__ANONYMOUS_s84) {
  _out = 0;
  _out = (tape__ANONYMOUS_s83[tape_index__ANONYMOUS_s84]);
  tape_index__ANONYMOUS_s84 = tape_index__ANONYMOUS_s84 + 1;
  return;
}
void run_guard(Guard* g, int z, bool& _out) {
  _out = 0;
  if ((g->o) == (0)) {
    _out = (g->z) == (z);
    return;
  }
  if ((g->o) == (1)) {
    _out = (g->z) > (z);
    return;
  }
  _out = (g->z) < (z);
  return;
}
void concatenate3(Array* a1, Array* a2, Array* a3, Array*& _out) {
  _out = NULL;
  _out = Array::create((a1->s + a2->s) + a3->s, a1->A, a1->s);
  CopyArr<int >((_out->A+ a1->s),a2->A, a2->s, a2->s);
  CopyArr<int >((_out->A+ a2->s + a1->s),a3->A, a3->s, a3->s);
  return;
}
void car(Array* a, bool& success, int& _out) {
  _out = 0;
  success = 1;
  if ((a->s) > (0)) {
    _out = (a->A[0]);
    return;
  }
  success = 0;
  _out = 0;
  return;
}
void empty_list(Array*& _out) {
  _out = NULL;
  _out = Array::create(0, NULL, 0);
  return;
}
void cdr(Array* a, bool& success, Array*& _out) {
  _out = NULL;
  if ((a->s) == (0)) {
    success = 0;
    _out = a;
    return;
  }
  success = 1;
  _out = Array::create(a->s - 1, (a->A+ 1), a->s - 1);
  return;
}
void singleton(int n, Array*& _out) {
  _out = NULL;
  int _tt10[1] = {n};
  _out = Array::create(1, _tt10, 1);
  return;
}
void filter(Guard* g, Array* a, Array*& _out) {
  _out = NULL;
  bool  __sa0=(0) < (a->s);
  int  i=0;
  int  outsz=0;
  int*  out= new int [a->s]; CopyArr<int >(out,0, a->s);
  while (__sa0) {
    bool  _out_s64=0;
    run_guard(g, (a->A[i]), _out_s64);
    if (_out_s64) {
      int  uo_s2=outsz;
      outsz = outsz + 1;
      (out[uo_s2]) = (a->A[i]);
    }
    i = i + 1;
    __sa0 = (i) < (a->s);
  }
  _out = Array::create(outsz, (out+ 0), outsz);
  delete[] out;
  return;
}

}

using namespace ANONYMOUS;
int main(int ac,char **av) {
  
  int n = 6;
  int input[n] = {5,9,2,1,8,3};
  int correct[n] = {1,2,3,5,8,9};
  Array *i;
  constant_array(n,input,i);
  Array *o;

  for (int attempt = 0; attempt < 1000000; attempt++) {
    bool a = false;
    int tape_index = 0;
    bool tape[143]; // = {0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,1,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,1,0,1,0,0,0,0,0,0,0};
    for (int k = 0; k < 143; k++)
      tape[k] = rand()%2 == 0;
    try {
      recursive_expression(i,15,o,tape,tape_index);
    } catch(...) {
      //      cout << "Assertion failure\n";
      a = true;
    }
    if (!a) {
      for (int j = 0; j < o->s; j++) {
	cout << o->A[j] << " ";
	if (j < n && o->A[j] != correct[j]) a = true;
      }
      if (!a && o->s == n) cout << "\tCORRECT";
      cout << "\n";
    }
  }
}
