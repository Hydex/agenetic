The process for the ANN works as follows:

9  INPUT
4  HIDDEN
6  OUTPUT


|W11 W12 W13 W14 W15 W16 W17 W18 W19| |I1|  =  |N1|
|W21 W22 W23 W24 W25 W26 W27 W28 W29| |I2|     |N2|
|W31 W32 W33 W34 W35 W36 W37 W38 W39| |I3|     |N3|
|W41 W42 W43 W44 W45 W46 W47 W48 W49| |I4|     |N4|
                                      |I5|
                                      |I6|
                                      |I7|
                                      |I8|
                                      |I9|

[ INPUT x HIDDEN ]



| T1 0  0  0  | |N1|  =  |H1|
| 0  T2 0  0  | |N2|     |H2|
| 0  0  T3 0  | |N3|     |H3|
| 0  0  0  T4 | |N4|     |H4|

[ HIDDEN as identity ]



|w11 w12 w13 w14| |H1|  =  |n1|
|w21 w22 w23 w24| |H2|     |n2|
|w31 w32 w33 w34| |H3|     |n3|
|w41 w42 w43 w44| |H4|     |n4|
|w51 w52 w53 w54|          |n5|
|w61 w62 w63 w64|          |n6|

[ HIDDEN x OUTPUT ]



| t1 0  0  0  0  0  | |n1|  =  |h1|
| 0  t2 0  0  0  0  | |n2|     |h2|
| 0  0  t3 0  0  0  | |n3|     |h3|
| 0  0  0  t4 0  0  | |n4|     |h4|
| 0  0  0  0  t5 0  | |n5|     |h1|
| 0  0  0  0  0  t6 | |n6|     |h2|

[ OUTPUT as identity ]
