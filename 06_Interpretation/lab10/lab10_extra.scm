;; Extra Scheme Questions ;;

; Q6
(define (filter f lst)
  (if (null? lst)
    nil
    (if (f (car lst))
      (cons (car lst) (filter f (cdr lst)))
      (filter f (cdr lst)))
  )
)

(define (remove item lst)
  (filter (lambda (x) (not (= x item))) lst)
)


;;; Tests
(remove 3 nil)
; expect ()
(remove 3 '(1 3 5))
; expect (1 5)
(remove 5 '(5 3 5 5 1 4 5 4))
; expect (3 1 4 4)


; Q7
(define (composed f g)
  (lambda (x) (f (g x)))
)


; Q8
(define (max a b) (if (> a b) a b))
(define (min a b) (if (> a b) b a))
(define (gcd a b)
  (cond
    ((= b 0) a)
    ((= (modulo a b) 0) b)
    (else (gcd b (modulo a b)))
  )
)

;;; Tests
(gcd 24 60)
; expect 12
(gcd 1071 462)
; expect 21


; Q9
(define (split-at lst n)
  (cond
    ((null? lst) nil)
    ((= n 0) nil)
    (else (cons (car lst) (split-at (cdr lst) (- n 1))))
  )
)
; ESTE NO FUNCIONA
