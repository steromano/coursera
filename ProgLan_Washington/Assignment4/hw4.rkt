
#lang racket

(provide (all-defined-out)) ;; so we can put tests in a second file

;; put your code below

(define (sequence low high stride)
  (define (helper sofar next)
    (if (> next high)
        sofar
        (helper (append sofar (list next)) (+ next stride))))
  (helper null low))

(define (string-append-map xs suffix)
  (map (lambda (s) (string-append s suffix)) xs))

(define (list-nth-mod xs n)
  (cond [(< n 0) (error "list-nth-mod: negative number")]
        [(null? xs) (error "list-nth-mod: empty list")]
        [#t (let* ([l (length xs)]
                   [i (remainder n l)])
              (car (list-tail xs i)))]))

(define (stream-for-n-steps s n)
  (define pr (s))
  (if (= n 0)
      null
      (cons (car pr) (stream-for-n-steps (cdr pr) (- n 1)))))

(define (funny-number-stream)
  (define (gen n) (cons (if (= (remainder n 5) 0) (- n) n)
                        (lambda () (gen (+ n 1)))))
  (gen 1))

(define (dan-then-dog)
  (cons "dan.jpg" (lambda () (cons "dog.jpg" dan-then-dog))))

(define (stream-add-zero s)
  (define pr (s))
  (lambda () (cons (cons 0 (car pr)) (stream-add-zero (cdr pr)))))

(define (cycle-lists xs ys)
  (define (gen n) (cons (cons (list-nth-mod xs n) (list-nth-mod ys n))
                        (lambda () (gen (+ n 1)))))
  (lambda () (gen 0)))

(define (vector-assoc v vec)
  (define (loop i)
    (if (= i (vector-length vec))
        #f
        (let ([el (vector-ref vec i)])
          (if (and (pair? el) (equal? (car el) v))
              el
              (loop (+ i 1))))))
  (loop 0))

(define (cached-assoc xs n)
  (let ([cache (make-vector n #f)]
        [i 0])
    (lambda (v) 
      (define cached (vector-assoc v cache))
      (if cached
          cached
          (let ([ans (assoc v xs)])
            (if ans
                (begin (vector-set! cache i ans)
                       (set! i (if (= i (- n 1)) 0 (+ i 1)))
                       ans)
                ans))))))
    
 

  

                

