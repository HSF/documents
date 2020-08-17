---
title: HSF Technical Notes with Pandoc Example
TN-ID: TN-number
author: "Benedikt Hegner"
doi: my doi
institutes: CERN
date: 25 April 2016
abstract: This is example for a markdown text being transformed into an HSF technical note.
---
# Howto
This document serves as an example for how to create an HSF technical note with pandoc and markdown. You have to provide the meta-data given at the top of the sources of this document
```
---
title: HSF Technical Notes with Pandoc Example
TN-ID: TN-number
author: "Benedikt Hegner"
doi: my	doi
institutes: CERN
date: 25 April 2016
abstract: This is example for a markdown text being transformed into an HSF technical note.
---
```


and invoke
```
pandoc -o example.pdf --template pandoc_template.latex pandoc_example.md
```
That's all. 