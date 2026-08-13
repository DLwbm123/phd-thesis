.PHONY: thesis fast clean

thesis:
	latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex

fast:
	xelatex -interaction=nonstopmode -file-line-error main.tex

clean:
	latexmk -C main.tex
