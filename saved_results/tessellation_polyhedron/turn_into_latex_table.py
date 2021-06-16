import os
tesspoly_order = ['tetrahedron', 'cube', 'octahedron', 'icosahedron', 'hexagonal_antiprism', 'j1', 'j8', 'j10', 'j12', 'j13', 'j14', 'j15', 'j16', 'j17', 'j49', 'j50', 'j51', 'j84', 'j86', 'j87', 'j88', 'j89', 'j90']

imagename_order = [None]*len(tesspoly_order)

for dirpath, dirnames, filenames in os.walk("./"):
    for name in filenames:
            if name.endswith((".png")):
                # name=basename(name)
                for index, polyname in enumerate(tesspoly_order):
                    if(polyname+"@" in name):
                        if("partial" in name):
                            imagename_order[index]="rolls/newrolls/partial/"+name
                        elif("total" in name):
                            imagename_order[index]="rolls/newrolls/total/"+name

output = """
\makegapedcells 
\\begin{xltabular}{\columnwidth}{|X|X|X|X|}
\hline 
\label{tab:tesspolytable} Tessellation Polyhedron & Roll Type & CFO adjacency & Preview (clickable)

 
"""

for index,imagename in enumerate(imagename_order):
    polyname = tesspoly_order[index]
    output += "\hypertarget{TPtable%i}{  } \\\\  \\hline \n"%index
    output += """%s & %s 
    & \\raisebox{-.5\\height}{\\includegraphics[height=50pt]{rolls/newrolls/tesspoly_CFO_adjacency_matrices/%s}}
    & \\hyperlink{appendix:TPx%i}{\\raisebox{-.5\\height}{\\includegraphics[height=50pt]{%s}}}\n"""\
    %(polyname.replace("_"," ").capitalize(),"\\band" if "partial" in imagename else "\cover", polyname, index, imagename)

output += """\\\\  \\hline
\end{xltabular}


\printbibliography
\part{Annex}
\\begin{appendices}

Back to table \\autoref{tab:tesspolytable}
"""

for index,imagename in enumerate(imagename_order):
    polyname = tesspoly_order[index]
    output += """
\\begin{figure}[ht]
    \hypertarget{appendix:TPx%i}{  }
    \caption{%s}
    \centering
    \includegraphics[width=\columnwidth]{%s}\\\\
    Back to \hyperlink{TPtable%i}{table entry}
\end{figure}

"""%(index,polyname.replace("_"," ").capitalize(),imagename,index)

output+="""


\end{appendices}
\end{document}
"""

with open("latexoutput.txt","w") as f:
    f.write(output)