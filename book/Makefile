
default: 
	pdflatex book.tex 

final:
	pdflatex book.tex 
	bibtex book
	makeindex book.idx	
	pdflatex book.tex 
	pdflatex book.tex 

clean:
	rm *.aux *.blg *.bbl *.idx *.ilg *.log *.ind *.toc *.thm
