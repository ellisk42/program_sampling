#! /usr/bin/guile -s
!#

(define lt (lambda (x)
	     (lambda (y)
	       (<= x y))))
(define gt (lambda (x)
	     (lambda (y)
	       (>= x y))))
(define eq (lambda (x)
	     (lambda (y)
	       (= x y))))
(define nil '())
(define filter (lambda (f l)
		 (if (null? l)
		     l
		     (if (f (car l))
			 (cons (car l)
			       (filter f (cdr l)))
			 (filter f (cdr l))))))
(define (p1 x) (+ 1 x))
(define (m1 x) (- x 1))

(define argument (call-with-input-string (caddr (command-line))
					 read))
(define body (call-with-input-string (cadr (command-line))
				     read))
(write (eval
	`(letrec ((recur (lambda (a)
			   ,body)))
	   (recur ,argument))
	(interaction-environment)))
(newline)
