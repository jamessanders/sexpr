(define input (lambda (msg)
                (print msg)
                (getchar)))

(define test (lambda ()
               (define x (input "Enter a number: "))
               (define y (input "Enter another number: "))
               (print 
                 (concat "Add them together and you get: " 
                   (str (+ x y))))))


(define sqr (lambda (a) (* a a)))

(map sqr (range 0 100))

(if (exist? x)
  (print "x is defined")
  (print "x is not defined"))


