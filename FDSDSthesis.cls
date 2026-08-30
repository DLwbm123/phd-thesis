%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   复旦大学大数据学院研究生学位论文模板
%
%   版本号:   1.1
%   最后更新: 2025-11-05
%
%   若对本模板有任何意见或建议,
%   请联系模板作者 (yuqliu21@m.fudan.edu.cn)
%   或大数据学院研究生教务员 (mickeyqiyi@fudan.edu.cn).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{FDSDSthesis}

%%%%%%%%%%%%%%%%%%%%%%%%
% FontSize & FontStyle %
%%%%%%%%%%%%%%%%%%%%%%%%

\LoadClass[UTF8,scheme=chinese,zihao=-4,openany,linespread=1.383705]{ctexbook}

%\setmainfont[Mapping=tex-text]{Times New Roman} %可选择以 Times New Roman 作为西文字体
\setCJKmainfont[ExternalLocation=./FontStyle/,AutoFakeBold,
    ItalicFont=SimKai.ttf]{SimSun.ttf}
\setCJKsansfont[ExternalLocation=./FontStyle/]{SimHei.ttf}
\setCJKfamilyfont{hei}[ExternalLocation=./FontStyle/]{SimHei.ttf}

\ctexset{punct=CCT} %可选择 quanjiao/banjiao/kaiming/CCT
\ctexset{today=small} %可选择 small/big/old
\ctexset{space=false}
\ctexset{autoindent=true} %在字体大小发生变化时，是否自动调整段首缩进(\parindent)的大小

%%%%%%%%%%%%
% Packages %
%%%%%%%%%%%%

\RequirePackage{geometry}
\geometry{a4paper,
        hcentering,
        nomarginpar,
        centering,
        headheight=5mm,
        headsep=5mm,
        footskip=7.5mm}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage[colorlinks=false,
        pdfborder={0 0 0},
        CJKbookmarks=true,
        bookmarks=true,
        bookmarksnumbered=true,
        pdfstartview=FitH]{hyperref}
\RequirePackage{enumitem}
\RequirePackage{ifthen}
\RequirePackage{titlesec,titletoc}
\RequirePackage[title,titletoc]{appendix}[2009/09/02 v1.2b extra appendix facilities]
\RequirePackage{fancyhdr}
\RequirePackage{emptypage}
\RequirePackage{amsmath,amsfonts,amssymb,amsthm,bm}
%\RequirePackage{newtxmath} %使用 Times New Roman 字体时可配套使用该数学字体
\RequirePackage{zhnumber}
% The thesis uses algorithm2e; loading the legacy algorithm package here
% would define the same floating environment and cause a package conflict.
\RequirePackage{bibentry}
% \RequirePackage{natbib}

%%%%%%%%%%%%%%%
% Page styles %
%%%%%%%%%%%%%%%

% Nothing, empty page
\fancypagestyle{empty}{%
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}}

% Only page number
\fancypagestyle{plain}{%
\fancyhf{}
\fancyfoot[C]{\zihao{-5} \heiti \thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}}

% Page number, title of the chapter
\fancypagestyle{headings}{%
\fancyhf{}
\fancyhead[RO,LE]{\zihao{-5} \heiti \thepage}
\fancyhead[CO]{\zihao{-5} \heiti \nouppercase{\leftmark}}
\fancyhead[CE]{\zihao{-5} \heiti \mymarks}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0pt}}
\newcommand{\mymarks}{复旦大学大数据学院}
% \newcommand{\mymarks}{\ifthenelse{\equal{\value{secnumdepth}}{-2}}{\leftmark}{复旦大学博士学位论文}} % if not equal

% Style of front matter pages (content, abstract...)
\renewcommand\frontmatter{%
\cleardoublepage
\pagenumbering{roman}
\pagestyle{plain}
}

% Style of main matter pages (introduction, algorithm, conculsion...)
\renewcommand\mainmatter{%
\cleardoublepage
\pagenumbering{arabic}
\pagestyle{headings}
}

% Style of back matter pages (reference, thanks...)
\renewcommand\backmatter{%
\setcounter{secnumdepth}{-2}
\cleardoublepage
\pagestyle{headings}
}

%\newcommand{\ind}{\textup{Ind}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Chapter/Sections styles %
%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ctexset{%
chapter={%
        beforeskip=24pt,
        afterskip=18pt,
        fixskip=true,
        format={\zihao{3}\sffamily\heiti\centering},
        pagestyle=plain,
},
section={
        beforeskip=24pt,
        afterskip=12pt,
        fixskip=true,
        format={\zihao{4}\heiti\sffamily},
},
subsection={
        beforeskip=12pt,
        afterskip=12pt,
        fixskip=true,
        format={\zihao{-4}\heiti\sffamily},
},}

\titlecontents{chapter}[0em]{\smallskip\sffamily}{\thecontentslabel~}{}{\hfill\sffamily\contentspage\smallskip}
%\titlecontents{section}[1em]{\sffamily}{\thecontentslabel~}{}{\hspace{0.5em}\titlerule*{ .}\sffamily\contentspage}
%\titlecontents{subsection}[2em]{\sffamily}{\thecontentslabel~}{}{\hspace{0.5em}\titlerule*{ .}\sffamily\contentspage}

% Define \chapter*
\makeatletter
\let\oldchapter\chapter
\renewcommand*\chapter{\@ifstar{\starchapter}{\cleardoublepage\@dblarg\nostarchapter}}
\newcommand*\starchapter[1]{
\ifthenelse{\equal{\detokenize{#1}}{\detokenize{Abstract}}}
{\setcounter{secnumdepth}{-1}\oldchapter*{#1}\addcontentsline{toc}{chapter}{Abstract}\setcounter{secnumdepth}{3}}{\setcounter{secnumdepth}{-1}\oldchapter{#1}\setcounter{secnumdepth}{3}}}
\def\nostarchapter[#1]#2{\oldchapter[{#1}]{#2}}
\makeatother

%%%%%%%%%%%%%%%%%
% Theorem Style %
%%%%%%%%%%%%%%%%%

\theoremstyle{plain}
\newtheorem{theorem}{定理}[chapter]
\newtheorem{lemma}[theorem]{引理}
\newtheorem{proposition}[theorem]{命题}
\newtheorem{corollary}[theorem]{推论}

\theoremstyle{definition}
\newtheorem{definition}{定义}[chapter]
\newtheorem{example}{例}[chapter]

\theoremstyle{remark}
\newtheorem{remark}{注}[chapter]

\numberwithin{equation}{chapter}

%\newenvironment{prf}{{\noindent \heiti{证:}\ }}{\hfill $\Box$ \\ \smallskip}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Definition for personal information %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\makeatletter

\providecommand\ctitle[1]{}
\renewcommand\ctitle[1]{\edef\FDt@value@ctitle{#1}}

\providecommand\etitle[1]{}
\renewcommand\etitle[1]{\edef\FDt@value@etitle{#1}}

\providecommand\author[1]{}
\renewcommand\author[1]{\edef\FDt@value@author{#1}}

\providecommand\faculty[1]{}
\renewcommand\faculty[1]{\edef\FDt@value@faculty{#1}}

\providecommand\major[1]{}
\renewcommand\major[1]{\edef\FDt@value@major{#1}}

\providecommand\stuid[1]{}
\renewcommand\stuid[1]{\edef\FDt@value@stuid{#1}}

\providecommand\supervisor[1]{}
\renewcommand\supervisor[1]{\edef\FDt@value@supervisor{#1}}

\providecommand\secondsupervisor[1]{}
\renewcommand\secondsupervisor[1]{\edef\FDt@value@secondsupervisor{#1}}
\let\FDt@value@secondsupervisor\relax

\providecommand\mail[1]{}
\renewcommand\mail[1]{\edef\FDt@value@mail{#1}}

\providecommand\pubdate[1]{}
\renewcommand\pubdate[1]{\edef\FDt@value@pubdate{#1}}

\providecommand\degreeMoP[1]{}
\renewcommand\degreeMoP[1]{\edef\FDt@value@degreeMoP{#1}}

\providecommand\degreePoA[1]{}
\renewcommand\degreePoA[1]{\edef\FDt@value@degreePoA{#1}}

\providecommand\blindreview[1]{}
\renewcommand\blindreview[1]{\edef\FDt@value@blindreview{#1}}

% Default values
\providecommand*\FDt@value@ctitle{中文标题}
\providecommand*\FDt@value@etitle{English Title}
\providecommand*\FDt@value@author{匿名}
\providecommand*\FDt@value@faculty{大数据学院}
\providecommand*\FDt@value@major{统计学}
\providecommand*\FDt@value@mail{xxx@fudan.edu.cn}
\providecommand*\FDt@value@stuid{XXXXXXXXXX}
\providecommand*\FDt@value@supervisor{某某教授}
\providecommand*\FDt@value@pubdate{\today}
\providecommand*\FDt@value@degreeMoP{0}
\providecommand*\FDt@value@degreePoA{0}
\providecommand*{\FDt@value@blindreview}{1}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The template of the cover %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\makeatletter
\providecommand\makecover{}
\renewcommand\makecover{%

\pagestyle{empty}
\pagenumbering{alph}
\newgeometry{
    hcentering,
    nomarginpar,
    centering,
    top=30mm,
    bottom=25mm,
    left=26mm,
    right=26mm,
    headheight=5mm,
    headsep=5mm,
    footskip=7.5mm}

% Head: University Code
\begin{flushright}
    \zihao{-5}
    \begin{tabular}{rl}
    学校代码:&10246\\
    \phantom{学校代码:}&\\
    \end{tabular}
\end{flushright}

\vskip 2\baselineskip

% Logo of Fudan University
\begin{figure}[!htbp]
    \centering
    \includegraphics[width=0.5\textwidth]{FudanLOGO}
\end{figure}

\vskip 2\baselineskip

% Title
\begin{center}
{\zihao{2} {\ifnum\FDt@value@degreePoA=0{博士}\else{硕士}\fi{}学位论文}\par}
{\zihao{-3} {（\ifnum\FDt@value@degreeMoP=0{学术}\else{专业}\fi{}学位）}\par}
\vskip 2\baselineskip
{\zihao{-2} \textbf{\FDt@value@ctitle}\par}
\vskip 1\baselineskip
{\zihao{4} \textbf{\FDt@value@etitle}\par}
\end{center}

\vskip 1\baselineskip

% Personal information
\begin{center}
{
\zihao{4}
\def\arraystretch{1.2}% Line spacing
\ifnum\FDt@value@blindreview=0%
    \ifnum\FDt@value@degreeMoP=0%
        \begin{tabular}{rl}
        \makebox[5.5em][s]{编号}:\quad &\FDt@value@stuid\\
        \makebox[5.5em][s]{院系}:\quad &\FDt@value@faculty\\
        \makebox[5.5em][s]{专业}:\quad &\FDt@value@major\\
        \makebox[5.5em][s]{姓名}:\quad &\FDt@value@author\\
        \makebox[5.5em][s]{指导教师}:\quad &\FDt@value@supervisor
        \ifx\FDt@value@secondsupervisor\relax\\\else\\[-0.5em]&\FDt@value@secondsupervisor\\\fi
        \makebox[5.5em][s]{完成日期}:\quad &\FDt@value@pubdate\\
        \end{tabular}
    \else%
        \begin{tabular}{rl}
        \makebox[10.5em][s]{编号}:\quad &\FDt@value@stuid\\
        \makebox[10.5em][s]{院系}:\quad &\FDt@value@faculty\\
        \makebox[10.5em][s]{专业学位类别（领域）}:\quad &\FDt@value@major\\
        \makebox[10.5em][s]{姓名}:\quad &\FDt@value@author\\
        \makebox[10.5em][s]{指导教师}:\quad &\FDt@value@supervisor
        \ifx\FDt@value@secondsupervisor\relax\\\else\\[-0.5em]&\FDt@value@secondsupervisor\\\fi
        \makebox[10.5em][s]{完成日期}:\quad &\FDt@value@pubdate\\
        \end{tabular}
    \fi
\else%
    \ifnum\FDt@value@degreeMoP=0%
        \begin{tabular}{rl}
        \makebox[5.5em][s]{编号}:\quad &\FDt@value@stuid\\
        \makebox[5.5em][s]{院系}:\quad &\FDt@value@faculty\\
        \makebox[5.5em][s]{专业}:\quad &\FDt@value@major\\
        \makebox[5.5em][s]{完成日期}:\quad &\FDt@value@pubdate\\
        \end{tabular}
    \else%
        \begin{tabular}{rl}
        \makebox[10.5em][s]{编号}:\quad &\FDt@value@stuid\\
        \makebox[10.5em][s]{院系}:\quad &\FDt@value@faculty\\
        \makebox[10.5em][s]{专业学位类别（领域）}:\quad &\FDt@value@major\\
        \makebox[10.5em][s]{完成日期}:\quad &\FDt@value@pubdate\\
        \end{tabular}
    \fi
\fi
}
\end{center}

\restoregeometry
}%
\makeatother

%%%%%%%%%%
% Others %
%%%%%%%%%%

% graph address
\DeclareGraphicsExtensions{.mps,.pdf,.eps,.png}

% Put your name and title on the pdf file
\makeatletter
\newcommand\FDt@set@pdf@info{%
    \ifnum\FDt@value@blindreview=0%
        \hypersetup{pdftitle = {\FDt@value@ctitle},
                    pdfauthor = {\FDt@value@author}}%
    \else%
        \hypersetup{pdftitle = {\FDt@value@ctitle},
                    pdfauthor = {匿名}}%
    \fi}
\AtBeginDocument{\FDt@set@pdf@info}
\makeatother

% Style of enumerate
\setlist{nosep}
\setlist[itemize]{leftmargin=\parindent}
\setlist[enumerate]{leftmargin=\parindent}

% Algorithm naming is configured in main.tex through algorithm2e.
