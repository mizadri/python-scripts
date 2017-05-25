# coding: utf-8

lines = []

w1 = '''W1 & \texttt{GemsFDTD},\texttt{equake},\texttt{soplex},\texttt{milc},\texttt{povray},\texttt{bzip2} \\ \hline  %% M17
W2 & \texttt{galgel},\texttt{hmmer},\texttt{soplex},\texttt{lbm},\texttt{fma3d},\texttt{bzip2} \\ \hline  %% M16
W3 & \texttt{galgel},\texttt{equake},\texttt{gamess},\texttt{lbm},\texttt{bzip2},\texttt{astar} \\ \hline  %% M15
W4 & \texttt{twolf},\texttt{bwaves},\texttt{equake},\texttt{soplex},\texttt{astar},\texttt{gobmk} \\ \hline  %% M18
W5 & \texttt{GemsFDTD},\texttt{bwaves},\texttt{equake},\texttt{povray},\texttt{fma3d},\texttt{astar} \\ \hline  %% M14
W6 & \texttt{bwaves},\texttt{equake},\texttt{gamess},\texttt{lbm},\texttt{fma3d},\texttt{bzip2} \\ \hline  %% M13
W7 & \texttt{GemsFDTD},\texttt{applu},\texttt{perlbmk},\texttt{sixtrack},\texttt{astar},\texttt{gzip} \\ \hline  %% M12
W8 & \texttt{bwaves},\texttt{perlbmk},\texttt{povray},\texttt{fma3d},\texttt{astar},\texttt{gzip} \\ \hline  %% M11
W9 & \texttt{galgel},\texttt{perlbmk},\texttt{sixtrack},\texttt{mgrid},\texttt{astar},\texttt{libquantum} \\ \hline  %% M10
W10 & \texttt{GemsFDTD},\texttt{vortex},\texttt{perlbmk},\texttt{fma3d},\texttt{astar},\texttt{gzip} \\ \hline  %% M9
W11 & \texttt{bzip2},\texttt{equake},\texttt{hmmer},\texttt{vortex},\texttt{crafty},\texttt{astar} \\ \hline  %% M8
W12 & \texttt{gamess},\texttt{hmmer},\texttt{soplex},\texttt{art},\texttt{astar},\texttt{gzip} \\ \hline  %% M7'''
for l in w1.split('\n'):
    lines.append(l)
    
    
w2 = '''W13 & \texttt{GemsFDTD},\texttt{bwaves},\texttt{gamess},\texttt{hmmer},\texttt{crafty},\texttt{astar} \\ \hline  %% M6
W14 & \texttt{bzip2},\texttt{bwaves},\texttt{hmmer},\texttt{lucas},\texttt{gobmk},\texttt{gzip} \\ \hline  %% M5
%W15 & \texttt{hmmer},\texttt{soplex},\texttt{art},\texttt{lbm},\texttt{fma3d},\texttt{gobmk} \\ \hline  %% M4
W15 & \texttt{soplex},\texttt{art},\texttt{vortex},\texttt{lbm},\texttt{fma3d},\texttt{gobmk} \\ \hline  %% M4
W16 & \texttt{galgel},\texttt{equake},\texttt{hmmer},\texttt{lbm},\texttt{fma3d},\texttt{h264ref} \\ \hline  %% M3
W17 & \texttt{bwaves},\texttt{equake},\texttt{gamess},\texttt{povray},\texttt{astar},\texttt{libquantum} \\ \hline  %% M2
W18 & \texttt{GemsFDTD},\texttt{galgel},\texttt{gamess},\texttt{hmmer},\texttt{astar},\texttt{libquantum} \\ \hline  %% M1
W19 & \texttt{swim},\texttt{mcf},\texttt{perlbench},\texttt{h264ref},\texttt{gobmk},\texttt{gzip} \\ \hline  %% W36
W20 & \texttt{galgel},\texttt{equake},\texttt{hmmer},\texttt{povray},\texttt{mgrid},\texttt{gobmk} \\ \hline  %% W39
W21 & \texttt{galgel},\texttt{equake},\texttt{hmmer},\texttt{bzip2},\texttt{perlbench},\texttt{h264ref} \\ \hline  %% W3
W22 & \texttt{galgel},\texttt{equake},\texttt{gamess},\texttt{hmmer},\texttt{sixtrack},\texttt{povray} \\ \hline  %% W34
W23 & \texttt{gamess},\texttt{art},\texttt{bzip2},\texttt{gobmk},\texttt{sixtrack},\texttt{vortex} \\ \hline  %% W25
W24 & \texttt{galgel},\texttt{gamess},\texttt{hmmer},\texttt{povray},\texttt{perlbench},\texttt{gobmk} \\ \hline  %% W31'''
for l in w2.split('\n'):
    lines.append(l)
    

benchs = {}
for l in lines:
    i = 0
    for bench in l.split("{"):
        if i > 0:
            name = bench.split("}")[0]
            if name not in benchs:
                benchs[name] = 1
            else:
                benchs[name] += 1
        i += 1
print benchs
