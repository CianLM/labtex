from .linear import LinearRegression
from .measurement import MeasurementList

from typing import List, Union

import os

class Document:
    "A class for LaTeX template document creation with tables and graphs already inserted."
    def __init__(self,title : str,author : str):
        "Initialise a LaTeX document with an title and an author."
        # Customise these folders and the templates as you wish.
        Document.texfolder = "tex/"
        Document.graphfolder = "figures/"

        Document.template = r"""\documentclass[]{article}

\title{!title}
\author{!author}

\usepackage{amsmath,amssymb,amsfonts,amsthm,physics,graphicx,geometry,enumitem,booktabs}

\begin{document}

\maketitle

\abstract{

}

\section{Introduction}
\subsection{Aim}

\subsection{Theory}

\section{Method}

\section{Results}

!table

\section{Data Analysis}

!graph

\section{Discussion}

\section{Bibliography}

\end{document}
"""


        Document.tabletemplates = {
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

        Document.graphtemplates = {
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
        

        self.document = Document.template.replace("!title",title).replace("!author",author)
        self.tablenumber = 0
        self.graphnumber = 0

    def __repr__(self):
        return self.document

    def table(self,listheads : List[str], data : Union[List[MeasurementList]], \
        headers :List[str] = [], caption : str = "",style : str = "sideways"):
        """
        Add a table to the LaTeX document. 
        """
        assert len(listheads) == len(data)
        assert all(len(data[0]) == len(line) for line in data)
        columns = len(data[0])

        table = Document.tabletemplates["default"]
        self.tablenumber += 1

        table = table.replace("!tablenumber", str(self.tablenumber))
        table = table.replace("!caption",caption)

        if not (all(isinstance(line, MeasurementList) for line in data)):
            raise Exception("Data Error: Data should be a list of Measurement Lists.")

        if(style == "sideways"):
            table = table.replace("!columns", "*{" + str(1+columns) + "}c" )
            if(headers != []):
                table = table.replace("!data",
                fr"""{headers[0]} & \multicolumn{{{columns}}}{{c}}{{{headers[1]}}} \\
            \midrule !data"""
                )
            for i in range(len(data)):
                table = table.replace("!data",
                fr"""
            {listheads[i]}, { data[i].tableprint("uv") } \\ !data"""
                )

        elif(style == "upright"):
            table = table.replace("!columns", "*{" + str(len(data)) + "}c" )
            for i in range(len(data)):
                table = table.replace("!data",
                fr"""{listheads[i]}, {data[i].tableprint("u")} & !data"""
                )
            table = table.replace("& !data",
            r"""\\ 
            \midrule
            !data"""
            )
            tableprint = [m.tableprint("v")[1:].split("&") for m in data]
            indexfirst = [ [index[j] for index in tableprint] for j in range(len(tableprint[0]))]

            for index in indexfirst:
                table = table.replace("!data",
            rf""" {"&".join([*index])} \\
            !data""")


        else:
            raise Exception("Style Error: Only 'sideways' and 'upright' styles supported.")


        table = table.replace("!data","")
        self.document = self.document.replace("!table",table)

    def graph(self, data : List[MeasurementList], title : str = "", xnameandsymbol : str = "Name, Symbol", \
        ynameandsymbol : str = "Name, Symbol", caption : str = "", width : float = 0.8, style :str = "default", \
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
        eq.savefig(Document.graphfolder + filename,title,xnameandsymbol,ynameandsymbol)
        print(f"labtex: Wrote to '{Document.graphfolder + filename}.png'.")

        if(Document.graphfolder != '.'): # assuming the folder is a subfolder
            graph = graph.replace("!filename","../" + Document.graphfolder +  filename)
        else:
            graph = graph.replace("!filename", Document.graphfolder + filename)

        self.document = self.document.replace("!graph",graph)

        if (not os.path.exists(Document.graphfolder)):
            os.makedirs(Document.graphfolder)

    def save(self,filename: str ="labdocument"):
        "Save the document to 'filename.tex'."

        self.document = self.document.replace("!table","").replace("!graph","")

        if(not os.path.exists(Document.texfolder)):
            os.makdirs(Document.texfolder)

        with open(Document.texfolder + filename + '.tex','w') as outputfile:
            outputfile.write(self.document)

        print(f"labtex: Wrote to '{Document.texfolder + filename}.tex'.")