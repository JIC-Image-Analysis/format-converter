docker run -v ~/data_repo/root_reconstruction/Expt47_SDB265_8WT7.lif:/input.lif -v `pwd`/output:/output -e "BF_MAX_MEM=2048m" jicscicomp/bioformats /opt/tools/bftools/bfconvert /input.lif /output/%n.tif
7106fe6f-4d74-473a-84ce-16c716734823
62b11361e6fa7316df7cb183b0e3eaa657507680
