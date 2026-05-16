% ============================================================
%  logica.pl  —  Motor de Reglas en Prolog
%  Maneja: es_primo, factorial, mcd, es_par
% ============================================================

% ── Es primo ────────────────────────────────────────────────
es_primo(2) :- !.
es_primo(3) :- !.
es_primo(N) :-
    N > 3,
    N mod 2 =\= 0,
    \+ tiene_divisor(N, 3).

tiene_divisor(N, D) :-
    D * D =< N,
    (N mod D =:= 0 ; tiene_divisor(N, D + 2)).

% ── Factorial ───────────────────────────────────────────────
factorial(0, 1) :- !.
factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.

% ── Máximo común divisor (algoritmo de Euclides) ────────────
mcd(X, 0, X) :- X > 0, !.
mcd(X, Y, G) :-
    Y > 0,
    R is X mod Y,
    mcd(Y, R, G).

% ── Es par ──────────────────────────────────────────────────
es_par(N) :- 0 is N mod 2.
