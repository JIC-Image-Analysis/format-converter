# Microscopy file format conversion

This repository contains code for a smart tool (that process dtool datasets) to convert bioimaging file formats, using Bioformats.

```
docker run -v ~/data_repo/root_reconstruction/Expt47_SDB265_8WT7.lif:/input.lif -v `pwd`/output:/output -e "BF_MAX_MEM=2048m" jicscicomp/bioformats /opt/tools/bftools/bfconvert /input.lif /output/%n.tif
```
