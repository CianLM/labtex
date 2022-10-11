import subprocess
import regex as re
from labtex.linear import LinearRegression
from labtex.measurementlist import MeasurementList

from typing import Any, List, Union

import hashlib
import os

from labtex.nonlinear import NonlinearRegression
from matplotlib.pyplot import Figure

class Document:
    "A class for LaTeX template document creation with tables and graphs already inserted."
        # Customise these folders and the templates as you wish.
    texfolder = "tex/"
    figurefolder = "figures/"
    tablemarker = "%labtex-tables"
    figuremarker = "%labtex-figures"

    template = r"""\documentclass[]{article}

\title{!title}
\author{!author}

\usepackage{amsmath,amssymb,amsfonts,amsthm,physics,graphicx,geometry,enumitem,booktabs}

\begin{document}

\maketitle

\begin{abstract}

\end{abstract}

\section{Introduction}

\section{Theory}

\section{Method}

\section{Results}
!table
!tablemarker

\section{Data Analysis and Discussion}
!graph
!figuremarker

\section{Conclusion}

\section*{References}

\end{document}
"""


    tabletemplates = {
        "default": 
r"""\begin{table}[ht]!regex
    \centering
    \caption{!caption}
    \label{tab:!label}
    \begin{tabular}{!columns}
        \toprule
        !data
        \bottomrule
    \end{tabular}
\end{table}!table"""
    }

    graphtemplates = {
        "default": r"""
\begin{figure}[ht]!regex
    \centering
    \includegraphics[width=!width\textwidth]{!filename}
    \caption{!caption}
    \label{fig:!label}
\end{figure}!graph"""
    }
    
    def __init__(self, title : str, author : str, filename : str = "labdocument", silent : bool = False):
        "Initialise a LaTeX document with an title and an author."
        if os.path.exists(Document.texfolder + filename):
            self.document = open(Document.texfolder + filename).read()
        else:
            self.document = Document.template.replace("!title",title).replace("!author",author).replace("!tablemarker",Document.tablemarker).replace("!figuremarker",Document.figuremarker)
                # print("labtex: Overwriting existing file.")
        self.filename = filename
        self.tablenumber = 0
        self.graphnumber = 0
        self.silent = silent
        self.hashes = []
        self.unchanged_environments = {'tables': 0, 'figures': 0}

    def __repr__(self):
        return self.document

    def add_table(self,nameandsymbols : List[str], data : List[MeasurementList], \
        headers :List[str] = [], caption : str = "", label : str = "", style : str = "sideways"):
        """
        Add a table to the LaTeX document. 
        """
        hash_str = hashlib.sha1(str(data).encode("utf-8")).hexdigest()[:5]
        # id_str = f'%labtex-table-{self.tablenumber + 1}-{hash_str}'
        id_str = f'%labtex-table-{self.tablenumber + 1}'
        regex = re.compile('begin\{table\}\[[\w]{0,2}\]' + id_str + '.*?end{table}', re.DOTALL)
        
        self.hashes += [id_str]
        match = re.search(regex,self.document)
        table_code = self.table_code(nameandsymbols,data,headers,caption,label,style).strip()
        if match: # Replace table with the new table
            if (('\\' + match.group(0)) == table_code.replace('!table','')):
                # not self.silent and print("labtex: Figure code unchanged.")
                self.unchanged_environments['tables'] += 1
                return
            not self.silent and print("labtex: Updating table " + id_str)
            self.document = self.document.replace('\\' + match.group(0), table_code)
        else:
            key = Document.tablemarker
            not self.silent and print("labtex: Adding table " + id_str)
            if self.document.find(key) != -1:
                self.document = self.document.replace(key,'\n' + table_code + '\n' + key)
            else:
                self.document = self.document.replace('\\end{document}', '\n' + table_code + '\n' + '\\end{document}')

    # Called by add_table to generate the LaTeX code for the table
    def table_code(self,nameandsymbols : List[str], data : List[MeasurementList], \
        headers :List[str] = [], caption : str = "", label : str = "", style : str = "sideways"):

        assert len(nameandsymbols) == len(data)
        assert all(len(data[0]) == len(line) for line in data)
        columns = len(data[0])

        table = Document.tabletemplates["default"]
        self.tablenumber += 1
        # not self.silent and print(f"labtex: Adding table {self.tablenumber} to Document '{Document.texfolder + self.filename}'.")

        # generate 5 digit hash of the data
        # table = table.replace("!regex",f'%labtex-table-{self.tablenumber}-{hashlib.sha1(str(data).encode("utf-8")).hexdigest()[:5]}')
        table = table.replace("!regex",f'%labtex-table-{self.tablenumber}')
        table = table.replace("!label", str(self.tablenumber) if label == "" else label)
        table = table.replace("!caption",caption)

        if not (all(isinstance(line, MeasurementList) for line in data)):
            raise Exception("Data Error: Data should be a list of MeasurementLists.")

        if(style == "sideways"):
            # table = table.replace("!columns", "*{" + str(1+columns) + "}c" )
            table = table.replace("!columns", f"c|{ 'c' * columns}" )
            if(headers != [] and len(headers) >= 2):
                table = table.replace("!data",
                fr"""{headers[0]} & \multicolumn{{{columns}}}{{c}}{{{headers[1]}}} \\
            \midrule !data"""
                )
            for i in range(len(data)):
                table = table.replace("!data",
                fr"""
            {nameandsymbols[i]}{ data[i].tableprint() } \\ !data"""
                )

        elif(style == "upright"):
            table = table.replace("!columns", "*{" + str(len(data)) + "}c" )
            for i in range(len(data)):
                table = table.replace("!data",
                fr"""{nameandsymbols[i]}{data[i].tableprint(novalues=True)} & !data"""
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
        table = re.sub(r'\n[ \t]+\n', '\n', table)

        # self.document = self.document.replace("!table",table)
        return table

    def add_figure(self, fig : Figure, caption : str = "", label : str = "", width : float = 0.8, filename = ""):
        "Add figure to the LaTeX document."
        
        # Save figure to file
        if fig is not None:
            if (not os.path.exists(Document.figurefolder)):
                os.makedirs(Document.figurefolder)
            filename = f"graph{self.graphnumber + 1}.png" if not filename else filename
            fig.savefig(Document.figurefolder + filename)
            not self.silent and print(f"labtex: Wrote to '{Document.figurefolder + filename}'.")

        id_str = f'%labtex-figure-{self.graphnumber + 1}'
        regex = re.compile('begin\{figure\}\[[\w]{0,2}\]' + id_str + '.*?end{figure}', re.DOTALL)

        self.hashes += [id_str]
        match = re.search(regex,self.document)
        figure_code = self.figure_code(caption,label,width,filename).strip()
        if match: # Replace figure
            if (('\\' + match.group(0)) == figure_code.replace('!graph','')):
                # not self.silent and print("labtex: Figure code unchanged.")
                self.unchanged_environments['figures'] += 1
                return

            not self.silent and print("labtex: Updating figure " + id_str)
            self.document = self.document.replace('\\' + match.group(0), figure_code)
        else:
            key = Document.figuremarker
            print("labtex: Adding figure " + id_str)
            if self.document.find(key) != -1:
                self.document = self.document.replace(key,'\n' + figure_code + '\n' + key)
            else:
                self.document = self.document.replace('\\end{document}', '\n' + figure_code + '\n' + '\\end{document}')

        
    # Called by add_figure to generate the latex code for the figure
    def figure_code(self, caption : str = "", label : str = "", width : float = 0.8, filename = ""):
        graph = Document.graphtemplates['default']
        self.graphnumber += 1
        # graph = graph.replace("!regex",f'%labtex-graph-{self.graphnumber}-{hashlib.sha1(str(data).encode("utf-8")).hexdigest()[:5]}')
        graph = graph.replace("!regex",f'%labtex-figure-{self.graphnumber}')
        graph = graph.replace("!label",str(self.graphnumber) if label == "" else label)
        graph = graph.replace("!caption",caption)
        graph = graph.replace("!width",str(width))

        filename = f"graph{self.graphnumber}" if not filename else filename
        if(Document.figurefolder != '.'): # assuming the graph folder is a subfolder
            graph = graph.replace("!filename","../" + Document.figurefolder +  filename)
        else:
            graph = graph.replace("!filename", Document.figurefolder + filename)

        return graph

    def save(self, overwrite: bool = False):
        "Save the document to 'filename'."
        # Compile the tex file to check for errors
        if os.path.exists(Document.texfolder + self.filename):
            try:
                not self.silent and print(f"labtex: Compiling '{Document.texfolder + self.filename}' to check for errors.")
                subprocess.run(
                    ["pdflatex", "-halt-on-error", self.filename],
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    cwd=Document.texfolder,
                    check=True,
                    # suppress output

                )
            except:
                raise Exception("labtex: File failed to compile prior to saving. Save cancelled.")
        else:
            not self.silent and print(f"labtex: File '{Document.texfolder + self.filename}' does not exist. Creating new file.")
        # Remove tables and graphs that are not in the document
        # id_str = '(%labtex-table-\w{1,2}-\w{5})'
        id_str = '(%labtex-(?:table|figure)-\w{1,2})'
        regex = re.compile('(begin\{(table|figure)\}\[[\w]{0,2}\]' + id_str + '.*?end{(?:table|figure)})', re.DOTALL)
        match_all = regex.findall(self.document)
        # print(self.hashes)
        # print(len(match_all))
        for match, tof, id_str in match_all: # tof stands for 'table or figure'
            if id_str not in self.hashes:
                self.document = self.document.replace('\\' + match + '\n', '')
                not self.silent and print('labtex: Removing', id_str)

        # Display number of unchanged environments
        if not self.silent:
            self.unchanged_environments['tables'] != 0 and print(f"labtex: {self.unchanged_environments['tables']} unchanged tables.")
            self.unchanged_environments['figures'] != 0 and print(f"labtex: {self.unchanged_environments['figures']} unchanged figures.")

        self.document = self.document.replace("!table","").replace("!graph","")

        if(not os.path.exists(Document.texfolder)):
            not self.silent and print("labtex: Creating folder '" + Document.texfolder + "'.")
            os.makedirs(Document.texfolder)
        if(os.path.exists(Document.texfolder + self.filename)):
            not self.silent and print(f"labtex: '{Document.texfolder + self.filename}' already exists. { 'Overwriting.' if overwrite else 'Use `save(...,overwrite=True)` to overwrite.'}")
            if(not overwrite):
                return

        with open(Document.texfolder + self.filename,'w') as outputfile:
            outputfile.write(self.document)

        not self.silent and print(f"labtex: Wrote to '{Document.texfolder + self.filename}'.")

# Update document procedure:
# 1. For each table/graph call:
#   1.1. Check if table/graph is in file
#   1.2. If not, add it to bottom
#   1.3. If so, update/replace it
#   1.4. Remove tables/graphs that are not in the document
# 2. Save file


# Intended UX:
# 1. Create document
# 2. Add tables/graphs
# 3. Save document
# 4. Change contents of tables/graphs
# 5. This should keep their positions in the document even if the content changes
