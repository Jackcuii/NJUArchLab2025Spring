GEM5_ROOT ?= $(shell echo $$GEM5_ROOT)

ifndef GEM5_ROOT
$(error You are expected to set GEM5_ROOT to the root dir of your built gem5.)
endif

SOURCE_DIR := $(GEM5_ROOT)/m5out
TARGET_DIR := ./results
TARGET1 := ./results/lab1-1
TARGET2 := ./results/lab1-2
TARGET3 := ./results/lab1-3
TARGET4 := ./results/lab1-4
TARGET5 := ./results/lab1-5

SCRIPT := ./lab1.py
RETRIEVE := ./retrieve.py
CLOCK_RATES := 0.5GHz 1GHz 2GHz 3GHz
ICACHE_SIZES := 2kB 4kB 8kB 16kB 32kB 64kB
DCACHE_SIZES := 2kB 4kB 8kB 16kB 32kB 64kB 128kB 256kB
L2CACHE_SIZES := 128kB 256kB 512kB 1024kB 2048kB 4096kB
LINE_SIZES := 8 16 32 64 128 256

PLOT := ./plot.py
# 设置 Python 路径以包含 gem5 的 Python 模块
# export PYTHONPATH := $(GEM5_ROOT):$(PYTHONPATH)

run: run_lab1


run_lab1: create_target_dir
	@echo "GEM5_ROOT: $(GEM5_ROOT)"
	@echo "Going to run the codes for Lab1."
	$(MAKE) run_script

run_script:
	mkdir -p $(TARGET1)
	@for clock in $(CLOCK_RATES); do \
		echo "\033[33m Run with clk: $$clock, L1ICache: 16kB, L1DCache: 64kB, L2Cache: 256kB, CacheLine: 64B \033[0m"; \
		$(GEM5_ROOT)/build/X86/gem5.opt --outdir=./m5out $(SCRIPT) \
			--binary ./Eratosthenes \
			--clock $$clock; \
		$(MAKE) copy_results TARGETN=1; \
		python3 $(RETRIEVE) $(TARGET1)/result_clock.json $(TARGET1)/stats.txt $$clock "simSeconds"; \
		python3 $(RETRIEVE) $(TARGET1)/result_cycles.json $(TARGET1)/stats.txt $$clock "system.cpu.numCycles"; \
		python3 $(RETRIEVE) $(TARGET1)/result_insts.json $(TARGET1)/stats.txt $$clock "simInsts"; \
		$(MAKE) rename_results TARGET_NAME=$$clock TARGETN=1; \
	done
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "

	mkdir -p $(TARGET2)
	@for icache_size in $(ICACHE_SIZES); do \
		echo "\033[33m Run with icache_size: $$icache_size, L1DCache: 64kB, L2Cache: 256kB, CacheLine: 64B \033[0m"; \
		$(GEM5_ROOT)/build/X86/gem5.opt --outdir=./m5out $(SCRIPT) \
			--binary ./Eratosthenes \
			--l1i_size $$icache_size; \
		$(MAKE) copy_results TARGETN=2; \
		python3 $(RETRIEVE) $(TARGET2)/result_miss.json $(TARGET2)/stats.txt $$icache_size "system.cpu.icache.overallMissRate::total"; \
		$(MAKE) rename_results TARGET_NAME=$$icache_size TARGETN=2; \
	done
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "

	mkdir -p $(TARGET3)
	@for dcache_size in $(DCACHE_SIZES); do \
		echo "\033[33m Run with dcache_size: $$dcache_size, L1ICache: 16kB, L2Cache: 256kB, CacheLine: 64B \033[0m"; \
		$(GEM5_ROOT)/build/X86/gem5.opt --outdir=./m5out $(SCRIPT) \
			--binary ./Eratosthenes \
			--l1d_size $$dcache_size; \
		$(MAKE) copy_results TARGETN=3; \
		python3 $(RETRIEVE) $(TARGET3)/result_miss.json $(TARGET3)/stats.txt $$dcache_size "system.cpu.dcache.demandMissRate::total"; \
		$(MAKE) rename_results TARGET_NAME=$$dcache_size TARGETN=3; \
	done
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "

	mkdir -p $(TARGET4)
	@for l2_size in $(L2CACHE_SIZES); do \
		echo "\033[33m Run with l2_size: $$l2_size, L1ICache: 16kB, L1DCache: 64kB, CacheLine: 64B \033[0m"; \
		$(GEM5_ROOT)/build/X86/gem5.opt --outdir=./m5out $(SCRIPT) \
			--binary ./Eratosthenes \
			--l2_size $$l2_size; \
		$(MAKE) copy_results TARGETN=4; \
		python3 $(RETRIEVE) $(TARGET4)/result_miss.json $(TARGET4)/stats.txt $$l2_size "system.l2cache.overallMissRate::total"; \
		$(MAKE) rename_results TARGET_NAME=$$l2_size TARGETN=4; \
	done
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "

	mkdir -p $(TARGET5)
	@for line_size in $(LINE_SIZES); do \
		echo "\033[33m Run with line_size: $$line_size, L1ICache: 16kB, L1DCache: 64kB, L2Cache: 256kB \033[0m"; \
		$(GEM5_ROOT)/build/X86/gem5.opt --outdir=./m5out $(SCRIPT) \
			--binary ./Eratosthenes \
			--cache_line_size $$line_size; \
		$(MAKE) copy_results TARGETN=5; \
		python3 $(RETRIEVE) $(TARGET5)/result_miss_l1i.json $(TARGET5)/stats.txt $$line_size "system.cpu.icache.overallMissRate::total"; \
		python3 $(RETRIEVE) $(TARGET5)/result_miss_l1d.json $(TARGET5)/stats.txt $$line_size "system.cpu.dcache.demandMissRate::total"; \
		python3 $(RETRIEVE) $(TARGET5)/result_miss_l2.json $(TARGET5)/stats.txt $$line_size "system.l2cache.overallMissRate::total"; \
		$(MAKE) rename_results TARGET_NAME=$$line_size TARGETN=5; \
	done
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo " "
	@echo "All Done!"

	@echo "Plotting the results..."
	$(MAKE) plot

	rm -rf ./m5out
	
plot:
	python3 $(PLOT)

rename_results:
ifndef TARGET_NAME
	$(error TARGET_NAME is required for rename_results)
endif
ifndef TARGETN
	$(error TARGETN is required for rename_results)
endif
	@mv $(TARGET$(TARGETN))/config.ini $(TARGET$(TARGETN))/$(TARGET_NAME).ini
	@mv $(TARGET$(TARGETN))/stats.txt $(TARGET$(TARGETN))/$(TARGET_NAME).txt
	@mv $(TARGET$(TARGETN))/config.json $(TARGET$(TARGETN))/$(TARGET_NAME).json

create_target_dir:
	@echo "Make result directory $(TARGET_DIR)."
	mkdir -p $(TARGET_DIR)

copy_results:
ifndef TARGETN
	$(error TARGETN is required for copy_results)
endif
	@cp -r ./m5out/* $(TARGET$(TARGETN))

clean:
	@echo "Clean $(TARGET_DIR)"
	rm -rf $(TARGET_DIR)
	rm -rf ./m5out


# just to complement the mistake, regenerate the retrieve results of lab1-2 to lab1-5
#temp:
#	@echo "Regenerate the retrieve results of lab1-2 to lab1-5"
#	@for l1i_size in $(ICACHE_SIZES); do \
#		python3 $(RETRIEVE) $(TARGET2)/result_miss.json $(TARGET2)/$$l1i_size.txt $$l1i_size "system.cpu.icache.overallMissRate::total"; \
#	done
#	@for l1d_size in $(DCACHE_SIZES); do \
#		python3 $(RETRIEVE) $(TARGET3)/result_miss.json $(TARGET3)/$$l1d_size.txt $$l1d_size "system.cpu.dcache.demandMissRate::total"; \
#	done
#	@for l2_size in $(L2CACHE_SIZES); do \
#		python3 $(RETRIEVE) $(TARGET4)/result_miss.json $(TARGET4)/$$l2_size.txt $$l2_size "system.l2cache.overallMissRate::total"; \
#	done
#	@for line_size in $(LINE_SIZES); do \
		python3 $(RETRIEVE) $(TARGET5)/result_miss_l1i.json $(TARGET5)/$$line_size.txt $$line_size "system.cpu.icache.overallMissRate::total"; \
		python3 $(RETRIEVE) $(TARGET5)/result_miss_l1d.json $(TARGET5)/$$line_size.txt $$line_size "system.cpu.dcache.demandMissRate::total"; \
		python3 $(RETRIEVE) $(TARGET5)/result_miss_l2.json $(TARGET5)/$$line_size.txt $$line_size "system.l2cache.overallMissRate::total"; \
	done
