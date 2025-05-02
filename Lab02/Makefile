GEM5_ROOT ?= $(shell echo ${GEM5_ROOT})


ifndef GEM5_ROOT
$(error You are expected to set GEM5_ROOT to the root dir of your built gem5.)
endif

$(info Gem5 is at $(GEM5_ROOT))

OUTPUT_TARGET_DIR = $(shell pwd)/res
OUTPUT_SOURCE_DIR = $(GEM5_ROOT)/m5out

$(info Output target dir is $(OUTPUT_TARGET_DIR))
$(info Output source dir is $(OUTPUT_SOURCE_DIR))

CURRENT_DIR = $(shell pwd)

makeslow:
	gcc -Wall -O2 -S -static cmov-slow.c -o ncmov-slow.s
	gcc -DCMOV -Wall -O2 -S -static cmov-slow.c -o cmov-slow.s
	gcc -Wall -O2 -static  cmov-slow.c -o ncmov-slow
	gcc -DCMOV -Wall -O2 -static cmov-slow.c -o cmov-slow

makegem5:
	gcc -Wall -O2 -S -static cmov.c -o ncmov.s
	gcc -DCMOV -Wall -O2 -S -static cmov.c -o cmov.s
	gcc -Wall -O2 -static  cmov.c -o ncmov
	gcc -DCMOV -Wall -O2 -static cmov.c -o cmov

dumpgem5:
	objdump -d ncmov > ncmov.dump
	objdump -d cmov > cmov.dump

dumpslow:
	objdump -d ncmov-slow > ncmov-slow.dump
	objdump -d cmov-slow > cmov-slow.dump


run-native:
	@echo "---------- Running branch-over ---------"
	@time $(CURRENT_DIR)/ncmov-slow
	@echo "---------- Running cmov ---------"
	@time $(CURRENT_DIR)/cmov-slow

run-gem5:
	@echo "---------- Running branch-over with localBP ---------"
	$(GEM5_ROOT)/build/X86/gem5.opt --outdir=$(GEM5_ROOT)/m5out --debug-flags=O3PipeView --debug-start=0 --debug-file=trace.out $(GEM5_ROOT)/configs/example/se.py --cmd=$(CURRENT_DIR)/ncmov --cpu-type=DerivO3CPU --caches --l2cache --bp-type=LocalBP 
	@$(MAKE) copy-result RESULT=ncmov-localbp
	@echo "---------- Running cmov with localBP ---------"
	$(GEM5_ROOT)/build/X86/gem5.opt --outdir=$(GEM5_ROOT)/m5out --debug-flags=O3PipeView --debug-start=0 --debug-file=trace.out $(GEM5_ROOT)/configs/example/se.py --cmd=$(CURRENT_DIR)/cmov --cpu-type=DerivO3CPU --caches --l2cache --bp-type=LocalBP
	@$(MAKE) copy-result RESULT=cmov-localbp

	@echo "---------- Running branch-over with TournamentBP ---------"
	$(GEM5_ROOT)/build/X86/gem5.opt --outdir=$(GEM5_ROOT)/m5out --debug-flags=O3PipeView --debug-start=0 --debug-file=trace.out $(GEM5_ROOT)/configs/example/se.py --cmd=$(CURRENT_DIR)/ncmov --cpu-type=DerivO3CPU --caches --l2cache --bp-type=TournamentBP
	@$(MAKE) copy-result RESULT=ncmov-tournamentbp
	@echo "---------- Running cmov with TournamentBP ---------"
	$(GEM5_ROOT)/build/X86/gem5.opt --outdir=$(GEM5_ROOT)/m5out --debug-flags=O3PipeView --debug-start=0 --debug-file=trace.out $(GEM5_ROOT)/configs/example/se.py --cmd=$(CURRENT_DIR)/cmov --cpu-type=DerivO3CPU --caches --l2cache --bp-type=TournamentBP
	@$(MAKE) copy-result RESULT=cmov-tournamentbp

run-new-pred:
	@echo "---------- Running branch-over with ReplayBP ---------"
	$(GEM5_ROOT)/build/X86/gem5.opt --outdir=$(GEM5_ROOT)/m5out --debug-flags=O3PipeView --debug-start=0 --debug-file=trace.out $(GEM5_ROOT)/configs/example/se.py --cmd=$(CURRENT_DIR)/ncmov --cpu-type=DerivO3CPU --caches --l2cache --bp-type=ReplayBP
	@$(MAKE) copy-result RESULT=ncmov-replaybp

register-new-pred:
	@read -p "CAUTION: This action will replace all the Custom Predictor in gem5. Press enter to continue..."
	@mv ./pred/replay.cc $(GEM5_ROOT)/src/cpu/pred/replay.cc
	@mv ./pred/replay.hh $(GEM5_ROOT)/src/cpu/pred/replay.hh
	@mv ./pred/SConscript $(GEM5_ROOT)/src/cpu/pred/SConscript
	@mv ./pred/BranchPredictor.py $(GEM5_ROOT)/src/cpu/pred/BranchPredictor.py
	@echo "Custom Predictor Files Settled Down."
	@echo "Rebuilding gem5..."
	@cd $(GEM5_ROOT) && scons build/X86/gem5.opt -j40
	@echo "gem5 rebuilt."
	@cd $(CURRENT_DIR)

copy-result:
	@mkdir -p $(OUTPUT_TARGET_DIR)/$(RESULT)
	@mv $(OUTPUT_SOURCE_DIR)/* $(OUTPUT_TARGET_DIR)/$(RESULT)/
	@\$(GEM5_ROOT)/util/o3-pipeview.py -c 500 -o $(OUTPUT_TARGET_DIR)/$(RESULT)/pipeview.out --color $(OUTPUT_TARGET_DIR)/$(RESULT)/trace.out
	@echo "Results copied to $(OUTPUT_TARGET_DIR)/$(RESULT)/"

retrieve:
	@python3 retrieve.py ncmov-localbp
	@python3 retrieve.py cmov-localbp
	@python3 retrieve.py ncmov-tournamentbp
	@python3 retrieve.py cmov-tournamentbp

clean-result:
	@rm -rf $(OUTPUT_TARGET_DIR)/*
