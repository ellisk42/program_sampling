// working
if (problemNumber == 1) {
  if (EXAMPLE1)
    testCase("My name is John.", 	"John");
  if (EXAMPLE2)
    testCase("My name is Bill.", 	"Bill");
  if (EXAMPLE3)
    testCase("My name is May.", 	"May");
  if (EXAMPLE4)
    testCase("My name is Mary.", 	"Mary");
  if (EXAMPLE5)
    testCase("My name is Josh.", 	"Josh");
 }
// working
if (problemNumber == 2) {
  if (EXAMPLE1)
    testCase("james", 	"james.");
  if (EXAMPLE2)
    testCase("charles", 	"charles.");
  if (EXAMPLE3)
    testCase("thomas", 	"thomas.");
  if (EXAMPLE4)
    testCase("paul", 	"paul.");
  if (EXAMPLE5)
    testCase("chris", 	"chris.");
 }
// working
if (problemNumber == 3) {
  if (EXAMPLE1)
    testCase("don steve g.","dsg");
  if (EXAMPLE2)
    testCase("Kev Jason Mat","KJM");
  if (EXAMPLE3)
    testCase("Jose Larry S","JLS");
  if (EXAMPLE4)
    testCase("Art Joe Juan","AJJ");
  if (EXAMPLE5)
    testCase("Ray F. Timothy","RFT");
 }
// working
if (problemNumber == 4) {
  if (EXAMPLE1)
    testCase("brent.hard@ho","brent hard");
  if (EXAMPLE2)
    testCase("matt.ra@yaho","matt ra");
  if (EXAMPLE3)
    testCase("jim.james@har","jim james");
  if (EXAMPLE4)
    testCase("ruby.clint@g","ruby clint");
  if (EXAMPLE5)
    testCase("josh.smith@g","josh smith");
 }
	
if (problemNumber == 5) {
  if (EXAMPLE1)
    testCase("John DOE 3 Data [TS]865-000-0000 - - 453442-00 06-23-2009","865-000-0000");
  if (EXAMPLE2)
    testCase("A FF MARILYN 30’S 865-000-0030 - 4535871-00 07-07-2009","865-000-0030");
  if (EXAMPLE3)
    testCase("A GEDA-MARY 100MG 865-001-0020 - - 5941-00 06-23-2009","865-001-0020");
  if (EXAMPLE4)
    testCase("Sue DME 42 [ST]865-003-0100 -- 5555-99 08-22-2010","865-003-0100");
  if (EXAMPLE5)
    testCase("Edna DEECS [SSID] 865-001-0003 --23954-11 09-01-2010","865-001-0003");
 }
// won't work with current implementation
if (problemNumber == 6) {
  if (EXAMPLE1)
    testCase("Company\\Code\\index.html","Company\\Code\\");
  if (EXAMPLE2)
    testCase("Company\\Docs\\Spec\\specs.doc","Company\\Docs\\Spec\\");
  if (EXAMPLE3)
    testCase("Work\\Presentations\\talk.ppt","Work\\Presentations\\");
  if (EXAMPLE4)
    testCase("Work\\Records\\2010\\January.dat","Work\\Records\\2010\\");
  if (EXAMPLE5)
    testCase("Proj\\Numerical\\Simulators\\NBody\\nbody.c","Proj\\Numerical\\Simulators\\NBody\\");
 }
// an example of ambiguity
if (problemNumber == 7) {
  if (EXAMPLE1)
    testCase("hi","hi hi");
  if (EXAMPLE2)
    testCase("bye","hi bye");
  if (EXAMPLE3)
    testCase("adios","hi adios");
  if (EXAMPLE4)
    testCase("joe","hi joe");
  if (EXAMPLE5)
    testCase("icml","hi icml");
 }
// working
if (problemNumber == 8) {
  if (EXAMPLE1)
    testCase("Oege de Moor","Oege de Moor");
  if (EXAMPLE2)
    testCase("Kathleen Fisher AT&T Labs","Kathleen Fisher AT&T Labs");
  if (EXAMPLE3)
    testCase("Microsoft Research","Microsoft Research");
  if (EXAMPLE4)
    testCase("John Morse Institute","John Morse Institute");
  if (EXAMPLE5)
    testCase("Jennifer Smith Law Firm","Jennifer Smith Law Firm");
 }
// working
if (problemNumber == 9) {
  if (EXAMPLE1)
    testCase("1/21/2001","01");
  if (EXAMPLE2)
    testCase("22.02.2002","02");
  if (EXAMPLE3)
    testCase("2003-23-03","03");
  if (EXAMPLE4)
    testCase("21/1/2001","01");
  if (EXAMPLE5)
    testCase("5/5/1987","87");
 }
// working
if (problemNumber == 10) {
  if (EXAMPLE1)
    testCase("Eyal Dechter","Dechter, Eyal");
  if (EXAMPLE2)
    testCase("Joshua Tenenbaum","Tenenbaum, Joshua");
  if (EXAMPLE3)
    testCase("Stephen Muggleton","Muggleton, Stephen");
  if (EXAMPLE4)
    testCase("Kevin Ellis","Ellis, Kevin");
  if (EXAMPLE5)
    testCase("Dianhuan Lin","Lin, Dianhuan");
 }
// working
if (problemNumber == 11) {
  if (EXAMPLE1)
    testCase("12/31/13","12.31");
  if (EXAMPLE2)
    testCase("1/23/2009","1.23");
  if (EXAMPLE3)
    testCase("4/12/2023","4.12");
  if (EXAMPLE4)
    testCase("6/23/15","6.23");
  if (EXAMPLE5)
    testCase("7/15/2015","7.15");
 }
// not working and I don't understand why
if (problemNumber == 12) {
  if (EXAMPLE1)
    testCase("Three <2: vincent> Jeff","(2: vincent)");
  if (EXAMPLE2)
    testCase("Don Kyle <3: ricky> virgil","(3: ricky)");
  if (EXAMPLE3)
    testCase("herbert is <2: marion> morris","(2: marion)");
  if (EXAMPLE4)
    testCase("fransisco eduardo <1: apple trees>","(1: apple trees)");
  if (EXAMPLE5)
    testCase("country music <9: refrigerator>","(9: refrigerator)");
 }
// not working
if (problemNumber == 13) {
  if (EXAMPLE1)
    testCase("3113 Greenfield Ave., Los Angeles, CA 90034","Los Angeles");
  if (EXAMPLE2)
    testCase("43 St. Margaret St. #1, Dorchester, MA 02125","Dorchester");
  if (EXAMPLE3)
    testCase("43 Vassar St. 46-4053, Cambridge, MA 02139","Cambridge");
  if (EXAMPLE4)
    testCase("47 Foskett St. #2, Cambridge, MA 02144","Cambridge");
  if (EXAMPLE5)
    testCase("3 Ames St., Portland, OR 02142","Portland");
 }

// working
if (problemNumber == 14) {
  if (EXAMPLE1)
    testCase("Verlene Ottley  ","V.O");
  if (EXAMPLE2)
    testCase("Oma Cornelison  ","O.C");
  if (EXAMPLE3)
    testCase("Marin Lorentzen  ","M.L");
  if (EXAMPLE4)
    testCase("Annita Nicely  ","A.N");
  if (EXAMPLE5)
    testCase("Joanie Faas  ","J.F");
 }
// working
if (problemNumber == 15) {
  if (EXAMPLE1)
    testCase("Agripina Kuehner  ","Hi Agripina!");
  if (EXAMPLE2)
    testCase("Brittany Alarcon  ","Hi Brittany!");
  if (EXAMPLE3)
    testCase("Adelia Swindell  ","Hi Adelia!");
  if (EXAMPLE4)
    testCase("Marcie Michalak  ","Hi Marcie!");
  if (EXAMPLE5)
    testCase("Eugena Eurich  ","Hi Eugena!");
 }

// working
if (problemNumber == 16) {
  if (EXAMPLE1)
    testCase("#include <stdio.h>","stdio");
  if (EXAMPLE2)
    testCase("#include <malloc.h>","malloc");
  if (EXAMPLE3)
    testCase("#include <stdlib.h>","stdlib");
  if (EXAMPLE4)
    testCase("#include <sys.h>","sys");
  if (EXAMPLE5)
    testCase("#include <os.h>","os");
 }
// working
if (problemNumber == 17) {
  if (EXAMPLE1)
    testCase("aa",	   "aaa");
  if (EXAMPLE2)
    testCase("abc",	   "abcc");
  if (EXAMPLE3)
    testCase("xyz",	   "xyzz");
  if (EXAMPLE4)
    testCase("4",	   "44");
  if (EXAMPLE5)
    testCase("john",   "johnn");
 }
// working with the large array bounds
if (problemNumber == 18) {
  if (EXAMPLE1)
    testCase("3113 Greenfield Ave., LA, CA 90034",	"3113");
  if (EXAMPLE2)
    testCase("43 St. Margaret St. #1, Dorchester, MA 02125","43");
  if (EXAMPLE3)
    testCase("43 Vassar St. 46-4053, Cambridge, MA 02139",	"43");
  if (EXAMPLE4)
    testCase("47 Foskett St. #2, Cambridge, MA 02144",	"47");
  if (EXAMPLE5)
    testCase("3 Ames St., Portland, OR 02142", 		"3");
 }
// working
if (problemNumber == 19) {
  if (EXAMPLE1)
    testCase("aa",	   "aaaa");
  if (EXAMPLE2)
    testCase("abc",	   "abcabc");
  if (EXAMPLE3)
    testCase("xyz",	   "xyzxyz");
  if (EXAMPLE4)
    testCase("4",	   "44");
  if (EXAMPLE5)
    testCase("john",   "johnjohn");
 }
