HEADER = r'''
\documentclass[10pt, a4paper]{article}
\usepackage{xltxtra}
\usepackage{graphicx}
\usepackage{wrapfig}

\setmainfont[Mapping=tex-text,Ligatures={Common},Numbers=OldStyle]{Junicode}
%%\newcommand{\old}[1]{\fontspec[Alternate=1,Ligatures={Common, Rare}, Swashes={LineInitial, LineFinal}]{Hoefler Text}}

\renewcommand{\abstractname}{\centering \textsc{{Background}}}

\begin{document}
\author{\textsc{%s}}
\title{\Huge{\textsc{%s}}}
\date{}
\maketitle
'''

PARAGRAPH = r'''
{\centering \section{}}
\begin{samepage}
\noindent
%s
\end{samepage}
\vspace{0.5cm}
'''

OPTION = r'''If you want to %s, turn to {\bf%s}.
'''

GOTO = r'''Turn to {\bf%d}.
'''

FOOTER = r'''
\end{document}
'''

IMAGE = r'''
\includegraphics[width=2.5cm]{images/chick.png}
'''

BACKGROUND = r'''
\begin{abstract}
\noindent
\small{\emph{%s}}
\end{abstract}
'''

SINGLE_ENEMY = r'''
\vspace{0.5cm}
    \begin{center}
        \begin{tabular*}{0.75\textwidth}{@{\extracolsep{\fill}}lcc}
        %s & \textsc{strength} %s & \textsc{skill} %s\\
        \end{tabular*}
    \end{center}
\vspace{0.5cm}'''
    
ENEMY_WIN = r'''If you win, turn to {\bf%s}'''

ENEMY_LOSE = r''', if you lose, turn to {\bf%s}.'''
    
MULTIPLE_ENEMY_HEADER = r'''
\vspace{0.5cm}
        \begin{center}
            \begin{tabular*}{0.75\textwidth}{@{\extracolsep{\fill}}lcc}
                & \textsc{strength} & \textsc{skill} \\
'''

MULTIPLE_ENEMY_NAME_AND_STATS = r'''            %s & %s & %s \\
'''

MULTIPLE_ENEMY_FOOTER = r'''            \end{tabular*}
        \end{center}
\vspace{0.5cm}'''
        
r'''
        \begin{center}
            \begin{tabular*}{0.5\textwidth}{@{\extracolsep{\fill}}lcc}
                & \textsc{strength} & \textsc{skill} \\
            ROCK CRAB & 34 & 45 \\
            SMALL MOUSE & 32 & 10 \\
            \end{tabular*}
        \end{center}'''
