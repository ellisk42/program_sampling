#include <stdio.h>
#include <stdlib.h>

typedef unsigned int word;
#define WSIZE (8*sizeof(word))

typedef struct pMatrix {
  size_t m, n, nsz;
   /* nsz = (n + WSIZE-1)/WSIZE */
  word **data;
} pMatrix;

pMatrix *create_pMatrix(size_t m, size_t n);
void free_pMatrix(pMatrix *pm);
void pack_matrix(int *data, pMatrix *pm);
size_t calculate_rank(pMatrix *primal);

int main() {
  // read matrix from standard input
  int r,c;
  scanf("%d",&r);
  scanf("%d",&c);

  if (r > c) {
    printf("ERROR: input must have fewer rows and columns\n");
    return 2;
  }

  int *data = malloc(sizeof(int)*r*c);
  for (int j = 0; j < r*c; j++) {
    scanf("%d",data+j);
    if (data[j] != 0 && data[j] != 1) {
      printf("ERROR: matrix not binary\n");
      return 1;
    }
  }
  
  /*int data[16] = {1,     1,     0,//     0,
		  1,     1,     0,//     0,
		  0,     0,     1,//     0,
		  0,     0,     0}; //,     1};*/

  pMatrix *pm = create_pMatrix(r,c);
  pack_matrix(data,pm);
  printf("%d\n",(int)calculate_rank(pm));
  return 0;
}
/*
void mexFunction(int nlhs, mxArray *plhs[],
    int nrhs, const mxArray *prhs[])
{
  pMatrix *primal;
  size_t k, n;

  if (nrhs != 1 || nlhs > 1) {
    mexErrMsgTxt("Usage: [rank] = RankMod2(matrix)");
  }

  if (!mxIsLogical(prhs[0]) || mxGetNumberOfDimensions(prhs[0]) != 2) {
    mexErrMsgTxt("Usage: input must be a logical matrix");
  }

  k = mxGetM(prhs[0]);
  n = mxGetN(prhs[0]);
  if (k > n) {
    mxErrMsgTxt("Usage: input must have fewer rows than columns");
    // case where rows is greater than columns
    // k = rows
    // n = columns
  }

  if ((primal = create_pMatrix(k, n)) == NULL) {
    mxErrMsgTxt("Out of memory creating pMatrix");
  }
  pack_matrix(mxGetLogicals(prhs[0]), primal);

  plhs[0] = mxCreateDoubleScalar(calculate_rank(primal));

  free_pMatrix(primal);
}
*/
pMatrix *create_pMatrix(size_t m, size_t n)
  /* create a packed matrix object on the heap */
{
  pMatrix *pm;
  size_t i;

  if ((pm = (pMatrix *)malloc(sizeof(pMatrix))) == NULL)
    return NULL;

  pm->m = m, pm->n = n, pm->nsz = (pm->n + WSIZE-1)/WSIZE;

  if ((pm->data = (word **)calloc(m, sizeof(word *))) == NULL) {
    free(pm);
    return NULL;
  }

  for (i = 0; i < m; ++i) {
    if ((pm->data[i] = (word *)calloc(n, sizeof(word *))) == NULL) {
      size_t j;
      for (j = 0; j < i; ++j)
	free(pm->data[j]);
      free(pm->data); free(pm);
      return NULL;
    }
  }

  return pm;
}

void free_pMatrix(pMatrix *pm)
  /* delete a packed matrix object */
{
  size_t i;

  for (i = 0; i < pm->m; ++i)
    free(pm->data[i]);
  free(pm->data); free(pm);
}

void pack_matrix(int *data, pMatrix *pm)
  /* converts a logical array into a packed boolean format.
   * Note that Matlab stores matrices by columns */
{
  size_t i, j;
  word jm;

  for (j = 0, jm = 1; j < pm->n; ++j%WSIZE ? (jm <<= 1): (jm = 1))
    for (i = 0; i < pm->m; ++i)
      if (*data++)
	pm->data[i][j/WSIZE] |= jm;
}

void xor(word *src, word *dst, size_t n);

size_t calculate_rank(pMatrix *primal)
  /* Implements the first phase of Gaussian elimination to calculate the
   * rank.
   */
{
  size_t i, j, k;
  word jm;
  word **p, *q;

  p = primal->data;

  for (i = j = 0, jm = 1;
      i < primal->m && j < primal->n;
      ++j % WSIZE ? (jm <<= 1): (jm = 1))
  {
    /* look for a pivot element */
    for (k = i; k < primal->m; ++k)
      if (p[k][j/WSIZE] & jm)
	break;
    if (k == primal->m)
      /* entire column is zero: this means that this column will
       * correspond to a free variable (or, in coding parlance, a
       * message bit) in the dual */
      continue;

    /* swap rows if we have to */
    if (i != k)
      q = p[i], p[i] = p[k], p[k] = q;
    else
      k = i+1;

    /* eliminate the rest of the column */
    while (k < primal->m) {
      if (p[k][j/WSIZE] & jm)
	xor(&p[i][j/WSIZE], &p[k][j/WSIZE], primal->nsz-j/WSIZE);
      ++k;
    }

    ++i;
  }
  return i;
}

void xor(word *src, word *dst, size_t n)
  /* add the src to the dst mod 2 */
{
  while (n-- > 0)
    *dst++ ^= *src++;
}
