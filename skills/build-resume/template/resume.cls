\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2015/05/25 An elegant R茅sum茅 class]
\LoadClass[10pt]{article}

% disable indent globally
\setlength{\parindent}{0pt}
% paragraph spacing for skill entries, self-eval lines
\setlength{\parskip}{0.6ex}
% some general improvements, defines the XeTeX logo
\RequirePackage{xltxtra}
% use xifthen
\RequirePackage{xifthen}
% use xcolor for customizing color
\RequirePackage[usenames,dvipsnames]{xcolor}
% loading fonts
\RequirePackage{fontspec}
% Main document font - use Times New Roman (system font on Windows)
\setmainfont{Times New Roman}

\RequirePackage[
	a4paper,
	left=0.4in,
	right=0.4in,
	top=0.4in,
	bottom=0.3in,
	nohead
]{geometry}

\RequirePackage{titlesec}
\RequirePackage{enumitem}
\setlist{noitemsep}
\setlist[itemize]{topsep=0.25em, leftmargin=1.5pc}
\setlist[enumerate]{topsep=0.25em, leftmargin=1.5pc}
\RequirePackage[super]{nth}

\titleformat{\section}
  {\Large\scshape\raggedright}
  {}{0em}
  {}
  [\titlerule]
\titlespacing*{\section}{0cm}{*1}{*1}

\titleformat{\subsection}
  {\large\raggedright}
  {}{0em}
  {}
\titlespacing*{\subsection}{0cm}{*1}{*0.5}

\newcommand{\datedsection}[2]{%
  \section[#1]{#1 \hfill #2}%
}
\newcommand{\datedsubsection}[2]{%
  \subsection[#1]{#1 \hfill #2}%
}
\newcommand{\datedline}[2]{%
  {\par #1 \hfill #2 \par}%
}

\newcommand{\name}[1]{
  \centerline{\Huge\scshape{#1}}
  \vspace{1.2ex}
}
\newcommand{\contactInfo}[2]{
  \centerline{\sffamily\large{Phone: #1} \textperiodcentered\ Email: #2}
  \vspace{1.2ex}
}
\newcommand{\otherInfo}[4]{
  \centerline{\sffamily\large{\ {#1}}
    \ifthenelse{\isempty{#2}}%
      { }
      {\textperiodcentered\ \ {#2} }
    \ifthenelse{\isempty{#3}}%
      { }
      {\textperiodcentered\ \ {#3} }
    \ifthenelse{\isempty{#4}}%
      { }
      {\textperiodcentered\ \ {#4} }
  }
  \vspace{0.7ex}
}

\newcommand{\yourphoto}[1]{
  \hfill \smash{\includegraphics[width={#1}\paperwidth]{images/you.jpg}}
}

\newcommand{\role}[2]{
  {\par \textit{#1} ~ #2 \par}
  \vspace{0.5ex}
}

% add
\newcommand{\sepspace}{\vspace*{1em}}

\newcommand{\MyName}[1]{
    \noindent
	\Huge \usefont{OT1}{phv}{m}{n} #1 \hfill
	\par \normalsize \normalfont
}

\newcommand{\SimpleEntry}[1]{
	\noindent\hangindent=0.5cm\hangafter=0
	#1 \par
}

\newcommand{\Content}[3]{
    \begin{itemize}[parsep=1.2ex]
    \item \songti #1
    \item \songti #2
    \item \songti #3
    \end{itemize}
    \normalsize \par
}

\newcommand{\Contenttwo}[2]{
    \begin{itemize}[parsep=1.2ex]
    \item \songti #1
    \item \songti #2
    \end{itemize}
    \normalsize \par
}

% Prefix label: same size as body, bold, with hair space after
\newcommand{\prefix}[1]{{\textbf{#1}\,}}

% Project separator: subtle dashed line between projects
\newcommand{\projectsep}{%
  \par\vspace{-0.6ex}
  \noindent{\color{black!65}\leaders\hbox to 0.7em{\hss\rule[2pt]{3pt}{0.6pt}\hss}\hfill}
  \par\vspace{-1.5ex}
}
