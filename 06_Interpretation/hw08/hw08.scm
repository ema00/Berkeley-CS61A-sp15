; Scheme

(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cddr s))
)

(define (sign x)
  (cond
    ((< x 0) -1)
    ((> x 0) 1)
    (else 0)
  )
)

(define (ordered? s)
  (cond
    ((null? s) true)
    ((null? (cdr s)) true)
    (else (and
            (or
              (< (car s) (cadr s))
              (= (car s) (cadr s))
            )
            (ordered? (cdr s))
          )
    )
  )
)

(define (nodots s)
  (cond
    ((null? s) nil)
    ((and (number? (cdr s)) (pair? (car s))) (list (nodots (car s)) (cdr s)))
    ((pair? (car s)) (cons (nodots (car s)) (cdr s)))
    ((and (pair? s) (number? (cdr s))) (list (car s) (cdr s)))
    (else (cons (car s) (nodots (cdr s))))
  )
)



; Sets as sorted lists

(define (empty? s) (null? s))

(define (contains? s v)
    (cond
      ((empty? s) false)
      ((> (car s) v) false)
      ((= (car s) v) true)
      (else (contains? (cdr s) v))
    )
)

; Equivalent Python code, for your reference:
;
; def empty(s):
;     return s is Link.empty
;
; def contains(s, v):
;     if empty(s):
;         return False
;     elif s.first > v:
;         return False
;     elif s.first == v:
;         return True
;     else:
;         return contains(s.rest, v)

(define (add s v)
    (cond
      ((empty? s) (list v))
      ((< (car s) v) (cons (car s) (add (cdr s) v)))
      ((= (car s) v) (cons v (cdr s)))
      (else (cons v s))
    )
)

(define (intersect s t)
  (cond
    ((or (empty? s) (empty? t)) nil)
    ((= (car s) (car t)) (cons (car s) (intersect (cdr s) (cdr t))))
    ((< (car s) (car t)) (intersect (cdr s) t))
    (else (intersect s (cdr t)))
  )
)

; Equivalent Python code, for your reference:
;
; def intersect(set1, set2):
;     if empty(set1) or empty(set2):
;         return Link.empty
;     else:
;         e1, e2 = set1.first, set2.first
;         if e1 == e2:
;             return Link(e1, intersect(set1.rest, set2.rest))
;         elif e1 < e2:
;             return intersect(set1.rest, set2)
;         elif e2 < e1:
;             return intersect(set1, set2.rest)

(define (union s t)
  (cond
    ((empty? s) t)
    ((empty? t) s)
    ((< (car s) (car t)) (cons (car s) (union (cdr s) t)))
    ((> (car s) (car t)) (cons (car t) (union s (cdr t))))
    (else (cons (car s) (union (cdr s) (cdr t))))
  )
)

; Tail-Calls in Scheme

(define (exp-recursive b n)
  (if (= n 0)
      1
      (* b (exp-recursive b (- n 1)))))

; Tail-Call exp
(define (exp b n)
  (define (exp_tr b n r)
    (if (= n 0)
      r
      (exp_tr b (- n 1) (* r b))
    )
  )
  (exp_tr b n 1)
)

; Tail-Call Filter
(define (filter pred lst)
  (define (filter_tr pred lst res)
    (cond
      ((eq? lst nil) res)
      ((pred (car lst)) (filter_tr pred (cdr lst) (append res (list (car lst)))))
      (else (filter_tr pred (cdr lst) res))
    )
  )
  (filter_tr pred lst nil)
)
