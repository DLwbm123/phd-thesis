$pdf_mode = 5;
$interaction = 'nonstopmode';
$bibtex_use = 2;
$clean_ext = 'acn acr alg glg glo gls ist loa run.xml';
$bibtex = 'bash scripts/run_bibtex.sh %O %S';

# Match the PDF version of included vector figures.
$xdvipdfmx = 'xdvipdfmx -V 7 -E -o %D %O %S';
