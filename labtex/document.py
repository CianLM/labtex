from labtex.linear import LinearRegression
from labtex.measurementlist import MeasurementList

from typing import List, Union

import os

class Document:
    "A class for LaTeX template document creation with tables and graphs already inserted."
        # Customise these folders and the templates as you wish.
    texfolder = "tex/"
    graphfolder = "figures/"

    template = r"""\documentclass[]{article}

\title{!title}
\author{!author}

\usepackage{amsmath,amssymb,amsfonts,amsthm,physics,graphicx,geometry,enumitem,booktabs}

\begin{document}

\maketitle

\abstract{

}

\section{Introduction}

\section{Theory}

\section{Method}

\section{Results}

!table

\section{Data Analysis}

!graph

\section{Discussion}

\section*{References}

\end{document}
"""


    tabletemplates = {
        "default": r"""
\begin{table}[ht]
    \centering
    \caption{!caption}
    \label{tab:!tablenumber}
    \begin{tabular}{!columns}
        \toprule
        !data
        \bottomrule
    \end{tabular}
\end{table}

!table
"""
    }

    graphtemplates = {
        "default": r"""
\begin{figure}[ht]
    \centering
    \includegraphics[width=!width\textwidth]{!filename.png}
    \caption{!caption}
    \label{fig:!graphnumber}
\end{figure}
!graph
"""
    }
    
    def __init__(self,title : str,author : str):
        "Initialise a LaTeX document with an title and an author."

        self.document = Document.template.replace("!title",title).replace("!author",author)
        self.tablenumber = 0
        self.graphnumber = 0

    def __repr__(self):
        return self.document

    def table(self,nameandsymbol : List[str], data : List[MeasurementList], \
        headers :List[str] = [], caption : str = "",style : str = "sideways"):
        """
        Add a table to the LaTeX document. 
        """
        assert len(nameandsymbol) == len(data)
        assert all(len(data[0]) == len(line) for line in data)
        columns = len(data[0])

        table = Document.tabletemplates["default"]
        self.tablenumber += 1

        table = table.replace("!tablenumber", str(self.tablenumber))
        table = table.replace("!caption",caption)

        if not (all(isinstance(line, MeasurementList) for line in data)):
            raise Exception("Data Error: Data should be a list of Measurement Lists.")

        if(style == "sideways"):
            # table = table.replace("!columns", "*{" + str(1+columns) + "}c" )
            table = table.replace("!columns", f"c|{ 'c' * columns}" )
            if(headers != []):
                table = table.replace("!data",
                fr"""{headers[0]} & \multicolumn{{{columns}}}{{c}}{{{headers[1]}}} \\
            \midrule !data"""
                )
            for i in range(len(data)):
                table = table.replace("!data",
                fr"""
            {nameandsymbol[i]}{ data[i].tableprint() } \\ !data"""
                )

        elif(style == "upright"):
            table = table.replace("!columns", "*{" + str(len(data)) + "}c" )
            for i in range(len(data)):
                table = table.replace("!data",
                fr"""{nameandsymbol[i]}{data[i].tableprint(novalues=True)} & !data"""
                )
            table = table.replace("& !data",
            r"""\\ 
            \midrule
            !data"""
            )
            tableprint = [ml.tableprint(nounits=True)[1:].split("&") for ml in data]
            indexfirst = [ [index[j] for index in tableprint] for j in range(len(tableprint[0]))]

            for index in indexfirst:
                table = table.replace("!data",
            rf""" {"&".join([*index])} \\
            !data""")

        else:
            raise Exception("Style Error: Only 'sideways' and 'upright' styles are supported.")


        table = table.replace("!data","")
        self.document = self.document.replace("!table",table)

    def graph(self, data : List[MeasurementList], title : str = "", xnameandsymbol : str = "Name, Symbol", \
        ynameandsymbol : str = "Name, Symbol", caption : str = "", width : float = 0.8, style : str = "default", \
        showline : bool = True):
        "Add a graph to the LaTeX document."
        graph = Document.graphtemplates[style]
        self.graphnumber += 1
        graph = graph.replace("!graphnumber",str(self.graphnumber))
        graph = graph.replace("!caption",caption)
        graph = graph.replace("!width",str(width))

        if len(data) != 2 or not all(
            isinstance(listitem, MeasurementList) for listitem in data
        ):
            raise Exception("2 MeasurementLists needed for graphing.")

        eq = LinearRegression(*data)
        filename = f"graph{self.graphnumber}"

        if(Document.graphfolder != '.'): # assuming the graph folder is a subfolder
            graph = graph.replace("!filename","../" + Document.graphfolder +  filename)
        else:
            graph = graph.replace("!filename", Document.graphfolder + filename)

        self.document = self.document.replace("!graph",graph)

        if (not os.path.exists(Document.graphfolder)):
            os.makedirs(Document.graphfolder)
        plt = eq.plot(title,xnameandsymbol,ynameandsymbol,showline,self.graphnumber)
        plt.savefig(Document.graphfolder + filename)
        print(f"labtex: Wrote to '{Document.graphfolder + filename}.png'.")

    def save(self,filename: str ="labdocument",overwrite: bool = False):
        "Save the document to 'filename.tex'."

        self.document = self.document.replace("!table","").replace("!graph","")

        if(not os.path.exists(Document.texfolder)):
            print("labtex: Creating folder '" + Document.texfolder + "'.")
            os.makedirs(Document.texfolder)
        if(os.path.exists(Document.texfolder + filename + ".tex")):
            print(f"labtex: '{Document.texfolder + filename}.tex' already exists. { 'Overwriting.' if overwrite else 'Use `save(...,overwrite=True)` to overwrite.'}")
            if(not overwrite):
                return

        with open(Document.texfolder + filename + '.tex','w') as outputfile:
            outputfile.write(self.document)

        print(f"labtex: Wrote to '{Document.texfolder + filename}.tex'.")