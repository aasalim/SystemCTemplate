BUILD_DIR?= build

# If command is 'make coverage'
ifeq ($(MAKECMDGOALS),coverage)
    COVERAGE ?= 1
endif

ifeq ($(COVERAGE), 1)
    BUILD_TYPE ?= Debug
	CONAN_FLAGS += -o conantemplate/*:coverage=True
else
    BUILD_TYPE ?= Release
endif

# Defaults to building the project
all: build

# Configure poetry
pre-configure:
	@poetry install

# Configure CMake
configure: pre-configure
	@poetry run conan install . --build=missing -s build_type=$(BUILD_TYPE) $(CONAN_FLAGS)

# Build
build: configure
	@poetry run conan build . -s build_type=$(BUILD_TYPE) $(CONAN_FLAGS)

coverage: build
	@mkdir -p $(BUILD_DIR)/coverage
	@poetry run gcovr -r. -s \
		--exclude 'build/.*' --exclude 'tests/.*'  --exclude 'external/.*' \
		--html-details --html-title "Code Coverage Report" \
		-o $(BUILD_DIR)/coverage/CoverageReport.html

# Clean build directory
clean:
	@echo Cleaning build directory...
	@rm -rf $(BUILD_DIR)
	@echo Cleaned!
	
conansource: pre-configure
	@conan source .

conanclean: pre-configure
	@rm -rf external/*/
	@conan remove "*" -c

conancreate: pre-configure
	@conan create .
	
conanlist: pre-configure
	@conan list "*"
