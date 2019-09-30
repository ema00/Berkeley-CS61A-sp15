;; Scheme ;;
(define (accumulate combiner start n term)
  (if (= n 0)
      start
      (accumulate combiner (combiner start (term n)) (- n 1) term)
  )
)

;;; Tests
(define (identity x) x)
(accumulate * 1 5 identity)
; expect 120

(define (square x) (* x x))
(accumulate + 0 5 square)
; expect 55



(define (how-many-dotsX s)
  (cond
    ((null? s) 0)
    ((number? s) 1)
    ((and (pair? (car s)) (number? (cdr s))) (+ 1 (how-many-dots (cdr s))))
    (else (how-many-dots (cdr s)))
  )
)

(define (how-many-dots s)
  (cond
    ((null? s) 0)
    ((number? s) 1)
    ((pair? (car s)) (+ (how-many-dots (car s)) (how-many-dots (cdr s))))
    (else (how-many-dots (cdr s)))
  )
)

;;; Tests

(how-many-dots '(1 2 3))
; expect 0
(how-many-dots '(1 2 . 3))
; expect 1
(how-many-dots '((1 . 2) 3 . 4))
; expect 2
(how-many-dots '((((((1 . 2) . 3) . 4) . 5) . 6) . 7))
; expect 6
(how-many-dots '(1 . (2 . (3 . (4 . (5 . (6 . (7))))))))
; expect 0



(define (swap s)
  (define (swapt s r)
    (cond
      ((null? s) r)
      ((null? (cdr s)) (cons (car s) r))
      (else (swapt (cdr (cdr s)) (cons (car s) (cons (car (cdr s)) r))))
    )
  )
  (define (reverse s r)
    (if (null? s)
      r
      (reverse (cdr s) (cons (car s) r))
    )
  )

  (reverse (swapt s nil) nil)
)

;;; Tests

(swap (list 1 2 3 4))
; expect (2 1 4 3)
(swap (list 1 2 3 4 5))
; expect (2 1 4 3 5)
