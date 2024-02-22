## Customize Makefile settings for vccf
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

VESSEL_CSV = https://raw.githubusercontent.com/hubmapconsortium/hra-vccf/main/Vessel.csv

$(TMPDIR)/vessel.csv:
	wget $(VESSEL_CSV) -O $@

$(PATTERNDIR)/data/default/vessel.tsv $(TEMPLATEDIR)/vessel_relation.tsv: $(TMPDIR)/vessel.csv
	python $(SCRIPTSDIR)/etl/vessel_ETL.py --input $< --pattern $@ --template $(TEMPLATEDIR)/vessel_relation.tsv

update_vessel_data: $(PATTERNDIR)/data/default/vessel.tsv

VESSEL_ORGAN_CROSSWALK = https://raw.githubusercontent.com/hubmapconsortium/hra-vccf/main/VesselOrganCrosswalk.csv

$(TMPDIR)/vessel_organ_crosswalk.csv:
	wget $(VESSEL_ORGAN_CROSSWALK) -O $@

$(TEMPLATEDIR)/vessel_organ_crosswalk.tsv: $(TMPDIR)/vessel_organ_crosswalk.csv
	python $(SCRIPTSDIR)/etl/vessel_organ_crosswalk_ETL.py --input $< --template $@ --vessels $(PATTERNDIR)/data/default/vessel.tsv

.PHONY: update_vessel_organ_crosswalk
update_vessel_organ_crosswalk: $(TEMPLATEDIR)/vessel_organ_crosswalk.tsv

.PHONY: update_templates
update_templates: update_vessel_data update_vessel_organ_crosswalk