# Build mode: native (default) or emsdk
BUILD_MODE  ?= native

CFLAGS      = -Wall -Wextra -std=c99 -O2 -Wno-zero-length-array -Wno-empty-translation-unit
DEBUG_FLAGS = -O0 -g -DBE_DEBUG
TEST_FLAGS  = $(DEBUG_FLAGS) --coverage -fno-omit-frame-pointer -fsanitize=address -fsanitize=undefined
LIBS        = -lm
TARGET      = ../berry
CC          = clang # install clang!! gcc seems to produce a defect berry binary
MKDIR       = mkdir
LFLAGS      =
PREFIX      = /usr/local
BINDIR      = $(PREFIX)/bin

INCPATH     = src default re1.5
SRCPATH     = src default re1.5
GENERATE    = generate
CONFIG      = default/berry_conf.h
COC         = tools/coc/coc
CONST_TAB   = $(GENERATE)/be_const_strtab.h
BUILDDIR    = build

# Emsdk-specific configuration
ifeq ($(BUILD_MODE), emsdk)
    CFLAGS   := -Wall -Wextra -std=c99 -O2 -Wno-zero-length-array -Wno-empty-translation-unit
    LIBS     := -lm -ldl
    TARGET   := ../dist/berry.js
    CC       := emcc
    # Export JavaScript-to-Berry execution API functions
    # NO_EXIT_RUNTIME=1 keeps the runtime alive after main() exits so we can call berry_execute later
    LFLAGS   := -s WASM=0 -s ASYNCIFY -s 'ASYNCIFY_IMPORTS=["_js_readbuffer"]' -s NO_EXIT_RUNTIME=1 \
                -s 'EXPORTED_FUNCTIONS=["_main","_berry_execute","_berry_execute_result","_berry_call_global","_berry_call_global_args","_berry_get_global","_berry_set_global","_berry_set_vm","_tasmota_millis","_malloc","_free"]' \
                -s 'EXPORTED_RUNTIME_METHODS=["ccall","cwrap","UTF8ToString","stringToUTF8","lengthBytesUTF8"]'
    # Use default config for emsdk unless PLATFORM_DIR is specified
    PLATFORM_DIR ?= default
    INCPATH  := src $(PLATFORM_DIR) re1.5
    SRCPATH  := src $(PLATFORM_DIR) re1.5
    CONFIG   := $(PLATFORM_DIR)/berry_conf.h
    TARGETDIR := ../dist
    BUILDDIR := build-emsdk
endif

# Platform-specific configuration (only for native builds)
ifneq ($(BUILD_MODE), emsdk)
    ifeq ($(OS), Windows_NT) # Windows
        CFLAGS    += -Wno-format -DTASMOTA # for "%I64d" warning, mimick Tasmota env with 32 bits int and 32 bits float
        LFLAGS    += -Wl,--out-implib,berry.lib # export symbols lib for dll linked
        TARGET    := $(TARGET).exe
        PYTHON    ?= python # only for windows and need python3
        COC       := $(PYTHON) $(COC)
    else
        CFLAGS    += -DUSE_READLINE_LIB
        LIBS      += -lreadline -ldl
        OS        := $(shell uname)
        ifeq ($(OS), Linux)
            LFLAGS += -Wl,--export-dynamic
        endif
    endif
endif

ifneq ($(V), 1)
    Q=@
    MSG=@echo
else
    MSG=@true
endif

SRCS     = $(foreach dir, $(SRCPATH), $(wildcard $(dir)/*.c))
OBJS     = $(patsubst %.c, $(BUILDDIR)/%.o, $(SRCS))
DEPS     = $(patsubst %.c, $(BUILDDIR)/%.d, $(SRCS))
INCFLAGS = $(foreach dir, $(INCPATH), -I"$(dir)")

.PHONY : clean

all: $(TARGET)

debug: CFLAGS += $(DEBUG_FLAGS)
debug: all

test: CFLAGS += $(TEST_FLAGS)
test: LFLAGS += $(TEST_FLAGS)
test: all
	$(MSG) [Run Testcases...]
	$(Q) ./testall.be
	$(Q) $(RM) */*.gcno */*.gcda

$(TARGET): $(OBJS) $(TARGETDIR) bundle-modules
	$(MSG) [Linking...]
	$(Q) $(CC) $(OBJS) $(LFLAGS) $(LIBS) -o $@
	$(MSG) done

# Bundle Berry modules into JavaScript for virtual filesystem
# This target runs after WASM build to generate berry-modules.js
bundle-modules:
ifeq ($(BUILD_MODE), emsdk)
	$(MSG) [Bundle] Berry modules for virtual filesystem
	$(Q) (cd .. && python3 scripts/bundle-berry-modules.py)
	$(MSG) [Bundle] Animation examples for browser UI
	$(Q) (cd .. && python3 scripts/bundle-animation-examples.py)
	$(MSG) done
endif

$(TARGETDIR):
	$(Q) $(MKDIR) -p $(TARGETDIR)

$(BUILDDIR)/%.o: %.c | $(BUILDDIR)
	$(MSG) [Compile] $<
	$(Q) $(MKDIR) -p $(dir $@)
	$(Q) $(CC) -MM $(CFLAGS) $(INCFLAGS) -MT"$(patsubst %.o,%.d,$@)" -MT"$@" $< > $(patsubst %.o,%.d,$@)
	$(Q) $(CC) $(CFLAGS) $(INCFLAGS) -c $< -o $@

$(BUILDDIR):
	$(Q) $(MKDIR) -p $(BUILDDIR)

sinclude $(DEPS)

$(OBJS): $(CONST_TAB)

$(CONST_TAB): $(GENERATE) $(SRCS) $(CONFIG)
	$(MSG) [Prebuild] generate resources
	$(Q) $(COC) $(SRCPATH) -c $(CONFIG) -o $(GENERATE)

$(GENERATE):
	$(Q) $(MKDIR) $(GENERATE)

install:
	mkdir -p $(DESTDIR)$(BINDIR)
	cp $(TARGET) $(DESTDIR)$(BINDIR)/$(TARGET)

uninstall:
	$(RM) $(DESTDIR)$(BINDIR)/$(TARGET)

prebuild: $(GENERATE)
	$(MSG) [Prebuild] generate resources
	$(Q) $(COC) -o $(GENERATE) $(SRCPATH) -c $(CONFIG)
	$(MSG) done

clean:
	$(MSG) [Clean...]
	$(Q) $(RM) -r $(BUILDDIR) build build-emsdk $(GENERATE)/* berry.lib $(TARGET)
	$(MSG) done
