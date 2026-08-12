.PHONY: thesis fast clean style overlap qa

thesis:
	latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex

fast:
	xelatex -interaction=nonstopmode -file-line-error main.tex

clean:
	latexmk -C main.tex

style:
	python3 scripts/style_audit.py --input chapters --patterns qa/style_red_flags.csv --output qa/style_audit_report.md

overlap:
	python3 scripts/reference_overlap_audit.py --thesis chapters --reference sources/reference_thesis --output qa/reference_overlap_report.md

qa: thesis style overlap
