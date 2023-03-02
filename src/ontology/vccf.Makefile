## Customize Makefile settings for vccf
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

VESSEL_CSV = https://raw.githubusercontent.com/hubmapconsortium/hra-vccf/main/Vessel.csv

$(TMPDIR)/vessel.csv:
	wget $(VESSEL_CSV) -O $@

