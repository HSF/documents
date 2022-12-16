# Analysis Ecosystem II Report

This is the LaTeX source version of the [Analysis Ecosystem II Workshop](https://indico.cern.ch/event/1125222/) report.

Online versions are at:

- Zenodo, <https://doi.org/10.5281/zenodo.7003962>
- arXiv, <https://arxiv.org/abs/2212.04889>

## Compiling

The style file is JHEP, but with a customised author list as the journal official way to do it scales badly for many authors. The references are in *biblatex*, to be processed with `biber` and compile correctly in TexLive 2022 and recent MiKTeX distributions.

```sh
pdflatex AEII
biber AEII
pdflatex AEII # x2 if needed!
```
