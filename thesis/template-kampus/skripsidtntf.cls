%--------------------------------------------------------
%  Original class
%  By Dr. Pekik Nurwantoro
%  Computational Physics Group, FMIPA UGM
%
%  Version 1.0
%  Adapted to JTF format by
%  Dr. Alexander Agung
%  Nuclear Engineering Program
%  Department of Engineering Physics, FT-UGM
%  May 24, 2009
%
% Version 2.0
%  Modified to DTNTF format by
%  Dr. Alexander Agung
%  Nuclear Engineering Program
%  Department of Nuclear Engineering and Engineering Physics, FT-UGM
%  October 10, 2017
% 
% Version 3.0
%  Modified to DTNTF format by
%  Yakub Fahim Luckyarno
%  Engineering Physics Program
%  Department of Nuclear Engineering and Engineering Physics, FT-UGM
%  2025
% 
% Version 3.1
%  Modified to DTNTF format by
%  Sita Gandes Pinasti
%  Nuclear Engineering Program
%  Department of Nuclear Engineering and Engineering Physics, FT-UGM
%  2025
%--------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
%\ProvidesClass{skripsijtf}[2009/05/24 v1.0 The Engineering Physics Department UGM Skripsi Class]
% \ProvidesClass{skripsidtntf}[2017/10/10 v2.0 The Department of Nuclear Engineering and Engineering Physics UGM Skripsi Class]
% \ProvidesClass{skripsidtntf}[2025/07/14 v3.0 The Department of Nuclear Engineering and Engineering Physics UGM Skripsi Class]
\ProvidesClass{skripsidtntf}[2026/09/22 v3.3 The Department of Nuclear Engineering and Engineering Physics UGM Skripsi Class]

%\RequirePackage[bahasa]{packages/babel}
\RequirePackage[bahasa]{babel}
\RequirePackage{indentfirst}

\RequirePackage{setspace}
\RequirePackage[T1]{fontenc}
\RequirePackage{times}
\RequirePackage{graphicx,latexsym}
\RequirePackage{supertabular}
\usepackage{multirow}
%\usepackage{multicolumn}
\usepackage{rotating}
%\usepackage[none]{hyphenat}
 %\hyphenpenalty=10000
%\justify
\usepackage{parskip}
\usepackage[dvipsnames]{xcolor}

\setlength{\parskip}{8pt}

\newif\if@sarskripsi
\newif\if@sarproposal
\DeclareOption{tugasakhir}{\@sarskripsitrue\@sarproposalfalse}
\DeclareOption{proposal}{\@sarskripsifalse\@sarproposaltrue}

\newif\if@singlesp
\newif\if@doublesp
\DeclareOption{satuspasi}{\@singlesptrue\@doublespfalse}
\DeclareOption{duaspasi}{\@singlespfalse\@doublesptrue}
\newif\if@onehalfsp
\@onehalfspfalse
\DeclareOption{satusetengahspasi}{\@onehalfsptrue}

%\newif\if@langindo
%\newif\if@langeng
%\DeclareOption{indonesia}{\@langindotrue\@langengfalse}
%\DeclareOption{inggris}{\@langindofalse\@langengtrue}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ExecuteOptions{tugasakhir,duaspasi}
\ProcessOptions
\LoadClass[a4paper,12pt]{report}
%\RequirePackage{national}
%\bibliographystyle{plainnat}

\RequirePackage[toc,page,title,titletoc,header]{appendix}
\renewcommand{\appendixpagename}{LAMPIRAN}
\renewcommand{\appendixtocname}{LAMPIRAN}
\noappendicestocpagenum
%\renewcommand{\setthesection}{\thechapter.\@arabic\c@section.}
%\renewcommand{\setthesection}{\Alph{\section}}
\appendixtocoff
\appendixpageoff

\RequirePackage{ifthen}
\RequirePackage{nomencl}%
\setlength{\nomitemsep}{-\parsep}
\renewcommand{\nomname}{\nomenclaturename}%
%\makeglossary%
\makenomenclature

%\begin{enumerate}
%\item 
\renewcommand{\nomgroup}[1]{
   \vspace{1.25cm}
   \ifthenelse{\equal{#1}{A}} {\item[\large{\textbf{Lambang Romawi}}]} 
       {
       \ifthenelse{\equal{#1}{B}}{ \item[\large{\textbf{Lambang Yunani}}]}
           {
           \ifthenelse{\equal{#1}{C}}{\item[\large{\textbf{Subskrip}}]}
               {
               \ifthenelse{\equal{#1}{D}}{\item[\large{\textbf{Superskrip}}]}
                    {
                    \ifthenelse{\equal{#1}{E}}{\item[\large{\textbf{Singkatan}}]}}{}
               }
            }
       }
   }
   
\renewcommand{\nompreamble}{\vspace{-1.75cm}}   
\newcommand{\nomunit}[1]{%
   \renewcommand{\nomentryend}{\hspace*{\fill}#1}}
%\end{enumerate}


% -----------
% Setting Table of Contents
%-------------
   
%\RequirePackage[chapter,nottoc]{tocbibind}
%\renewcommand{\simplechapterdelim}{.}
%\simplechapter[Lampiran]

\RequirePackage[titles,subfigure]{tocloft}
\renewcommand{\cftchapaftersnum}{.   }
\renewcommand{\cftchappresnum}{ }
\renewcommand{\cfttabaftersnum}{.}
\renewcommand{\cftfigaftersnum}{.}
\newlength{\lebar}
%\settowidth{\lebar}{\cftchappresnum\cftchapaftersnum \@plus 25em}
\settowidth{\lebar}{\cftchappresnum\cftchapaftersnum}
\addtolength{\cftchapnumwidth}{\lebar}
\addtolength{\cftsecnumwidth}{\lebar}
\setlength{\cftfignumwidth}{2.5em}

\RequirePackage{enumitem}
\RequirePackage[labelsep=period,labelfont=bf, format=hang]{caption}
\RequirePackage{color}
\RequirePackage{listings}
\RequirePackage[it,IT]{subfigure}
\RequirePackage{url}
\urlstyle{rm}

%------------------------------------------------------------
%Layout
%------------------------------------------------------------
\setlength{\topmargin}{-1cm}
\setlength{\headheight}{12pt}
\setlength{\headsep}{2.3cm}
\setlength{\topskip}{1ex}
\setlength{\oddsidemargin}{1.46cm}
\setlength{\evensidemargin}{1.46cm}
\setlength{\textwidth}{14.3cm}
\setlength{\textheight}{22cm}
\setlength{\footskip}{1.5cm}
\setlength{\marginparsep}{0pt}
\setlength{\marginparwidth}{0pt}
\setlength{\parindent}{3em} %Indent approx 6 character


%------------------------------------------------------------
%The form of page numbering
%------------------------------------------------------------
\pagestyle{myheadings}
\markright{}
%\pagestyle{plain}

%------------------------------------------------------------
%Define page numbering in the first chapter
%------------------------------------------------------------
\def\ps@chapterheading{%
  \let\@evenhead\@empty\let\@oddhead\@empty
  \def\@oddfoot{\hfil\thepage\hfil}%
  \def\@evenfoot{\hfil\thepage\hfil}
  }

%------------------------------------------------------------
%Redefine chapter and sections
%------------------------------------------------------------
\setcounter{secnumdepth}{3}
\renewcommand \thepart {\@Roman\c@part}
\renewcommand \thechapter {\@Roman\c@chapter}
\renewcommand \thesection {\@Roman\c@chapter.\@arabic\c@section.}
\renewcommand\thesubsection   {\thesection\@arabic\c@subsection.}
\renewcommand\thesubsubsection   {\thesubsection\@arabic\c@subsection.}

\newcommand{\Lampiran}[2][?]{
  \setcounter{chapter}{0}%
  \setcounter{section}{0}%
\refstepcounter{chapter}
\addcontentsline{toc}{appendix}{\protect\numberline{\appendixname~\thechapter}#1}
{\raggedleft\large\bfseries\appendixname\
\thesection\par \centering#2\par}
\sectionmark{#1}
\@afterheading
\addvspace{\baselineskip}
}
\newcommand{\sLampiran}[1]{
\raggedleft\large\bfseries\appendixname
\@afterheading\addvspace{\baselineskip}
}

\renewcommand\appendix{\par
  \setcounter{chapter}{0}%
  \setcounter{section}{0}%
  \gdef\@chapapp{\appendixname}%
 % \gdef\cftchappresnum{LAMPIRAN }
  %\addcontentsline{toc}{appendix}{\protect\numberline{\appendixname~\thechapter}}
  \gdef\thechapter{\@Alph\c@chapter}
  \gdef\thesection{\thechapter.\@arabic\c@section.}
  \gdef\thefigure{\thechapter.\arabic{figure}}
  \gdef\theequation{\thechapter.\arabic{equation}}
  \gdef\thetable{\thechapter.\arabic{table}}
}

\renewcommand{\chapter}{\clearpage\thispagestyle{chapterheading}%
  \global\@topnum\z@ %Prevents figures from going at top of page
  \@afterindenttrue %Indent the 1st paragraph
  \secdef\@chapter\@schapter}
\renewcommand{\@makechapterhead}[1]{%
  {\parindent \z@ \centering \normalfont
    \ifnum \c@secnumdepth >\m@ne
        \large\bfseries \@chapapp\space \thechapter
        \par\nobreak
        \vskip 5\p@
    \fi
    \interlinepenalty\@M
    \large \bfseries \MakeUppercase{ #1} \par\nobreak
    \vskip 20\p@
    }}
\renewcommand{\@makeschapterhead}[1]{%
  {\parindent \z@ \centering \normalfont
    \interlinepenalty\@M \large \bfseries #1\par\nobreak \vskip 20\p@ }}
\renewcommand{\section}{\@startsection{section}{1}{\z@}%{\parindent}%
                                     {-3.5ex\@plus -1ex \@minus -.2ex}%
                                     {2.3ex \@plus .2ex}%
                                     {\normalfont\normalsize\bfseries}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{\z@}%
                                    {3.25ex \@plus1ex \@minus.2ex}%
                                    %{-1em}%
                                    {2.3ex \@plus .2ex}
                                    {\normalfont\normalsize\bfseries}}

\renewcommand{\thefigure}{\arabic{chapter}.\arabic{figure}}
\renewcommand{\theequation}{\arabic{chapter}.\arabic{equation}}
\renewcommand{\thetable}{\arabic{chapter}.\arabic{table}}
%\renewcommand{\thesubfigure}{\arabic{chapter}.\arabic{subfigure}}
\renewcommand{\thesubfigure}{\arabic{subfigure}}

%------------------------------------------------------------
%Redefine caption names
%------------------------------------------------------------
\def\captionsbahasa{%
\def\prefacename{KATA PENGANTAR}%
\def\contentsname{DAFTAR ISI}%
\def\listfigurename{DAFTAR GAMBAR}%
\def\listtablename{DAFTAR TABEL}%
\def\listappendixname{DAFTAR LAMPIRAN}%
\def\nomenclaturename{DAFTAR LAMBANG DAN SINGKATAN}%
\def\intisariname{INTISARI}%
\def\abstractname{ABSTRACT}
\def\partname{BAGIAN}%
\def\chaptername{BAB}%
\def\appendixname{LAMPIRAN}%
\def\refname{DAFTAR PUSTAKA}%
\def\bibname{DAFTAR PUSTAKA}%
\def\indexname{Indeks}%
\def\figurename{Gambar}%
\def\tablename{Tabel}%
\def\pagename{Halaman}%
\def\mottoname{HALAMAN MOTTO}
\def\approvalname{HALAMAN PENGESAHAN}
% \def\halamanpengesahan{HALAMAN PENGESAHAN}
\def\persembahanname{HALAMAN PERSEMBAHAN}
\def\judulname{HALAMAN JUDUL}
\def\plagiarismname{PERNYATAAN BEBAS PLAGIARISME}
\def\halamantugasname{HALAMAN TUGAS}
}


%------------------------------------------------------------]
%Define thesis's inputs
%------------------------------------------------------------
\gdef\@universityind{Universitas Gadjah Mada}
\gdef\@programind{Sarjana S1}
\gdef\@cityind{Yogyakarta}
%\gdef\@gelar{Sarjana S1}
\newcommand{\judul}[1]{\gdef\@judul{#1}}
\newcommand{\@judul}{}
\newcommand{\juduleng}[1]{\gdef\@juduleng{#1}}
\newcommand{\@juduleng}{}
\newcommand{\gelar}[1]{\gdef\@gelar{#1}}
\newcommand{\@gelar}{}
\newcommand{\jenisTA}[1]{\gdef\@jenisTA{#1}}
\newcommand{\@jenisTA}{}
\newcommand{\nama}[1]{\gdef\@nama{#1}}
\newcommand{\@nama}{}
\newcommand{\nim}[1]{\gdef\@nim{#1}}
\newcommand{\@nim}{}
\newcommand{\prodi}[1]{\gdef\@prodi{#1}}
\newcommand{\@prodi}{}
\newcommand{\prodieng}[1]{\gdef\@prodieng{#1}}
\newcommand{\@prodieng}{}
\newcommand{\jurusan}[1]{\gdef\@jurusan{#1}}
\newcommand{\@jurusan}{}
\newcommand{\thselesai}[1]{\gdef\@thselesai{#1}}
\newcommand{\@thselesai}{}
\newcommand{\thmasuk}[1]{\gdef\@thmasuk{#1}}
\newcommand{\@thmasuk}{}
\newcommand{\tglujian}[1]{\gdef\@tglujian{#1}}
\newcommand{\@tglujian}{\number\day~\ifcase\month\or
    Januari\or Februari\or Maret\or April\or Mei\or Juni\or
    Juli\or Agustus\or September\or Oktober\or November\or Desember\fi
    \space \number\year}
\newcommand{\tglujianeng}[1]{\gdef\@tglujianeng{#1}}
\newcommand{\@tglujianeng}{\number\day~\ifcase\month\or
    January\or February\or March\or April\or May\or June\or
    July\or August\or September\or October\or November\or December\fi
    \space \number\year}
\newcommand{\tglpenulisan}[1]{\gdef\@tglpenulisan{#1}}
\newcommand{\@tglpenulisan}{\number\day~\ifcase\month\or
    Januari\or Februari\or Maret\or April\or Mei\or Juni\or
    Juli\or Agustus\or September\or Oktober\or November\or Desember\fi
    \space \number\year}
\newcommand{\tglkelulusan}[1]{\gdef\@tglkelulusan{#1}}
\newcommand{\@tglkelulusan}{\number\day~\ifcase\month\or 
    Januari\or Februari\or Maret\or April\or Mei\or Juni\or 
    Juli\or Agustus\or September\or Oktober\or November\or Desember\fi
    \space \number\year}
\newcommand{\pembimbingutama}[1]{\gdef\@pembimbingutama{#1}}
\newcommand{\@pembimbingutama}{}

\newcommand{\ketuasidang}[1]{\gdef\@ketuasidang{#1}}%
\newcommand{\@ketuasidang}{}
\newcommand{\sekretarissidang}[1]{\gdef\@sekretarissidang{#1}}%
\newcommand{\@sekretarissidang}{}
\newcommand{\pengujiutama}[1]{\gdef\@pengujiutama{#1}}%
\newcommand{\@pengujiutama}{}
\newcommand{\anggotapenguji}[1]{\gdef\@anggotapenguji{#1}}%
\newcommand{\@anggotapenguji}{}

\newcommand{\nipanggotapenguji}[1]{\gdef\@nipanggotapenguji{#1}}%
\newcommand{\@nipanggotapenguji}{}
\newcommand{\nippengujiutama}[1]{
\gdef\@nippengujiutama{#1}}%
\newcommand{\@nippengujiutama}{}
\newcommand{\nipsekretarissidang}[1]{\gdef\@nipsekretarissidang{#1}}%
\newcommand{\@nipsekretarissidang}{}
\newcommand{\nipketuasidang}[1]{\gdef\@nipketuasidang{#1}}%
\newcommand{\@nipketuasidang}{}
\newcommand{\nippembimbingutama}[1]{\gdef\@nippembimbingutama{#1}}%
\newcommand{\@nippembimbingutama}{}

\newcommand{\permasalahan}[1]{\gdef\@permasalahan{#1}}
\newcommand{\@permasalahan}{}
%\newcommand{\lamaskripsi}[1]{\gdef\@lamaskripsi{#1}}%
%\newcommand{\@lamaskripsi}{}
\newcommand{\kajur}[1]{\gdef\@kajur{#1}}
\newcommand{\@kajur}{}
\newcommand{\nipkajur}[1]{\gdef\@nipkajur{#1}}%
\newcommand{\@nipkajur}{}
\newcommand{\UGM@supervisorsID}{%
  \vspace{1cm}
  \begin{center}
    \begin{tabular}{@{}l c l@{}}
      Pembimbing Utama     & : & \@pembimbingutama \\
    \end{tabular}
  \end{center}
}

\newcommand{\UGM@supervisorsEN}{%
  \vspace{1cm}
  \begin{center}
    \begin{tabular}{@{}l c l@{}}
      Supervisor     & : & \@pembimbingutama 
    \end{tabular}
  \end{center}
}

\newcommand{\KataKunci}[1]{%
  \par\vspace{0.25cm}
  \par\noindent\textbf{\textit{Kata kunci}}: #1\par
}

\newcommand{\Keywords}[1]{%
  \par\vspace{0.25cm}
  \par\noindent\textbf{\textit{Keywords}}: #1\par
}

\newcommand{\MateraiBox}{%
  \par\vspace{0.4cm}%
  \noindent
  \begingroup
    \setlength{\fboxsep}{10pt}% inner padding
    \setlength{\fboxrule}{0.6pt}% border thickness
    \fcolorbox{Red}{Peach!20}{%
     \parbox{!}{\raggedright
      \textit{Materai ASLI (e-Meterai)}\par
    Rp.\,10\,000\par
    dan tanda tangan
  }%
}

  \endgroup
  \par\vspace{0.6cm}%
}


%------------------------------------------------------------
%Define cover in Indonesian
%------------------------------------------------------------
\def\halamansampul{%
  \thispagestyle{empty}%
    \begin{center}
      {\normalfont\bfseries \@jenisTA}\par\nobreak
      \vspace{1.0cm}
      {\normalfont\large\bfseries\MakeUppercase{\@judul}}\par\nobreak
      \vspace{1.5cm}
    \vfill
    %\includegraphics[width=180pt]{logoUGM}
\includegraphics[width=5.5cm]{logoUGM}
    \vfill
      \vspace{1.5cm}
      {\normalfont 
        Disusun oleh: \\
        \@nama\\
        \@nim}\\
     \vspace{1.5cm}
      \begin{onehalfspace}
      {\normalfont\bfseries 
         DEPARTEMEN TEKNIK NUKLIR DAN TEKNIK FISIKA\\
         FAKULTAS TEKNIK\\
         {UNIVERSITAS GADJAH MADA}\\
         YOGYAKARTA\\
         \@thselesai}\\
      \end{onehalfspace}
      \end{center}
}  
%------------------------------------------------------------
%Define titlepage in Indonesian
%------------------------------------------------------------
\def\halamanjudul{%
  \newpage\thispagestyle{empty}%
  \pagenumbering{roman}
  \setcounter{page}{1}
    \begin{center}
      {\normalfont\large\bfseries\MakeUppercase{\@judul} }\par\nobreak
      \vspace{1.0cm}
      {\normalfont\bfseries\@jenisTA}\par\nobreak
      \vspace{1cm}
      \begin{onehalfspace}
      {\normalfont 
        untuk memenuhi sebagian persyaratan\\
        untuk memperoleh derajat \space\@gelar \space \\
        %\vspace{0.5cm}
        Program Studi \space\@prodi \space} \\
        %Jurusan \space\@jurusan}\\
  \vspace{1.3cm}
    \vfill
%    \includegraphics[width=180pt]{logoUGM}
        \includegraphics[width=5.5cm]{logoUGM}
       \vfill
      \vspace{1.2cm}
      {\normalfont 
        diajukan oleh \\
        \MakeUppercase{\@nama}\\
        \@nim}\\
      \vspace{1.2cm}

       {\normalfont kepada \\}
      {\normalfont\bfseries 
         DEPARTEMEN TEKNIK NUKLIR DAN TEKNIK FISIKA\\
         FAKULTAS TEKNIK\\
         {UNIVERSITAS GADJAH MADA}\\
         YOGYAKARTA\\
         \@thselesai}\\
      \end{onehalfspace}
      \end{center}
\addcontentsline{toc}{chapter}{\judulname}
}  

%------------------------------------------------------------
%Free from Plagiarism Page
%------------------------------------------------------------
\def\halamanpernyataan{%
  \newpage\thispagestyle{chapterheading}%
 
  \begin{onehalfspace}
 \begin{center}
  {\normalfont\large\bfseries PERNYATAAN BEBAS PLAGIASI}\par\nobreak
\end{center}
  \vspace{1cm}
 Saya yang bertanda tangan di bawah ini:
\par\nobreak
  \vspace{1.0cm}
\begin{onehalfspace}
\begin{tabular}{p{4cm}p{0.1cm}p{9cm}}
Nama  & : &\@nama\\
NIM   & : & \@nim\\
Tahun terdaftar & : & \@thmasuk \\
Program Studi & : & \@prodi \\
Fakultas & : & Teknik
\end{tabular}
\end{onehalfspace}

\vspace{1.0cm}
\noindent menyatakan bahwa dokumen ilmiah skripsi ini tidak terdapat bagian dari karya ilmiah lain yang telah diajukan untuk memperoleh gelar akademik di suatu lembaga Pendidikan Tinggi, dan juga tidak terdapat karya atau pendapat yang pernah ditulis atau diterbitkan oleh orang/lembaga lain, kecuali yang secara tertulis disitasi dalam dokumen ini dan disebutkan sumbernya secara lengkap dalam daftar pustaka.

\vspace{8pt}

\noindent Dengan demikian saya menyatakan bahwa dokumen ilmiah ini bebas dari unsur-unsur plagiasi dan apabila dokumen ilmiah Skripsi ini di kemudian hari terbukti merupakan plagiasi dari hasil karya penulis lain dan/atau dengan sengaja mengajukan karya atau pendapat yang merupakan hasil karya penulis lain, maka penulis bersedia menerima sanksi akademik dan/atau sanksi hukum yang berlaku. 

\vspace{1.3cm}
% --- Date (left) ---
\noindent\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad Yogyakarta, \@tglpenulisan

\vspace{0.8cm}

% --- Box on the RIGHT, but CONTENT inside the box is LEFT-aligned ---
\noindent
\begin{minipage}{\textwidth} % isolates alignment changes
  \hfill % pushes the box to the right margin
  \fcolorbox{Red}{Peach!20}{%
    \begin{minipage}{0.4\textwidth}
      \raggedright % <-- left-align text INSIDE the box
      \textit{Materai ASLI (e-Meterai)}\par
      Rp.\,10\,000\par
      dan tanda tangan
    \end{minipage}%
  }
\end{minipage}

\vspace{1.2cm}

% --- Signature (left) ---
\noindent\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad \MakeUppercase{\@nama}\par
\noindent\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad NIM. \@nim






    \end{onehalfspace}
%    \end{center}
\addcontentsline{toc}{chapter}{\plagiarismname}
}


%------------------------------------------------------------
%Approval Page
%------------------------------------------------------------
% \def\halamanpengesahan{
%   \newpage\thispagestyle{chapterheading}
  
%   \addcontentsline{toc}{chapter}{\approvalname}
% }
\def\halamanpengesahan{%
  \newpage\thispagestyle{chapterheading}%
  \begin{onehalfspace}
  % \begin{singlespace}
    \begin{center}
      {\normalfont\large\bfseries HALAMAN PENGESAHAN}\par\nobreak
      \vspace{0.5cm}
      {\normalfont \@jenisTA}\par\nobreak
      \vspace{0.5cm}
      {\normalfont\bfseries\MakeUppercase{\@judul}}\par\nobreak
      \vspace{0.5cm}
    \end{center}
    \begin{tabular}{p{4.5cm}p{0.1cm}p{9cm}}
      Nama Mahasiswa & : & \@nama \\ [0.5cm]
      Nomor Mahasiswa & : & \@nim \\ [0.5cm]
      Pembimbing & : & \@pembimbingutama \\ [0.5cm] 
    \end{tabular}
    \begin{center}
      Skripsi ini telah dipertahankan di depan Tim Penguji\\ 
      pada tanggal \@tglujian \\
    \end{center}
    \vspace{0.5cm}
    \begin{tabular}{p{4.5cm}p{0.1cm}p{9cm}}
      Ketua Sidang & : & \@pembimbingutama \\ [0.5cm]
      Penguji Utama & : & \@pengujiutama \\ [0.5cm]
      Anggota Penguji & : & \@anggotapenguji \\ [0.5cm]
    \end{tabular}
    
    \begin{center}
      Skripsi ini telah diterima dan dinyatakan memenuhi\\
      syarat kelulusan pada tanggal \@tglkelulusan \\
    \end{center}
    \vspace{1.5cm}
    \begin{center}
      Ketua Departemen Teknik Nuklir dan Teknik Fisika \\
      Fakultas Teknik UGM \\[2cm]
      \uline{\@kajur} \\
      NIP. \@nipkajur
    \end{center}
  \end{onehalfspace}
  % \end{singlespace}
\addcontentsline{toc}{chapter}{\approvalname}
}

%------------------------------------------------------------
%HALAMAN TUGAS
%------------------------------------------------------------
\def\halamantugas{%
  \newpage\thispagestyle{chapterheading}%
  \begin{center}
  \begin{onehalfspace}
  {\normalfont\large\bfseries HALAMAN TUGAS}\par\nobreak
  \vspace{0.5cm}
  \begin{minipage}{16cm}
    {\normalfont\large\bfseries KEMENTERIAN RISET, TEKNOLOGI, DAN PENDIDIKAN TINGGI}
  \end{minipage}
\par\nobreak
  \vspace{0.1cm}
  {\normalfont\large\bfseries UNIVERSITAS GADJAH MADA}\par\nobreak
  \vspace{0.1cm}
  {\normalfont\large\bfseries FAKULTAS TEKNIK}\par\nobreak
  \vspace{0.1cm}
  {\normalfont\large\bfseries DEPARTEMEN TEKNIK NUKLIR DAN TEKNIK FISIKA}\par\nobreak
\vspace{1.cm}
\hrule
  \vspace{0.5cm}


%  {\normalfont\large\bfseries TUGAS AKHIR}\par\nobreak
%  \vspace{0.5cm}
\begin{singlespace}
\begin{tabular}{p{4.4cm}p{0.1cm}p{9cm}}
Nama  & : &\@nama\\
NIM   & : & \@nim\\
Pembimbing &: & \@pembimbingutama \\
Pembimbing Pendamping &: & \@pembimbingpendamping   \\
Judul Skripsi &:& \@judul \\
Permasalahan &:& \@permasalahan\\
\end{tabular}
\end{singlespace}
\vspace{0.5cm}
\hrule

\vspace{1.cm}

\begin{singlespace}
\centering
\begin{tabular}{cp{.5cm}c}
Pembimbing Utama && Pembimbing Pendamping  \vspace{1.5cm}\\


\underline{\@pembimbingutama}&&\underline{\@pembimbingpendamping} \\
NIP. \@nippembimbingutama && NIP. \@nippembimbingpendamping

\end{tabular}
\end{singlespace}

\vspace{1cm}
Mengetahui,\\

\vspace{0.35cm}
Ketua Departemen Teknik Nuklir dan Teknik Fisika \\
Fakultas Teknik UGM \\

\vspace{1.25cm}
\begin{singlespace}\underline{\@kajur} \\
NIP. \@nipkajur
\end{singlespace}


    \end{onehalfspace}
    \end{center}
\addcontentsline{toc}{chapter}{\halamantugasname}
}


%------------------------------------------------------------
%Acknowledgment
%------------------------------------------------------------
\def\persembahan{%
  \clearpage\thispagestyle{chapterheading}%
\null%\vfill%Force the content of acknowledment to bottom page 
\addcontentsline{toc}{chapter}{\persembahanname}
}

%------------------------------------------------------------
%Motto
%------------------------------------------------------------
\def\motto{%
  \clearpage\thispagestyle{chapterheading}%
\null\vfill%Force the content of acknowledment to bottom page 
\addcontentsline{toc}{chapter}{\mottoname}
}

%------------------------------------------------------------
%Preface
%------------------------------------------------------------
\def\pengantar{%
    % \clearpage\thispagestyle{chapterheading}
    \chapter*{\prefacename}%
    
    % \begin{flushright}
    %     Yogyakarta, \@tglpenulisan
    % \end{flushright}
    % % %
    % \vspace{0.5cm}
    % \begin{flushright}
    %     Penulis
    % \end{flushright}

    \addcontentsline{toc}{chapter}{\prefacename}

}

%------------------------------------------------------------
%Nomenclature
%------------------------------------------------------------
\def\lambang{%
  \clearpage\thispagestyle{chapterheading}%
%  \printglossary%
%\addcontentsline{toc}{chapter}{\nomenclaturename}
\nomenclature[aa]{\emph{Lambang }}{\emph{Kuantitas } \nomunit{\emph{Satuan }}}%
\nomenclature[ba]{\emph{Lambang }}{\emph{Kuantitas } \nomunit{\emph{Satuan }}}%
\nomenclature[ca]{\emph{Lambang }}{\emph{Deskripsi }}%
\nomenclature[da]{\emph{Lambang }}{\emph{Deskripsi }}%
%\nomenclature[eaa]{\emph{Singkatan }}{\emph{ }}%
%\markboth{\nomname}{\nomname}
\addcontentsline{toc}{chapter}{\nomenclaturename}%
%\printglossary[2.5cm]%
\printnomenclature[2.5cm]
}

%------------------------------------------------------------
%Redefine Abstract in Indonesian
%------------------------------------------------------------
\def\intisari{%
    \clearpage\thispagestyle{chapterheading}%
    {\parindent \z@ \centering \normalfont
 %  {\normalsize\bfseries \intisariname}\par\nobreak
 %  \vskip 10\p@
        {\large\bfseries\MakeUppercase{\@judul}}
        \par\nobreak
        \vskip 6\p@
        \interlinepenalty\@M
        {\normalsize oleh}\par\nobreak
        \vskip 6\p@
        \begin{singlespace}
            {\normalsize \@nama \\ \@nim}
            \vskip 10\p@
            Diajukan kepada Departemen Teknik Nuklir dan Teknik Fisika Fakultas Teknik \\
            Universitas Gadjah Mada pada tanggal \@tglujian \\
            untuk memenuhi sebagian persyaratan untuk memperoleh derajat \\
            sarjana S-1 Program Studi \@prodi
        \end{singlespace}
        \par\nobreak
    } 
    \vspace{1cm}
    {\parindent \z@ \centering \normalfont
        {\normalsize\bfseries \intisariname}\par\nobreak 
    }
    \begin{singlespace}%
        \setlength{\parskip}{0.25\baselineskip}
        \addcontentsline{toc}{chapter}{\intisariname}
}
% --- INDONESIAN ---
\def\endintisari{%
  \vspace{0.8cm}
  \noindent
  \begin{tabular}{@{}l c l@{}}% @{} removes extra left/right padding
    Pembimbing Utama      & : & \@pembimbingutama \\
    Pembimbing Pendamping & : & \@pembimbingpendamping
  \end{tabular}
  \par\vfil\null\end{singlespace}%
}

%------------------------------------------------------------
%Redefine Abstract in English
%------------------------------------------------------------
\def\abstracteng{%
    \clearpage\thispagestyle{chapterheading}%
    {\parindent \z@ \centering \normalfont
%   {\normalsize\bfseries \abstractname}\par\nobreak
%   \vskip 10\p@
 %  {\large\bfseries\@juduleng}
        {\large\bfseries\MakeUppercase{\@juduleng}}
        \par\nobreak
        \vskip 6\p@
        \interlinepenalty\@M
        {\normalsize by}\par\nobreak
        \vskip 6\p@
        \begin{singlespace}
            {\normalsize \@nama \\ \@nim}
            \vskip 10\p@
            Submitted to the Department of Nuclear Engineering and Engineering Physics \\
            Faculty of Engineering Universitas Gadjah Mada on \@tglujianeng \\
            in partial fulfillment of the Degree of \\ Bachelor of Engineering in \@prodieng
        \end{singlespace}
        \par\nobreak
    } 
    \vspace{1cm}
    {\parindent \z@ \centering \normalfont
        {\normalsize\bfseries \abstractname}\par\nobreak 
    }
    \begin{singlespace}%
        \setlength{\parskip}{0.25\baselineskip}
        \addcontentsline{toc}{chapter}{\abstractname}
}
\def\endabstracteng{%
  \vspace{0.8cm}
  \noindent
  \begin{tabular}{@{}l c l@{}}
    Supervisor     & : & \@pembimbingutama \\
    Co-supervisor  & : & \@pembimbingpendamping
  \end{tabular}
  \par\vfil\null\end{singlespace}%
  \selectlanguage{bahasa}\clearpage\pagenumbering{arabic}\setcounter{page}{1}%
}



\AtBeginDocument{%
\if@doublesp%
\doublespacing%
\else\if@singlesp%
\singlespacing%
\else
\onehalfspacing%
\fi%
\fi
}

\endinput
