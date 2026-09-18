# QA2 report MLA-C01 (doble revision rigurosa con verificacion docs AWS)

- Revisadas A: 73/112  |  B: 73/112
- Desacuerdos A vs B: 2 (mla01-q20, mla02-q1)
- P0=0 P1=2 P2=9 OK=62
- TOTAL a corregir (P0+P1+P2): 11


## P1 (2)

### mla01-q21c  (A=FIX/3 B=FIX/3)
- respuesta_deberia_ser: TVD (correcta dentro del set porque KS no se ofrece), pero reescribir verdict/exam-tip: TVD mide medio de la diferencia L1 entre distribuciones y es la mejor opcion disponible; la etiqueta 'maxima divergencia/disparidad' corresponde a Kolmogorov-Smirnov (KS), que aqui no figura.
- [med/A] ?: Afirmacion imprecisa: presenta TVD como la metrica de 'maxima disparidad/divergencia entre distribuciones'; la doc oficial de Clarify asigna 'maximum divergence' a Kolmogorov-Smirnov (KS). TVD = medio de la diferencia L1.
- [med/A] ?: El exam-tip refuerza esa asociacion incorrecta y deberia reescribirse para no ensenar el concepto erroneo.
- [med/B] ?: El enunciado, refutaciones y tip equiparan TVD con 'maxima divergencia/maxima disparidad', definicion que AWS Clarify asigna a Kolmogorov-Smirnov (KS). TVD = mitad de la diferencia de norma L1 entre distribuciones. Recomendacion: reformular a 'TVD mide la diferencia (distancia L1/2) entre las distribuciones de resultados por grupo; entre las opciones dadas es la unica metrica de distancia de distribuciones' y evitar el termino 'maxima divergencia' (propio de KS). La respuesta seleccionada (TVD) sigue siendo la mejor entre las 4 opciones.

### mla02-q1  (A=PASS/5 B=FIX/3)
- [med/B] ?: Contradiccion interna (sev med): el cuerpo argumenta que Precision > FPR para medir falsos positivos, socavando la opcion marcada (FPR+F1).
- [med/B] ?: El matiz aproxima el distractor 'Precision+Accuracy' a la correctitud percibida, restando limpieza a la discriminacion entre opciones.
- [med/B] ?: Recomendacion: reescribir el 'Matiz importante' para que no eleve la Precision por encima del FPR; enmarcar FPR y Precision como complementarias y justificar el par de la fuente por combinar acotacion de FP (FPR) con balance Precision-Recall (F1).


## P2 (9)

### mla01-q1b  (A=PASS/4 B=PASS/5)

### mla01-q20  (A=PASS/5 B=FIX/4)
- [med/B] ?: Refutacion de FSx for Lustre lo tacha de 'efimero' en absoluto; FSx for Lustre ofrece despliegues persistentes (PERSISTENT_1/2) y scratch. Mejor: 'no es un object store durable de bajo costo pensado como base de data lake' sin afirmar que es efimero.

### mla01-q21a  (A=PASS/5 B=PASS/5)
- [med/A] ?: Nota menor: Clarify ya no admite nuevos clientes (doc), pero las definiciones y el temario MLA-C01 siguen vigentes; no es defecto de la carta.

### mla01-q37  (A=PASS/5 B=PASS/4)
- [med/B] ?: Kendall vs Spearman es una distincion de convencion/uso mas que de correccion estricta; el enunciado necesita el ancla 'muestra grande / mas usado por defecto' para que Spearman sea inequivocamente mejor que Kendall. Ya esta anclado, por eso PASS, pero por eso score 4 y no 5.

### mla01-q5  (A=PASS/5 B=PASS/5)

### mla01-q8  (A=PASS/5 B=PASS/5)

### mla02-q13  (A=PASS/5 B=PASS/5)

### mla02-q23  (A=PASS/5 B=PASS/4)
- [med/B] ?: Herencia de la fuente: la premisa 'interface endpoint por cross-region' es debil; la carta la mitiga con nota explicita, no corrige el enunciado base. No bloqueante.

### mla02-q29  (A=PASS/5 B=PASS/4)
- [med/B] ?: El distractor con Especificidad/AUC-ROC usa metricas que si son de clasificacion; la unicidad de la correcta descansa en 'cuarteto especifico pedido' mas que en invalidez. Mitigado por la nota honesta de la carta; no bloqueante.
