## Customize Makefile settings for vccf
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

VESSEL_CSV = https://raw.githubusercontent.com/hubmapconsortium/hra-vccf/main/Vessel.csv

$(TMPDIR)/vessel.csv:
	wget $(VESSEL_CSV) -O $@

$(PATTERNDIR)/data/default/vessel.tsv: $(TMPDIR)/vessel.csv
	python ../scripts/vessel_ETL.py --input $< --pattern $@

update_vessel_data: $(PATTERNDIR)/data/default/vessel.tsv
.PHONY: update_vessel_data