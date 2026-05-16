;;; ============================================================
;;;  calculos.lisp  —  Motor de Cálculo en Common Lisp
;;;  Maneja: operaciones aritméticas, potencia, raíz, logaritmo
;;; ============================================================

;; Suma de lista de números (estilo Lisp funcional)
(defun suma-lista (lst)
  (reduce #'+ lst :initial-value 0))

;; Producto de lista de números
(defun producto-lista (lst)
  (reduce #'* lst :initial-value 1))

;; Potencia entera eficiente (exponenciación rápida)
(defun potencia-rapida (base exp)
  (cond
    ((= exp 0) 1)
    ((evenp exp)
     (let ((mitad (potencia-rapida base (/ exp 2))))
       (* mitad mitad)))
    (t (* base (potencia-rapida base (- exp 1))))))

;; Raíz cuadrada con validación
(defun raiz-segura (n)
  (if (< n 0)
      (error "Raíz de número negativo")
      (sqrt (float n))))

;; Logaritmo natural con validación
(defun log-seguro (n)
  (if (<= n 0)
      (error "Logaritmo de número no positivo")
      (log (float n))))

;; Redondear a N decimales
(defun redondear (n decimales)
  (let ((factor (expt 10 decimales)))
    (/ (round (* n factor)) (float factor))))
